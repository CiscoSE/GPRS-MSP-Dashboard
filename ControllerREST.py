from flask import Flask, jsonify, request
import vManageAlarms
import vManageHealth
import DnacHealth
import DnacAppHealth
import vManageNWPI_readTrace
import DnacAlarms

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    """Return data about the devices. A sample return data for this function is provided in demodbdata.py
    parameters: None
    returns: JSON
    """
    data = { 
        "vManageHealth": vManageHealth.get_data(),
        "DnacHealth" : DnacHealth.get_data(),
        "vManageNWPI_readTrace" : vManageNWPI_readTrace.get_data(),
        "DnacAppHealth": DnacAppHealth.get_data(),
        "vManageAlarms": vManageAlarms.get_data(),
        "DnacAlarms": DnacAlarms.get_data()
        }
    
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
