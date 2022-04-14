#import ee
from folium import IFrame
import folium
from folium import plugins
import pyodbc
import os
from datetime import datetime
import requests
import urllib.request as req
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import time
video_user = 'videosoft'
video_password = 'videosoft'
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

Waruna=["Amethyst","Infinity","TenderHarmony","BroCombo","GarudaAsia"]
Soechi=["Immanuel","SC_ChampionXLV"]
LungSoon=["LungSoonFa-1","LungYuin","OceanVenture-II","OceanVenture-VI","PacificJourney-8","PacificPursuit-107","PacificPursuit-777","PacificJourney-101"]
FongKuo=["FongKuo-866"]
TsVessel=["Hochiminh","Ningbo","NanSha"]
EVERSHINING=["EverShining"]
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
map_path=open("path.txt","r")
read_path=map_path.readline().strip()
map_path.close()
def output_map_always(ship_name_list,points_list,head_list,vilocity_list,last_time_list,video_list,fleet_name):
    
    ##print(ship_name)
    ##print(head)
    #points=[[42.736389, 157.381389], [42.741667, 157.379722], [42.768611, 157.388333], [42.8275, 157.408056], [42.8725, 157.405556], [42.911667, 157.398889], [42.91, 157.396944], [42.909167, 157.395833], [42.907778, 157.393611], [42.905278, 157.391111], [42.904722, 157.389722], [42.902778, 157.3875], [42.900556, 157.385278], [42.899167, 157.383611], [42.896944, 157.381111], [42.895833, 157.379722], [42.893333, 157.376389], [42.891667, 157.374167], [42.889167, 157.371111], [42.885833, 157.367778], [42.883611, 157.365556], [42.880833, 157.362222], [42.878333, 157.359167], [42.876944, 157.3575], [42.873056, 157.353333], [42.870556, 157.350833], [42.866944, 157.348611], [42.864444, 157.346667], [42.860556, 157.343889], [42.858056, 157.342222], [42.853889, 157.338889], [42.851389, 157.336944], [42.847222, 157.335556], [42.844167, 157.334444], [42.841667, 157.333333], [42.838056, 157.332222], [42.835833, 157.331944], [42.832778, 157.331667], [42.830556, 157.331111], [42.828333, 157.331111], [42.826111, 157.328611], [42.825, 157.356111], [42.826389, 157.356944], [42.828333, 157.356667], [42.83, 157.358889], [42.831944, 157.357778], [42.835833, 157.360556], [42.837222, 157.362222], [42.91, 157.3025], [42.973889, 157.246667]]    

    folium.Map.add_ee_layer = add_ee_layer
    #points = [[23, 121],[23.3, 121.5],[23.5, 121.796666]]
    my_map = folium.Map(location=points_list[0], tiles=None,width='100%', height='100%',zoom_start=6,world_copy_jump=True)   
    #my_map = folium.Map(basemap=basemaps.NASAGIBS.ViirsTrueColorCR, center=points[0], zoom=6, tiles=None,width='100%', height='100%',zoom_start=6)   
    vis_params = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
        }
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    basemaps['Google Maps'].add_to(my_map)
    

    my_map.add_child(folium.LayerControl())
    for i,name2,head2,vilocity2,last_time2,video2 in zip(points_list,ship_name_list,head_list,vilocity_list,last_time_list,video_list):
        if video2=="True":
            angle_con="img/"+str(int(head2))+".png"
        else:
            angle_con="img2/"+str(int(head2))+".png"
        
        #angle_con="flask_test/templates/img/"+str(int(head2))+".png"
        myIcon = folium.CustomIcon(angle_con,icon_size = (60, 60),icon_anchor = (15, 30)) 
        ##print(i)
        #print(last_time2)
        #time_spl=str(last_time2).split(",")
        #year=time_spl[0]
        #mon=time_spl[1]
        #day=time_spl[2]
        #hour=time_spl[3]
        #min=time_spl[4]
        #final_updateTime=str(year)+"-"+str(mon)+"-"+str(day)+" "+str(hour)+":"+str(min)
        final_updateTime=last_time2
        name_and_angle="<hr style='width: 100%; height: 10px; border: none; background-color: #004B97'><font size=\"6\">"+"Ship: "+name2+"</font><br>"+"<hr //>"+"<font size=\"4\">"+"Head angle: "+str(head2)+"<br>"+"Position: ("+str(i[0])+","+str(i[1])+")"+"<br>"+"Velocity: "+str(vilocity2)+"<br>"+"</font><hr //>"+"<font size=\"5\">"+"Last_Update: "+str(final_updateTime)+"</font><br><br>"
        # Add custom basemaps
        #name_and_angle="<table border='1'><tr><td>Vessel</td><td>Head angle</td><td>GPS</td><td>Vilocity</td><td>Last Update</td></tr>"+"<tr><td>"+name2+"</td>"+"<td>"+str(head2)+"</td>"+"<td>"+str(points[0])+"</td>"+"<td>"+str(vilocity2)+"</td>"+"<td>"+str(last_time2)+"</td></tr></table>"
        iframe_andy="""
        <!DOCTYPE html>
        <html>
        <head>
        """
        iframe_andy2="""
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link type="text/css" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
        <script src="http://192.168.0.201:8080/Ship_map_dashboard/Ship_map_dashboard/jquery.min.js"></script>
        </head>
        <body>  
        </body>
        </html>
        """
        iframe_andy3=iframe_andy+name_and_angle+iframe_andy2
        iframe_andy3=folium.Html(iframe_andy3,script=True)
        iframe = IFrame(html=iframe_andy3, width=400, height=220)
        popup = folium.Popup(iframe, max_width=400)
        # Add the elevation model to the map object.
        #my_map.add_ee_layer(dem.updateMask(dem.gt(0)), vis_params, 'DEM')

        # Add a layer control panel to the map.
        #my_map.add_child(folium.Polygon(locations=[i], weight=10,color="white",popup=name_and_angle)) #i_v2=direction
        
        folium.Marker(location=i,popup=popup,icon = myIcon).add_to(my_map)
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
        #folium.GeoJson('vo_SWP(45)_DNW3_EIRP.json', name="geojson").add_to(my_map)
        #my_map.add_child(folium.GeoJson('vo_SWP(45)_DNW3_EIRP.json', name='geojson'))
        #my_map.add_child(child=m3)
        # Add fullscreen button
                    
        #my_map.add_child(folium.PolyLine(locations=points, weight=3)) 
        #file_name0=str(ship_name)+".html"
    plugins.Fullscreen().add_to(my_map)
    file_name0=fleet_name+".html"
    new_path=read_path+"\\\\"+file_name0
    my_map.save(new_path)

