import pytest
from django.core.exceptions import ValidationError
from pos.models import Receipt, Transaction
from django.utils import timezone

@pytest.mark.django_db
class TestReceipt:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.transaction = Transaction.objects.create(
            product_id=1,  # Assuming a product with ID 1 exists
            amount=100.00,
            date=timezone.now()
        )
        self.receipt = Receipt.objects.create(
            transaction=self.transaction,
            receipt_number="12345",
            generated_date=timezone.now()
        )

    def test_receipt_creation(self):
        assert self.receipt.transaction == self.transaction
        assert self.receipt.receipt_number == "12345"
        assert self.receipt.email_sent is False

    def test_receipt_uniqueness(self):
        with pytest.raises(ValidationError):
            Receipt.objects.create(
                transaction=self.transaction,
                receipt_number="12345",
                generated_date=timezone.now()
            )

    def test_send_via_email(self):
        self.receipt.send_via_email()
        assert self.receipt.email_sent is True