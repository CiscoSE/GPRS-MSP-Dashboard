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

from flask import Flask, request, jsonify
import Teamswebhookreceiver

app = Flask(__name__)

@app.route('/', methods=['POST'])
def entry():
    return Teamswebhookreceiver.runme(request=request)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
