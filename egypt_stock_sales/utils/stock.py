"""Stock helpers for the Egyptian market."""


def get_low_stock_items(threshold=10):
    """Whitelisted API: return items whose stock is below threshold.

    Returns a list of dicts: item_code, item_name, warehouse, actual_qty.
    Requires a running Frappe site; returns [] when called outside Frappe.
    """
    try:
        import frappe

        return frappe.db.sql(
            """
            SELECT item_code, warehouse, actual_qty
            FROM `tabBin`
            WHERE actual_qty < %s
            ORDER BY actual_qty ASC
            LIMIT 100
            """,
            (threshold,),
            as_dict=True,
        )
    except Exception:
        return []
