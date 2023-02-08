from flask import Blueprint, jsonify, request
from tarifs import Tarif
from data_csv import DataCsv

data_csv_api = Blueprint('data_csv',__name__)

@data_csv_api.route('/newDay', methods=['POST'])
def newDay():
    try:
        data = request.form.to_dict()
        data_csv = DataCsv()
        data_csv.checkDateExist(data['dateRegister'])

        tarif = Tarif(data['dateRegister'], data['hourIn'], data['hourOut'])
        nb_hours = tarif.hourCount()
        daily_indemnity = tarif.dailyIndemnity(nb_hours)

        # TODO voir algo
        #hours_cost = tarif.dailyCostHour(nb_hours)

        data_csv.post_data(data, nb_hours, daily_indemnity)
        
        return jsonify({'message' : "ok new day", "status":200})
    except Exception as e:
        return jsonify({'message' : str(e), "status":404})


@data_csv_api.route('/detailsMonth/<year_month>', methods=['GET'])
def detailsMonth(year_month):
    try:
        data_csv = DataCsv()

        df = data_csv.getDetails(year_month)
        total_hours_month = data_csv.get_hours_month(df)
        total_cost_month = data_csv.get_total_cost_month(df)
        df_html = df.to_html(classes='table text-center')
        return jsonify({'message' : "ok details month",
                        "tab_data" : df_html, 
                        "totalHours": total_hours_month, 
                        "totalCostMonth": total_cost_month,
                        "status":200})
    except Exception as e:
        return jsonify({'message' : str(e), "status":404})


@data_csv_api.route('/updateLine', methods=['POST'])
def updateLine():
    try:
        data = request.get_json()

        tarif = Tarif(data['dateRegister'], data['hourIn'], data['hourOut'])
        nb_hours = tarif.hourCount()
        daily_indemnity = tarif.dailyIndemnity(nb_hours)

        DataCsv().updateData(data, nb_hours, daily_indemnity)
        return jsonify({'message' : "ok update line","status":200})
    except Exception as e:
        return jsonify({'message' : str(e), "status":404})


@data_csv_api.route('/deleteLine', methods=['POST'])
def deleteLine():
    try:
        data = request.get_json()
        DataCsv().deleteData(data)
        return jsonify({'message' : "ok update line","status":200})
    except Exception as e:
        return jsonify({'message' : str(e), "status":404})

