
from parser.target.cbr.bank_sector_loans_db import Bank_Sector_Loans_Db;


class Targets():

    def parse_targets(self):
        parser = Bank_Sector_Loans_Db()
        parser.start()