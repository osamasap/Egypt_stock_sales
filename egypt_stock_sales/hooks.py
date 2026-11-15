app_name = "egypt_stock_sales"
app_title = "Egypt Stock & Sales"
app_publisher = "Osama"
app_description = "Inventory and sales for the Egyptian market on ERPNext"
app_email = "osamasap@users.noreply.github.com"
app_license = "gpl-3.0"
app_version = "0.1.0"

# Fixtures: keep settings in version control
fixtures = ["Egypt Sales Settings"]

doc_events = {
    "Sales Invoice": {
        "validate": "egypt_stock_sales.utils.egypt_tax.apply_egypt_taxes",
    },
}

# Whitelisted API methods are called from the desk / reports
# egypt_stock_sales.utils.stock.get_low_stock_items
