from flask import Flask, render_template, request
from dashboard_forms import Dashform
#import create_pickle as p_j
import json
import os

app = Flask(__name__)
app.secret_key = 'dash_flask_key'
creddir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'credentials/dash_id.json')
# creddir_2 = os.path.join(os.path.dirname(
#    os.path.dirname(os.path.realpath(__file__))), 'credentials')
tempdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'www/templates/dash_id_template.json')


def Convert(string):
    li = list(string.split(","))
    k = []
    for i in li:
        str(i).replace(' ', '')
        k.append(i)
    return k


def formatting(string):
    string = string.replace("[", "")
    string = string.replace("]", "")
    string = string.replace("'", "")
    string = string.replace(" ", "")
    return string


def json_exists(file_name):
    return os.path.exists(file_name)


def getinfo():
    data = []
    if json_exists(creddir):
        with open(creddir, "r") as rdash_id:
            data = json.load(rdash_id)
        return data
    else:
        with open(tempdir, "r") as f1, open(creddir, "w+") as f2:
            f2.write(f1.read())
            f2.close
        with open(creddir, "r") as rdash_id:
            data = json.load(rdash_id)
        return data


def save_json(res):
    with open(creddir, 'r') as f:
        data = json.load(f)
        data["Transit"]["T_URL"] = res["T_URL"]
        data["Transit"]["T_API_KEY"] = res["T_API_KEY"]
        data["Transit"]["Stops"] = Convert(res["Stops"])
        data["Transit"]["T_BUS"] = res["T_BUS"]
        data["Transit"]["T_BUS_TIME"] = res["T_BUS_TIME"]

        data["Weather"]["W_URL"] = res["W_URL"]
        data["Weather"]["UNITS"] = res["UNITS"]
        data["Weather"]["W_API_KEY"] = res["W_API_KEY"]

        data["Geolocation"]["G_URL"] = res["G_URL"]
        data["Geolocation"]["G_API_KEY"] = res["G_API_KEY"]

        data["Currency"]["C_URL_1"] = res["C_URL_1"]
        data["Currency"]["C_API_KEY_1"] = res["C_API_KEY_1"]
        data["Currency"]["C_URL_3"] = res["C_URL_3"]
        data["Currency"]["C_URL_4"] = res["C_URL_4"]
        data["Currency"]["CURR_CHECK"] = Convert(res["CURR_CHECK"])

        data["Stocks"]["STOCK_W_URL"] = res["STOCK_W_URL"]
        data["Stocks"]["STOCK_WE_URL"] = res["STOCK_WE_URL"]
        data["Stocks"]["STOCK_API"] = res["STOCK_API"]
        data["Stocks"]["STOCK_CHECK"] = Convert(res["STOCK_CHECK"])

        data["Tasklist"]["gsheet_json"] = res["gsheet_json"]
        data["Tasklist"]["sheetname"] = res["sheetname"]

        data["G_Meetings"]["CREDENTIALS_FILE"] = res["CREDENTIALS_FILE"]

        data["News"]["NEWS_URL"] = res["NEWS_URL"]
        data["News"]["NEWS_API"] = res["NEWS_API"]
        data["News"]["NEWS_SOURCES"] = str(res["NEWS_SOURCES"]).replace(' ', '')

        data["System"]["waking_time"] = res["waking_time"]
        data["System"]["sleeping_time"] = res["sleeping_time"]
        data["System"]["mod_1_choice"] = res["mod_1_choice"]
        data["System"]["mod_2_choice"] = res["mod_2_choice"]
        data["System"]["mod_3_choice"] = res["mod_3_choice"]
        data["System"]["mod_4_choice"] = res["mod_4_choice"]
        data["System"]["refresh_time"] = res["refresh_time"]
        data["System"]["awake"] = res["awake"]

    os.remove(creddir)
    with open(creddir, 'w+') as f:
        json.dump(data, f, indent=4)


