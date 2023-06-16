"""
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

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
    """Return data about the devices.
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
