from pydantic import BaseModel

class FillingsRequestDto(BaseModel):
    url: str = "https://www.sec.gov/cgi-bin/browse-edgar"
    headers: dict
    params: dict