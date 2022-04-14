"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template
from flask_test import app
from flask import Flask
from flask import url_for
from flask import request,redirect
from flask import make_response
import pyodbc
import os
from folium import IFrame
import time
import pandas as pd
#import ee
import folium
from IPython.display import Image
from folium import plugins
from IPython.display import display
import webbrowser  
from IPython.display import Image
#from satelite_data import JC85,JC110,NP,NP2,NP3,SWP,SBC2,SEP,SEP2,T11N,T12PA,T12SA
import configparser
import matplotlib.pyplot as plt
import matplotlib.dates as md
from scipy import stats
import numpy
import pandas as pd
from sklearn import linear_model
from pylab import figure, show
import requests
import urllib.request as req
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import pymysql
from datetime import timedelta

plt.switch_backend('agg')
#from ipyleaflet import Map, basemaps
video_url="http://surveillance.lhsatellite.com:8080/status"

server = 'vesselstatusdb.database.windows.net' 
database = 'VesselStatusDB' 
username = 'lunghwa' 
password = 'LHE@debug' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


@app.route('/home',methods=["GET","POST"])
def home():
    if request.method=="POST":
        return render_template(
            'Path.html',
            title='Path',
            year=datetime.now().year,
            Ship_name=a
        )
        """Renders the home page."""
        return render_template(
            'index.html',
            title='Home Page',
            year=datetime.now().year,
        )
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        )
 

basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
    ),
    'Google Satellite': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Google Terrain': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Terrain',
        overlay = True,
        control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    )
}



##print(data_path)
# Define a method for displaying Earth Engine image tiles on a folium map.
def add_ee_layer(self, ee_object, vis_params, name):
    
    try:    
        # display ee.Image()
        if isinstance(ee_object, ee.image.Image):    
            map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)
        # display ee.ImageCollection()
        elif isinstance(ee_object, ee.imagecollection.ImageCollection):    
            ee_object_new = ee_object.mosaic()
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)
        
        elif isinstance(ee_object, ee.geometry.Geometry):    
            folium.GeoJson(
            data = ee_object.getInfo(),
            name = name,
            overlay = True,
            control = True
        ).add_to(self)
        
        elif isinstance(ee_object, ee.featurecollection.FeatureCollection):  
            ee_object_new = ee.Image().paint(ee_object, 0, 2)
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
        ).add_to(self)
    
    except:
        print("Could not display {}".format(name))
    
exit_program = 0
config = configparser.ConfigParser()
config.read('mypy.ini')
##print(config['mypy']['ip'])
#host = config['http']['host']
data_path=config['mypy']['path']
data_path=str(data_path)

iframe_path_txt=open("iframe_path.txt","r")
read_iframe_path=iframe_path_txt.readline().strip()
iframe_path_txt.close()




def online_ratio(ship_name,start_date,end_date):
    server = 'vesselstatusdb.database.windows.net' 
    database = 'VesselStatusDB' 
    username = 'lunghwa' 
    password = 'LHE@debug' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM dbo.Ku_All_result_history WHERE Ship_name=? AND time BETWEEN ? AND ? ORDER BY time DESC",ship_name,start_date,end_date)

    online_data=cursor.fetchall()
    num_online_data=len(online_data)
    d1=datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
    d2=datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
    delta=d2-d1
    sec=delta.total_seconds()
    hour=sec/3600
    ##print(hour)
    total_online=hour*6
    ##print(total_online)
    ratio=num_online_data/total_online
    perc=str(round(ratio*100,2))+"%"
    ##print(f"num_online_data = {num_online_data}")
    ##print(f"total_online = {total_online}")
    return perc





def output_map(ship_name,points,points2,head,vilocity,last_time,lat,lon,video,final_position,path2_or_path3,language):
    global data_path
    global new_path
    language=language
    #if video=="True":
    #    angle_con="flask_test/templates/img/"+str(int(head))+".png"
    #else:
    #    angle_con="flask_test/templates/img2/"+str(int(head))+".png"
    angle_con="flask_test/templates/img3/"+str(int(head))+".png"
    #angle_con="flask_test/templates/img/"+str(int(head))+".png"
    myIcon = folium.CustomIcon(angle_con,icon_size = (60, 60),icon_anchor = (15, 30)) 
    #points=[[42.736389, 157.381389], [42.741667, 157.379722], [42.768611, 157.388333], [42.8275, 157.408056], [42.8725, 157.405556], [42.911667, 157.398889], [42.91, 157.396944], [42.909167, 157.395833], [42.907778, 157.393611], [42.905278, 157.391111], [42.904722, 157.389722], [42.902778, 157.3875], [42.900556, 157.385278], [42.899167, 157.383611], [42.896944, 157.381111], [42.895833, 157.379722], [42.893333, 157.376389], [42.891667, 157.374167], [42.889167, 157.371111], [42.885833, 157.367778], [42.883611, 157.365556], [42.880833, 157.362222], [42.878333, 157.359167], [42.876944, 157.3575], [42.873056, 157.353333], [42.870556, 157.350833], [42.866944, 157.348611], [42.864444, 157.346667], [42.860556, 157.343889], [42.858056, 157.342222], [42.853889, 157.338889], [42.851389, 157.336944], [42.847222, 157.335556], [42.844167, 157.334444], [42.841667, 157.333333], [42.838056, 157.332222], [42.835833, 157.331944], [42.832778, 157.331667], [42.830556, 157.331111], [42.828333, 157.331111], [42.826111, 157.328611], [42.825, 157.356111], [42.826389, 157.356944], [42.828333, 157.356667], [42.83, 157.358889], [42.831944, 157.357778], [42.835833, 157.360556], [42.837222, 157.362222], [42.91, 157.3025], [42.973889, 157.246667]]
     
    if len(points)>=2:
        folium.Map.add_ee_layer = add_ee_layer
        #points = [[23, 121],[23.3, 121.5],[23.5, 121.796666]]
        
        vis_params = {
          'min': 0,
          'max': 4000,
          'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
          }
        
        my_map = folium.Map(location=final_position, tiles=None,width='100%', height='100%',zoom_start=6,world_copy_jump=True)

        # Add custom basemaps
        basemaps['Google Satellite Hybrid'].add_to(my_map)
        basemaps['Google Maps'].add_to(my_map)
        ##print(last_time)
        time_spl2=str(last_time).split(",")
        year2=time_spl2[0]
        mon2=time_spl2[1]
        day2=time_spl2[2]
        hour2=time_spl2[3]
        min2=time_spl2[4]
        final_updateTime2=str(year2)+"-"+str(mon2)+"-"+str(day2)+" "+str(hour2)+":"+str(min2)

        # Add the elevation model to the map object.
        #my_map.add_ee_layer(dem.updateMask(dem.gt(0)), vis_params, 'DEM')

        # Add a layer control panel to the map.
        my_map.add_child(folium.LayerControl())
        if language=="TW":
            name_and_angle="<hr style='width: 100%; height: 10px; border: none; background-color: #004B97'><font size=\"6\">"+"船名: "+ship_name+"</font><br>"+"<hr //>"+"<font size=\"4\">"+"航向角: "+str(head)+"<br>"+"座標: ("+str(lat)+","+str(lon)+")"+"<br>"+"速度: "+str(vilocity)+"<br>"+"</font><hr //>"+"<font size=\"5\">"+"最後更新時間: "+str(final_updateTime2)+"</font><br><br>"
        else:
            name_and_angle="<hr style='width: 100%; height: 10px; border: none; background-color: #004B97'><font size=\"6\">"+"Ship: "+ship_name+"</font><br>"+"<hr //>"+"<font size=\"4\">"+"Head angle: "+str(head)+"<br>"+"Position: ("+str(lat)+","+str(lon)+")"+"<br>"+"Velocity: "+str(vilocity)+"<br>"+"</font><hr //>"+"<font size=\"5\">"+"Last_Update: "+str(final_updateTime2)+"</font><br><br>"
        # Add custom basemaps
        #name_and_angle="<table><tr><td>Vessel</td><td>Head angle</td><td>GPS</td><td>Vilocity</td><td>Last Update</td></tr>"+"<tr><td>"+ship_name+"</td>"+"<td>"+str(head)+"</td>"+"<td>"+str(vilocity)+"</td>"+"<td>"+str(last_time)+"</td></tr></table>"


        iframe_geffory="""
        <!DOCTYPE html>
        <html>
        <head>
        """
        
        iframe_geffory2="""
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link type="text/css" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
        <script src="http://192.168.0.201:8080/Ship_map_dashboard/Ship_map_dashboard/jquery.min.js"></script>
        </head>
        <body>
        
        </body>
        </html>
        """
        iframe_geffory3=iframe_geffory+name_and_angle+iframe_geffory2
        iframe_geffory3=folium.Html(iframe_geffory3,script=True)
        iframe = IFrame(html=iframe_geffory3, width=400, height=220)
        popup = folium.Popup(iframe, max_width=400)
        # Add the elevation model to the map object.
        #my_map.add_ee_layer(dem.updateMask(dem.gt(0)), vis_params, 'DEM')

        # Add a layer control panel to the map.
        #my_map.add_child(folium.Polygon(locations=[i], weight=10,color="white",popup=name_and_angle)) #i_v2=direction
        
        folium.Marker(location=final_position,popup=popup,icon = myIcon).add_to(my_map)
        plugins.Fullscreen().add_to(my_map)
        #my_map.add_child(folium.PolyLine(locations=JC85, weight=3,color="white",)) 
        #my_map.add_child(folium.PolyLine(locations=JC110, weight=3,color="white",)) 
        #my_map.add_child(folium.PolyLine(locations=NP, weight=3,color="white",)) 
        #my_map.add_child(folium.PolyLine(locations=NP2, weight=3,color="white",)) 
        #my_map.add_child(folium.PolyLine(locations=NP3, weight=3,color="white",)) 
        #my_map.add_child(folium.PolyLine(locations=SWP, weight=3,color="white",))
        #my_map.add_child(folium.PolyLine(locations=SBC2, weight=3,color="white",))
        #my_map.add_child(folium.PolyLine(locations=SEP, weight=3,color="white",))
        #my_map.add_child(folium.PolyLine(locations=SEP2, weight=3,color="white",))
        #my_map.add_child(folium.PolyLine(locations=T11N, weight=3,color="white",))
        #my_map.add_child(folium.PolyLine(locations=T12PA, weight=3,color="white",))
        #my_map.add_child(folium.PolyLine(locations=T12SA, weight=3,color="white",))
        for i in points:
            #for x in i:
            my_map.add_child(folium.PolyLine(locations=i, weight=3,color="green")) 
        for i2 in points2:
            #for x2 in i2:
            my_map.add_child(folium.PolyLine(locations=i2, weight=3,color="red")) 
        #file_name0=str(ship_name)+".html"
        file_name0="Ship_path.html"
        if path2_or_path3=="path2":
            new_path=read_iframe_path+"\\"+file_name0
            print(new_path)
            my_map.save(new_path)
        



    
        #webbrowser.get('windows-default').open_new(file_name0)

