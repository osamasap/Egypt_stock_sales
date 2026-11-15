# Testing Egypt Stock & Sales on ERPNext

## What was already tested (without a running ERPNext)

- Python compiles cleanly: `hooks.py`, `egypt_tax.py`, `stock.py`, DocType and report files
- Unit tests pass (4/4):
  - VAT 14% on 1000 EGP = 140 EGP
  - Withholding 1% on 1000 EGP = 10 EGP
  - Invoice totals: net 1000 + VAT 140 − withholding 10 = **1130 EGP**
  - Zero total = 0
- DocType JSON (`Egypt Sales Settings`) and report JSON (`Egypt Sales Summary`) are valid JSON

## What still needs a live ERPNext

A full install needs Docker (or bench) + MariaDB + Redis, at least 4 GB free RAM.
It cannot run on the current Muse VM — no Docker, no bench, and only ~0.5 GB free RAM.

## Test it on your machine (Docker)

```bash
docker compose up -d
# wait 2-3 minutes, open http://localhost:8080 (Administrator / admin)
docker compose exec backend bash -c "./install.sh erpnext.localhost"
```

## Manual test checklist (in ERPNext Desk)

1. Open **Egypt Sales Settings** — VAT rate should be 14, withholding 1, currency EGP
2. Create a Customer and an Item (stock item, EGP price 1000)
3. Create a **Sales Invoice** for that customer/item, net total 1000
4. Save — check `egypt_vat_amount` = 140, `egypt_withholding_amount` = 10
5. Submit the invoice, then open report **Egypt Sales Summary** — it should list the invoice with net 1000, VAT 140, grand total 1140 in the report view (report VAT is calculated on net, before withholding)
6. Check low-stock: set an item's stock below 10, call `egypt_stock_sales.utils.stock.get_low_stock_items`

## Known limitations (v0.1.0)

- VAT/withholding are stored in custom fields `egypt_vat_amount`, `egypt_withholding_amount`, `egypt_grand_total` — create them via Customize Form on Sales Invoice, or add them in a patch in the next version
- The report assumes VAT 14% in SQL; if you change the rate in settings, update the report too (planned fix: read the rate from settings)
- No e-invoicing integration yet