def output_map_always_tw(ship_name_list,points_list,head_list,vilocity_list,last_time_list,video_list,fleet_name):
    
    ##print(ship_name)
    ##print(head)
    #points=[[42.736389, 157.381389], [42.741667, 157.379722], [42.768611, 157.388333], [42.8275, 157.408056], [42.8725, 157.405556], [42.911667, 157.398889], [42.91, 157.396944], [42.909167, 157.395833], [42.907778, 157.393611], [42.905278, 157.391111], [42.904722, 157.389722], [42.902778, 157.3875], [42.900556, 157.385278], [42.899167, 157.383611], [42.896944, 157.381111], [42.895833, 157.379722], [42.893333, 157.376389], [42.891667, 157.374167], [42.889167, 157.371111], [42.885833, 157.367778], [42.883611, 157.365556], [42.880833, 157.362222], [42.878333, 157.359167], [42.876944, 157.3575], [42.873056, 157.353333], [42.870556, 157.350833], [42.866944, 157.348611], [42.864444, 157.346667], [42.860556, 157.343889], [42.858056, 157.342222], [42.853889, 157.338889], [42.851389, 157.336944], [42.847222, 157.335556], [42.844167, 157.334444], [42.841667, 157.333333], [42.838056, 157.332222], [42.835833, 157.331944], [42.832778, 157.331667], [42.830556, 157.331111], [42.828333, 157.331111], [42.826111, 157.328611], [42.825, 157.356111], [42.826389, 157.356944], [42.828333, 157.356667], [42.83, 157.358889], [42.831944, 157.357778], [42.835833, 157.360556], [42.837222, 157.362222], [42.91, 157.3025], [42.973889, 157.246667]]    

    folium.Map.add_ee_layer = add_ee_layer
    #points = [[23, 121],[23.3, 121.5],[23.5, 121.796666]]
    my_map = folium.Map(location=points_list[0], tiles=None,width='100%', height='100%',zoom_start=6,world_copy_jump=True)   
    #my_map = folium.Map(basemap=basemaps.NASAGIBS.ViirsTrueColorCR, center=points[0], zoom=6, tiles=None,width='100%', height='100%',zoom_start=6)   
    vis_params = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
        }
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    basemaps['Google Maps'].add_to(my_map)
    

    my_map.add_child(folium.LayerControl())
    for i,name2,head2,vilocity2,last_time2,video2 in zip(points_list,ship_name_list,head_list,vilocity_list,last_time_list,video_list):
        if video2=="True":
            angle_con="img/"+str(int(head2))+".png"
        else:
            angle_con="img2/"+str(int(head2))+".png"
        
        #angle_con="flask_test/templates/img/"+str(int(head2))+".png"
        myIcon = folium.CustomIcon(angle_con,icon_size = (60, 60),icon_anchor = (15, 30)) 
        ##print(i)
        #print(last_time2)
        #time_spl=str(last_time2).split(",")
        #year=time_spl[0]
        #mon=time_spl[1]
        #day=time_spl[2]
        #hour=time_spl[3]
        #min=time_spl[4]
        #final_updateTime=str(year)+"-"+str(mon)+"-"+str(day)+" "+str(hour)+":"+str(min)
        final_updateTime=last_time2
        name_and_angle="<hr style='width: 100%; height: 10px; border: none; background-color: #004B97'><font size=\"6\">"+"船名: "+name2+"</font><br>"+"<hr //>"+"<font size=\"4\">"+"航向角: "+str(head2)+"<br>"+"座標: ("+str(i[0])+","+str(i[1])+")"+"<br>"+"速度: "+str(vilocity2)+"<br>"+"</font><hr //>"+"<font size=\"5\">"+"最後更新時間: "+str(final_updateTime)+"</font><br><br>"
        # Add custom basemaps
        #name_and_angle="<table border='1'><tr><td>Vessel</td><td>Head angle</td><td>GPS</td><td>Vilocity</td><td>Last Update</td></tr>"+"<tr><td>"+name2+"</td>"+"<td>"+str(head2)+"</td>"+"<td>"+str(points[0])+"</td>"+"<td>"+str(vilocity2)+"</td>"+"<td>"+str(last_time2)+"</td></tr></table>"
        iframe_andy="""
        <!DOCTYPE html>
        <html>
        <head>
        """
        iframe_andy2="""
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link type="text/css" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
        <script src="http://192.168.0.201:8080/Ship_map_dashboard/Ship_map_dashboard/jquery.min.js"></script>
        </head>
        <body>  
        </body>
        </html>
        """
        iframe_andy3=iframe_andy+name_and_angle+iframe_andy2
        iframe_andy3=folium.Html(iframe_andy3,script=True)
        iframe = IFrame(html=iframe_andy3, width=400, height=220)
        popup = folium.Popup(iframe, max_width=400)
        # Add the elevation model to the map object.
        #my_map.add_ee_layer(dem.updateMask(dem.gt(0)), vis_params, 'DEM')

        # Add a layer control panel to the map.
        #my_map.add_child(folium.Polygon(locations=[i], weight=10,color="white",popup=name_and_angle)) #i_v2=direction
        
        folium.Marker(location=i,popup=popup,icon = myIcon).add_to(my_map)
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
        #folium.GeoJson('vo_SWP(45)_DNW3_EIRP.json', name="geojson").add_to(my_map)
        #my_map.add_child(folium.GeoJson('vo_SWP(45)_DNW3_EIRP.json', name='geojson'))
        #my_map.add_child(child=m3)
        # Add fullscreen button
                    
        #my_map.add_child(folium.PolyLine(locations=points, weight=3)) 
        #file_name0=str(ship_name)+".html"
    plugins.Fullscreen().add_to(my_map)
    file_name0=fleet_name+"_TW.html"
    new_path=read_path+"\\\\"+file_name0
    my_map.save(new_path)
