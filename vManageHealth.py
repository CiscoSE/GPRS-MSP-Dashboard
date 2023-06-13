import vManage_auth
from pprint import pprint


def get_data():
    returnData = {}
    deviceData = []
    seen = []
    data = vManage_auth.get_data("/dataservice/device/bfd/sites/detail?state=siteup")["data"]
    for item in data:
        returnData['networkHealth'] = 1
        tmp={}
        tmp["name"] = item["host-name"]
        seen.append(item["host-name"])
        tmp["deviceFamily"] = item["device-type"].lower()
        tmp["reachabilityHealth"] = item["reachability"].lower()
        tmp["ipAddress"] = item["system-ip"]
        tmp["uuid"] = item["uuid"]
        tmp["deviceHealth"] = "positive"
        tmp['url'] = "https://"+vManage_auth.vmanage_ip+"/?_open=ext#/app/monitor/devices/dashboard/health?systemIp="+item["system-ip"]+"&"+ "localSystemIp="+item["local-system-ip"]+"&"+"device-model="+item["device-type"]+"&"+"uuid="+item["uuid"]
        deviceData.append(tmp.copy())
    data = vManage_auth.get_data("/dataservice/device/bfd/sites/detail?state=sitepartial")["data"]
    for item in data:
        returnData['networkHealth'] = -1
        tmp={}
        tmp["name"] = item["host-name"]
        seen.append(item["host-name"])
        tmp["deviceFamily"] = item["device-type"].lower()
        tmp["reachabilityHealth"] = item["reachability"].lower()
        tmp["ipAddress"] = item["system-ip"]
        tmp["uuid"] = item["uuid"]
        tmp["deviceHealth"] = "moderate"
        tmp['url'] = "https://"+vManage_auth.vmanage_ip+"/?_open=ext#/app/monitor/devices/dashboard/health?systemIp="+item["system-ip"]+"&"+ "localSystemIp="+item["local-system-ip"]+"&"+"device-model="+item["device-type"]+"&"+"uuid="+item["uuid"]
        deviceData.append(tmp.copy())
    data = vManage_auth.get_data("/dataservice/device/bfd/sites/detail?state=sitedown")["data"]
    for item in data:
        returnData['networkHealth'] = 0
        tmp={}
        tmp["name"] = item["host-name"]
        seen.append(item["host-name"])
        tmp["deviceFamily"] = item["device-type"].lower()
        tmp["reachabilityHealth"] = item["reachability"].lower()
        tmp["ipAddress"] = item["system-ip"]
        tmp["uuid"] = item["uuid"]
        tmp["deviceHealth"] = "critical"
        tmp['url'] = "https://"+vManage_auth.vmanage_ip+"/?_open=ext#/app/monitor/devices/dashboard/health?systemIp="+item["system-ip"]+"&"+ "localSystemIp="+item["local-system-ip"]+"&"+"device-model="+item["device-type"]+"&"+"uuid="+item["uuid"]
        deviceData.append(tmp.copy())
    data = vManage_auth.get_data("/dataservice/health/devices")["devices"]
    for item in data:
        if(item["name"] not in seen):
            tmp={}
            tmp["name"] = item["name"]
            seen.append(item["name"])
            tmp["deviceFamily"] = item["device_type"].lower()
            tmp["reachabilityHealth"] = item["reachability"].lower()
            tmp["ipAddress"] = item["system_ip"]
            tmp["uuid"] = item["uuid"]
            if(item["health"] == "green"):
                tmp["deviceHealth"] = "positive"
            elif(item["health"] == "yellow"):
                tmp["deviceHealth"] = "moderate"
            elif(item["health"] == "red"):
                tmp["deviceHealth"] = "critical"
            tmp['url'] = "https://"+vManage_auth.vmanage_ip+"/?_open=ext#/app/monitor/devices/dashboard/health?systemIp="+item["system_ip"]+"&"+ "localSystemIp="+item["local_system_ip"]+"&"+"device-model="+item["device_type"]+"&"+"uuid="+item["uuid"]
            deviceData.append(tmp.copy())
    return [returnData, deviceData]



if __name__ == "__main__":
    pprint(get_data())