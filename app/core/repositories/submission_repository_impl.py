from core.entities.submission_document import SubmissionDocument

from domain.models.submissions.submission import Submission
from domain.usecases.repositories.submission_repository import SubmissionRepository

class SubmissionRepositoryImpl(SubmissionRepository):

    async def add_data(self, submission: Submission) -> Submission:
        submission_doc = SubmissionDocument(**submission.model_dump())
        await submission_doc.insert()
        return Submission(**submission_doc.model_dump())