cctv_url="http://surveillance.lhsatellite.com:8080/status"
def get_cctv_status(ship_name):
    global cctv_url
    login_cctv=requests.get(cctv_url,timeout=(15,20),auth=HTTPBasicAuth(video_user, video_password))
    if (login_cctv.status_code == requests.codes.ok): 
        video_soup=BeautifulSoup(login_cctv.text,"html.parser")
        find_data_tr=video_soup.find_all("tr")
        find_data_tr_str=str(find_data_tr)
        if ship_name in find_data_tr_str:
            for i in find_data_tr:
                total_data_video=str(i.text)
                data_spl=total_data_video.split("\n")
                if len(data_spl)>=2:
                    if ship_name==str(data_spl[2]):
                        video_active=data_spl[1]
                        video_active=str(video_active)
                        cursor.execute("SELECT TOP 1 time FROM dbo.Ku_All_result_history where Ship_name=? order by time desc",ship_name)
                        RE_detect_time=cursor.fetchone()
                        #print(rock_name)
                        #print(str(RE_detect_time))
                        RE_detect_time2=str(RE_detect_time).split("(")
                        RE_detect_time3=str(RE_detect_time2[2])
                        RE_detect_time4=RE_detect_time3.split(")")
                        RE_detect_time5=str(RE_detect_time4[0]).strip()
                        RE_detect_time6=RE_detect_time5.split(",")
                        RE_detect_time_year=str(RE_detect_time6[0]).strip()
                        RE_detect_time_mon=str(RE_detect_time6[1]).strip()
                        RE_detect_time_day=str(RE_detect_time6[2]).strip()
                        RE_detect_time_hour=str(RE_detect_time6[3]).strip()
                        RE_detect_time_min=str(RE_detect_time6[4]).strip()
                        #RE_detect_time_sec=str(RE_detect_time6[5]).strip()
                        RE_detect_time_full=RE_detect_time_year+"-"+RE_detect_time_mon+"-"+RE_detect_time_day+" "+RE_detect_time_hour+":"+RE_detect_time_min
                        fin_time=datetime.strptime(RE_detect_time_full, "%Y-%m-%d %H:%M")
                        #print(f"fully time is : {fin_time}")
                        utc_time_now=datetime.utcnow()
                        #print(f"Now time is : {utc_time_now}")
                        if utc_time_now>=fin_time:
                            #print("Now time > Last update")
                            delta_last_time_sec=(utc_time_now-fin_time).seconds
                        elif fin_time>utc_time_now:
                            #print("Now time < Last update")
                            delta_last_time_sec=(fin_time-utc_time_now).seconds
                        #print(f"the delta time is : {delta_last_time_sec}")
                        cursor.execute("SELECT L_delta FROM dbo.VideoSoft_web_status WHERE ship_name=?",ship_name)
                
                        videosoft_db_data=cursor.fetchall()
                        if videosoft_db_data!=[]:
                            for i in videosoft_db_data:
                                if i[0]=="NoData":
                                    se_last_time=10000
                                else:
                                    se_last_time=int(i[0])
                        if (video_active=="True") or (delta_last_time_sec<=700) or (se_last_time<=700):
                            #video_status2='/static/img/GreenLight002.png'
                            video_status2='True'
                        else:
                            #video_status2='/static/img/RedLight002.png'
                            video_status2='False'
                        new_video=video_status2
                        ##print(total_data)
                        ##print("---------------------------------------")
                        #print(f"the {rock_name} CCTV_Active is : {new_video}")
                            
                        ##print(data_spl[1])
                        ##print(data_spl[2])
                        ##print(data_spl[3])
                        
        else:
            video_active="No data"
            cursor.execute("SELECT TOP 1 time FROM dbo.Ku_All_result_history where Ship_name=? order by time desc",ship_name)
            RE_detect_time=cursor.fetchone()
            #print(rock_name)
            #print(str(RE_detect_time))
            RE_detect_time2=str(RE_detect_time).split("(")
            RE_detect_time3=str(RE_detect_time2[2])
            RE_detect_time4=RE_detect_time3.split(")")
            RE_detect_time5=str(RE_detect_time4[0]).strip()
            RE_detect_time6=RE_detect_time5.split(",")
            RE_detect_time_year=str(RE_detect_time6[0]).strip()
            RE_detect_time_mon=str(RE_detect_time6[1]).strip()
            RE_detect_time_day=str(RE_detect_time6[2]).strip()
            RE_detect_time_hour=str(RE_detect_time6[3]).strip()
            RE_detect_time_min=str(RE_detect_time6[4]).strip()
            #RE_detect_time_sec=str(RE_detect_time6[5]).strip()
            RE_detect_time_full=RE_detect_time_year+"-"+RE_detect_time_mon+"-"+RE_detect_time_day+" "+RE_detect_time_hour+":"+RE_detect_time_min
            fin_time=datetime.strptime(RE_detect_time_full, "%Y-%m-%d %H:%M")
            #print(f"fully time is : {fin_time}")
            utc_time_now=datetime.utcnow()
            #print(f"Now time is : {utc_time_now}")
            if utc_time_now>=fin_time:
                #print("Now time > Last update")
                delta_last_time_sec=(utc_time_now-fin_time).seconds
            elif fin_time>utc_time_now:
                #print("Now time < Last update")
                delta_last_time_sec=(fin_time-utc_time_now).seconds
            #print(f"the delta time is : {delta_last_time_sec}")
            cursor.execute("SELECT L_delta FROM dbo.VideoSoft_web_status WHERE ship_name=?",ship_name)            
            videosoft_db_data=cursor.fetchall()
            if videosoft_db_data!=[]:
                for i in videosoft_db_data:
                    if i[0]=="NoData":
                        se_last_time=10000
                    else:
                        se_last_time=int(i[0])
            if (video_active=="True") or (delta_last_time_sec<=700) or (se_last_time<=700):
                #video_status2='/static/img/GreenLight002.png'
                video_status2='True'
            else:
                #video_status2='/static/img/RedLight002.png'
                video_status2='False'
            new_video=video_status2
            #print(f"the {rock_name} CCTV_Active is : {new_video}")
    return new_video

