
r = 4
path = "request" + str(r) + ".txt"
path1 = "request5.txt"

f = open(path, "r")
f1 = open(path1, 'a')

request = []
tmp_data = 0
for line in f:
    data = float(line)
    if len(request) < 300:
        data = data/10
        data = int(data)

        if data != int(tmp_data):
            # print(data, tmp_data)
            request.append(data)

        tmp_data = data


f.close()
print(request)
print(len(request))
req_m = []


for i in request:
    for j in range(6):
        req_m.append(i)
        data = str(i) + '\n'
        if len(req_m) < 301:
            f1.write(data)
f1.close()

