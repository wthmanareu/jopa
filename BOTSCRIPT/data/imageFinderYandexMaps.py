import requests
import sys


def get_coords(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates.split(" ")
    else:
        return None, None


def get_map(lon_lat, type, delta="0.005", point=None):
    if point is None:
        map_params = {
            "ll": lon_lat,
            "spn": ",".join([delta, delta]),
            "l": type
        }
    else:
        map_params = {
            "ll": lon_lat,
            "spn": ",".join([delta, delta]),
            "l": type,
            "pt": point
        }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    return requests.get(map_api_server, params=map_params).content


def save_geo(toponim, map_type, filename, size="0.005", point=False):
    try:
        lat, lon = get_coords(toponim)
        lon_lat = f"{lat},{lon}"
        if point:
            content = get_map(lon_lat, map_type, size, lon_lat)
        else:
            content = get_map(lon_lat, map_type, size)
        try:
            with open(f'{filename}', 'wb') as file:
                file.write(content)
            return filename
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
    except Exception as e:
        return 'No data' + str(e)