def get_new_gps(ship_name_list,fleet_name):
    
    points_array=[]
    head_array=[]
    ship_name_array=[]
    vilocity_array=[]
    datetime_array=[]
    cctv_array=[]
    for ship_name in ship_name_list:
        cursor.execute("SELECT GPS_lat,GPS_lon,Head_angle,Ship_name,Vilocity,Time_now FROM dbo.Predict_system WHERE Ship_name=?",ship_name)
        gps_head=cursor.fetchall()
        #print(gps_head)  #[(1.713889, 101.462778, 0.29)]
        for i in gps_head:
            
            #points.append(i[0])
            #points.append(i[1])
            cctv_status=get_cctv_status(ship_name)
            #print(f"points={points}")
            #print(f"head={i[2]}") #head
            print(f"ship_name={i[3]}") #ship_name
            print(f"vilocity={i[4]}") #vilocity
            #print(f"datetime={i[5]}") #datetime
            print(f"cctv status={cctv_status}")
            #points_array.append(points)
            #head_array.append(i[2])
            ship_name_array.append(i[3])
            vilocity_array.append(i[4])
            #datetime_array.append(i[5])
            cctv_array.append(cctv_status)
            print("----------------------------------------")
        cursor.execute("SELECT lat,lon,final_time,heading FROM dbo.KU_SE_GPS WHERE ship_name=?",ship_name)
        total_final_gps=cursor.fetchall()
        for i2 in total_final_gps:
            points=[]
            points.append(i2[0])
            points.append(i2[1])
            print(f"datetime={i2[2]}") #datetime
            time_clean=str(i2[2]).split(".")
            time_final=str(time_clean[0])
            points_array.append(points)
            datetime_array.append(time_final)
            head_array.append(i2[3])
    print(f"points array={points_array}")
    print(f"head array={head_array}")
    print(f"ship name array={ship_name_array}")
    print(f"vilocity array={vilocity_array}")
    print(f"datetime array={datetime_array}")
    print(f"cctv array={cctv_array}")
    print("----------------------------------------")
    output_map_always(ship_name_array,points_array,head_array,vilocity_array,datetime_array,cctv_array,fleet_name)
    output_map_always_tw(ship_name_array,points_array,head_array,vilocity_array,datetime_array,cctv_array,fleet_name)
server = 'vesselstatusdb.database.windows.net' 
database = 'VesselStatusDB' 
username = 'lunghwa' 
password = 'LHE@debug' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT Ship_name FROM dbo.Ku_All_result")
db_get_ship_name_data=cursor.fetchall()
#print(db_get_ship_name_data)
while True:
    try:
        print("Start!!")
        get_new_gps(Waruna,"Waruna")
        get_new_gps(Soechi,"Soechi")
        get_new_gps(LungSoon,"LungSoon")
        get_new_gps(FongKuo,"FongKuo")
        get_new_gps(TsVessel,"TsVessel")
        get_new_gps(EVERSHINING,"EVERSHINING")
        print("Sleep~~~~~~~~~~~~~~~~")
        time.sleep(10)
    except Exception as e:
        print(e)
    

            



