import Dnac_auth
from pprint import pprint

 
def get_data():
    """
    Get application health from DNAC

    params: 
                none

    Returns:
                json: json response from Dnac

    example:
                [{'events': 'health: 5, packetLossPercent: 60, '
                              'networkLatency: 84, Jitter: None',
                    'health': 'critical',
                    'name': 'http',
                    'url': 'https://10.1.100.4/dna/assurance/application/details?id=http&siteId=4f885bef-c58b-4daf-8e1e-f71576b69721'},
                   {'events': 'health: 5, packetLossPercent: 58, '
                              'networkLatency: 3, Jitter: None',
                    'health': 'critical',
                    'name': 'ssl',
                    'url': 'https://10.1.100.4/dna/assurance/application/details?id=ssl&siteId=4f885bef-c58b-4daf-8e1e-f71576b69721'},
                   {'events': 'health: 1, packetLossPercent: 80, '
                              'networkLatency: 599, Jitter: None',
                    'health': 'critical',
                    'name': 'binary-over-http',
                    'url': 'https://10.1.100.4/dna/assurance/application/details?id=binary-over-http&siteId=4f885bef-c58b-4daf-8e1e-f71576b69721'},
                   {'events': 'health: 1, packetLossPercent: 50, '
                              'networkLatency: 2, Jitter: None',
                    'health': 'critical',
                    'name': 'google-play',
                    'url': 'https://10.1.100.4/dna/assurance/application/details?id=google-play&siteId=4f885bef-c58b-4daf-8e1e-f71576b69721'},
                   {'events': 'health: 5, packetLossPercent: 45, '
                              'networkLatency: 2, Jitter: None',
                    'health': 'critical',
                    'name': 'google-services',
                    'url': 'https://10.1.100.4/dna/assurance/application/details?id=google-services&siteId=4f885bef-c58b-4daf-8e1e-f71576b69721'},
                   {'events': 'health: 5, packetLossPercent: 76, '
                              'networkLatency: 5, Jitter: None',
                    'health': 'critical',
                    'name': 'ocsp',
                    'url': 'https://10.1.100.4/dna/assurance/application/details?id=ocsp&siteId=4f885bef-c58b-4daf-8e1e-f71576b69721'}]

    """
    result = []
    siteid=[]
    tmp = Dnac_auth.get_data(uri="/dna/intent/api/v1/site")['response']
    for item in tmp:
        siteid.append(item["id"])
    for item in siteid:
        query = {
            "siteId": item
        }
        tmp = Dnac_auth.get_data(uri="/dna/intent/api/v1/application-health", query=query)['response']
        for item2 in tmp:
            if(item2["health"]!=None):
                if(item2["health"]<8):
                    if(type(item2["networkLatency"])==float):
                        item2["networkLatency"] = round(item2["networkLatency"])
                    if(type(item2["packetLossPercent"])==float):
                        item2["packetLossPercent"] = round(item2["packetLossPercent"])
                    if(type(item2["jitter"])==float):
                        item2["jitter"] = round(item2["jitter"])


                    result.append({"name":item2["name"],"events": "health: " +str(item2["health"])+ ", packetLossPercent: "+str(item2["packetLossPercent"]) + ", networkLatency: "+str(item2["networkLatency"])+ ", Jitter: "+ str(item2["jitter"]) , "url": Dnac_auth.BASE_URL + "/dna/assurance/application/details?id="+item2["name"]+"&siteId="+item, "health":"critical"})
    return result

if __name__ == "__main__":
    pprint(get_data())

