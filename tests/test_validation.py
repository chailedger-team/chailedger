import pytest

from app.errors import ValidationError
from app.validation import kenyan_phone, kilograms, month, positive_int, timestamp


@pytest.mark.parametrize(
    "raw",
    ["0712345678", "+254712345678", "254712345678", "0712 345 678", "0712-345-678"],
)
def test_kenyan_phone_normalises_common_formats(raw):
    assert kenyan_phone(raw) == "+254712345678"


def test_kenyan_phone_accepts_new_01_prefix():
    assert kenyan_phone("0110123456") == "+254110123456"


@pytest.mark.parametrize("raw", ["12345", "0812345678", "+255712345678", "", None, 712345678])
def test_kenyan_phone_rejects_invalid(raw):
    with pytest.raises(ValidationError):
        kenyan_phone(raw)


def test_kilograms_rounds_to_two_decimals():
    assert kilograms("12.3456", "kg", 150) == 12.35


@pytest.mark.parametrize("raw", [0, -5, 151, "abc", None, True])
def test_kilograms_rejects_invalid(raw):
    with pytest.raises(ValidationError):
        kilograms(raw, "kg", 150)


@pytest.mark.parametrize("raw", [0, -1, "x", None, True, 2.5])
def test_positive_int_rejects_invalid(raw):
    with pytest.raises(ValidationError):
        positive_int(raw, "id")


def test_positive_int_accepts_numeric_string():
    assert positive_int("7", "id") == 7


def test_month_validation():
    assert month("2026-10") == "2026-10"
    assert len(month(None)) == 7
    with pytest.raises(ValidationError):
        month("10-2026")


def test_timestamp_validation():
    assert timestamp("2026-10-22T08:30") == "2026-10-22T08:30:00"
    with pytest.raises(ValidationError):
        timestamp("yesterday")