@ app.route('/', methods=['POST', 'GET'])
def login():
    form = Dashform()
    d_data = getinfo()
    form.res_msg.label = ""

    if request.method == 'POST':
        form.res_msg.label = ""

        if request.form['btn'] == 'Submit':
            results = request.form
            save_json(results)
            form.res_msg.label = "Information saved successfully"
        '''elif request.form['btn'] == 'Generate Pickle File':
            results = request.form
            p_j.get_calendar_service(results["CREDENTIALS_FILE"], creddir_2)
'''
        d_data = getinfo()
        form.T_URL.data = str(d_data["Transit"]["T_URL"])
        form.T_API_KEY.data = str(d_data["Transit"]["T_API_KEY"])
        form.Stops.data = formatting(str(d_data["Transit"]["Stops"]))
        form.T_BUS.data = str(d_data["Transit"]["T_BUS"])
        form.T_BUS_TIME.data = str(d_data["Transit"]["T_BUS_TIME"])
        form.W_URL.data = str(d_data["Weather"]["W_URL"])
        form.W_API_KEY.data = str(d_data["Weather"]["W_API_KEY"])
        form.UNITS.data = str(d_data["Weather"]["UNITS"])
        form.C_URL_1.data = str(d_data["Currency"]["C_URL_1"])
        form.C_API_KEY_1.data = str(d_data["Currency"]["C_API_KEY_1"])
        form.C_URL_3.data = str(d_data["Currency"]["C_URL_3"])
        form.C_URL_4.data = str(d_data["Currency"]["C_URL_4"])
        form.CURR_CHECK.data = formatting(str(d_data["Currency"]["CURR_CHECK"]))
        form.STOCK_W_URL.data = str(d_data["Stocks"]["STOCK_W_URL"])
        form.STOCK_WE_URL.data = str(d_data["Stocks"]["STOCK_WE_URL"])
        form.STOCK_API.data = str(d_data["Stocks"]["STOCK_API"])
        form.STOCK_CHECK.data = formatting(str(d_data["Stocks"]["STOCK_CHECK"]))
        form.G_URL.data = str(d_data["Geolocation"]["G_URL"])
        form.G_API_KEY.data = str(d_data["Geolocation"]["G_API_KEY"])
        form.gsheet_json.data = str(d_data["Tasklist"]["gsheet_json"])
        form.sheetname.data = str(d_data["Tasklist"]["sheetname"])
        form.CREDENTIALS_FILE.data = str(d_data["G_Meetings"]["CREDENTIALS_FILE"])
        form.NEWS_URL.data = str(d_data["News"]["NEWS_URL"])
        form.NEWS_API.data = str(d_data["News"]["NEWS_API"])
        form.NEWS_SOURCES.data = formatting(str(d_data["News"]["NEWS_SOURCES"]))
        form.waking_time.data = str(d_data["System"]["waking_time"])
        form.sleeping_time.data = str(d_data["System"]["sleeping_time"])
        form.mod_1_choice.data = str(d_data["System"]["mod_1_choice"])
        form.mod_2_choice.data = str(d_data["System"]["mod_2_choice"])
        form.mod_3_choice.data = str(d_data["System"]["mod_3_choice"])
        form.mod_4_choice.data = str(d_data["System"]["mod_4_choice"])
        form.refresh_time.data = str(d_data["System"]["refresh_time"])
        form.awake.data = str(d_data["System"]["awake"])

        return render_template('Settings.html', form=form)

    elif request.method == 'GET':
        # populate the form on start
        d_data = getinfo()
        form.res_msg.label = ""
        form.T_URL.data = str(d_data["Transit"]["T_URL"])
        form.T_API_KEY.data = str(d_data["Transit"]["T_API_KEY"])
        form.Stops.data = formatting(str(d_data["Transit"]["Stops"]))
        form.T_BUS.data = str(d_data["Transit"]["T_BUS"])
        form.T_BUS_TIME.data = str(d_data["Transit"]["T_BUS_TIME"])
        form.W_URL.data = str(d_data["Weather"]["W_URL"])
        form.W_API_KEY.data = str(d_data["Weather"]["W_API_KEY"])
        form.UNITS.data = str(d_data["Weather"]["UNITS"])
        form.C_URL_1.data = str(d_data["Currency"]["C_URL_1"])
        form.C_API_KEY_1.data = str(d_data["Currency"]["C_API_KEY_1"])
        form.C_URL_3.data = str(d_data["Currency"]["C_URL_3"])
        form.C_URL_4.data = str(d_data["Currency"]["C_URL_4"])
        form.CURR_CHECK.data = formatting(str(d_data["Currency"]["CURR_CHECK"]))
        form.STOCK_W_URL.data = str(d_data["Stocks"]["STOCK_W_URL"])
        form.STOCK_WE_URL.data = str(d_data["Stocks"]["STOCK_WE_URL"])
        form.STOCK_API.data = str(d_data["Stocks"]["STOCK_API"])
        form.STOCK_CHECK.data = formatting(str(d_data["Stocks"]["STOCK_CHECK"]))
        form.G_URL.data = str(d_data["Geolocation"]["G_URL"])
        form.G_API_KEY.data = str(d_data["Geolocation"]["G_API_KEY"])
        form.gsheet_json.data = str(d_data["Tasklist"]["gsheet_json"])
        form.sheetname.data = str(d_data["Tasklist"]["sheetname"])
        form.CREDENTIALS_FILE.data = str(d_data["G_Meetings"]["CREDENTIALS_FILE"])
        form.NEWS_URL.data = str(d_data["News"]["NEWS_URL"])
        form.NEWS_API.data = str(d_data["News"]["NEWS_API"])
        form.NEWS_SOURCES.data = formatting(str(d_data["News"]["NEWS_SOURCES"]))
        form.waking_time.data = str(d_data["System"]["waking_time"])
        form.sleeping_time.data = str(d_data["System"]["sleeping_time"])
        form.mod_1_choice.data = str(d_data["System"]["mod_1_choice"])
        form.mod_2_choice.data = str(d_data["System"]["mod_2_choice"])
        form.mod_3_choice.data = str(d_data["System"]["mod_3_choice"])
        form.mod_4_choice.data = str(d_data["System"]["mod_4_choice"])
        form.refresh_time.data = str(d_data["System"]["refresh_time"])
        form.awake.data = str(d_data["System"]["awake"])
        return render_template('Settings.html', form=form)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@ app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()

    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
