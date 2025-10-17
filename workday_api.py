import requests
import xmltodict
import time

class WorkdayAPI:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.company_reference = 'dde36542331f1000b66f45813fbd0000'  # Example company reference

    def get_search_data(self):
        """Send a search SOAP request and return the parsed response."""
        from utils import SOAPBuilder
        soap_body = SOAPBuilder.get_search_soap_body(self.username, self.password, self.company_reference)
        response = requests.post(self.url, data=soap_body, headers={"Content-Type": "text/xml"})
        response.raise_for_status()
        return xmltodict.parse(response.content)

    def post_with_retries(self, payload, max_retries=3, backoff_sec=2):
        """Post payload to Workday with retries and return the parsed response."""
        last_exception = None
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(self.url, data=payload, headers={"Content-Type": "text/xml; charset=UTF-8"})
                response.raise_for_status()
                return response.content
            except Exception as e:
                last_exception = e
                print(f"Attempt {attempt} failed: {e}")
                if attempt < max_retries:
                    time.sleep(backoff_sec * attempt)
        raise last_exception