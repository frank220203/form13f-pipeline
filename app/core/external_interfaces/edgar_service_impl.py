from typing import List
from core.config import Settings

from domain.models.submission import Submission
from domain.usecases.services.edgar_service import EdgarService

class EdgarServiceImpl(EdgarService):

    __url: str
    __data_url: str
    __meta_url: str
    __tickers_url: str
    __submissions_url: str

    def __init__(self, settings: Settings):
        self.__url = settings.get_sec_url()
        self.__data_url = settings.get_data_url()
        self.__meta_url = settings.get_meta_url()
        self.__tickers_url = settings.get_tickers_url()
        self.__submissions_url = settings.get_submissions_url()
        
    def get_edgar_tickers_url(self) -> str:
        return self.__url + self.__tickers_url
    
    def get_submissions_url(self, cik: str) -> str:
        return f"{self.__submissions_url}{cik}.json"
    
    def get_portfolio_url(
            self, 
            cik: str, 
            accession_number: str, 
            type: str = None,
            file_name: str = None
            ) -> str:
        cik = cik[3:]
        accession_number = accession_number.replace("-", '')
        url = ""
        if type == "meta":
            url = f"{self.__data_url}/{cik}/{accession_number}{self.__meta_url}"
        elif type == "data":
            url = f"{self.__url}{file_name}"
        else:
            url = f"{self.__data_url}/{cik}/{accession_number}"
        return url
    
    def find_submissions(self, submissions: Submission, filing_type: List[str]) -> Submission:
        recent = submissions.filings['recent']
        filtered_filings = {'recent':[{}]}
        filtered_recent = []
        accession_numbers = recent['accessionNumber']
        filings_dates = recent['filingDate']
        report_dates = recent['reportDate']
        acceptance_date_times = recent['acceptanceDateTime']
        forms = recent['form']

        for target in filing_type:
            for i, form_type in enumerate(forms):
                if form_type == target:
                    filtered_recent.append({
                        'form':form_type,
                        'accessionNumber':accession_numbers[i],
                        'filingDate':filings_dates[i],
                        'reportDate':report_dates[i],
                        'acceptanceDateTime':acceptance_date_times[i]
                    })

        filtered_filings['recent'] = filtered_recent
        submissions.filings = filtered_filings
        return submissions