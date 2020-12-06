import mybackend
from flask import Flask
from flask import jsonify
from flask import request


app= Flask(__name__)

@app.route('/')
def index():
    return "ho"

@app.route('/startlocation/<startlocation>/timeduration/<timeduration>/k/<k>', methods=['GET'])
def startlocation(startlocation, timeduration,k):
    db=mybackend.Database()
    ans= db.check_if_station_exist(startlocation)
    if ans==1:
        destinations= db.calculate_res(startlocation,timeduration, k)
        destinations= destinations.split('\n')
        return jsonify(destinations)
    if ans==0:
        return jsonify({"message: location does not exist"})


if __name__ == '__main__':
    app.run()