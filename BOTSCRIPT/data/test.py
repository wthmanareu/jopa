import requests


def saveImgYandex(name, filename):
    img = name
    p = requests.get(img)
    out = open(f"static/img/imagesForGeographicTest/{filename}.png", "wb")
    out.write(p.content)
    out.close()
    return f"static/img/imagesForGeographicTest/{filename}.png"