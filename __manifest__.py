# Copyright 2026 Be OnlyOne
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mercado Pago Website Installments",
    "summary": "Offer Mercado Pago Checkout Pro installments on website payments",
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Accounting/Payment Providers",
    "version": "17.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [
        "payment_mercado_pago",
    ],
    "data": [
        "views/payment_provider_views.xml",
        "views/payment_transaction_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
