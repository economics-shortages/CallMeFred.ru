import requests

class Browserless():
    r: requests.Response

    def getUrl(self):
        pass

    def init_url(self, url: str):
        self.r = requests.get(url, allow_redirects=True)
    
    def save(self, target_file):
        open(target_file, 'wb').write(self.r.content)


