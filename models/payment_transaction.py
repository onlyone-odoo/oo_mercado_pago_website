# Copyright 2026 Be OnlyOne
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    mercado_pago_installments = fields.Integer(
        string="Installments",
        help="Number of installments chosen by the customer on Mercado Pago.",
        readonly=True,
        copy=False,
    )

    def _mercado_pago_prepare_preference_request_payload(self):
        """Override of `payment_mercado_pago` to allow Checkout Pro installments.

        The native module hard-codes ``payment_methods.installments`` to 1.
        """
        payload = super()._mercado_pago_prepare_preference_request_payload()
        if self.provider_code != "mercado_pago":
            return payload
        payload.setdefault("payment_methods", {})[
            "installments"
        ] = self.provider_id._get_mercado_pago_max_installments()
        return payload

    def _process_notification_data(self, notification_data):
        """Override of `payment` to store the installments chosen on Mercado Pago.

        The native flow already fetches ``GET /v1/payments/{id}`` to confirm the
        payment. A second GET is used here so we do not duplicate that logic.
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != "mercado_pago" or not self.provider_reference:
            return
        verified_payment_data = self.provider_id._mercado_pago_make_request(
            f"/v1/payments/{self.provider_reference}", method="GET"
        )
        installments = verified_payment_data.get("installments")
        if installments:
            self.write({"mercado_pago_installments": installments})
