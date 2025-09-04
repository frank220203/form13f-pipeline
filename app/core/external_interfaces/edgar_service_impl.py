from typing import List

from domain.config_manager import ConfigManager
from domain.models.submissions.filings.recent import Recent
from domain.usecases.services.edgar_service import EdgarService

class EdgarServiceImpl(EdgarService):

    __url: str
    __data_url: str
    __meta_url: str
    __tickers_url: str
    __submissions_url: str

    def __init__(self, settings: ConfigManager):
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
    
    def filter_recent(self, recent: Recent, filing_type: List[str]) -> Recent:
        filtered_forms = []
        accession_numbers = recent.accession_number
        filtered_accession_numbers = []
        filings_dates = recent.filing_date
        filtered_filings_dates = []
        report_dates = recent.report_date
        filtered_report_dates = []
        acceptance_date_times = recent.acceptance_date_time
        filtered_acceptance_date_times = []

        for target in filing_type:
            for i, form_type in enumerate(recent.form):
                if form_type == target:
                    filtered_forms.append(form_type)
                    filtered_accession_numbers.append(accession_numbers[i])
                    filtered_filings_dates.append(filings_dates[i])
                    filtered_report_dates.append(report_dates[i])
                    filtered_acceptance_date_times.append(acceptance_date_times[i])

        recent.form = filtered_forms
        recent.accession_number = filtered_accession_numbers
        recent.filing_date = filtered_filings_dates
        recent.report_date = filtered_report_dates
        recent.acceptance_date_time = filtered_acceptance_date_times

        return recent