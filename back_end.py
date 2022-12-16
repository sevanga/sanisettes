from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon
from utils import calculate_distance
from api import get_directions_response
import pandas as pd 


class Customer:
    
    def __init__(self, position, is_pmr, mode):
        self.position = position
        self.is_pmr = is_pmr
        self.mode = mode



def colors_for_pmr(df):
    colors = []
    for i in range(len(df)):
        if df['ACCES_PMR'].iloc[i] == ('oui' or 'Oui'):
            colors.append('green')
        else:
            colors.append('red')
    return colors 



def nearest_toilet(customer, df):
    
    z = 0
    for i in range(len(df)):
        distance = calculate_distance(customer.position[0], customer.position[1], 
                                      df['LAT'].iloc[i], df['LONG'].iloc[i])
        if i == 0:
            lowest_distance = distance
        if distance <= lowest_distance:
            lowest_distance = distance
            z = i
    
    nearest_toilet = df.iloc[z]
    
    return nearest_toilet, lowest_distance


def create_map(response):
   # use the response
        mls = response.json()['features'][0]['geometry']['coordinates']
    
        points = [(i[1], i[0]) for i in mls[0]]
        m = folium.Map()
        # add marker for the start and ending points
        for point in [points[0], points[-1]]:
            folium.Marker(point).add_to(m)
        
        # add the lines
        folium.PolyLine(points, weight=4, opacity=1).add_to(m)
        # create optimal zoom
        df = pd.DataFrame(mls[0]).rename(columns={0:'Lon', 1:'Lat'})[['Lat', 'Lon']]
        sw = df[['Lat', 'Lon']].min().values.tolist()
        ne = df[['Lat', 'Lon']].max().values.tolist()
        m.fit_bounds([sw, ne])
        return m


def i_need_to_pee(customer, df):
    
    data = df 
    
    # handi persons condition 
    if customer.is_pmr == True: data = data[(data['ACCES_PMR'] == 'oui') | data['ACCES_PMR'] == 'Oui']
    
    nearest_toil, dist = nearest_toilet(customer, data)
    
    # getting the direction
    #response = get_directions_response(customer.position[0], customer.position[1], nearest_toilet['LAT'], nearest_toilet['LONG'], api_key)
    response = get_directions_response(customer.position[0], customer.position[1], 
                                       nearest_toil['LAT'], nearest_toil['LONG'], 
                                       mode=customer.mode, key="key_is_hidden_from_public_display")
    
    m = create_map(response)
    return m
