# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _name_search(self, name="", args=None, operator="ilike", limit=100):
        search_in_supplier = self.env.context.get(
            "sale_product_supplierinfo_search"
        ) or self.env.context.get("search_in_vendor_info")
        if not search_in_supplier:
            return super()._name_search(
                name=name, args=args, operator=operator, limit=limit
            )

        # First, perform the standard search
        products = super()._name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        product_ids = [p[0] for p in products]

        if len(products) < limit:
            # If the standard search doesn't fill the limit, search in supplier info
            supplier_limit = limit - len(products)
            supplier_info_domain = [
                ("product_tmpl_id.product_variant_ids", "!=", False),
                "|",
                ("product_name", operator, name),
                ("product_code", operator, name),
            ]
            if product_ids:
                supplier_info_domain.append(
                    ("product_tmpl_id.product_variant_ids", "not in", product_ids)
                )

            supplier_info = self.env["product.supplierinfo"].search(
                supplier_info_domain, limit=supplier_limit
            )

            if supplier_info:
                # Manually construct the name to include vendor info
                new_products = []
                supplier_products_added = set()
                for info in supplier_info:
                    for product in info.product_tmpl_id.product_variant_ids:
                        if product.id not in product_ids and product.id not in supplier_products_added:
                            display_name = (
                                f"[{product.default_code or ''}] {product.name} "
                                f"(Vendor: {info.product_code})"
                            )
                            new_products.append((product.id, display_name))
                            supplier_products_added.add(product.id)
                products.extend(new_products)

        return products
