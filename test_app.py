import pytest
from app import get_vendors, add_vendor, delete_vendor, main


def test_get_vendors():
    vendors = get_vendors()
    assert "error" not in vendors


def test_vendor_addition_deletion():
    response = add_vendor("Test Vendor", "Test Vendor", "Misc", "test")
    assert "error" not in response
    delete_response = delete_vendor("Test Vendor")
    assert "error" not in delete_response


@pytest.mark.parametrize(
    "file, bank",
    [
        ("test_transactions_axis.txt", "axis"),
        ("test_transactions_hdfc.txt", "hdfc"),
        ("test_transactions_yes.txt", "yes"),
    ],
)
def test_main(file, bank):
    response = main(file, bank)
    assert "error" not in response
