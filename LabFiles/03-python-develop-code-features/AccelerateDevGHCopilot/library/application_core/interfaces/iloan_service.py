from abc import ABC, abstractmethod
from ..enums.loan_return_status import LoanReturnStatus
from ..enums.loan_extension_status import LoanExtensionStatus
from ..entities.book_item import BookItem
from ..entities.loan import Loan
from ..entities.patron import Patron

class ILoanService(ABC):
    @abstractmethod
    def return_loan(self, loan_id: int) -> LoanReturnStatus:
        pass

    @abstractmethod
    def extend_loan(self, loan_id: int) -> LoanExtensionStatus:
        pass

    @abstractmethod
    def checkout_book(
        self,
        patron: Patron,
        book_item: BookItem,
        loan_id: int | None = None
    ) -> Loan:
        pass
