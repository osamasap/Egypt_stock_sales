#!/bin/bash
# Install Egypt Stock & Sales on an existing ERPNext site.
# Usage (inside a bench directory, or in the Docker backend container):
#   ./install.sh [site-name]
# Default site: erpnext.localhost
set -e
SITE="${1:-erpnext.localhost}"

echo "Installing egypt_stock_sales on site: $SITE"
bench get-app https://github.com/osamasap/Egypt_stock_sales
bench --site "$SITE" install-app egypt_stock_sales
bench --site "$SITE" migrate

echo ""
echo "Done. Open Egypt Sales Settings and set VAT rate (default 14) and withholding rate (default 1)."
echo "Then create a Sales Invoice with net total 1000 EGP and check:"
echo "  VAT = 140 EGP, withholding = 10 EGP, grand total = 1130 EGP"
