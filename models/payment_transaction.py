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
        """Override of `payment_mercado_pago` to tune the Checkout Pro preference.

        The native module hard-codes ``payment_methods.installments`` to 1
        and does not set ``purpose``. ``purpose`` is a top-level preference
        attribute, so requiring a logged-in account does not replace
        ``payment_methods`` or any other native key. It is omitted unless
        the provider asks for it, which keeps the current payload.
        """
        payload = super()._mercado_pago_prepare_preference_request_payload()
        if self.provider_code != "mercado_pago":
            return payload
        payload.setdefault("payment_methods", {})[
            "installments"
        ] = self.provider_id._get_mercado_pago_max_installments()
        if self.provider_id.mercado_pago_require_account:
            payload["purpose"] = "wallet_purchase"
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
