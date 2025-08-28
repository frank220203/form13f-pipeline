from abc import ABC, abstractmethod
from domain.models.submissions.submission import Submission

class SubmissionRepository(ABC):
    @abstractmethod
    async def add_data(self, submission: Submission) -> Submission:
        pass