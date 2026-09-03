# Copyright 2026 Be OnlyOne
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.payment.tests.http_common import PaymentHttpCommon
from odoo.addons.payment_mercado_pago.tests.common import MercadoPagoCommon


@tagged("post_install", "-at_install")
class TestMercadoPagoWebsiteInstallments(MercadoPagoCommon, PaymentHttpCommon):

    def test_preference_payload_uses_default_max_installments(self):
        """Checkout Pro preferences must allow up to 12 installments by default."""
        tx = self._create_transaction(flow="redirect")
        payload = tx._mercado_pago_prepare_preference_request_payload()
        self.assertEqual(payload["payment_methods"]["installments"], 12)

    def test_preference_payload_uses_configured_max_installments(self):
        """The provider setting must be sent as the Checkout Pro installment cap."""
        self.provider.mercado_pago_max_installments = 6
        tx = self._create_transaction(flow="redirect")
        payload = tx._mercado_pago_prepare_preference_request_payload()
        self.assertEqual(payload["payment_methods"]["installments"], 6)

    def test_max_installments_must_be_at_least_one(self):
        """Reject an installment cap below 1 for Mercado Pago providers."""
        self.provider.mercado_pago_max_installments = 12
        with self.assertRaises(ValidationError):
            self.provider.mercado_pago_max_installments = 0

    def test_processing_notification_data_stores_installments(self):
        """Store the installments returned by Mercado Pago on the transaction."""
        tx = self._create_transaction(flow="redirect")
        verification_data = dict(self.verification_data, installments=6)
        with patch(
            "odoo.addons.payment_mercado_pago.models.payment_provider.PaymentProvider"
            "._mercado_pago_make_request",
            return_value=verification_data,
        ):
            tx._process_notification_data(self.redirect_notification_data)
        self.assertEqual(tx.mercado_pago_installments, 6)
        self.assertEqual(tx.state, "done")
