from pydantic import BaseModel
from domain.models.submissions.addresses.mailing import Mailing
from domain.models.submissions.addresses.business import Business

class Address(BaseModel):
    mailing: Mailing
    business: Business