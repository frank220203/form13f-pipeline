from pymongo.errors import DuplicateKeyError
from core.entities.submission_document import SubmissionDocument

from domain.models.submissions.submission import Submission
from domain.usecases.repositories.submission_repository import SubmissionRepository

class SubmissionRepositoryImpl(SubmissionRepository):

    async def add_data(self, submission: Submission) -> Submission:
        submission_doc = SubmissionDocument(**submission.model_dump())
        try:
            await submission_doc.insert()
        except DuplicateKeyError:
            print("submission_doc 중복")
        return Submission(**submission_doc.model_dump())