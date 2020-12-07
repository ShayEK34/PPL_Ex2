import mybackend
from flask import Flask
from flask import jsonify
from flask import request


app= Flask(__name__)

@app.route('/')
def index():
    return "welcome\n you can use this example:\n http://127.0.0.1:5000/startlocation/City Hall/timeduration/23/k/3"

"""
the main application service function-
Produces recommendations for the web application client 
gets from client: startlocation= start location, 
                  timeduration= trip time
                  k= number of recommendations
"""
@app.route('/startlocation/<startlocation>/timeduration/<timeduration>/k/<k>', methods=['GET'])
def startlocation(startlocation, timeduration,k):
    valid_input=valid_values(startlocation, timeduration,k)
    if(valid_input=="valid"):
        db=mybackend.Database()
        ans= db.check_if_station_exist(startlocation)
        if ans==1:
            destinations= db.calculate_res(startlocation,timeduration, k)
            destinations= destinations.split('\n')
            return jsonify(destinations)
        if ans==0:
            str= "message: location does not exist"
            return jsonify(str)
    else:
        return jsonify(valid_input)

"""
check if the param input is consists only of number 
"""
def only_numbers(param):
    return all(char.isdigit() for char in param)

"""
check valid values
check if inputs not empty  and if valid by the rules
"""
def valid_values(startlocation, timeduration,k):
    str="valid"
    if startlocation=='':
        str= 'startlocation can not be empty'
    if only_numbers(startlocation):
        str = 'location can not be only numbers'
    if timeduration == '':
        str ='spend time should not by empty'
    if not only_numbers(timeduration):
        str ='spend time is not valid'
    if k == '':
        str='recommendations should not by empty'
    if not only_numbers(k):
        str='recommendations is not valid'
    return str


if __name__ == '__main__':
    app.run()