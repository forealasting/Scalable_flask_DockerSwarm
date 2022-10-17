from flask import Flask, request, jsonify, current_app, g
import time
import pymongo
import docker
# client = pymongo.MongoClient("mongodb+srv://ncku_gwhsu:123@cluster0.wtz5pwg.mongodb.net/?retryWrites=true&w=majority")
# db = client['containers']['delay1']  # service1

app = Flask(__name__)


# Before each request
@app.before_request
def before_request():
    g.start_time = time.time()


# After request handler
@app.after_request
def after_request(response):
    t = time.time() - g.start_time
    current_app.logger.debug(f"Time used: {time.time() - g.start_time}")

    path = 'output1.txt'
    f = open(path, 'a')
    data = str(t) + '\n'
    f.write(data)
    f.close()
    # mydict = {num_req: t, 'delete': True}
    # db.insert_one(mydict)
    # print(mydict)
    return response


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        # just calculate
        ans = []
        for i in range(1000):
            tmp = i**(i+1)
            ans.append(tmp)
        data = request.form
        global num_req
        num_req = data['num']
        # print(type(num_req))
        # print('num of requests = ', num_req)


        return 'store data to mongodb'

    else:
        return 'Hello Dcnlab'


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)  # threaded=False


