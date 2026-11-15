"""Egypt tax calculations — pure Python, no Frappe dependency.

This keeps the math testable without a running bench.
All amounts are in EGP.
"""

EGYPT_VAT_RATE = 14.0
WITHHOLDING_PRESETS = (1.0, 3.0, 5.0)


def calculate_vat(net_total, vat_rate=EGYPT_VAT_RATE):
    """Return VAT amount for a net total, rounded to 2 decimals."""
    if net_total is None or net_total < 0:
        raise ValueError("net_total must be >= 0")
    if vat_rate is None or vat_rate < 0:
        raise ValueError("vat_rate must be >= 0")
    return round(float(net_total) * float(vat_rate) / 100.0, 2)


def calculate_withholding(net_total, withholding_rate=1.0):
    """Return withholding tax (خصم منبع) for a net total."""
    if net_total is None or net_total < 0:
        raise ValueError("net_total must be >= 0")
    if withholding_rate is None or withholding_rate < 0:
        raise ValueError("withholding_rate must be >= 0")
    return round(float(net_total) * float(withholding_rate) / 100.0, 2)


def calculate_invoice_totals(net_total, vat_rate=EGYPT_VAT_RATE, withholding_rate=1.0):
    """Return a dict with vat, withholding and grand total in EGP."""
    vat = calculate_vat(net_total, vat_rate)
    withholding = calculate_withholding(net_total, withholding_rate)
    grand_total = round(float(net_total) + vat - withholding, 2)
    return {
        "net_total": round(float(net_total), 2),
        "vat_amount": vat,
        "withholding_amount": withholding,
        "grand_total": grand_total,
        "currency": "EGP",
    }


def apply_egypt_taxes(doc, method=None):
    """Frappe hook: run on Sales Invoice validate.

    Reads rates from Egypt Sales Settings when available, otherwise
    uses the Egyptian defaults (VAT 14%, withholding 1%).
    Sets custom fields on the invoice document.
    """
    try:
        import frappe

        settings = frappe.get_single("Egypt Sales Settings")
        vat_rate = float(settings.vat_rate or EGYPT_VAT_RATE)
        withholding_rate = float(settings.withholding_rate or 1.0)
    except Exception:
        vat_rate = EGYPT_VAT_RATE
        withholding_rate = 1.0

    net_total = float(getattr(doc, "net_total", 0) or 0)
    totals = calculate_invoice_totals(net_total, vat_rate, withholding_rate)

    # Custom fields — create them in ERPNext via Customize Form,
    # or add them in a patch in a later version.
    doc.egypt_vat_amount = totals["vat_amount"]
    doc.egypt_withholding_amount = totals["withholding_amount"]
    doc.egypt_grand_total = totals["grand_total"]
