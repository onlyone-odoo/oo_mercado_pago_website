`1.1.0`
-------

- Add an option on the Mercado Pago provider to accept only buyers logged
  in to a Mercado Pago account. It is disabled by default. When enabled,
  the Checkout Pro preference includes ``purpose = "wallet_purchase"``. Guest
  checkout, cash and bank transfer are not offered. The installment cap
  and the other native preference keys stay unchanged.

`1.0.0`
-------

- Enable Mercado Pago Checkout Pro installments on website payments. The
  native provider forced a single installment; the maximum is now
  configurable (default 12) and the chosen plan is stored on the
  transaction.
