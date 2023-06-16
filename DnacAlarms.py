"""
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

import Dnac_auth
from pprint import pprint


def get_data():
    """Get data from DNAC

    Args:   None
    
    Returns:   List of dict

    """
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
