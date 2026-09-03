# Copyright 2026 Be OnlyOne
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    mercado_pago_max_installments = fields.Integer(
        string="Maximum Installments",
        help="Maximum number of installments offered in Mercado Pago Checkout "
        "Pro. The plans actually shown still depend on the card, issuer and "
        "amount. Interest-free promotions are configured in Mercado Pago, not "
        "in Odoo.",
        default=12,
    )

    @api.constrains("mercado_pago_max_installments", "code")
    def _check_mercado_pago_max_installments(self):
        for provider in self.filtered(lambda p: p.code == "mercado_pago"):
            if provider.mercado_pago_max_installments < 1:
                raise ValidationError(
                    _("The maximum number of installments must be at least 1.")
                )

    def _get_mercado_pago_max_installments(self):
        """Return the Checkout Pro installment cap for this provider.

        :return: Maximum installments to send in the preference payload.
        :rtype: int
        """
        self.ensure_one()
        return self.mercado_pago_max_installments or 12
