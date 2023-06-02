import Dnac_auth
from pprint import pprint


fiveTuple = [ 
    {"sourceIP":"172.16.1.200",
     "sourcePort":"9999",
     "destIP":"121.10.10.2",
     "destPort":"8888",
     "protocol":"tcp"
     }

    ]


def do_pathtrace():
   for item in fiveTuple:
      data=Dnac_auth.post_data(uri="/dna/intent/api/v1/flow-analysis",body=item)
      pprint(data)

def get_pathtracehistory():
   data = Dnac_auth.get_data(uri="/dna/intent/api/v1/flow-analysis")["response"]
   for item in data:
      if(item["status"]=="COMPLETED"):
        return(item["id"])

def get_pathtracedetails():
   uri = "/dna/intent/api/v1/flow-analysis/" + get_pathtracehistory()
   data = Dnac_auth.get_data(uri=uri)["response"]
   pprint(data)


if __name__ == "__main__":
    pprint(get_pathtracedetails())