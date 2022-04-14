from datetime import datetime
from flask import render_template
from ajax_data import app
import os
import pyodbc
server = 'vesselstatusdb.database.windows.net' 
database = 'VesselStatusDB' 
username = 'lunghwa' 
password = 'LHE@debug' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()



@app.route('/ajax/<vessel_name>')
def home(vessel_name):
    server = 'vesselstatusdb.database.windows.net' 
    database = 'VesselStatusDB' 
    username = 'lunghwa' 
    password = 'LHE@debug' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute("SELECT active,delta_last_time from dbo.VideoSoft_web_status where ship_name=?",vessel_name)
    videosoft_not_clean_data=cursor.fetchall()
    print(videosoft_not_clean_data)    
    videosoft_split_data=str(videosoft_not_clean_data).split(",")
    active_not_clean=str(videosoft_split_data[0]).split("'")
    active_real=str(active_not_clean[1])
    delta_not_clean=str(videosoft_split_data[1]).split(")")
    delta_real=float(delta_not_clean[0])
    print(f"active={active_real}")
    print(f"delta={delta_real}")
    cursor.execute("SELECT L_delta from dbo.VideoSoft_web_status where ship_name=?",vessel_name)
    L_time=cursor.fetchall()
    for i in L_time:
        L_delta_time=i[0]
    if L_delta_time=="NoData":
        L_delta_time=10000
    else:
        L_delta_time=int(L_delta_time)
    print(f"L_delta_time={L_delta_time}")
    if active_real=="True" or delta_real<=700 or L_delta_time<=700:
        light_path="/static/img/V3-GreenLight.png"
        light_path2="/static/img/V4-CamOpen-6.png"
        #light_path="/static/img/HOME.png"
        #light_path2="/static/img/CAM_ERROR_BUTTON.png"
    else:
        light_path="/static/img/V3-RedLight.png"
        light_path2="/static/img/V4-CamClose-6.png"
        #light_path="/static/img/HOME.png"
        #light_path2="/static/img/CAM_ERROR_BUTTON.png"
    return render_template(
        'vessel_status.html',
        light_path=light_path,
        light_path2=light_path2,
    )


