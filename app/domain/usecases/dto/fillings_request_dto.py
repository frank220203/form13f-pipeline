from pydantic import BaseModel, model_validator

class FillingsRequestDto(BaseModel):
    url: str = "https://www.sec.gov"
    headers: dict
    params: dict
    endpoint: str

    @model_validator(mode='after')
    def make_full_url(cls, values):
        values.url = f"{values.url}/{values.endpoint}"
        return values