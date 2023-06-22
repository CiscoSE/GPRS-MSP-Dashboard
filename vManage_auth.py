import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import credentials

# Replace these variables with your own values 
username = credentials.vManage_username
password = credentials.vManage_password
vmanage_ip = '10.1.100.11'

def authenticate(vmanage_ip, username, password):
    url = f"https://{vmanage_ip}/j_security_check"
    payload = {"j_username": username, "j_password": password}
    session = requests.session()
    response = session.post(url, data=payload, verify=False)
    
    if response.status_code == 200:
        token_url = f"https://{vmanage_ip}/dataservice/client/token"
        token_response = session.get(token_url, verify=False)
        if token_response.status_code == 200:
            token = token_response.text
            return session, token
        else:
            raise Exception("Failed to obtain API token")
    else:
        raise Exception("Authentication failed")

def get_data(uri, query=None, query2 = None, vmanage_ip=vmanage_ip):
    session, token = authenticate(vmanage_ip, username, password)
    count = 60
    while True:
        url = f"https://{vmanage_ip}{uri}"
        headers = {"X-XSRF-TOKEN": token}
    
        params = {}
        if query2:
            params["query"] = json.dumps(query2)
        elif query:
            params = query

        response = session.get(url, headers=headers, params=params, verify=False)
        if response.status_code == 200:
            count = 60
            try:
                return response.json()
            except Exception as e:
                continue
        elif(response.status_code == 429):
            count = count * 1.25
            print("got response 429 from Vmanage, retrying in " + count + " seconds..")
            time.sleep(count)
            continue
        else:
            print(response, response.text)
            continue
        
def post_data(uri, param=None, vmanage_ip=vmanage_ip):
    session, token = authenticate(vmanage_ip, username, password)
    url = f"https://{vmanage_ip}{uri}"
    headers = {"X-XSRF-TOKEN": token}
    response = session.post(url, headers=headers, json=param, verify=False)
    if response.status_code == 200:
        return response
    else:
        print(response, response.text)
        raise Exception("Failed to get data")