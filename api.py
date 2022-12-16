
import requests


def get_directions_response(lat1, long1, lat2, long2, mode='drive', key='no_key'):
        url = "https://route-and-directions.p.rapidapi.com/v1/routing"
        key = key
        host = "route-and-directions.p.rapidapi.com"
        headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": host}
        querystring = {"waypoints":f"{str(lat1)},{str(long1)}|{str(lat2)},{str(long2)}","mode":mode}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response

