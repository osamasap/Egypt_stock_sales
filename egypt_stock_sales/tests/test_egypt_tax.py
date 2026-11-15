"""Tests for Egypt tax calculations — run without Frappe/bench."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from egypt_stock_sales.utils.egypt_tax import (
    calculate_invoice_totals,
    calculate_vat,
    calculate_withholding,
)


def test_vat_14_percent():
    assert calculate_vat(1000) == 140.0
    assert calculate_vat(1000, 14.0) == 140.0


def test_withholding_1_percent():
    assert calculate_withholding(1000) == 10.0
    assert calculate_withholding(1000, 3.0) == 30.0


def test_invoice_totals_egp():
    totals = calculate_invoice_totals(1000)
    assert totals == {
        "net_total": 1000.0,
        "vat_amount": 140.0,
        "withholding_amount": 10.0,
        "grand_total": 1130.0,
        "currency": "EGP",
    }


def test_zero_total():
    assert calculate_invoice_totals(0)["grand_total"] == 0.0
