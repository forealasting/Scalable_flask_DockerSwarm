import pymongo
import pandas as pd
client = pymongo.MongoClient("mongodb+srv://ncku_gwhsu:123@cluster0.wtz5pwg.mongodb.net/?retryWrites=true&w=majority")
db = client['containers']['delay1']

collection  = list(db.find())
data = pd.DataFrame(collection)

# print(data)
all_time = sum(data['123'])

avg = sum(data['123'])/len(data['123'])
print(len(data['123']))
max_d = max(data['123'])
min_d = min(data['123'])
print(all_time)
print(avg*1000)
print(max_d*1000, min_d*1000)

# cursor = db.find({})
# for document in cursor:
#      print(document)
