import pymongo
import pandas as pd
client = pymongo.MongoClient("mongodb+srv://ncku_gwhsu:123@cluster0.wtz5pwg.mongodb.net/?retryWrites=true&w=majority")
db_cpu = client['state']['cpu_u1']

collection = list(db_cpu.find())
data = pd.DataFrame(collection)

all_time = sum(data['cpu_u'])
avg = sum(data['cpu_u'])/len(data['cpu_u'])
max_d = max(data['cpu_u'])
min_d = min(data['cpu_u'])
print(data['cpu_u'])
print(len(data['cpu_u']))

# cursor = db.find({})
# for document in cursor:
#      print(document)
real_data = []
for cpu_u in data['cpu_u']:
    if cpu_u > 1:
        real_data.append(cpu_u)

avg = sum(real_data)/len(real_data)
max_d = max(real_data)
min_d = min(real_data)

print(avg)
print(max_d, min_d)