def output_map_single(ship_name,head,vilocity,last_time,lat,lon,final_position,language):
    global data_path
    global new_path
    language=language
    #if video=="True":
    #    angle_con="flask_test/templates/img/"+str(int(head))+".png"
    #else:
    #    angle_con="flask_test/templates/img2/"+str(int(head))+".png"
    angle_con="flask_test/templates/img3/"+str(int(head))+".png"
    #angle_con="flask_test/templates/img/"+str(int(head))+".png"
    myIcon = folium.CustomIcon(angle_con,icon_size = (60, 60),icon_anchor = (15, 30)) 
    #points=[[42.736389, 157.381389], [42.741667, 157.379722], [42.768611, 157.388333], [42.8275, 157.408056], [42.8725, 157.405556], [42.911667, 157.398889], [42.91, 157.396944], [42.909167, 157.395833], [42.907778, 157.393611], [42.905278, 157.391111], [42.904722, 157.389722], [42.902778, 157.3875], [42.900556, 157.385278], [42.899167, 157.383611], [42.896944, 157.381111], [42.895833, 157.379722], [42.893333, 157.376389], [42.891667, 157.374167], [42.889167, 157.371111], [42.885833, 157.367778], [42.883611, 157.365556], [42.880833, 157.362222], [42.878333, 157.359167], [42.876944, 157.3575], [42.873056, 157.353333], [42.870556, 157.350833], [42.866944, 157.348611], [42.864444, 157.346667], [42.860556, 157.343889], [42.858056, 157.342222], [42.853889, 157.338889], [42.851389, 157.336944], [42.847222, 157.335556], [42.844167, 157.334444], [42.841667, 157.333333], [42.838056, 157.332222], [42.835833, 157.331944], [42.832778, 157.331667], [42.830556, 157.331111], [42.828333, 157.331111], [42.826111, 157.328611], [42.825, 157.356111], [42.826389, 157.356944], [42.828333, 157.356667], [42.83, 157.358889], [42.831944, 157.357778], [42.835833, 157.360556], [42.837222, 157.362222], [42.91, 157.3025], [42.973889, 157.246667]]
     
    
    folium.Map.add_ee_layer = add_ee_layer
    #points = [[23, 121],[23.3, 121.5],[23.5, 121.796666]]
        
    vis_params = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
        }
        
    my_map = folium.Map(location=final_position, tiles=None,width='100%', height='100%',zoom_start=6,world_copy_jump=True)

    # Add custom basemaps
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    basemaps['Google Maps'].add_to(my_map)
    ##print(last_time)
    
    final_updateTime2=last_time

    # Add the elevation model to the map object.
    #my_map.add_ee_layer(dem.updateMask(dem.gt(0)), vis_params, 'DEM')

    # Add a layer control panel to the map.
    my_map.add_child(folium.LayerControl())
    if language=="TW":
        name_and_angle="<hr style='width: 100%; height: 10px; border: none; background-color: #004B97'><font size=\"6\">"+"船名: "+ship_name+"</font><br>"+"<hr //>"+"<font size=\"4\">"+"航向角: "+str(head)+"<br>"+"座標: ("+str(lat)+","+str(lon)+")"+"<br>"+"速度: "+str(vilocity)+"<br>"+"</font><hr //>"+"<font size=\"5\">"+"最後更新時間: "+str(final_updateTime2)+"</font><br><br>"
    else:
        name_and_angle="<hr style='width: 100%; height: 10px; border: none; background-color: #004B97'><font size=\"6\">"+"Ship: "+ship_name+"</font><br>"+"<hr //>"+"<font size=\"4\">"+"Head angle: "+str(head)+"<br>"+"Position: ("+str(lat)+","+str(lon)+")"+"<br>"+"Velocity: "+str(vilocity)+"<br>"+"</font><hr //>"+"<font size=\"5\">"+"Last_Update: "+str(final_updateTime2)+"</font><br><br>"
    # Add custom basemaps
    #name_and_angle="<table><tr><td>Vessel</td><td>Head angle</td><td>GPS</td><td>Vilocity</td><td>Last Update</td></tr>"+"<tr><td>"+ship_name+"</td>"+"<td>"+str(head)+"</td>"+"<td>"+str(vilocity)+"</td>"+"<td>"+str(last_time)+"</td></tr></table>"


    iframe_geffory="""
    <!DOCTYPE html>
    <html>
    <head>
    """
        
    iframe_geffory2="""
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link type="text/css" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
    <script src="http://192.168.0.201:8080/Ship_map_dashboard/Ship_map_dashboard/jquery.min.js"></script>
    </head>
    <body>
        
    </body>
    </html>
    """
    iframe_geffory3=iframe_geffory+name_and_angle+iframe_geffory2
    iframe_geffory3=folium.Html(iframe_geffory3,script=True)
    iframe = IFrame(html=iframe_geffory3, width=400, height=220)
    popup = folium.Popup(iframe, max_width=400)
    # Add the elevation model to the map object.
    #my_map.add_ee_layer(dem.updateMask(dem.gt(0)), vis_params, 'DEM')

    # Add a layer control panel to the map.
    #my_map.add_child(folium.Polygon(locations=[i], weight=10,color="white",popup=name_and_angle)) #i_v2=direction
        
    folium.Marker(location=final_position,popup=popup,icon = myIcon).add_to(my_map)
    plugins.Fullscreen().add_to(my_map)
    #my_map.add_child(folium.PolyLine(locations=JC85, weight=3,color="white",)) 
    #my_map.add_child(folium.PolyLine(locations=JC110, weight=3,color="white",)) 
    #my_map.add_child(folium.PolyLine(locations=NP, weight=3,color="white",)) 
    #my_map.add_child(folium.PolyLine(locations=NP2, weight=3,color="white",)) 
    #my_map.add_child(folium.PolyLine(locations=NP3, weight=3,color="white",)) 
    #my_map.add_child(folium.PolyLine(locations=SWP, weight=3,color="white",))
    #my_map.add_child(folium.PolyLine(locations=SBC2, weight=3,color="white",))
    #my_map.add_child(folium.PolyLine(locations=SEP, weight=3,color="white",))
    #my_map.add_child(folium.PolyLine(locations=SEP2, weight=3,color="white",))
    #my_map.add_child(folium.PolyLine(locations=T11N, weight=3,color="white",))
    #my_map.add_child(folium.PolyLine(locations=T12PA, weight=3,color="white",))
    #my_map.add_child(folium.PolyLine(locations=T12SA, weight=3,color="white",))
        
    #file_name0=str(ship_name)+".html"
    file_name0="Ship_path.html"
        
    new_path=read_iframe_path+"\\"+file_name0
    print(new_path)
    my_map.save(new_path)
        



    
     



def db_catch_predict_data():
    server = 'vesselstatusdb.database.windows.net' 
    database = 'VesselStatusDB' 
    username = 'lunghwa' 
    password = 'LHE@debug' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    sql_cmd="SELECT Ship_name,GPS_lat,GPS_lon,Head_angle,Vilocity,Time_now FROM dbo.Predict_system"
    cursor.execute(sql_cmd)
    
    db_return_data=cursor.fetchall()
    #for i in db_return_data:
    #    #print(i)
    return db_return_data


def split_list(L,n):
    for i in range(0,len(L),n):
        yield L[i:i+n]

SQLALCHEMY_TRACK_MODIFICATIONS = False
view_dect=0


