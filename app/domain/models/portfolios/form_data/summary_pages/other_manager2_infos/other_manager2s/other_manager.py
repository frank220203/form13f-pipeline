from pydantic import BaseModel, Field, AliasChoices

class OtherManager(BaseModel):
    form13_f_file_number: str = Field(..., alias=AliasChoices("form13FFileNumber", "form13_f_file_number"))
    name: str