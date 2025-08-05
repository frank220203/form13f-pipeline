from typing import Optional
from pydantic import Field, BaseModel, model_validator

class FilingsRequestDto(BaseModel):
    email: str = Field(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구")
    endpoint: str = Field(..., description="ex) /cgi-bin/browse-edgar/getcompany")
    meta: Optional[dict] = None
    params: Optional[dict] = None
    headers: Optional[dict] = None

    @model_validator(mode='after')
    def make_headers(cls, values):
        values.headers = {'User-Agent': values.email}
        print(values)
        return values