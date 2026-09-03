=================================
Mercado Pago Website Installments
=================================

.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: https://onlyone.odoo.com/
    :alt: Be OnlyOne

|badge1| |badge2| |badge3|

Enable installment payments (cuotas) for Mercado Pago Checkout Pro on
Odoo 18 website and payment links. The native ``payment_mercado_pago``
module forces a single installment; this addon raises that cap and lets
the customer choose the plan on Mercado Pago.

**Table of contents**

.. contents::
   :local:

Configuration
=============

1. Install **Payment Provider: Mercado Pago** and this module.
2. Go to *Invoicing > Configuration > Payment Providers > Mercado Pago*.
3. Set **Maximum Installments** (default 12). This is the ceiling sent
   in the Checkout Pro preference; Mercado Pago still filters plans by
   card, issuer and amount.
4. Use the Checkout Pro Access Token (not Point or QR credentials).
5. Configure interest-free promotions and Mercado Crédito in the
   Mercado Pago panel of the same account. Those are not set in Odoo.

Usage
=====

1. Pay a website order (or payment link) with Mercado Pago.
2. Odoo redirects to Checkout Pro. The customer picks the payment method
   and the number of installments.
3. After approval, Odoo confirms the transaction and stores the chosen
   installments on the payment transaction.

Known issues / Roadmap
======================

* Installment selection stays on Mercado Pago (Checkout Pro). An inline
  Card Payment Brick on the Odoo website is out of scope.
* Interest-free installments cannot be defined from Odoo
  (``differential_pricing``).

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/onlyone-odoo/oo_mercado_pago_website/issues>`_.
In case of trouble, please check there if your issue has already been
reported. If you spotted it first, help us smash it by providing a
detailed and welcomed feedback.

Do not contact contributors directly about support or help with
technical issues.

Credits
=======

Authors
~~~~~~~

* Be OnlyOne

Contributors
~~~~~~~~~~~~

* `Be OnlyOne <https://onlyone.odoo.com/>`_

  * Matías Bressanello

Maintainers
~~~~~~~~~~~

This module is maintained by Be OnlyOne.
