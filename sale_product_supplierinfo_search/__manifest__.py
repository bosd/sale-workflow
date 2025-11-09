# -*- coding: utf-8 -*-
{
    "name": "Sale Product Supplierinfo Search",
    "summary": """
        Search for products by vendor's product code or name on sales order lines.
    """,
    "version": "19.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "sale_management",
    ],
    "data": [
        "views/sale_order_views.xml",
        "views/product_views.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
}
