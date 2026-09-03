# Copyright 2026 Be OnlyOne
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models


def post_init_hook(env):
    """Set the default installment cap on existing Mercado Pago providers.

    New Integer columns default to 0 on existing rows. Checkout Pro would then
    receive ``installments: 0`` unless we coerce those records to 12.
    """
    env["payment.provider"].search(
        [
            ("code", "=", "mercado_pago"),
            ("mercado_pago_max_installments", "<=", 0),
        ]
    ).write({"mercado_pago_max_installments": 12})
