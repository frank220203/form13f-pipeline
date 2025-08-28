from pydantic import BaseModel
from domain.models.submissions.filings.recent import Recent

class Filing(BaseModel):
    recent: Recent = None