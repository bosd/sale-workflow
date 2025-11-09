# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestSaleProductSupplierinfoSearch(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ProductProduct = self.env["product.product"]
        self.Supplier = self.env["res.partner"]
        self.SupplierInfo = self.env["product.supplierinfo"]

        # Main test product
        self.product_test_a = self.ProductProduct.create(
            {
                "name": "Test Product A",
                "default_code": "TEST-A",
                "detailed_type": "product",
            }
        )
        self.supplier = self.Supplier.create({"name": "Test Supplier"})
        self.supplier_info_a = self.SupplierInfo.create(
            {
                "partner_id": self.supplier.id,
                "product_tmpl_id": self.product_test_a.product_tmpl_id.id,
                "product_name": "Vendor Name A",
                "product_code": "VENDOR-A",
            }
        )

        # Second product for search order testing
        self.product_test_b = self.ProductProduct.create(
            {
                "name": "Test Product B",
                "default_code": "TEST-B-NAME",
                "detailed_type": "product",
            }
        )
        self.supplier_info_b = self.SupplierInfo.create(
            {
                "partner_id": self.supplier.id,
                "product_tmpl_id": self.product_test_b.product_tmpl_id.id,
                "product_code": "VENDOR-B",
            }
        )

    def test_search_without_context(self):
        """Test that search works as default without context."""
        products = self.ProductProduct.name_search(name="TEST-A")
        self.assertEqual(len(products), 1, "Should find by default code.")
        self.assertEqual(products[0][0], self.product_test_a.id)

        products = self.ProductProduct.name_search(name="VENDOR-A")
        self.assertEqual(len(products), 0, "Should NOT find by vendor code.")

    def test_search_with_context_finds_by_vendor_info(self):
        """Test that search includes vendor info with the context."""
        Product = self.ProductProduct.with_context(sale_product_supplierinfo_search=True)

        products = Product.name_search(name="VENDOR-A")
        self.assertEqual(len(products), 1, "Should find by vendor code.")
        self.assertEqual(products[0][0], self.product_test_a.id)

        products = Product.name_search(name="Vendor Name A")
        self.assertEqual(len(products), 1, "Should find by vendor name.")
        self.assertEqual(products[0][0], self.product_test_a.id)

    def test_search_with_custom_display_name(self):
        """Test that the display name is correctly modified."""
        Product = self.ProductProduct.with_context(sale_product_supplierinfo_search=True)
        products = Product.name_search(name="VENDOR-A")
        self.assertEqual(len(products), 1)

        product_id, display_name = products[0]
        self.assertEqual(product_id, self.product_test_a.id)
        self.assertIn("[TEST-A] Test Product A", display_name)
        self.assertIn("(Vendor: VENDOR-A)", display_name)

    def test_search_priority(self):
        """Test that default results are returned before supplier info results."""
        # Product A's name matches 'TEST-B-NAME'
        self.product_test_a.write({'name': 'TEST-B-NAME'})
        # Product B's vendor code is 'VENDOR-B'

        Product = self.ProductProduct.with_context(sale_product_supplierinfo_search=True)

        # This search term matches Product A by name and Product B by its default_code
        products = Product.name_search(name="TEST-B-NAME")

        self.assertEqual(len(products), 2, "Should find two products.")

        # Odoo's default name_search is not deterministic in order for same-level matches.
        # However, our logic *appends* supplier results.
        # A search for 'VENDOR-B' should find product_test_b via supplier info.
        # A search for 'TEST-B-NAME' should find product_test_a and product_test_b via standard search.

        # Let's test the append logic explicitly.
        # 'TEST-B-NAME' matches product_test_b by default_code (standard search)
        # 'VENDOR-A' matches product_test_a by supplier_code (supplier search)
        self.product_test_b.write({'default_code': 'UNIQUE-CODE'})
        self.supplier_info_a.write({'product_code': 'UNIQUE-CODE'})

        products = Product.name_search(name="UNIQUE-CODE", limit=2)
        self.assertEqual(len(products), 2, "Should find both products.")

        # The product found by its default_code should be first.
        product_ids_in_order = [p[0] for p in products]
        self.assertEqual(
            product_ids_in_order,
            [self.product_test_b.id, self.product_test_a.id],
            "The standard search result should appear before the supplier info result.",
        )
