import vManage_auth
from pprint import pprint

def get_data():
    result = []
    query = {"query":{
        "field": "active",
        "type": "boolean",
        "value": ["true"],
        "operator": "equal"
    }}
    data = vManage_auth.get_data("/dataservice/alarms",query2=query)["data"]
    for item in data:
        if(item["acknowledged"]==False and item["active"]==True):
            item["severity"] = item["severity"].lower()
            if('host-name' not in item['values'][0].keys()):
                item['values'][0]['host-name'] = "NA"
            if(item["severity"]=="medium"):
                item["severity"] = "moderate"
            if(item["severity"]=="minor"):
                item["severity"] = "warning"
            result.append({"summary": item["eventname"], "name": item['values'][0]['host-name'], "severity": item["severity"] , "url" : "https://"+vManage_auth.vmanage_ip + "/#/app/monitor/alarms/details/" + str(item["uuid"])})
    return result

if __name__ == "__main__":
    pprint(get_data())
