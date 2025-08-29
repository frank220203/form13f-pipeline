from pydantic import BaseModel, Field, AliasChoices
from domain.models.portfolios.form_data.cover_pages.filing_managers.filing_manager import FilingManager

class CoverPage(BaseModel):
    report_calendar_or_quartor: str = Field(..., alias=AliasChoices("reportCalendarOrQuarter", "report_calendar_or_quartor"))
    is_amendment: str = Field(..., alias=AliasChoices("isAmendment", "is_amendment"))
    filing_manager: FilingManager = Field(..., alias=AliasChoices("filingManager", "filing_manager"))
    report_type: str = Field(..., alias=AliasChoices("reportType", "report_type"))
    form13_f_file_number: str = Field(..., alias=AliasChoices("form13FFileNumber", "form13_f_file_number"))
    provide_info_for_instruction5: str = Field(..., alias=AliasChoices("provideInfoForInstruction5", "provide_info_for_instruction5"))