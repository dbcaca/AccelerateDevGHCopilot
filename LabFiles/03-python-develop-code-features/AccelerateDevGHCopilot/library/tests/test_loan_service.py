import unittest
from unittest.mock import MagicMock
from application_core.services.loan_service import LoanService
from application_core.entities.book_item import BookItem
from application_core.entities.loan import Loan
from application_core.entities.patron import Patron
from application_core.enums.loan_return_status import LoanReturnStatus
from datetime import datetime, timedelta

class TestLoanService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = LoanService(self.mock_repo)

    def test_return_loan_success(self):
        loan = Loan(id=1, book_item_id=1, patron_id=1, patron=None, loan_date=datetime.now()-timedelta(days=10), due_date=datetime.now()+timedelta(days=10), return_date=None, book_item=None)
        self.mock_repo.get_loan.return_value = loan
        self.mock_repo.update_loan.return_value = None
        status = self.service.return_loan(1)
        self.assertEqual(status, LoanReturnStatus.SUCCESS)

    def test_return_loan_not_found(self):
        self.mock_repo.get_loan.return_value = None
        status = self.service.return_loan(1)
        self.assertEqual(status, LoanReturnStatus.LOAN_NOT_FOUND)

    def test_checkout_book_creates_and_persists_loan(self):
        self.mock_repo.get_all_loans.return_value = [
            Loan(
                id=3,
                book_item_id=1,
                patron_id=1,
                loan_date=datetime.now(),
                due_date=datetime.now() + timedelta(days=14)
            )
        ]
        now = datetime.now()
        patron = Patron(
            id=42,
            name="Patron",
            membership_end=now + timedelta(days=30),
            membership_start=now
        )
        book_item = BookItem(id=7, book_id=9, acquisition_date=now)

        loan = self.service.checkout_book(patron, book_item)

        self.assertEqual(loan.id, 4)
        self.assertEqual(loan.book_item_id, book_item.id)
        self.assertEqual(loan.patron_id, patron.id)
        self.assertEqual(loan.return_date, None)
        self.assertEqual(loan.due_date - loan.loan_date, timedelta(days=14))
        self.mock_repo.add_loan.assert_called_once_with(loan)

if __name__ == "__main__":
    unittest.main()