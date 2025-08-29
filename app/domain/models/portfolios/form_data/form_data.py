from pydantic import BaseModel, Field, AliasChoices
from domain.models.portfolios.form_data.cover_pages.cover_page import CoverPage
from domain.models.portfolios.form_data.signature_block import SignatureBlock
from domain.models.portfolios.form_data.summary_pages.summary_page import SummaryPage

class FormData(BaseModel):
    cover_page: CoverPage = Field(..., alias=AliasChoices("coverPage", "cover_page"))
    signature_block: SignatureBlock = Field(..., alias=AliasChoices("signatureBlock", "signature_block"))
    summary_page: SummaryPage = Field(..., alias=AliasChoices("summaryPage", "summary_page"))