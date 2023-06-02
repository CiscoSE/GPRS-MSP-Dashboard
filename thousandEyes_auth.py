import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
from pprint import pprint
import credentials

def get_data(uri):
     while True:
        url = f"https://api.thousandeyes.com{uri}"
        headers = {"Authorization": "Bearer "+credentials.thousandEyes_token}
        response = requests.get(url, headers=headers, params={"format":"json"}, verify=False)
        if response.status_code == 200:
            return response.json()
        elif(response.status_code == 429):
            print("got response 429 from ThousandEyes, retrying in 60 seconds..")
            time.sleep(60)
            continue
        else:
            print(response, response.text)
            raise Exception("Failed to get data")


if __name__ == "__main__":
    pprint(get_data(uri="/v6/web/http-server/3732333"))

    