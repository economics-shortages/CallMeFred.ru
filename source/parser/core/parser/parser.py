from parser.core.parser.browser import Browser
from parser.core.parser.browserless import Browserless

class Parser():

    def get_parser(self, browserless:bool = False):
        if browserless:
            return Browserless()
        else:
            return Browser()