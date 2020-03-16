# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Pricelist Item menu",
    "summary": "Adds a menu access to Pricelist Item",
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "12.0.1.0.0",
    "category": "Point Of Sale",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": [
        'point_of_sale',
        'product_pricelist_item_button',
        'product_pricelist_full'
    ],
    "data": [
        "views/product_pricelist_views.xml",
    ],
    'installable': True,
}