Waruna=["BroCombo","Infinity","TenderHarmony","Amethyst","GarudaAsia"]
Soechi=["Immanuel","SC_ChampionXLV"]
LungSoon=["LungSoonFa-1","LungYuin","OceanVenture-II","OceanVenture-VI","PacificJourney-8","PacificPursuit-107","PacificPursuit-777","PacificJourney-101"]
FongKuo=["FongKuo-866"]
TsVessel=["Hochiminh","Ningbo","NanSha"]
EVERSHINING=["EverShining"]
#Waruna_Soechi=Waruna+Soechi
total_ship_list=["Waruna","Soechi","LungSoon","FongKuo"]
@app.route('/Path2/<vessel_group>/<lan>',methods=["GET","POST"])
def Path2(vessel_group,lan):
    print("-----------------------Path2-----------------------")
    search_data='default'
    video_user = 'videosoft'
    video_password = 'videosoft'
    language=lan
    vessel_array=[]
    if vessel_group=="Waruna":
        vessel_array=Waruna
    elif vessel_group=="Soechi":
        vessel_array=Soechi
    elif vessel_group=="LungSoon":
        vessel_array=LungSoon
    elif vessel_group=="FongKuo":
        vessel_array=FongKuo
    elif vessel_group=="TsVessel":
        vessel_array=TsVessel
    elif vessel_group=="EVERSHINING":
        vessel_array=EVERSHINING
    else:
        print("vessel_array=error")
    ##print("GOT!!!!!!!!!!!!!!!!!!!")
    global view_dect
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    global data_path
    oh=data_path+"\\"+"Ship_path.html"
    global start_date
    global end_date
    global name
    global PORT

    global end_date_error_view
    path_fleet="/Path2/"+vessel_group
    current_time=datetime.now
    ar1=[]
    points=[]
    points2=[]
    points3=[]
    new_name_list=[]
    new_gps_list=[]
    new_head_list=[]
    new_vilocity_list=[]
    new_update_time_list=[]
    new_video_list=[]
    new_video_list2=[]
    new_video_list3=[]
    name="Vessel"
    vessel_db="Ship_name"
    con="SELECT "+vessel_db+" FROM dbo.Ku_All_result"
    cursor.execute(con)
    a=cursor.fetchall()
    ##print(a)



    total_ship_data=db_catch_predict_data()
    ##print(total_ship_data)
    position_list=[]
    name_list2=[]
    head_list2=[]
    vilocity_list2=[]
    time_list2=[]
    start_time2=time.time()

    for i in a:
        i2=str(i)
        i3=i2.split("'")
        i4=i3[1]
        i5=str(i4)
        ##print(i5)
        if i5 in vessel_array:
            ar1.append(i5)
    ar_sort=sorted(ar1)                
    
    for i2 in ar_sort:
        cursor.execute("SELECT Ship_name,GPS_lat,GPS_lon,Head_angle,Vilocity,Time_now FROM dbo.Predict_system where Ship_name=?",i2)
        full_data=cursor.fetchall()
        ##print(full_data)
        # [('OceanVenture-VI', 39.778611, 148.974444, 230.25, 21.74, datetime.datetime(2021, 11, 19, 1, 29))]

        full_data2=str(full_data)
        if full_data2!="[]":
            full_data3=full_data2.split(",")
            #----------------------------------------------------------------------------------------
            full_data_name=full_data3[0]
            ##print(full_data_name)
            full_data_name2=str(full_data_name)
            full_data_name3=full_data_name2.split("'")
            full_data_name4=full_data_name3[1]
            full_data_name5=str(full_data_name4).strip()
            #print(full_data_name5)
            new_name_list.append(full_data_name5)
            #----------------------------------------------------------------------------------------
            full_data_lat=full_data3[1]
            full_data_lat2=str(full_data_lat)
            full_data_lon=full_data3[2]
            full_data_lon2=str(full_data_lon)
            full_data_position=full_data_lat2+","+full_data_lon2
            full_data_position=full_data_position.strip()
            #print(full_data_position)
            new_gps_list.append(full_data_position)
            #----------------------------------------------------------------------------------------
            full_data_head=full_data3[3]
            full_data_head2=str(full_data_head).strip()
            #print(full_data_head2)
            new_head_list.append(full_data_head2)
            #----------------------------------------------------------------------------------------
            full_data_vilocity=full_data3[4]
            full_data_vilocity2=str(full_data_vilocity).strip()
            #print(full_data_vilocity2)
            new_vilocity_list.append(full_data_vilocity2)
            #----------------------------------------------------------------------------------------
            full_data_year=full_data3[5]
            full_data_year2=str(full_data_year)
            full_data_year3=full_data_year2.split("(")
            full_data_year4=full_data_year3[1]
            full_data_year5=str(full_data_year4).strip()
            ##print(full_data_year5)
            #----------------------------------------------------------------------------------------
            full_data_month=full_data3[6]
            full_data_month2=str(full_data_month).strip()
            ##print(full_data_month2)
            #----------------------------------------------------------------------------------------
            full_data_day=full_data3[7]
            full_data_day2=str(full_data_day).strip()
            ##print(full_data_day2)
            #----------------------------------------------------------------------------------------
            full_data_hour=full_data3[8]
            full_data_hour2=str(full_data_hour).strip()
            ##print(full_data_hour2)
            #----------------------------------------------------------------------------------------
            full_data_min=full_data3[9]
            full_data_min2=str(full_data_min)
            full_data_min3=full_data_min2.split(")")
            full_data_min4=full_data_min3[0]
            full_data_min5=str(full_data_min4).strip()
            ##print(full_data_min5)
            #----------------------------------------------------------------------------------------
            fully_date=full_data_year5+"-"+full_data_month2+"-"+full_data_day2+" "+full_data_hour2+":"+full_data_min5
            #print(fully_date)
            new_update_time_list.append(fully_date)
    end_time2=time.time()
    print(f"cost time2 = {end_time2-start_time2}")
    if request.method=="GET":
        start_time3=time.time()
        #if vessel_group in total_ship_list:
        start_date=request.values.get("get_date")
        end_date=request.values.get("get_date1")
        end_date_error_view=end_date
        name=request.values.get("get_ship_name")
        
        search_data=request.values.get("search")
        if search_data==None:
            search_data=""
        #print(f"The search data is : {search_data}\n")
        if end_date!=None:
            end_date=end_date+" "+"23:59:59"
        else:
            end_date=""
        print(f"Get date!! start date={start_date}  end date={end_date}")
        
        if (name!=None) and (name!='') and (name!="Vessel"):
            print(f"name={name}")
            cursor.execute("SELECT Ship_name,GPS_lat,GPS_lon,Head_angle,Vilocity,Time_now FROM dbo.Predict_system where Ship_name=?",name)
            table_beta=cursor.fetchall()
            table_beta2=str(table_beta)
            table_beta3=table_beta2.split("(")
            table_beta4=table_beta3[1]
            table_beta_time=table_beta3[2]
            ##print(i_time)
            table_beta_time2=str(table_beta_time).split(")")
            table_beta_time3=table_beta_time2[0]
            ##print(i_time3)
            table_beta4=str(table_beta4)
            table_beta5=table_beta4.split(",")
            ship_name_db=str(table_beta5[0])
            ship_name_split=ship_name_db.split("'")
            real_ship_name=str(ship_name_split[1]).strip()
            LAT=float(str(table_beta5[1]).strip())
            LON=float(str(table_beta5[2]).strip())
            #add_position=LAT+","+LON
            head=float(str(table_beta5[3]).strip())
            vilocity=float(str(table_beta5[4]).strip())
            last_time=table_beta_time3
            #print(LAT)
            #print(LON)
            #print(head)
            #print(vilocity)
            #print(last_time)
            

            
        else:
            LAT=0
            LON=0
            #add_position=LAT+","+LON
            head=0
            vilocity=0
            last_time="0"
      
 
        if start_date!=None:
            start_date=start_date.strip()
        if end_date!=None:
            end_date=end_date.strip()
        if ((name!=None) and (name!="Vessel")):
            print(f"name------{name}")
            print(f"start_date-------{start_date}")
            print(f"end_date-------{end_date}")

            if((name!="Vessel")and(start_date!="")and(end_date!="23:59:59")):
                cursor.execute("SELECT TOP 1 gps_lat,gps_lon,CCTV_Active FROM dbo.Ku_All_result_history where Ship_name=? and gps_lat!='0' and time>=? and time<=? order by time desc",name,start_date,end_date)
                the_ship_last_position=cursor.fetchall()
                print(f"the ship last position is : {the_ship_last_position}")
                if the_ship_last_position!=[]:
                    final_position_not_split=str(the_ship_last_position).split("'")
                    final_position_lat=str(final_position_not_split[1]).strip()
                    final_position_lon=str(final_position_not_split[3]).strip()
                    new_cctv=str(final_position_not_split[5]).strip()
                    #print(new_cctv)
                    final_lat_lon=[float(final_position_lat),float(final_position_lon)]
                    #print(final_lat_lon)
                    gps_time_array=[]
                    got_you_array=[] #Ku-Online
                    got_you_array2=[] #Ku-offline
                    cursor.execute("SELECT gps_lat,gps_lon,time FROM dbo.Ku_All_result_history where Ship_name=? and gps_lat!='0' and time>=? and time<=? order by time desc",name,start_date,end_date)
                    get_db_data=cursor.fetchall()
                    ##print(get_db_data)
                    for i in get_db_data:
                        ##print(i)
                        gps_time_array.append(i[0])
                        gps_time_array.append(i[1])
                        gps_time_array.append(i[2])
                    ##print(gps_time_array)
                    for x in range(2,len(gps_time_array)-1,3):
                        time_delta=gps_time_array[x]-gps_time_array[x+3]
                        time_delta_sec=time_delta.seconds
                        if time_delta_sec<=1080:
                            lat_alpha=str(gps_time_array[x-2]).strip()
                            lon_alpha=str(gps_time_array[x-1]).strip()
                            alpha_pos=lat_alpha+","+lon_alpha
                            lat_beta=str(gps_time_array[x+1]).strip()
                            lon_beta=str(gps_time_array[x+2]).strip()
                            beta_pos=lat_beta+","+lon_beta
                            got_you_array.append(float(lat_alpha))
                            got_you_array.append(float(lon_alpha))
                            got_you_array.append(float(lat_beta))
                            got_you_array.append(float(lon_beta))
                        else:
                            lat_alpha=str(gps_time_array[x-2]).strip()
                            lon_alpha=str(gps_time_array[x-1]).strip()
                            alpha_pos=lat_alpha+","+lon_alpha
                            lat_beta=str(gps_time_array[x+1]).strip()
                            lon_beta=str(gps_time_array[x+2]).strip()
                            beta_pos=lat_beta+","+lon_beta
                            got_you_array2.append(float(lat_alpha))
                            got_you_array2.append(float(lon_alpha))
                            got_you_array2.append(float(lat_beta))
                            got_you_array2.append(float(lon_beta))

                    got_you_array_new_list=list(split_list(got_you_array,2))
                    got_you_array_new_list=list(split_list(got_you_array_new_list,2))
                    got_you_array_new_list2=list(split_list(got_you_array2,2))
                    got_you_array_new_list2=list(split_list(got_you_array_new_list2,2))

                    yoyo_points=got_you_array_new_list
                    yoyo_points2=got_you_array_new_list2
                    print(".........Output map track start!!")
                    output_map(name,yoyo_points,yoyo_points2,head,vilocity,last_time,LAT,LON,new_cctv,final_lat_lon,"path2",language)
                    print(".........Output map track finish..")
                else:
                    return render_template(
                    'NoData.html',
                    title='NoData',
                    )

            else:
                print("wowowowowowow")
                

        #if name!=None:
        #    con_name=str(name)+".html"
        #    return render_template(
        #        con_name,
        #        title='Path',
        #        year=datetime.now().year,
        #        Ship_name=ar1
        #    )
        #read_port=open("PORT.txt","r")
        #read_real_port=read_port.readline().strip()
        ##print(read_real_port)
        #read_port.close()
        #if name!=None:
        #    con_name2="http://localhost:"+str(read_real_port)+"/Path?get_ship_name="+str(name)
        #    #print(con_name2)
        #else:
        #    con_name2=""

        #new_name_list=[]
        #new_gps_list=[]
        #new_head_list=[]
        #new_vilocity_list=[]
        #new_update_time_list=[]
        print(new_name_list)
        #user3_test=requests.get(video_url,timeout=(15,20),auth=HTTPBasicAuth(video_user, video_password)) #左側選單抓出所有船的燈號
        #if (user3_test.status_code == requests.codes.ok):   
        #user3=req.Request(video_url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"})
        #with req.urlopen(user3)  as video_read:
        #    user_read=video_read.read()
        for name_read in new_name_list:
            ####################################################################
            cursor.execute("SELECT active,delta_last_time,L_delta FROM dbo.VideoSoft_web_status WHERE ship_name=?",name_read)
                
            videosoft_db_data=cursor.fetchall()
            if videosoft_db_data!=[]:
                for i in videosoft_db_data:
                    videosoft_active2=i[0]
                    videosoft_delta_time4=i[1]
                    se_last_time=i[2]
                #print(f"videosoft_db={videosoft_db_data_str}")
                if se_last_time=="NoData":
                    se_last_time=10000
                print(f"name={name_read}")
                print(f"videosoft_active={videosoft_active2}")
                print(f"videosoft_delta_time={videosoft_delta_time4}")
                if ((videosoft_active2=="True") or (videosoft_delta_time4<=700) or (int(se_last_time)<=700)):
                    video_status="/static/img/V3-GreenLight.png"
                else:
                    
                    video_status="/static/img/V3-RedLight.png"
                new_video_list.append(name_read)
                new_video_list.append(video_status)
            else:
                new_video_list.append(name_read)
                new_video_list.append("/static/img/V3-RedLight.png")


            ####################################################################
        print(f"new_video_list={new_video_list}")        
        light_video_spl_array=list(split_list(new_video_list,2))
        uniq_array_light=[]
        uniq_array_light2=[]
        for i in light_video_spl_array:
            if i not in uniq_array_light:
                uniq_array_light.append(i)
        for x in uniq_array_light:
            uniq_array_light2.append(x[1])
        #print(f"uniq_array_light={uniq_array_light}")
        print(uniq_array_light2)

        cctv_button_status_list=[]
        for y in uniq_array_light2:
            if y=="/static/img/V3-GreenLight.png":
                cctv_button_status_list.append("/static/img/V4-CamOpen-6.png")#/static/img/camera_img.png
            else:
                cctv_button_status_list.append("/static/img/V4-CamClose-6.png")#/static/img/CAM_ERROR_BUTTON.png

        if ((start_date=="") or (end_date=="23:59:59") or (end_date_error_view==None) or (name==None)) and (vessel_group!="Ship_path.html"):
            start_date=""
            end_date=""
            end_date_error_view=""
            name="Vessel"
            #iframe_path="/static/Fleet/"+vessel_group+".html"
            if (language=="TW"):
                MAP_PATH="/static/Fleet/"+vessel_group+"_TW.html"
            else:
                MAP_PATH="/static/Fleet/"+vessel_group+".html"
            iframe_path=MAP_PATH
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"vessel_group={vessel_group}")
            print(f"MAP_PATH={MAP_PATH}")
            print(f"iframe_path={iframe_path}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            basedir=os.path.abspath(os.path.dirname(__file__))
            MAP_PATH="/static/Fleet/Ship_path.html"
            #MAP_PATH="Ship_path"
            iframe_path=MAP_PATH
            print("======================================")
            print(f"vessel_group={vessel_group}")
            print(f"MAP_PATH={MAP_PATH}")
            print(f"iframe_path={iframe_path}")
            print("======================================")
            #iframe_path="../templates/Ship_path.html"
        
        ##print(f"the new_name_list is : {new_name_list}")
        #print(f"the new_name_list is : {new_name_list}")
        first_url_array=[]
        for i in new_name_list:
            i=str(i)
            #print(i)
            cursor.execute("SELECT mjpeg_url from dbo.Portal_cam_data where ship_name=?",i)
            no_clear_url=cursor.fetchall()
            if no_clear_url!=[]:
                #print(f"no_clear_url={no_clear_url}")
                no_clear_url2=str(no_clear_url).split("'")
                no_clear_url3=str(no_clear_url2[1])
                #no_clear_url3=no_clear_url3.replace("videosoft:videosoft","")  just test
                #print(no_clear_url3)
                first_url_array.append(no_clear_url3)
            else:
                first_url_array.append("NoData")
        #print(first_url_array)
        end_time3=time.time()
        print(f"cost time3={end_time3-start_time3}")
        print(f"new_name_list={new_name_list}")
        light_status_id_list=[]
        for i in range(1,len(new_name_list)+1,1):
            i2="light_status"+str(i)
            light_status_id_list.append(i2)
        print(light_status_id_list)

        cctv_status_id_list=[]
        for x in range(1,len(new_name_list)+1,1):
            x2="cctv_id"+str(x)
            cctv_status_id_list.append(x2)
        print(f"cctv_status_id_list={cctv_status_id_list}")

        get_new_web=[]
        light_path=open("light_path.txt","r")
        read_light_path=light_path.readline().strip()

        cctv_status_url=open("light_path.txt","r")
        read_cctv_status=cctv_status_url.readline().strip()
        cctv_status_url.close()
        for i in new_name_list:
            i2=read_cctv_status+str(i)
            get_new_web.append(i2)
        light_path.close()

        


        return render_template(
            'Path2.html',
            title='Path2',
            year=datetime.now().year,
            Ship_name=new_name_list,
            gps=new_gps_list,
            head_angle=new_head_list,
            vilocity_back=new_vilocity_list,
            go_update_time=new_update_time_list,
            select_name=name,
            date1=start_date,
            date2=end_date,
            date3=end_date_error_view,
            search=search_data,
            vsg=vessel_group,
            cute_dog='/static/img/CAM_ERROR.png',
            IFRAME_PATH=iframe_path,
            PATH_FLEET=path_fleet,
            new_name_list=new_name_list,
            new_gps_list=new_gps_list,
            new_head_list=new_head_list,
            new_vilocity_list=new_vilocity_list,
            new_update_time_list=new_update_time_list,
            uniq_array_light2=uniq_array_light2,
            first_url_array=first_url_array,
            light_status_id_list=light_status_id_list,
            get_new_web=get_new_web,
            cctv_status_id_list=cctv_status_id_list,
            cctv_button_status_list=cctv_button_status_list,
            LANGUAGE=language,
            mylist = zip(new_name_list, new_gps_list,new_head_list,new_vilocity_list,new_update_time_list,uniq_array_light2,first_url_array,light_status_id_list,cctv_status_id_list,cctv_button_status_list)
            
        )

    print("----------------------Path2(end)----------------------")
        
        #os.remove(oh)


@app.route('/Path3/<rock_name>/<vessel_group2>/<lan>',methods=["GET","POST"])
def Path3(rock_name,vessel_group2,lan):
    start_date_test=request.values.get("get_date")
    end_date_test=request.values.get("get_date1")
   
    print("-----------------------Path3-----------------------")
    language=lan
    #print(f"#########################path_3{vessel_group2}")
    video_user = 'videosoft'
    video_password = 'videosoft'
    #Waruna_Soechi=["BroCombo","Defiance","Infinity","TenderHarmony","AMETHYST"]
    #print("GOT!!!!!!!!!!!!!!!!!!!")
    global view_dect
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    global data_path
    oh=data_path+"\\"+"Ship_path.html"
    global start_date
    global end_date
    global name
    global PORT
    global end_date_error_view
    ya_crew_list=[]
    vessel_track="/static/img/Coordinate.png"
    current_time=datetime.now
    #print(rock_name)
    ar1=[]
    points=[]
    points2=[]
    points3=[]
    new_name_list=[]
    new_gps_list=[]
    new_head_list=[]
    new_vilocity_list=[]
    new_update_time_list=[]
    new_video_list=[]
    name="Ship_name"
    db_catch_time_array=[]

    cursor.execute("SELECT esn FROM dbo.ship_info where ship_name=?",rock_name)
    ship_info_esn=cursor.fetchone()
    ##print(ship_info_esn)
    ship_info_esn=str(ship_info_esn)
    ship_info_esn2=ship_info_esn.split("'")
    ship_info_esn3=str(ship_info_esn2[1])#esn
    ##print(ship_info_esn3) 

    # 資料庫設定
    #db_settings = {
    #    "host": "10.10.0.31",
    #    "port": 3306,
    #    "user": "hughes1",
    #    "password": "Hughes@2020",
    #    "db": "hughes-regional",
    #    "charset": "utf8"
    #}
    db_settings = {
        "host": "10.0.0.224",
        "port": 3306,
        "user": "apuser",
        "password": "123456",
        "db": "hughes-regional",
        "charset": "utf8"
        }
    try:
        # 建立Connection物件
        conn2 = pymysql.connect(**db_settings)
    except Exception as ex:
        print(ex)
    esn_test=ship_info_esn3
    #print(esn_test)
    with conn2.cursor() as cursor2:
        command = "Select branch_id from ships_base where esn = "
        command2=command+str(esn_test)
        ##print(command2)
        cursor2.execute(command2)
        branch_id_test2=cursor2.fetchall()
        #print(f" the branch id is : {branch_id_test2}")
        branch_id_test3=str(branch_id_test2).split("(")
        branch_id_test4=branch_id_test3[2]
        branch_id_test5=str(branch_id_test4).split(",")
        branch_id_test6=str(branch_id_test5[0]).strip()
        #print("=================================branch_id=================================")
        #print(f"the branch id is : {branch_id_test6}\n")  #final_branch_id
        #print("=================================captain===================================")
        command3_cap="Select user_id from rob_agency_branch where id="
        command4_cap=command3_cap+branch_id_test6
        cursor2.execute(command4_cap)
        cap_id=cursor2.fetchall()
        #print(cap_id)
        cap_id2=str(cap_id).split("(")
        cap_id3=str(cap_id2[2])
        cap_id4=cap_id3.split(",")
        cap_id5=str(cap_id4[0])
    
        command5_cap="Select name,id,end_date from rob_user_flow_package where user_id="
        command6_cap=command5_cap+cap_id5
        con_str_cap=" and end_date > CURDATE()"
        command7_cap=command6_cap+con_str_cap
        ##print(command7_cap)
        cursor2.execute(command7_cap)
        cap_pack_flow=cursor2.fetchall()
        #print(f"{cap_pack_flow}\n")

        if (len(cap_pack_flow)!=0):
            #print("test")
            for i_cap in cap_pack_flow:
                #print("test")
                i_cap2=str(i_cap).split(",")
                i_cap3=str(i_cap2[1]).strip()#search_id
                i_cap4=str(i_cap2[0]).strip()
                i_cap5=i_cap4.split("'")
                i_cap6=str(i_cap5[1])
                command8_cap="Select user_id,name,left_amount from rob_user_flow_detail where product_type = '1' and package_id = "
                command9_cap=command8_cap+i_cap3
                cursor2.execute(command9_cap)
                final_cap_list=cursor2.fetchall()
                for haha_cap in final_cap_list:
                    haha2_cap=str(haha_cap).split(",")
                    haha3_cap=str(haha2_cap[2])
                    haha4_cap=haha3_cap.split(")")
                    haha5_cap=str(haha4_cap[0])
                    haha5_cap=float(haha5_cap)
                    haha5_cap=round(haha5_cap,3)
                    haha5_cap=haha5_cap/1000
                    haha5_cap=format(haha5_cap,",")
                    
                    command10_cap="Select login_phone,name from rob_user_info where id = "
                    command11_cap=command10_cap+cap_id5
                    cursor2.execute(command11_cap)
                    cap_user_info=cursor2.fetchall()
                    ##print(cap_user_info)
                    for cap_info in cap_user_info:
                        cap_info=str(cap_info)
                        cap_info2=cap_info.split(",")
                        cap_info3=str(cap_info2[0])#account
                        cap_info4=str(cap_info2[1])#captain name
                        cap_info3_x=cap_info3.split("'")
                        cap_info3_y=str(cap_info3_x[1])
                        ##print(cap_info3_y)#final_account
                        cap_info4_x=cap_info4.split("'")
                        cap_info4_y=str(cap_info4_x[1])
                        ##print(cap_info4_y)
              
                        #print(f"the captain id : {cap_id5}")
                        #print(f"the search id {i_cap3}")
                        #print(f"Captain Name : {cap_info4_y}")
                        if language=="TW":
                            cap_info4_y="Captain Name : "+cap_info4_y
                            #print(f"Captain Acount : {cap_info3_y}")
                            cap_info3_y="帳號名稱 : "+cap_info3_y
                            #print(f"The Captain Package : {i_cap6}")
                            i_cap6="套餐包 : "+i_cap6
                            #print(f"Captain Left Traffic : {haha5_cap}")
                            haha5_cap="剩餘流量(MB) : "+haha5_cap
                        else:
                            cap_info4_y="Captain Name : "+cap_info4_y
                            #print(f"Captain Acount : {cap_info3_y}")
                            cap_info3_y="Captain Account : "+cap_info3_y
                            #print(f"The Captain Package : {i_cap6}")
                            i_cap6="Package : "+i_cap6
                            #print(f"Captain Left Traffic : {haha5_cap}")
                            haha5_cap="Left(MB) : "+haha5_cap
                
        else:
            ##print("test2")
            if language=="TW":
                cap_info4_y="帳號名稱 : 無資料"
                cap_info3_y="帳號名稱 : 無資料"
                i_cap6="套餐包 : 無資料"
                haha5_cap="剩餘流量(MB) : 無資料"
            else:
                cap_info4_y="No data"
                cap_info3_y="CAP Account : No data"
                i_cap6="Package : No data"
                haha5_cap="Left(MB) : No data"


                




        #print("===================================crew====================================")
        command3_crew="Select user_id from rob_agency_branch_user where branch_id="
        command4_crew=command3_crew+branch_id_test6
        cursor2.execute(command4_crew)
        crew_id=cursor2.fetchall()
        ##print(crew_id)
        for i_crew in crew_id:
            ##print(i)
            crew_id2=str(i_crew).split("(")
            crew_id3=str(crew_id2[1])
            crew_id4=crew_id3.split(",")
            crew_id5=str(crew_id4[0])
            ##print(crew_id5)
            command5_crew="Select name,id,end_date from rob_user_flow_package where user_id="
            command6_crew=command5_crew+crew_id5
            con_str_crew=" and end_date > CURDATE()"
            command7_crew=command6_crew+con_str_crew
            ##print(command7_crew)
            cursor2.execute(command7_crew)
            crew_pack_flow=cursor2.fetchall()
            #print(f"{crew_pack_flow}\n")
            if (len(crew_pack_flow)!=0):
                for j_crew in crew_pack_flow:
                    j2_crew=str(j_crew).split(",")
                    j3_crew=str(j2_crew[1])
                    j4_crew=str(j2_crew[0])
                    j5_crew=j4_crew.split("'")
                    j6_crew=str(j5_crew[1])
                    command8_crew="Select user_id,name,left_amount from rob_user_flow_detail where product_type = '1' and package_id = "
                    command9_crew=command8_crew+j3_crew
                    cursor2.execute(command9_crew)
                    final_crew_list=cursor2.fetchall()
                    #print(final_crew_list)
                    for haha_crew in final_crew_list:
                        haha2_crew=str(haha_crew).split(",")
                        haha3_crew=str(haha2_crew[2])
                        haha4_crew=haha3_crew.split(")")
                        haha5_crew=str(haha4_crew[0])
                        haha5_crew=float(haha5_crew)
                        haha5_crew=round(haha5_crew,3)
                        haha5_crew=haha5_crew/1000
                        haha5_crew=format(haha5_crew,",")
                        
                        command10_crew="Select login_phone,name from rob_user_info where id = "
                        command11_crew=command10_crew+crew_id5
                        cursor2.execute(command11_crew)
                        crew_user_info=cursor2.fetchall()
                        ##print(crew_user_info)
                        for crew_info in crew_user_info:
                            crew_info=str(crew_info)
                            crew_info2=crew_info.split(",")
                            crew_info3=str(crew_info2[0])#account
                            crew_info4=str(crew_info2[1])#crewtain name
                            crew_info3_x=crew_info3.split("'")
                            crew_info3_y=str(crew_info3_x[1])
                            ##print(crew_info3_y)#final_account
                            crew_info4_x=crew_info4.split("'")
                            crew_info4_y=str(crew_info4_x[1])
                            ##print(crew_info4_y)
                            #print(f"the crew id is : {crew_id5}")
                            #print(f"the search id is {j3_crew}\n")
                            ##print(f"crew name is : {crew_info4_y}")
                            #print(f"crew acount is : {crew_info3_y}")
                            #print(f"the crew package is : {j6_crew}")
                            #print(f"crew left traffic is : {haha5_crew}")
                            #ya_crew_list.append("Crew Name : "+crew_info4_y)
                            if language=="TW":
                                ya_crew_list.append("帳號名稱 : "+crew_info3_y)
                                ya_crew_list.append("套餐包 : "+j6_crew)
                                ya_crew_list.append("剩餘流量(MB) : "+haha5_crew)
                            else:
                                ya_crew_list.append("Crew Account : "+crew_info3_y)
                                ya_crew_list.append("Package : "+j6_crew)
                                ya_crew_list.append("Left(MB) : "+haha5_crew)
                            #print("==================================================================")
            
            else:
                #ya_crew_list.append("Crew Name : No Data")
                if language=="TW":
                    ya_crew_list.append("帳號名稱 : 無資料")
                    ya_crew_list.append("套餐包 : 無資料")
                    ya_crew_list.append("剩餘流量(MB) : 無資料")
                else:
                    ya_crew_list.append("Crew Account : No Data")
                    ya_crew_list.append("Package : No Data ")
                    ya_crew_list.append("Left(MB) : No Data")






    ya_crew_list2=list(split_list(ya_crew_list,4))

    con="SELECT "+name+" FROM dbo.Ku_All_result"
    cursor.execute(con)
    a=cursor.fetchall()
    ##print(a)

    


    cap_traffic_data="tenderxxunlimited - unlimited-512-1"
    cap_remain="400 MB"
    crew_traffic_data="tenderxx2gb - 2GB Month"
    crew_remain="36 MB"

    cursor.execute("SELECT Ship_name,esn FROM dbo.Ku_All_result where Ship_name=?",rock_name)
    name_esn_data=cursor.fetchall()
    #print(f"the vessel name and esn is : {name_esn_data}")

    cursor.execute("SELECT Ship_name,GPS_lat,GPS_lon,Head_angle,Vilocity,Time_now FROM dbo.Predict_system where Ship_name=?",rock_name)
    full_data=cursor.fetchall()
    #print(full_data)
    # [('OceanVenture-VI', 39.778611, 148.974444, 230.25, 21.74, datetime.datetime(2021, 11, 19, 1, 29))]
            
    full_data2=str(full_data)
    if full_data2!="[]":
        full_data3=full_data2.split(",")
        #print(f"full_data3={full_data3}")
        #----------------------------------------------------------------------------------------
        full_data_name=full_data3[0]
        #print(full_data_name)
        full_data_name2=str(full_data_name)
        full_data_name3=full_data_name2.split("'")
        full_data_name4=full_data_name3[1]
        full_data_name5=str(full_data_name4).strip()
        #print(full_data_name5)
        
        #----------------------------------------------------------------------------------------
        full_data_lat=full_data3[1]
        full_data_lat2=str(full_data_lat)
        full_data_lon=full_data3[2]
        full_data_lon2=str(full_data_lon)
        full_data_position=full_data_lat2+","+full_data_lon2
        full_data_position=full_data_position.strip()
        #print(full_data_position)
      
        #----------------------------------------------------------------------------------------
        full_data_head=full_data3[3]
        full_data_head2=str(full_data_head).strip()
        #print(full_data_head2)
      
        #----------------------------------------------------------------------------------------
        full_data_vilocity=full_data3[4]
        full_data_vilocity2=str(full_data_vilocity).strip()
        #print(full_data_vilocity2)
     
        #----------------------------------------------------------------------------------------
        full_data_year=full_data3[5]
        full_data_year2=str(full_data_year)
        full_data_year3=full_data_year2.split("(")
        full_data_year4=full_data_year3[1]
        full_data_year5=str(full_data_year4).strip()
        ##print(full_data_year5)
        #----------------------------------------------------------------------------------------
        full_data_month=full_data3[6]
        full_data_month2=str(full_data_month).strip()
        ##print(full_data_month2)
        #----------------------------------------------------------------------------------------
        full_data_day=full_data3[7]
        full_data_day2=str(full_data_day).strip()
        ##print(full_data_day2)
        #----------------------------------------------------------------------------------------
        full_data_hour=full_data3[8]
        full_data_hour2=str(full_data_hour).strip()
        ##print(full_data_hour2)
        #----------------------------------------------------------------------------------------
        full_data_min=full_data3[9]
        full_data_min2=str(full_data_min)
        full_data_min3=full_data_min2.split(")")
        full_data_min4=full_data_min3[0]
        full_data_min5=str(full_data_min4).strip()

        print(f"full_data_min5={full_data_min5}")
        #----------------------------------------------------------------------------------------
        fully_date=full_data_year5+"-"+full_data_month2+"-"+full_data_day2+" "+full_data_hour2+":"+full_data_min5
        
 
    cursor.execute("SELECT Time_now FROM dbo.Predict_system where Ship_name=?",rock_name)
    predict_system_time=cursor.fetchall()
    if predict_system_time!=[]:
        for i in predict_system_time:
            print(f"predict_system_time={i[0]}")
            fully_date=i[0]
    for i in a:
        i2=str(i)
        i3=i2.split("'")
        i4=i3[1]
        i5=str(i4)
        ##print(i5)
        ar1.append(i5) #total_ship_name
    #ar_sort=sorted(ar1)
    
    if request.method=="GET":
        #print(rock_name)
        start_date=request.values.get("get_date")
        end_date=request.values.get("get_date1")
        end_date_error_view=end_date
        cursor.execute("SELECT TOP 150 time FROM dbo.Ku_All_result_history where Ship_name=? order by time desc",rock_name)
        test_data=cursor.fetchall()
        for i in test_data:
            ##print(i)
            db_catch_time_array.append(i)

        #print(db_catch_time_array)
        new_db_catch_time=db_catch_time_array[0]
        old_db_catch_time=db_catch_time_array[(len(db_catch_time_array)-1)]
        #print(old_db_catch_time)
        ####################################################################################################################
        new_db_catch_time=str(new_db_catch_time).split("(")
        new_db_catch_time=new_db_catch_time[2].split(")")
        new_db_catch_time=str(new_db_catch_time[0])
        new_db_catch_time=new_db_catch_time.split(",")
        new_db_catch_year=str(new_db_catch_time[0]).strip()
        new_db_catch_mon=str(new_db_catch_time[1]).strip()
        new_db_catch_day=str(new_db_catch_time[2]).strip()

        new_db_catch_time=new_db_catch_year+"-"+new_db_catch_mon+"-"+new_db_catch_day+" 23:59:59"
        datetime_new_db_catch_time=datetime.strptime(new_db_catch_time, "%Y-%m-%d %H:%M:%S")
        ####################################################################################################################
        old_db_catch_time=str(old_db_catch_time).split("(")
        old_db_catch_time=old_db_catch_time[2].split(")")
        old_db_catch_time=str(old_db_catch_time[0])
        old_db_catch_time=old_db_catch_time.split(",")
        old_db_catch_year=str(old_db_catch_time[0]).strip()
        old_db_catch_mon=str(old_db_catch_time[1]).strip()
        old_db_catch_day=str(old_db_catch_time[2]).strip()

        old_db_catch_time=old_db_catch_year+"-"+old_db_catch_mon+"-"+old_db_catch_day+" 00:00:00"
        datetime_old_db_catch_time=datetime.strptime(old_db_catch_time, "%Y-%m-%d %H:%M:%S")

        #print(f"new data is : {datetime_new_db_catch_time} , old data is : {datetime_old_db_catch_time}")
        #online_1="30%"

        #name=request.values.get("get_ship_name")
        name=rock_name
        if (start_date!=None) and (start_date!="") and (end_date!=None) and (end_date!=""):
            #print("#######################################################################################")
            if end_date!=None:
                start_date=start_date+" "+"00:00:00"
                end_date=end_date+" "+"23:59:59"
            else:
                end_date=""
            
            online_1=online_ratio(name,start_date,end_date)
            #print(f"date_start={start_date},date_end={end_date},select_name={name}")
            cursor.execute("SELECT Ship_name,gps_lat,gps_lon FROM dbo.Ku_All_result_history where ship_name=? AND time BETWEEN ? AND ? ORDER BY time DESC",name,start_date,end_date)
            select_ship_data=cursor.fetchall()
            file_name=str(name)+".txt"
            path_file=open(file_name,"w")
            for i in select_ship_data:
                con_gps=str(i[1]).strip()+","+str(i[2]).strip()
                path_file.write(con_gps+"\n")
            if (name!=None) and (name!='') and (name!="Ship_name"):
                #print(f"name={name}")
                cursor.execute("SELECT Ship_name,GPS_lat,GPS_lon,Head_angle,Vilocity,Time_now FROM dbo.Predict_system where Ship_name=?",name)
                table_beta=cursor.fetchall()
                table_beta2=str(table_beta)
                table_beta3=table_beta2.split("(")
                table_beta4=table_beta3[1]
                table_beta_time=table_beta3[2]
                ##print(i_time)
                table_beta_time2=str(table_beta_time).split(")")
                table_beta_time3=table_beta_time2[0]
                ##print(i_time3)
                table_beta4=str(table_beta4)
                table_beta5=table_beta4.split(",")
                ship_name_db=str(table_beta5[0])
                ship_name_split=ship_name_db.split("'")
                real_ship_name=str(ship_name_split[1]).strip()
                LAT=float(str(table_beta5[1]).strip())
                LON=float(str(table_beta5[2]).strip())
                #add_position=LAT+","+LON
                head=float(str(table_beta5[3]).strip())
                vilocity=float(str(table_beta5[4]).strip())
                last_time=table_beta_time3
                #print(LAT)
                #print(LON)
                #print(head)
                #print(vilocity)
                #print(last_time)
            

            
            else:
                LAT=0
                LON=0
                #add_position=LAT+","+LON
                head=0
                vilocity=0
                last_time="0"
      
            path_file.close()
            path_file_read=open(file_name,"r")
            path_file_read2=path_file_read.readline().strip()
            while path_file_read2:
                points.append(path_file_read2)
                path_file_read2=path_file_read.readline().strip()
            path_file_read.close()

            for i in points:
                if "G" not in i:
                    ##print(i)
                    i2=str(i).split(",")
                    i3_lat=i2[0]
                    i3_lon=i2[1]
                    if float(i3_lon)>=-180 and float(i3_lon)<0:
                        i3_lon=float(i3_lon)+360.0
                    if float(i3_lat)!=0.0 and float(i3_lon)!=0.0:
                        points2.append(float(i3_lat))
                        points2.append(float(i3_lon))



                 
            points3=list(split_list(points2,2))
            ##print(points3)
            #print("\n")
        

            
            

            
            if name!=None:
                cursor.execute("SELECT TOP 1 gps_lat,gps_lon,CCTV_Active FROM dbo.Ku_All_result_history where Ship_name=? and gps_lat!='0' and time>=? and time<=? order by time desc",name,start_date,end_date)
                the_ship_last_position=cursor.fetchall()
                ##print(f"the ship last position is : {the_ship_last_position}")
                if the_ship_last_position!=[]:
                    final_position_not_split=str(the_ship_last_position).split("'")
                    final_position_lat=str(final_position_not_split[1]).strip()
                    final_position_lon=str(final_position_not_split[3]).strip()
                    new_cctv=str(final_position_not_split[5]).strip()
                    final_lat_lon=[float(final_position_lat),float(final_position_lon)]
                    #print(final_lat_lon)
                    gps_time_array=[]
                    got_you_array=[] #Ku-Online
                    got_you_array2=[] #Ku-offline
                    cursor.execute("SELECT gps_lat,gps_lon,time FROM dbo.Ku_All_result_history where Ship_name=? and gps_lat!='0' and time>=? and time<=? order by time desc",name,start_date,end_date)
                    get_db_data=cursor.fetchall()
                    for i in get_db_data:
                        ##print(i)
                        gps_time_array.append(i[0])
                        gps_time_array.append(i[1])
                        gps_time_array.append(i[2])
                    ##print(gps_time_array)
                    for x in range(2,len(gps_time_array)-1,3):
                        time_delta=gps_time_array[x]-gps_time_array[x+3]
                        time_delta_sec=time_delta.seconds
                        if time_delta_sec<=1080:
                            lat_alpha=str(gps_time_array[x-2]).strip()
                            lon_alpha=str(gps_time_array[x-1]).strip()
                            alpha_pos=lat_alpha+","+lon_alpha
                            lat_beta=str(gps_time_array[x+1]).strip()
                            lon_beta=str(gps_time_array[x+2]).strip()
                            beta_pos=lat_beta+","+lon_beta
                            got_you_array.append(float(lat_alpha))
                            got_you_array.append(float(lon_alpha))
                            got_you_array.append(float(lat_beta))
                            got_you_array.append(float(lon_beta))
                        else:
                            lat_alpha=str(gps_time_array[x-2]).strip()
                            lon_alpha=str(gps_time_array[x-1]).strip()
                            alpha_pos=lat_alpha+","+lon_alpha
                            lat_beta=str(gps_time_array[x+1]).strip()
                            lon_beta=str(gps_time_array[x+2]).strip()
                            beta_pos=lat_beta+","+lon_beta
                            got_you_array2.append(float(lat_alpha))
                            got_you_array2.append(float(lon_alpha))
                            got_you_array2.append(float(lat_beta))
                            got_you_array2.append(float(lon_beta))

                    got_you_array_new_list=list(split_list(got_you_array,2))
                    got_you_array_new_list=list(split_list(got_you_array_new_list,2))
                    got_you_array_new_list2=list(split_list(got_you_array2,2))
                    got_you_array_new_list2=list(split_list(got_you_array_new_list2,2))

                    yoyo_points=got_you_array_new_list
                    yoyo_points2=got_you_array_new_list2


                    output_map(name,yoyo_points,yoyo_points2,head,vilocity,last_time,LAT,LON,new_cctv,final_lat_lon,"path2",language)
        
                else:
                    return render_template(
                    'NoData.html',
                    title='NoData',
                    )
            #if name!=None:
            #    con_name=str(name)+".html"
            #    return render_template(
            #        con_name,
            #        title='Path',
            #        year=datetime.now().year,
            #        Ship_name=ar1
            #    )
            #read_port=open("PORT.txt","r")
            #read_real_port=read_port.readline().strip()
            ##print(read_real_port)
            #read_port.close()
            #if name!=None:
            #    con_name2="http://localhost:"+str(read_real_port)+"/Path?get_ship_name="+str(name)
            #    #print(con_name2)
            #else:
            #    con_name2=""

            #new_name_list=[]
            #new_gps_list=[]
            #new_head_list=[]
            #new_vilocity_list=[]
            #new_update_time_list=[]
       
            #mylist = zip(new_name_list, new_gps_list,new_head_list,new_vilocity_list,new_update_time_list)
            #context = {
            #            'mylist': mylist,
            #        }
            ##print("--------")
            ##print(rock_name)
            
            map_path_yoyo="/static/Fleet/Ship_path.html"
            print(f"fully_date={fully_date}")
            return render_template(
                'Path3.html',
                title='Path3',
                year=datetime.now().year,
                Ship_name=new_name_list,
                gps=full_data_position,
                head_angle=full_data_head2,
                vilocity_back=full_data_vilocity2,
                go_update_time=fully_date,
                select_name=name,
                date1=start_date,
                date2=end_date,
                date3=end_date_error_view,
                rock_name2=rock_name,
                cap=cap_traffic_data,
                cap_rem=cap_remain,
                crew=crew_traffic_data,
                crew_rem=crew_remain,
                #video=new_video,
                vsg=vessel_group2,
                captain_name=cap_info4_y,
                captain_account=cap_info3_y,
                captain_package=i_cap6,
                captain_left=haha5_cap,
                vessel_track_img=vessel_track,
                total_crew_list=ya_crew_list2,
                online_ratio=online_1,
                map_path_yoyo=map_path_yoyo,
                LANGUAGE=language
                #rock_gps=rock_gps,
                #rock_head=rock_head,
                #rock_vilocity=rock_vilocity,
                #rock_time=rock_time,
                #mylist = zip(new_name_list, new_gps_list,new_head_list,new_vilocity_list,new_update_time_list)
            )
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            cursor.execute("SELECT Vilocity FROM dbo.Predict_system where Ship_name=?",name)
            predict_system_data=cursor.fetchall()
            full_gps_array=[]
            for i in predict_system_data:
                
                vilocity=i[0]
                
            cursor.execute("SELECT lat,lon,heading,final_time from dbo.KU_SE_GPS WHERE ship_name=?",name)
            path3_get_ku_se_data=cursor.fetchall()
            for i in path3_get_ku_se_data:
                gps_lat=i[0]
                gps_lon=i[1]
                head_angle=i[2]
                time_now=i[3]
            total_gps=str(gps_lat)+","+str(gps_lon)
            full_gps_array.append(gps_lat)
            full_gps_array.append(gps_lon)
            output_map_single(name,head_angle,vilocity,fully_date,gps_lat,gps_lon,full_gps_array,language)
            
            map_path_yoyo="/static/Fleet/Ship_path.html"
            print(f"fully_date={fully_date}")
            return render_template(
                'Path3.html',
                title='Path3',
                year=datetime.now().year,
                
                gps=total_gps,
                head_angle=head_angle,
                vilocity_back=vilocity,
                go_update_time=fully_date,
                select_name=name,
                date1=time_now,
                date2=time_now,
               
                rock_name2=rock_name,
                cap=cap_traffic_data,
                cap_rem=cap_remain,
                crew=crew_traffic_data,
                crew_rem=crew_remain,
                #video=new_video,
                vsg=vessel_group2,
                captain_name=cap_info4_y,
                captain_account=cap_info3_y,
                captain_package=i_cap6,
                captain_left=haha5_cap,
                vessel_track_img=vessel_track,
                total_crew_list=ya_crew_list2,
                map_path_yoyo=map_path_yoyo,
                
                LANGUAGE=language
                #online_ratio=online_1
                #rock_gps=rock_gps,
                #rock_head=rock_head,
                #rock_vilocity=rock_vilocity,
                #rock_time=rock_time,
                #mylist = zip(new_name_list, new_gps_list,new_head_list,new_vilocity_list,new_update_time_list)
            )
        
        #os.remove(oh)
    print("----------------------Path3(end)----------------------")
@app.route('/Dashboard',methods=["GET","POST"])
def Dashboard():
    return render_template(
            'Dashboard.html',
            current_time=datetime.now
        )

@app.route('/Search/<vessel_group2>/<lan>',methods=["GET","POST"])
def Search(vessel_group2,lan):
    db_catch_time_array=[]
    global tmp_search
    language=lan
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    #vessel_group2=""
    #print(f"#########################search{vessel_group2}")
    if vessel_group2=="Waruna":
        cor_group=Waruna
    elif vessel_group2=="Soechi":
        cor_group=Soechi
    elif vessel_group2=="LungSoon":
        cor_group=LungSoon
    elif vessel_group2=="FongKuo":
        cor_group=FongKuo
    elif vessel_group2=="TsVessel":
        cor_group=TsVessel
    elif vessel_group2=="EVERSHINING":
        cor_group=EVERSHINING
    first_fozy_search=request.values.get("search")
    if first_fozy_search==None:
        #print("yoyoyo")
        first_fozy_search=request.values.get("test")
    
    #print(f"{first_fozy_search}")
    if ("'" not in first_fozy_search):
        search_data_first="SELECT Ship_name FROM dbo.Ku_All_result where Ship_name like '%"+first_fozy_search+"%'"
        cursor.execute(search_data_first)
    else:
        first_fozy_search="NoAnyData"
        search_data_first="SELECT Ship_name FROM dbo.Ku_All_result where Ship_name like '%"+first_fozy_search+"%'"
        cursor.execute(search_data_first)
        


    search_data_second=cursor.fetchone()
    #print(f"search_data_second is : {search_data_second}")
    if search_data_second!=None and ("'" not in first_fozy_search):
        search_data_str=str(search_data_second).split("'")
        search_data=str(search_data_str[1])
    else:
        search_data="No_data"
    video_user = 'videosoft'
    video_password = 'videosoft'
    #Waruna_Soechi=["BroCombo","Defiance","Infinity","TenderHarmony","AMETHYST"]
    #print("GOT!!!!!!!!!!!!!!!!!!!")
    global view_dect
    
    global data_path
    oh=data_path+"\\"+"Ship_path.html"
    global start_date
    global end_date
    global name
    global PORT
    ya_crew_list=[]
    global end_date_error_view
    vessel_track="/static/img/Coordinate.png"
    current_time=datetime.now
    ar1=[]
    points=[]
    points2=[]
    points3=[]
    new_name_list=[]
    new_gps_list=[]
    new_head_list=[]
    new_vilocity_list=[]
    new_update_time_list=[]
    new_video_list=[]
    name="Ship_name"
    con="SELECT "+name+" FROM dbo.Ku_All_result"
    cursor.execute(con)
    a=cursor.fetchall()
    ##print(a)
    #print(f"search data is :{search_data}")
    if search_data==None:
        search_data=request.values.get("test")
    fozy_search_msg="SELECT esn FROM dbo.ship_info where ship_name like '%"+search_data+"%'"
    
    cursor.execute(fozy_search_msg)
    ship_info_esn=cursor.fetchone()
    #print(f"the ship_info_esn is : {ship_info_esn}")
    if (ship_info_esn==None) and search_data not in cor_group:
        alert_window=1
        return render_template(
                'alert.html',
                title='alert',
               
                
            )
   
        
    elif ship_info_esn!=None and (search_data in cor_group):
        alert_window=0
        ##print(ship_info_esn)
        ship_info_esn=str(ship_info_esn)
        ship_info_esn2=ship_info_esn.split("'")
        ship_info_esn3=str(ship_info_esn2[1])#esn
        ##print(ship_info_esn3) 

        # 資料庫設定
        #db_settings = {
        #"host": "10.10.0.31",
        #"port": 3306,
        #"user": "hughes1",
        #"password": "Hughes@2020",
        #"db": "hughes-regional",
        #"charset": "utf8"
        #}

        db_settings = {
        "host": "10.0.0.224",
        "port": 3306,
        "user": "apuser",
        "password": "123456",
        "db": "hughes-regional",
        "charset": "utf8"
        }
        try:
            # 建立Connection物件
            conn2 = pymysql.connect(**db_settings)
        except Exception as ex:
            print(ex)
        esn_test=ship_info_esn3
        #print(esn_test)
        with conn2.cursor() as cursor2:
            command = "Select branch_id from ships_base where esn = "
            command2=command+str(esn_test)
            ##print(command2)
            cursor2.execute(command2)
            branch_id_test2=cursor2.fetchall()
            ##print(f" the branch id is : {branch_id_test2}")
            branch_id_test3=str(branch_id_test2).split("(")
            branch_id_test4=branch_id_test3[2]
            branch_id_test5=str(branch_id_test4).split(",")
            branch_id_test6=str(branch_id_test5[0]).strip()
            #print("=================================branch_id=================================")
            #print(f"the branch id is : {branch_id_test6}\n")  #final_branch_id
            #print("=================================captain===================================")
            command3_cap="Select user_id from rob_agency_branch where id="
            command4_cap=command3_cap+branch_id_test6
            cursor2.execute(command4_cap)
            cap_id=cursor2.fetchall()
            #print(cap_id)
            cap_id2=str(cap_id).split("(")
            cap_id3=str(cap_id2[2])
            cap_id4=cap_id3.split(",")
            cap_id5=str(cap_id4[0])
    
            command5_cap="Select name,id,end_date from rob_user_flow_package where user_id="
            command6_cap=command5_cap+cap_id5
            con_str_cap=" and end_date > CURDATE()"
            command7_cap=command6_cap+con_str_cap
            ##print(command7_cap)
            cursor2.execute(command7_cap)
            cap_pack_flow=cursor2.fetchall()
            #print(f"{cap_pack_flow}\n")
            if (len(cap_pack_flow)!=0):
                for i_cap in cap_pack_flow:
                    i_cap2=str(i_cap).split(",")
                    i_cap3=str(i_cap2[1]).strip()#search_id
                    i_cap4=str(i_cap2[0]).strip()
                    i_cap5=i_cap4.split("'")
                    i_cap6=str(i_cap5[1])
                    command8_cap="Select user_id,name,left_amount from rob_user_flow_detail where product_type = '1' and package_id = "
                    command9_cap=command8_cap+i_cap3
                    cursor2.execute(command9_cap)
                    final_cap_list=cursor2.fetchall()
                    for haha_cap in final_cap_list:
                        haha2_cap=str(haha_cap).split(",")
                        haha3_cap=str(haha2_cap[2])
                        haha4_cap=haha3_cap.split(")")
                        haha5_cap=str(haha4_cap[0])
                        haha5_cap=float(haha5_cap)
                        haha5_cap=round(haha5_cap,3)
                        haha5_cap=haha5_cap/1000
                        haha5_cap=format(haha5_cap,",")
                       
                        command10_cap="Select login_phone,name from rob_user_info where id = "
                        command11_cap=command10_cap+cap_id5
                        cursor2.execute(command11_cap)
                        cap_user_info=cursor2.fetchall()
                        ##print(cap_user_info)
                        for cap_info in cap_user_info:
                            cap_info=str(cap_info)
                            cap_info2=cap_info.split(",")
                            cap_info3=str(cap_info2[0])#account
                            cap_info4=str(cap_info2[1])#captain name
                            #print(f"the cap name is {cap_info4}")
                            cap_info3_x=cap_info3.split("'")
                            cap_info3_y=str(cap_info3_x[1])
                            ##print(cap_info3_y)#final_account
                            cap_info4_x=cap_info4.split("'")
                            cap_info4_y=str(cap_info4_x[1])
                            ##print(cap_info4_y)
              
                            if language=="TW":
                                cap_info4_y="Captain Name : "+cap_info4_y
                                #print(f"Captain Acount : {cap_info3_y}")
                                cap_info3_y="帳號名稱 : "+cap_info3_y
                                #print(f"The Captain Package : {i_cap6}")
                                i_cap6="套餐包 : "+i_cap6
                                #print(f"Captain Left Traffic : {haha5_cap}")
                                haha5_cap="剩餘流量(MB) : "+haha5_cap
                            else:
                                cap_info4_y="Captain Name : "+cap_info4_y
                                #print(f"Captain Acount : {cap_info3_y}")
                                cap_info3_y="Captain Account : "+cap_info3_y
                                #print(f"The Captain Package : {i_cap6}")
                                i_cap6="Package : "+i_cap6
                                #print(f"Captain Left Traffic : {haha5_cap}")
                                haha5_cap="Left(MB) : "+haha5_cap
            else:
                if language=="TW":
                    cap_info4_y="帳號名稱 : 無資料"
                    cap_info3_y="帳號名稱 : 無資料"
                    i_cap6="套餐包 : 無資料"
                    haha5_cap="剩餘流量(MB) : 無資料"
                else:
                    cap_info4_y="No data"
                    cap_info3_y="CAP Account : No data"
                    i_cap6="Package : No data"
                    haha5_cap="Left(MB) : No data"
                




            #print("===================================crew====================================")
            command3_crew="Select user_id from rob_agency_branch_user where branch_id="
            command4_crew=command3_crew+branch_id_test6
            cursor2.execute(command4_crew)
            crew_id=cursor2.fetchall()
            ##print(crew_id)
            for i_crew in crew_id:
                ##print(i)
                crew_id2=str(i_crew).split("(")
                crew_id3=str(crew_id2[1])
                crew_id4=crew_id3.split(",")
                crew_id5=str(crew_id4[0])
                ##print(crew_id5)
                command5_crew="Select name,id,end_date from rob_user_flow_package where user_id="
                command6_crew=command5_crew+crew_id5
                con_str_crew=" and end_date > CURDATE()"
                command7_crew=command6_crew+con_str_crew
                ##print(command7_crew)
                cursor2.execute(command7_crew)
                crew_pack_flow=cursor2.fetchall()
                #print(f"{crew_pack_flow}\n")
                if (len(crew_pack_flow)!=0):
                    for j_crew in crew_pack_flow:
                        j2_crew=str(j_crew).split(",")
                        j3_crew=str(j2_crew[1])
                        j4_crew=str(j2_crew[0])
                        j5_crew=j4_crew.split("'")
                        j6_crew=str(j5_crew[1])
                        command8_crew="Select user_id,name,left_amount from rob_user_flow_detail where product_type = '1' and package_id = "
                        command9_crew=command8_crew+j3_crew
                        cursor2.execute(command9_crew)
                        final_crew_list=cursor2.fetchall()
                        #print(final_crew_list)
                        for haha_crew in final_crew_list:
                            haha2_crew=str(haha_crew).split(",")
                            haha3_crew=str(haha2_crew[2])
                            haha4_crew=haha3_crew.split(")")
                            haha5_crew=str(haha4_crew[0])
                            haha5_crew=float(haha5_crew)
                            haha5_crew=round(haha5_crew,3)
                            haha5_crew=haha5_crew/1000
                            haha5_crew=format(haha5_crew,",")
                            
                            command10_crew="Select login_phone,name from rob_user_info where id = "
                            command11_crew=command10_crew+crew_id5
                            cursor2.execute(command11_crew)
                            crew_user_info=cursor2.fetchall()
                            ##print(crew_user_info)
                            for crew_info in crew_user_info:
                                crew_info=str(crew_info)
                                crew_info2=crew_info.split(",")
                                crew_info3=str(crew_info2[0])#account
                                crew_info4=str(crew_info2[1])#crewtain name
                                crew_info3_x=crew_info3.split("'")
                                crew_info3_y=str(crew_info3_x[1])
                                ##print(crew_info3_y)#final_account
                                crew_info4_x=crew_info4.split("'")
                                crew_info4_y=str(crew_info4_x[1])
                                ##print(crew_info4_y)
                                #print(f"the crew id is : {crew_id5}")
                                #print(f"the search id is {j3_crew}\n")
                                ##print(f"crew name is : {crew_info4_y}")
                                #print(f"crew acount is : {crew_info3_y}")
                                #print(f"the crew package is : {j6_crew}")
                                #print(f"crew left traffic is : {haha5_crew}")
                                #ya_crew_list.append("Crew Name : "+crew_info4_y)
                                if language=="TW":
                                    ya_crew_list.append("帳號名稱 : "+crew_info3_y)
                                    ya_crew_list.append("套餐包 : "+j6_crew)
                                    ya_crew_list.append("剩餘流量(MB) : "+haha5_crew)
                                else:
                                    ya_crew_list.append("Crew Account : "+crew_info3_y)
                                    ya_crew_list.append("Package : "+j6_crew)
                                    ya_crew_list.append("Left(MB) : "+haha5_crew)
                                #print("==================================================================")

                else:
                    if language=="TW":
                        ya_crew_list.append("帳號名稱 : 無資料")
                        ya_crew_list.append("套餐包 : 無資料")
                        ya_crew_list.append("剩餘流量(MB) : 無資料")
                    else:
                        ya_crew_list.append("Crew Account : No Data")
                        ya_crew_list.append("Package : No Data ")
                        ya_crew_list.append("Left(MB) : No Data")




        ya_crew_list2=list(split_list(ya_crew_list,4))



        cap_traffic_data="tenderxxunlimited - unlimited-512-1"
        cap_remain="400 MB"
        crew_traffic_data="tenderxx2gb - 2GB Month"
        crew_remain="36 MB"
        #print(f"{search_data}")
        Ku_fozy="SELECT Ship_name,esn FROM dbo.Ku_All_result where Ship_name like '%"
        Ku_fozy2=Ku_fozy+search_data+"%'"
        cursor.execute(Ku_fozy2)
        name_esn_data=cursor.fetchall()
        #print(f"the vessel name and esn is : {name_esn_data}")

        Ku_fozy3="SELECT Ship_name,GPS_lat,GPS_lon,Head_angle,Vilocity,Time_now FROM dbo.Predict_system where Ship_name like '%"+search_data+"%'"
        cursor.execute(Ku_fozy3)
        full_data=cursor.fetchall()
        #print(full_data)
        # [('OceanVenture-VI', 39.778611, 148.974444, 230.25, 21.74, datetime.datetime(2021, 11, 19, 1, 29))]
            
        full_data2=str(full_data)
        if full_data2!="[]":
            full_data3=full_data2.split(",")
            
            #----------------------------------------------------------------------------------------
            full_data_name=full_data3[0]
            #print(full_data_name)
            full_data_name2=str(full_data_name)
            full_data_name3=full_data_name2.split("'")
            full_data_name4=full_data_name3[1]
            full_data_name5=str(full_data_name4).strip()
            #print(full_data_name5)
        
            #----------------------------------------------------------------------------------------
            full_data_lat=full_data3[1]
            full_data_lat2=str(full_data_lat)
            full_data_lon=full_data3[2]
            full_data_lon2=str(full_data_lon)
            full_data_position=full_data_lat2+","+full_data_lon2
            full_data_position=full_data_position.strip()
            #print(full_data_position)
      
            #----------------------------------------------------------------------------------------
            full_data_head=full_data3[3]
            full_data_head2=str(full_data_head).strip()
            #print(full_data_head2)
      
            #----------------------------------------------------------------------------------------
            full_data_vilocity=full_data3[4]
            full_data_vilocity2=str(full_data_vilocity).strip()
            #print(full_data_vilocity2)
     
            #----------------------------------------------------------------------------------------
            full_data_year=full_data3[5]
            full_data_year2=str(full_data_year)
            full_data_year3=full_data_year2.split("(")
            full_data_year4=full_data_year3[1]
            full_data_year5=str(full_data_year4).strip()
            ##print(full_data_year5)
            #----------------------------------------------------------------------------------------
            full_data_month=full_data3[6]
            full_data_month2=str(full_data_month).strip()
            ##print(full_data_month2)
            #----------------------------------------------------------------------------------------
            full_data_day=full_data3[7]
            full_data_day2=str(full_data_day).strip()
            ##print(full_data_day2)
            #----------------------------------------------------------------------------------------
            full_data_hour=full_data3[8]
            full_data_hour2=str(full_data_hour).strip()
            ##print(full_data_hour2)
            #----------------------------------------------------------------------------------------
            full_data_min=full_data3[9]
            full_data_min2=str(full_data_min)
            full_data_min3=full_data_min2.split(")")
            full_data_min4=full_data_min3[0]
            full_data_min5=str(full_data_min4).strip()
            ##print(full_data_min5)
            #----------------------------------------------------------------------------------------
            fully_date=full_data_year5+"-"+full_data_month2+"-"+full_data_day2+" "+full_data_hour2+":"+full_data_min5
            ##print(fully_date)
 
        cursor.execute("SELECT Time_now FROM dbo.Predict_system where Ship_name=?",search_data)
        predict_system_time=cursor.fetchall()
        if predict_system_time!=[]:
            for i in predict_system_time:
                print(f"predict_system_time={i[0]}")
                fully_date=i[0]

        for i in a:
            i2=str(i)
            i3=i2.split("'")
            i4=i3[1]
            i5=str(i4)
            ##print(i5)
            ar1.append(i5) #total_ship_name
    
    
        if request.method=="GET":

            #print(search_data)
            start_date=request.values.get("get_date")
            end_date=request.values.get("get_date1")
            #online_1="30%"
            end_date_error_view=end_date
            
            cursor.execute("SELECT TOP 150 time FROM dbo.Ku_All_result_history where Ship_name=? order by time desc",search_data)
            test_data=cursor.fetchall()
            for i in test_data:
                ##print(i)
                db_catch_time_array.append(i)

            #print(db_catch_time_array)
            new_db_catch_time=db_catch_time_array[0]
            old_db_catch_time=db_catch_time_array[(len(db_catch_time_array)-1)]
            #print(old_db_catch_time)
            ####################################################################################################################
            new_db_catch_time=str(new_db_catch_time).split("(")
            new_db_catch_time=new_db_catch_time[2].split(")")
            new_db_catch_time=str(new_db_catch_time[0])
            new_db_catch_time=new_db_catch_time.split(",")
            new_db_catch_year=str(new_db_catch_time[0]).strip()
            new_db_catch_mon=str(new_db_catch_time[1]).strip()
            new_db_catch_day=str(new_db_catch_time[2]).strip()

            new_db_catch_time=new_db_catch_year+"-"+new_db_catch_mon+"-"+new_db_catch_day+" 23:59:59"
            datetime_new_db_catch_time=datetime.strptime(new_db_catch_time, "%Y-%m-%d %H:%M:%S")
            ####################################################################################################################
            old_db_catch_time=str(old_db_catch_time).split("(")
            old_db_catch_time=old_db_catch_time[2].split(")")
            old_db_catch_time=str(old_db_catch_time[0])
            old_db_catch_time=old_db_catch_time.split(",")
            old_db_catch_year=str(old_db_catch_time[0]).strip()
            old_db_catch_mon=str(old_db_catch_time[1]).strip()
            old_db_catch_day=str(old_db_catch_time[2]).strip()

            old_db_catch_time=old_db_catch_year+"-"+old_db_catch_mon+"-"+old_db_catch_day+" 00:00:00"
            datetime_old_db_catch_time=datetime.strptime(old_db_catch_time, "%Y-%m-%d %H:%M:%S")

            #print(f"new data is : {datetime_new_db_catch_time} , old data is : {datetime_old_db_catch_time}")
            #name=request.values.get("get_ship_name")
            name=search_data
            if (start_date!=None) and (start_date!="") and (end_date!=None) and (end_date!=""):
                #print("#######################################################################################")
                if end_date!=None:
                    start_date=start_date+" "+"00:00:00"
                    end_date=end_date+" "+"23:59:59"
                else:
                    end_date=""
                online_1=online_ratio(name,start_date,end_date)
                #print(f"date_start={start_date},date_end={end_date},select_name={name}")
                cursor.execute("SELECT Ship_name,gps_lat,gps_lon FROM dbo.Ku_All_result_history where ship_name=? AND time BETWEEN ? AND ? ORDER BY time DESC",name,start_date,end_date)
                select_ship_data=cursor.fetchall()
                file_name=str(name)+".txt"
                path_file=open(file_name,"w")
                for i in select_ship_data:
                    con_gps=str(i[1]).strip()+","+str(i[2]).strip()
                    path_file.write(con_gps+"\n")
                if (name!=None) and (name!='') and (name!="Ship_name"):
                    #print(name)
                    cursor.execute("SELECT Ship_name,GPS_lat,GPS_lon,Head_angle,Vilocity,Time_now FROM dbo.Predict_system where Ship_name=?",name)
                    table_beta=cursor.fetchall()
                    table_beta2=str(table_beta)
                    table_beta3=table_beta2.split("(")
                    table_beta4=table_beta3[1]
                    table_beta_time=table_beta3[2]
                    ##print(i_time)
                    table_beta_time2=str(table_beta_time).split(")")
                    table_beta_time3=table_beta_time2[0]
                    ##print(i_time3)
                    table_beta4=str(table_beta4)
                    table_beta5=table_beta4.split(",")
                    ship_name_db=str(table_beta5[0])
                    ship_name_split=ship_name_db.split("'")
                    real_ship_name=str(ship_name_split[1]).strip()
                    LAT=float(str(table_beta5[1]).strip())
                    LON=float(str(table_beta5[2]).strip())
                    #add_position=LAT+","+LON
                    head=float(str(table_beta5[3]).strip())
                    vilocity=float(str(table_beta5[4]).strip())
                    last_time=table_beta_time3
                    #print(LAT)
                    #print(LON)
                    #print(head)
                    #print(vilocity)
                    #print(last_time)
            

            
                else:
                    LAT=0
                    LON=0
                    #add_position=LAT+","+LON
                    head=0
                    vilocity=0
                    last_time="0"
      
                path_file.close()
                path_file_read=open(file_name,"r")
                path_file_read2=path_file_read.readline().strip()
                while path_file_read2:
                    points.append(path_file_read2)
                    path_file_read2=path_file_read.readline().strip()
                path_file_read.close()

                for i in points:
                    if "G" not in i:
                        ##print(i)
                        i2=str(i).split(",")
                        i3_lat=i2[0]
                        i3_lon=i2[1]
                        if float(i3_lon)>=-180 and float(i3_lon)<0:
                            i3_lon=float(i3_lon)+360.0
                        if float(i3_lat)!=0.0 and float(i3_lon)!=0.0:
                            points2.append(float(i3_lat))
                            points2.append(float(i3_lon))



                 
                points3=list(split_list(points2,2))
                ##print(points3)
                #print("\n")
            

                


            
                if name!=None:
                    cursor.execute("SELECT TOP 1 gps_lat,gps_lon,CCTV_Active FROM dbo.Ku_All_result_history where Ship_name=? and gps_lat!='0' and time>=? and time<=? order by time desc",name,start_date,end_date)
                    the_ship_last_position=cursor.fetchall()
                    ##print(f"the ship last position is : {the_ship_last_position}")
                    if the_ship_last_position!=[]:
                        final_position_not_split=str(the_ship_last_position).split("'")
                        final_position_lat=str(final_position_not_split[1]).strip()
                        final_position_lon=str(final_position_not_split[3]).strip()
                        new_cctv=str(final_position_not_split[5]).strip()
                        final_lat_lon=[float(final_position_lat),float(final_position_lon)]
                        #print(final_lat_lon)
                        gps_time_array=[]
                        got_you_array=[] #Ku-Online
                        got_you_array2=[] #Ku-offline
                        cursor.execute("SELECT gps_lat,gps_lon,time FROM dbo.Ku_All_result_history where Ship_name=? and gps_lat!='0' and time>=? and time<=? order by time desc",name,start_date,end_date)
                        get_db_data=cursor.fetchall()
                        for i in get_db_data:
                            ##print(i)
                            gps_time_array.append(i[0])
                            gps_time_array.append(i[1])
                            gps_time_array.append(i[2])
                        ##print(gps_time_array)
                        for x in range(2,len(gps_time_array)-1,3):
                            time_delta=gps_time_array[x]-gps_time_array[x+3]
                            time_delta_sec=time_delta.seconds
                            if time_delta_sec<=1080:
                                lat_alpha=str(gps_time_array[x-2]).strip()
                                lon_alpha=str(gps_time_array[x-1]).strip()
                                alpha_pos=lat_alpha+","+lon_alpha
                                lat_beta=str(gps_time_array[x+1]).strip()
                                lon_beta=str(gps_time_array[x+2]).strip()
                                beta_pos=lat_beta+","+lon_beta
                                got_you_array.append(float(lat_alpha))
                                got_you_array.append(float(lon_alpha))
                                got_you_array.append(float(lat_beta))
                                got_you_array.append(float(lon_beta))
                            else:
                                lat_alpha=str(gps_time_array[x-2]).strip()
                                lon_alpha=str(gps_time_array[x-1]).strip()
                                alpha_pos=lat_alpha+","+lon_alpha
                                lat_beta=str(gps_time_array[x+1]).strip()
                                lon_beta=str(gps_time_array[x+2]).strip()
                                beta_pos=lat_beta+","+lon_beta
                                got_you_array2.append(float(lat_alpha))
                                got_you_array2.append(float(lon_alpha))
                                got_you_array2.append(float(lat_beta))
                                got_you_array2.append(float(lon_beta))

                        got_you_array_new_list=list(split_list(got_you_array,2))
                        got_you_array_new_list=list(split_list(got_you_array_new_list,2))
                        got_you_array_new_list2=list(split_list(got_you_array2,2))
                        got_you_array_new_list2=list(split_list(got_you_array_new_list2,2))

                        yoyo_points=got_you_array_new_list
                        yoyo_points2=got_you_array_new_list2

                        output_map(name,yoyo_points,yoyo_points2,head,vilocity,last_time,LAT,LON,new_cctv,final_lat_lon,"path2",language)
        
                    else:
                        return render_template(
                        'NoData.html',
                        title='NoData',
                        )

                #if name!=None:
                #    con_name=str(name)+".html"
                #    return render_template(
                #        con_name,
                #        title='Path',
                #        year=datetime.now().year,
                #        Ship_name=ar1
                #    )
                #read_port=open("PORT.txt","r")
                #read_real_port=read_port.readline().strip()
                ##print(read_real_port)
                #read_port.close()
                #if name!=None:
                #    con_name2="http://localhost:"+str(read_real_port)+"/Path?get_ship_name="+str(name)
                #    #print(con_name2)
                #else:
                #    con_name2=""

                #new_name_list=[]
                #new_gps_list=[]
                #new_head_list=[]
                #new_vilocity_list=[]
                #new_update_time_list=[]
       
                #mylist = zip(new_name_list, new_gps_list,new_head_list,new_vilocity_list,new_update_time_list)
                #context = {
                #            'mylist': mylist,
                #        }
                ##print("--------")
                ##print(rock_name)
                
                #print(new_video)
                map_path_yoyo="/static/Fleet/Ship_path.html"
                return render_template(
                    'Search.html',
                    title='Search',
                    year=datetime.now().year,
                    Ship_name=new_name_list,
                    gps=full_data_position,
                    head_angle=full_data_head2,
                    vilocity_back=full_data_vilocity2,
                    go_update_time=fully_date,
                    tmp_date=first_fozy_search,
                    select_name=name,
                    date1=start_date,
                    date2=end_date,
                    date3=end_date_error_view,
                    search_data2=search_data,
                    cap=cap_traffic_data,
                    cap_rem=cap_remain,
                    crew=crew_traffic_data,
                    crew_rem=crew_remain,
                    
                    vsg=vessel_group2,
                    captain_name=cap_info4_y,
                    captain_account=cap_info3_y,
                    captain_package=i_cap6,
                    captain_left=haha5_cap,
                    vessel_track_img=vessel_track,
                    total_crew_list=ya_crew_list2,
                    alert_msg=alert_window,
                    online_ratio=online_1,
                    map_path_yoyo=map_path_yoyo,
                    LANGUAGE=language
                    #rock_gps=rock_gps,
                    #rock_head=rock_head,
                    #rock_vilocity=rock_vilocity,
                    #rock_time=rock_time,
                    #mylist = zip(new_name_list, new_gps_list,new_head_list,new_vilocity_list,new_update_time_list)
                )
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                cursor.execute("SELECT Vilocity FROM dbo.Predict_system where Ship_name=?",name)
                predict_system_data=cursor.fetchall()
                full_gps_array=[]
                for i in predict_system_data:
                
                    vilocity=i[0]
                
                cursor.execute("SELECT lat,lon,heading,final_time from dbo.KU_SE_GPS WHERE ship_name=?",name)
                search_get_ku_se_data=cursor.fetchall()
                for i in search_get_ku_se_data:
                    gps_lat=i[0]
                    gps_lon=i[1]
                    head_angle=i[2]
                    time_now=i[3]
                total_gps=str(gps_lat)+","+str(gps_lon)
                full_gps_array.append(gps_lat)
                full_gps_array.append(gps_lon)
                output_map_single(name,head_angle,vilocity,fully_date,gps_lat,gps_lon,full_gps_array,language)
            
                map_path_yoyo="/static/Fleet/Ship_path.html"
                return render_template(
                    'Search.html',
                    title='Search',
                    year=datetime.now().year,
              
                    gps=total_gps,
                    head_angle=head_angle,
                    vilocity_back=vilocity,
                    go_update_time=fully_date,
                    select_name=name,
                    date1=time_now,
                    date2=time_now,
                
                    search_data2=search_data,
                    cap=cap_traffic_data,
                    cap_rem=cap_remain,
                    crew=crew_traffic_data,
                    crew_rem=crew_remain,
                    #video=new_video,
                    vsg=vessel_group2,
                    captain_name=cap_info4_y,
                    captain_account=cap_info3_y,
                    captain_package=i_cap6,
                    captain_left=haha5_cap,
                    vessel_track_img=vessel_track,
                    total_crew_list=ya_crew_list2,
                    map_path_yoyo=map_path_yoyo,
                    LANGUAGE=language
                    #online_ratio=online_1
                    #rock_gps=rock_gps,
                    #rock_head=rock_head,
                    #rock_vilocity=rock_vilocity,
                    #rock_time=rock_time,
                    #mylist = zip(new_name_list, new_gps_list,new_head_list,new_vilocity_list,new_update_time_list)
                )

    
    else:
        alert_window=1
        return render_template(
                'alert.html',
                title='alert',
               
                
            )
@app.route('/CCTV/<vessel_name>/<lan>',methods=["GET","POST"])
def CCTV(vessel_name,lan):
    switch_url_array=[]
    button_name_array=[]
    language=lan
    server = 'vesselstatusdb.database.windows.net' 
    database = 'VesselStatusDB' 
    username = 'lunghwa' 
    password = 'LHE@debug' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    vessel_id=vessel_name
    #sql_command="SELECT switch_url from dbo.Portal_cam_data where ship_name="
    cursor.execute("SELECT switch_url,cam_count from dbo.Portal_cam_data where ship_name=?",str(vessel_id))
    ##print(vessel_id)
    switch_url=cursor.fetchall()
    #print(f"switch_url={switch_url}")
    switch_url2=str(switch_url).split("'")
    switch_final_url=str(switch_url2[1])
    #print(f"switch_url={switch_final_url}")
    cam_count=str(switch_url2[2])
    cam_count2=cam_count.split(",")
    cam_count3=str(cam_count2[1]).strip()
    cam_count4=cam_count3.split(")")
    cam_count_final=str(cam_count4[0])
    ##print(f"cam_count={cam_count_final}")
    switch_final_url2=switch_final_url[:len(switch_final_url)-1]
    ##print(switch_final_url2)
    for i in range(1,int(cam_count_final)+1,1):
        switch_final_url3=switch_final_url2+str(i)
        switch_url_array.append(switch_final_url3)
        if language=="TW":
            button_name="鏡頭"+str(i)
        else:
            button_name="CAM"+str(i)
        button_name_array.append(button_name)
    #print(switch_url_array)

    url_and_btn_array=zip(button_name_array,switch_url_array) 

        
    
    
    #http://videosoft:videosoft@surveillance.lhsatellite.com:8080/video.mjpg?machineid=BroCombo&streamid=1
    vessel_cam_url="http://videosoft:videosoft@surveillance.lhsatellite.com:8080/video.mjpg?machineid="+str(vessel_id)+"&streamid=1"
    vessel_cam_url2="http://surveillance.lhsatellite.com:8080/video.mjpg?machineid="+str(vessel_id)+"&streamid=1"
    return render_template(
    'CCTV.html',
    test_url="http://vesselstatus.eastasia.cloudapp.azure.com/Ku_All_result.aspx",
    ship_name=vessel_id,
    url=vessel_cam_url,
    iframe_url=vessel_cam_url2,
    total_array=url_and_btn_array,
    switch_array=switch_url_array,
    
    )
@app.route('/Path/Map/<vessel_group>',methods=["GET","POST"])
def Map(vessel_group):
    global name
    global view_dect
    global start_date
    global end_date
    global end_date_error_view
    map_path="/Fleet/"+vessel_group+".html"
    #con_data=str(name)+".html"
    #print(name)
    #print(start_date)
    #print(end_date_error_view)
    if ((name!=None) and (name!="Ship_name") and (start_date!=None) and (start_date!="") and (end_date_error_view!=None) and (end_date_error_view!="")):  
        return render_template(
            'Ship_path.html',
            current_time=datetime.now
        )
    elif name==None:
        return render_template(
            'Ship_path.html'
            )
    elif name=="Ship_name":
        return render_template(
            'Ship_path.html'
            )
    else:
        return render_template(
            'Ship_path.html'
            )

@app.route('/Path/new_Map',methods=["GET","POST"])
def new_Map():
    global name
    global view_dect
    global start_date
    global end_date
    global end_date_error_view
    #con_data=str(name)+".html"
    #print(name)
    #print(start_date)
    #print(end_date_error_view)
    if ((name!="Ship_name") and (start_date==None) and (end_date_error_view==None)):  
        return render_template(
            'Ship_path.html',
            current_time=datetime.now
        )
    
    else:
        return render_template(
            'Ship_path.html'
            )


@app.route('/Path/Map2',methods=["GET","POST"])
def Map2():
    return render_template(
        'MAP.html'
        )
    
    
