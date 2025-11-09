# Sale Product Supplierinfo Search

This module extends the search functionality on the sales order line and in the product catalog to allow users to find products by their vendor's product code or name, as stored in the supplier information (`product.supplierinfo`).

## Business Case

For businesses that use an internal reference system for products to mask the original manufacturer's part number, this module provides a significant workflow improvement. Sales teams can directly search for a product using the vendor code a customer might provide, without needing to leave the sales order to look it up in the product catalog first. This speeds up the quoting and sales process and reduces errors.

## Configuration

No special configuration is needed. The extended search is automatically enabled on sales order lines. To use it in the main product search view, select the "Vendor Product Code" or "Vendor Product Name" filter.

## Usage

1.  **On a Sales Order Line**:
    *   Click on the "Product" field to open the search dropdown.
    *   Type the vendor's product code or product name.
    *   The matching product will appear in the search results.

2.  **In the Product Catalog**:
    *   Go to `Sales > Products`.
    *   In the search bar, click the filters dropdown.
    *   Select "Vendor Product Code" or "Vendor Product Name".
    *   Enter the vendor code/name in the search bar.

## Known Issues / Roadmap

*   The display name in the search dropdown is not yet modified to show the vendor code. This is a planned improvement.

## Bug Tracker

Bugs are tracked on [GitHub Issues](https://github.com/OCA/sale-workflow/issues). In case of trouble, please check there if your issue has already been reported. If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

## Credits

### Authors

*   Odoo Community Association (OCA)

### Maintainers

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

This module is part of the [OCA/sale-workflow](https://github.com/OCA/sale-workflow) project on GitHub.

You are welcome to contribute. To learn how please visit [https://odoo-community.org/page/Contribute](https://odoo-community.org/page/Contribute).
