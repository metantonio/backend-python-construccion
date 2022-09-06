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
        if(data["metodo"]=="POST"):
            f = requests.post(URL_BACKEND+data["endpoint"], json=data["objeto"])
    
            answer = f.json()
            print("existen "+str(len(answer))+" registros en: "+data["endpoint"])
    
            items = answer

   
            save_path = './respaldo' #donde la ruta relativa es en relación a la raíz del proyecto   
            completeName = os.path.join(save_path, data["archivo"]) 
  

            with open(completeName, "w") as text_file:
                json.dump(items, text_file, indent = 6)

            return jsonify({"msg":f'Archivo {data["archivo"]} generado'}), 200
    else:
        return jsonify({"msg":"error en la data"}), 400

 
