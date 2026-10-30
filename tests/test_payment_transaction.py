# Copyright 2026 Be OnlyOne
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.oo_mercado_pago_website.models.payment_transaction import (
    PaymentTransaction,
)
from odoo.addons.payment.tests.http_common import PaymentHttpCommon
from odoo.addons.payment_mercado_pago.tests.common import MercadoPagoCommon


@tagged("post_install", "-at_install")
class TestMercadoPagoWebsiteInstallments(MercadoPagoCommon, PaymentHttpCommon):

    def _expected_preference_payload(self, tx, require_account=False):
        """Build the native preference plus this module's expected changes.

        ``payment_methods.installments`` replaces the native cap of 1.
        ``purpose`` is added only when a logged-in Mercado Pago account is
        required. Every other native key is left untouched.
        """
        payload = super(
            PaymentTransaction, tx
        )._mercado_pago_prepare_preference_request_payload()
        payment_methods = dict(payload.get("payment_methods") or {})
        payment_methods["installments"] = (
            tx.provider_id._get_mercado_pago_max_installments()
        )
        payload = dict(payload)
        payload["payment_methods"] = payment_methods
        if require_account:
            payload["purpose"] = "wallet_purchase"
        return payload

    def test_require_account_is_disabled_by_default(self):
        """Do not force a Mercado Pago login unless an admin enables it."""
        self.assertFalse(self.provider.mercado_pago_require_account)

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

    def test_preference_payload_without_account_keeps_native_shape(self):
        """A disabled flag must not add purpose or drop native keys."""
        self.provider.mercado_pago_max_installments = 9
        self.provider.mercado_pago_require_account = False
        tx = self._create_transaction(flow="redirect")
        payload = tx._mercado_pago_prepare_preference_request_payload()
        self.assertEqual(payload, self._expected_preference_payload(tx))
        self.assertNotIn("purpose", payload)
        self.assertEqual(payload["payment_methods"]["installments"], 9)

    def test_preference_payload_with_account_sets_wallet_purchase(self):
        """Require a logged-in account without replacing the installment cap."""
        self.provider.mercado_pago_max_installments = 6
        self.provider.mercado_pago_require_account = True
        tx = self._create_transaction(flow="redirect")
        payload = tx._mercado_pago_prepare_preference_request_payload()
        self.assertEqual(
            payload,
            self._expected_preference_payload(tx, require_account=True),
        )
        self.assertEqual(payload["purpose"], "wallet_purchase")
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
