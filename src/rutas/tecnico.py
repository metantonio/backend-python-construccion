import os
from ..main import request, jsonify, app
import requests, json
from time import sleep
import asyncio
import os.path
import pandas as pd
import openpyxl 

URL_BACKEND = os.environ.get('BASE_URL')

@app.route('/tecnico', methods=['POST'])
def fetching():
    data = request.get_json()
    if isinstance(data, dict):        
        return jsonify({"msg":"Estructura correcta de data"}), 200
    else:
        return jsonify({"msg":"error en la data"}), 400

 
