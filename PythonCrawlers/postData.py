import requests
import pandas as pd
import ndjson

host = 'https://search-aw-index-qvgyj7lx56ums2xlhsylupjkbu.us-east-1.es.amazonaws.com'
region = 'us-east-1'
service = 'es'

def appendIndex(df):
    INDEX = 'wikibook'
    TYPE = 'wiki_content'
    data_list = []
    for each_row in df.to_dict(orient="records"):
        data_list.append({"index" : {"_index": INDEX, "_type": TYPE}})
        data_list.append(each_row)
    return data_list

df = pd.read_csv('contentFromOracle.csv', encoding='ISO-8859-1')
df_1 = pd.read_csv('content.csv', encoding='ISO-8859-1')
headers = {'Content-Type':'application/json'}
df = pd.concat([df,df_1],axis=0)
json_data = appendIndex(df)
jsonData = ndjson.dumps(json_data)
j = jsonData+ '\n'
response = requests.post(host + '/_bulk', data=j, headers=headers)
print(response.status_code)



