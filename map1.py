import folium
import json, requests
import pandas as pd

city = input("Enter the city you want to search: ")

url = 'https://api.foursquare.com/v2/venues/explore?near='+city

params = dict(
  client_id='GZPRKLSA05IUS4H2X5MEOAQJ1YHSWXPKY0EVZJKJBPLFZVJ4',
  client_secret='NMY1K3WWBFGB3SPV55M3J2IEQVNVF4XNHIHGXE1WWER4K2MW',
  v='20180323',
)
resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

li = []

for place in data["response"]["groups"][0]["items"]:
    name = place["venue"]["name"]
    lat = place["venue"]["location"]["lat"]
    long = place["venue"]["location"]["lng"]
    li.append({"name":name,"lat":lat,"long":long})

location = []
location.append(li[0]["lat"])
location.append(li[0]["long"])
map=folium.Map(location=location,zoom_start = 6,tiles = "Mapbox Bright")

fg = folium.FeatureGroup(name="My Map")

for places in li:
    temp = []
    temp.append(places["lat"])
    temp.append(places["long"])
    temp1 = places["name"]
    fg.add_child(folium.Marker(location=temp,popup = folium.Popup(temp1,parse_html=True),icon = folium.Icon(color="green")))

fg.add_child(folium.GeoJson(data=open("world.json","r",encoding="utf-8-sig").read(),
style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005']<10000000
else 'orange' if 10000000<=x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fg)

map.save("Map1.html")
