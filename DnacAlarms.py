import Dnac_auth
from pprint import pprint


def get_data():
    """ Get all alarms from DNAC

    params:   None
    
    Returns:   List of dictionaries containing the following keys:
                severity (str): severity of the alarm
                summary (str): summary of the alarm
                name (str): name of the device
                url (str): url to the alarm in DNAC

    example:
                [{'name': 'CPS-BDR',
                 'severity': 'major',
                 'summary': 'device_time_drift',
                 'url': 'https://10.1.100.4/dna/assurance/dashboards/issues-events/issues/open'},
                {'name': 'Appx_CSR1Kv',
                 'severity': 'moderate',
                 'summary': 'router_interface_excess_rx_tx_util',
                 'url': 'https://10.1.100.4/dna/assurance/dashboards/issues-events/issues/open'},
                {'name': 'Appx_CSR1Kv',
                 'severity': 'moderate',
                 'summary': 'router_interface_input_output_discards',
                 'url': 'https://10.1.100.4/dna/assurance/dashboards/issues-events/issues/open'},
                {'name': 'Appx_CSR1Kv',
                 'severity': 'major',
                 'summary': 'device_time_drift',
                 'url': 'https://10.1.100.4/dna/assurance/dashboards/issues-events/issues/open'},
                {'name': 'DC-Switch.demo.local',
                 'severity': 'major',
                 'summary': 'device_time_drift',
                 'url': 'https://10.1.100.4/dna/assurance/dashboards/issues-events/issues/open'},
                {'name': 'CPS-Edge2',
                 'severity': 'major',
                 'summary': 'device_time_drift',
                 'url': 'https://10.1.100.4/dna/assurance/dashboards/issues-events/issues/open'},
                {'name': 'CPS-Edge1',
                 'severity': 'major',
                 'summary': 'device_time_drift',
                 'url': 'https://10.1.100.4/dna/assurance/dashboards/issues-events/issues/open'},
                {'name': 'CPS-L2Border',
                 'severity': 'major',
                 'summary': 'device_time_drift',
                 'url': 'https://10.1.100.4/dna/assurance/dashboards/issues-events/issues/open'}]

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
