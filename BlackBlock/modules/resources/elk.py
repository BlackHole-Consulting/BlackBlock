import elasticsearch
import json

import time
from datetime import datetime
from pytz import timezone

timestamp=""
tz = timezone('UTC')
timestamp=datetime.now(tz)

dateelastic=str(str(timestamp).split(" ")[0])+"T"+str(str(timestamp).split(" ")[1].split("-")[0].split(".")[0])+"Z"

def elkpush(indexdat,jsondat):
    datafinal = json.loads(jsondat)
    datafinal["time"]=dateelastic
    es = elasticsearch.Elasticsearch("https://10.0.102.11:9200",verify_certs=False, http_auth=('writer', 'thepassword'))
    try:
        return (es.index(index=indexdat,doc_type="rhomb_core",body=json.dumps(datafinal)))
    except:
        pass
