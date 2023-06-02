import Dnac_auth
from pprint import pprint


def get_data():
    result = []
    data = Dnac_auth.get_data(uri="/dna/intent/api/v1/issues")["response"]
    for item in data:
        if(item["status"]!="active"):
            continue
        query = {
        "entity_type": "issue_id",
        "entity_value": item["issueId"]
        }
        tmp = Dnac_auth.get_data(uri="/dna/intent/api/v1/issue-enrichment-details", header=query)
        for i in tmp['issueDetails']['issue']:
            query = {
                "searchBy": i["deviceId"],
                "identifier": "uuid"
            }
            detailData = Dnac_auth.get_data(uri="/dna/intent/api/v1/device-detail", query=query)['response']
            i["issueSeverity"] = i["issueSeverity"].lower()
            if(i["issueSeverity"]=='high'):
                i["issueSeverity"] = "major"
            elif(i["issueSeverity"]=='medium'):
                i["issueSeverity"] = "moderate"
            elif(i["issueSeverity"]=='minor'):
                i["issueSeverity"] = "warning"
            result.append({"severity":i["issueSeverity"], "summary": i["issueName"], "name": detailData["nwDeviceName"], "url": Dnac_auth.BASE_URL + "/dna/assurance/dashboards/issues-events/issues/open" })
    return result

if __name__ == "__main__":
    pprint(get_data())
