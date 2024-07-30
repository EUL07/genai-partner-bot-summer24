import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl = fileurl
        self.name_dict = {}
        self.ticker_dict = {}

        headers = {'User-Agent': 'MLTGS gspivey@mlt.org'}

        try:
            r = requests.get(self.fileurl, headers=headers)
            r.raise_for_status()  # Raise an error for bad status codes

            self.filejson = r.json()  # Call json() method correctly
            print(r.text)  # Print the raw text for debugging
            print(self.filejson)  # Print the parsed JSON for debugging

            self.cik_json_to_dict()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            self.filejson = None

    def cik_json_to_dict(self):
        if not self.filejson or not isinstance(self.filejson, dict):
            print("No valid JSON data to process")
            return

        for entry in self.filejson.values():
            if not isinstance(entry, dict) or 'cik_str' not in entry or 'title' not in entry or 'ticker' not in entry:
                print("Unexpected entry format:", entry)
                continue

            cik = entry['cik_str']
            company_name = entry['title']
            ticker = entry['ticker']
            self.name_dict[company_name.upper()] = (cik, company_name, ticker)
            self.ticker_dict[ticker.upper()] = (cik, company_name, ticker)

    def name_to_cik(self, name):
        return self.name_dict.get(name.upper(), None)

    def ticker_to_cik(self, ticker):
        return self.ticker_dict.get(ticker.upper(), None)

    def cik_to_info(self, cik):
        for info in self.name_dict.values():
            if info[0] == cik:
                return info
        return None

# Example usage
if __name__ == "__main__":
    file_url = 'https://www.sec.gov/files/company_tickers.json'  # URL to fetch JSON data
    sec_edgar = SecEdgar(file_url)

    # Test lookups
    print(sec_edgar.name_to_cik('BANK OF MONTREAL /CAN/'))
    print(sec_edgar.ticker_to_cik('GDXU'))
    print(sec_edgar.cik_to_info(927971))
