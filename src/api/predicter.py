from flask_restful import Resource
from flask import request, jsonify, send_file
from model import predict
import subprocess
import csv
import json
import os

#class with a POST method to handle POST HTTP requests
class Run_Model(Resource):
    def post(self):
        #values to initialize the test_api.csv file that the trained model will run on.
        field_names = ["fecha_dato","ncodpers","ind_empleado","pais_residencia","sexo","age","fecha_alta","ind_nuevo","antiguedad","indrel","ult_fec_cli_1t","indrel_1mes","tiprel_1mes","indresi","indext","conyuemp","canal_entrada","indfall","tipodom","cod_prov","nomprov","ind_actividad_cliente","renta","segmento"]
        
        #initializing the .csv file with input from the parameters passed into the API URL or dummy data for irrelevant parameters.
        rows = [{
                "fecha_dato": "2016-06-28",
                "ncodpers": request.args.get('id'),
                "ind_empleado": "A",
                "pais_residencia": request.args.get('nationality'),
                "sexo": request.args.get('gender'),
                "age": request.args.get('age'),
                "fecha_alta": "2013-08-28",
                "ind_nuevo": "0",
                "antiguedad": request.args.get('seniority'),
                "indrel": "1",
                "ult_fec_cli_1t": "",
                "indrel_1mes": "1",
                "tiprel_1mes": request.args.get('relation_type'),
                "indresi": "S",
                "indext": "N",
                "conyuemp": "",
                "canal_entrada": "KAT",
                "indfall": "N",
                "tipodom": "1",
                "cod_prov": "28",
                "nomprov": request.args.get('region'),
                "ind_actividad_cliente": request.args.get('activity'),
                "renta": request.args.get('income'),
                "segmento": request.args.get('segment')
        }]

        #open test_api.csv (input file) and write the field names and their desired values.
        with open("files\\test_api.csv", 'w', encoding='UTF-8', newline='') as f:
            write = csv.DictWriter(f, fieldnames = field_names)
            write.writeheader()
            write.writerows(rows)

        f.close()

        #running the model.predict() method so the trained model can process the test data.
        predict()

        #open sub_xgb_new.csv (output file) for reading and save the prediction output.
        file = open('sub_xgb_new.csv')
        reader = csv.reader(file)

        headers = []
        headers = next(reader)

        values = []
        values = next(reader)
        
        file.close()

        #mapping the output from variable name to english for more relevant user experience.
        switch = {
                "ind_ahor_fin_ult1":	"Saving Account",
                "ind_aval_fin_ult1":	"Guarantees",
                "ind_cco_fin_ult1":	    "Current Accounts",
                "ind_cder_fin_ult1":	"Derivada Account",
                "ind_cno_fin_ult1":	    "Payroll Account",
                "ind_ctju_fin_ult1":    "Junior Account",
                "ind_ctma_fin_ult1":	"Más particular Account",
                "ind_ctop_fin_ult1":	"particular Account",
                "ind_ctpp_fin_ult1":	"particular Plus Account",
                "ind_deco_fin_ult1":	"Short-term deposits",
                "ind_deme_fin_ult1":	"Medium-term deposits",
                "ind_dela_fin_ult1":	"Long-term deposits",
                "ind_ecue_fin_ult1":	"e-account",
                "ind_fond_fin_ult1":	"Funds",
                "ind_hip_fin_ult1":	    "Mortgage",
                "ind_plan_fin_ult1":	"Pensions",
                "ind_pres_fin_ult1":	"Loans",
                "ind_reca_fin_ult1":	"Taxes",
                "ind_tjcr_fin_ult1":	"Credit Card",
                "ind_valo_fin_ult1":	"Securities",
                "ind_viv_fin_ult1":	    "Home Account",
                "ind_nomina_ult1":	    "Payroll",
                "ind_nom_pens_ult1":	"Pensions",
                "ind_recibo_ult1":	    "Direct Debit"
            }

        splits = values[1].split()
        prods = ""

        for split in splits:
            prods+= (switch.get(split)+", ")

        prods = prods[:-2]

        #processing the desired output to form a readable API response
        result = {
            headers[0]:values[0],
            headers[1]:prods
        }

        #initialize the output JSON file.
        with open("./files/output.json", "w") as f:
            temp = json.dumps(result)
            f.write(temp)
        f.close()
    
        return send_file(os.path.abspath("./files/output.json"))