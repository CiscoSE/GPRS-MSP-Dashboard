import Dnac_auth
from pprint import pprint

 
def get_data():
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

