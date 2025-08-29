
from pydantic import BaseModel
from domain.models.portfolios.header_data.filer_infos.filers.credential import Credential

class Filer(BaseModel):
    credentials: Credential