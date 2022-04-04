from parser.core.parser.parser import Parser
import time

class Bank_Sector_Loans_DbTMP():
    TARGET_URL = 'https://www.cbr.ru/statistics/bank_sector/int_rat/LoansDB/'
    parser = None

    def start(self):
        self.parser = Parser().get_parser(browserless=False)
        self.parser.init_url(self.TARGET_URL)
        frame_url = self.get_iframe_url()
        self.parser.init_url(frame_url)
        time.sleep(3)
        self.parser.print()
        self.download_file()

    def get_iframe_url(self) -> str:
        elem = self.parser.get_elems('iframe#html5src')
        return elem.get_attribute('src')

    def download_file(self):
        elem = self.parser.get_elems('#xc-URLButton-div-xgen_2893')
        elem.click();
        time.sleep(20)

    def upload_to_db(self):
        pass