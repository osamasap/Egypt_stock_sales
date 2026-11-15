# Egypt Stock & Sales for ERPNext

A custom Frappe app for the Egyptian market — inventory and sales on top of ERPNext.

It adds, without touching ERPNext core:

- **Egypt VAT (14%)** on Sales Invoices, with a configurable rate
- **Withholding tax (خصم منبع)** — 1% / 3% / 5% presets, configurable
- **Low-stock alerts** for items below a threshold
- **Egypt sales summary report** — sales by customer, item group and governorate
- Prices in **EGP**, with Arabic item descriptions supported

## Install

```bash
bench get-app https://github.com/osamasap/Egypt_stock_sales
bench --site yoursite.local install-app egypt_stock_sales
bench --site yoursite.local migrate
```

Requires ERPNext v15 / v16 and Frappe Framework v15 / v16.

## Configure

Open **Egypt Sales Settings** (single DocType) and set:

- VAT rate — default `14`
- Withholding tax rate — default `1`
- Low stock threshold — default `10`
- Enable low stock alerts

## How it works

- On Sales Invoice validation, `egypt_stock_sales.utils.egypt_tax` calculates
  VAT and withholding tax from the invoice net total, and stores them in
  custom fields on the invoice.
- The report `Egypt Sales Summary` groups posted Sales Invoices by customer
  and item group, with VAT and net totals in EGP.
- Low-stock items are listed by a whitelisted API method
  `egypt_stock_sales.utils.stock.get_low_stock_items`.

## Development

```bash
python -m pytest egypt_stock_sales/tests/test_egypt_tax.py -v
```

## License

GPL-3.0 — same as ERPNext.
