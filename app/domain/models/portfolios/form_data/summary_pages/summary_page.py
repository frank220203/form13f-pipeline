from pydantic import BaseModel, Field, AliasChoices
from domain.models.portfolios.form_data.summary_pages.other_manager2_infos.other_manager2_info import OtherManager2Info

class SummaryPage(BaseModel):
    other_included_managers_count: str = Field(..., alias=AliasChoices("otherIncludedManagersCount", "other_included_managers_count"))
    table_entry_total: str = Field(..., alias=AliasChoices("tableEntryTotal", "table_entry_total"))
    table_value_total: str = Field(..., alias=AliasChoices("tableValueTotal", "table_value_total"))
    is_confidential_omitted: str = Field(..., alias=AliasChoices("isConfidentialOmitted", "is_confidential_omitted"))
    other_manager2_info: OtherManager2Info = Field(..., alias=AliasChoices("otherManagers2Info", "other_manager2_info"))