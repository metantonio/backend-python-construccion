import os
from ..main import request, jsonify, app
import requests, json
from time import sleep
import asyncio
import os.path
import pandas as pd
import openpyxl 

URL_BACKEND = os.environ.get('BASE_URL')
SAVE_RESPALDO = os.environ.get('RESPALDO')

@app.route('/tecnico', methods=['POST'])
def fetching():
    data = request.get_json()
    if isinstance(data, dict):
        try:  
            if(data["metodo"]=="POST"):
                f = requests.post(URL_BACKEND+data["endpoint"], json=data["objeto"])    
                answer = f.json()
                print("existen "+str(len(answer))+" registros en: "+data["endpoint"])    
                items = answer   
                #save_path = './respaldo' #donde la ruta relativa es en relación a la raíz del proyecto   
                save_path = SAVE_RESPALDO
                completeName = os.path.join(save_path, data["archivo"])
                with open(completeName, "w") as text_file:
                    json.dump(items, text_file, indent = 6)

                return jsonify({"msg":f'Archivo {data["archivo"]} generado'}), 200
            elif(data["metodo"]=="GET"):
                f = requests.get(URL_BACKEND+data["endpoint"])
                answer = f.json()
                print("existen "+str(len(answer))+" registros en: "+data["endpoint"])    
                items = answer   
                save_path = './respaldo' #donde la ruta relativa es en relación a la raíz del proyecto
                save_path = SAVE_RESPALDO   
                completeName = os.path.join(save_path, data["archivo"])
                with open(completeName, "w") as text_file:
                    json.dump(items, text_file, indent = 6)

                return jsonify({"msg":f'Archivo {data["archivo"]} generado'}), 200
            else:
                return jsonify({"msg":"Método no válido"}), 401

        except Exception as err:
            print(err)
            return jsonify({"message":"internal error por data inválida o incompleta, vuelva a intentar por si los estados no se cargaron correctamente"}), 500
    else:
        return jsonify({"msg":"error en la data"}), 400

@app.route('/tecnicoExcel2Json', methods=['POST'])
def excel2json():
    lista_de_archivos = os.listdir(SAVE_RESPALDO)
    if len(lista_de_archivos) > 0:
        print("vamos a iniciar son " + str(len(lista_de_archivos)) + " Archivos")
        for x in lista_de_archivos:        
            if(x != ".DS_Store" and x!="excel2json.py" and x[-3:]=="xls"):
                print(x[:-3])
                print(x[-3:])
                df_excel = pd.read_excel("./"+x,sheet_name="Hoja1")            
                df_excel_columnas = df_excel.columns
                print("Excel Heads: \n", df_excel_columnas)
                df_excel.to_json(path_or_buf= x[:-4]+'.json',orient='records')
        return jsonify({"msg":f'Archivos JSON generados'}), 200
    else:
        return jsonify({"msg":"error en generar archivos .json"}), 400

@app.route('/tecnicoJson2Excel', methods=['POST'])
def json2excel():
    lista_de_archivos = os.listdir(SAVE_RESPALDO)
    #print(lista_de_archivos)
    if len(lista_de_archivos) > 0:
        print("vamos a iniciar con " + str(len(lista_de_archivos)) + " Archivos")
        ind=0
        for x in lista_de_archivos:                               
            if(x != ".DS_Store" and x!="excel2json.py" and x!="Tablas.json" and x[-4:]=='json'):
                #print(x[:-4])
                #print(x[-4:])
                print(x)
                print(ind)
                print(x[:-4]+'json')
                with open(x[:-4]+'json') as json_file:
                    data = json.load(json_file)
                    df = pd.DataFrame(data)
                    #df.to_excel("./"+x[:-4]+"xlsx") #funciona pero no tengo controlo sobre nombre hoja o reescritura
                    with pd.ExcelWriter(x[:-4]+"xlsx", mode='w') as writer:
                        df.to_excel(writer, sheet_name="Hoja1")
            ind=ind+1
        return jsonify({"msg":f'Archivos EXCEL generados'}), 200

    else:
        return jsonify({"msg":"error en generar archivos .xls"}), 400