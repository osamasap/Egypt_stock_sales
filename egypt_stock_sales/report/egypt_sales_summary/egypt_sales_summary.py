"""Egypt Sales Summary — script report over posted Sales Invoices."""

import frappe


def execute(filters=None):
    columns = [
        {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"fieldname": "item_group", "label": "Item Group", "fieldtype": "Data", "width": 150},
        {"fieldname": "invoices", "label": "Invoices", "fieldtype": "Int", "width": 90},
        {"fieldname": "net_total", "label": "Net Total (EGP)", "fieldtype": "Currency", "width": 140},
        {"fieldname": "vat_amount", "label": "VAT 14% (EGP)", "fieldtype": "Currency", "width": 140},
        {"fieldname": "grand_total", "label": "Grand Total (EGP)", "fieldtype": "Currency", "width": 140},
    ]

    conditions = "si.docstatus = 1"
    if filters and filters.get("from_date"):
        conditions += " AND si.posting_date >= %(from_date)s"
    if filters and filters.get("to_date"):
        conditions += " AND si.posting_date <= %(to_date)s"

    data = frappe.db.sql(
        f"""
        SELECT
            si.customer AS customer,
            sii.item_group AS item_group,
            COUNT(DISTINCT si.name) AS invoices,
            SUM(sii.net_amount) AS net_total,
            ROUND(SUM(sii.net_amount) * 0.14, 2) AS vat_amount,
            ROUND(SUM(sii.net_amount) * 1.14, 2) AS grand_total
        FROM `tabSales Invoice` si
        JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
        WHERE {conditions}
        GROUP BY si.customer, sii.item_group
        ORDER BY net_total DESC
        """,
        filters or {},
        as_dict=True,
    )

    return columns, data
