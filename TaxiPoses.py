import folium
import json
import requests

mat_lat = [[0] * 5] * 5
mat_lon = [[0] * 5] * 5

width = 0.03
xlat = 45.085#<
ylon = 41.92949#>
json_list = []
poses = []
cur_driv = []
list_markers = []

def createJsonStr(tariff,lon, lat, cur_drivers):
    json_string = {
        "classes": [
            tariff
        ],
        "current_drivers": 
            []
        ,
        "full_adjust_task": True,
        "id": "",
        "point": [
            lon,
            lat
        ],
        "simplify": True,
        "supported": [
            "code_dispatch"
        ]
    }
    return json_string

def getTaxiResponseText(js_str):
    response = requests.post("https://uc.taxi.yandex.net/3.0/nearestdrivers?block_id=default",json=js_str)
    text = json.loads(response.text)
    return text

def getTaxiPosits(text):
    if (checkIsTaxiResponseEmpty(text)):
        list_pos=[]
        for i in text['drivers']:
            for a in i['positions']:
                list_pos.append((a['lat'],a['lon']))
                break
        return list_pos
    else:
        return []

def getTaxiIds(text):
    if (checkIsTaxiResponseEmpty(text)):
        list_id=[]
        for i in text['drivers']:
            list_id.append(i['id'])
        return list_id
    else:
        return []

def checkIsTaxiResponseEmpty(text):
    if (bool(text)):
        if (bool(text['drivers'])):
            if bool(text['drivers'][0]['positions']):
                if bool(text['drivers'][0]['positions'][0]):
                    return True
    return False



def createMapHtml():
    for i in range(len(mat_lat)):
        for j in range(len(mat_lat[i])):
            mat_lat[i][j] = 45.085-width*i
            mat_lon[i][j] = 41.92949+width*j
            #json_list.append(createJsonStr(mat_lon[i][j],mat_lat[i][j]))
            resp_text = getTaxiResponseText(createJsonStr("uberx",mat_lon[i][j],mat_lat[i][j],list(set(cur_driv))))
            cur_driv.extend(getTaxiIds(resp_text))
            poses.extend(getTaxiPosits(resp_text))

    map = folium.Map(location=[45.0376,41.9665], zoom_start = 12)

    for aq,bq in poses:
        list_markers.append(folium.Circle(
            radius=50,
            location=[aq,bq],
            popup='',
            color='crimson',
            fill=True))

    for markers in list_markers:
        markers.add_to(map)   
    return map._repr_html_()

def getTaxiUniquePosits(text,cur_ids):
    if (checkIsTaxiResponseEmpty(text)):
        list_pos=[]
        for i in text['drivers']:
            if not (i['id'] in list(set(cur_ids))):
                for a in i['positions']:
                    list_pos.append((a['lat'],a['lon']))
                    break
            return list_pos
    else:
        return []

def getUpdatedPosits(tariff):
    list_pos_upd = []
    cur_drivers_upd = []
    for i in range(len(mat_lat)):
        for j in range(len(mat_lat[i])):
            mat_lat[i][j] = 45.085-width*i
            mat_lon[i][j] = 41.92949+width*j
            #json_list.append(createJsonStr(mat_lon[i][j],mat_lat[i][j]))
            resp_text = getTaxiResponseText(createJsonStr(tariff,mat_lon[i][j],mat_lat[i][j],list(set(cur_drivers_upd))))
            #list_pos_upd.extend(getTaxiUniquePosits(resp_text,cur_drivers_upd))
            list_pos_upd.extend(getTaxiPosits(resp_text))
            cur_drivers_upd.extend(getTaxiIds(resp_text))
    return list_pos_upd
