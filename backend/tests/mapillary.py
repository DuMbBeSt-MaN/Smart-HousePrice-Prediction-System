import webbrowser

def get_satellite_preview(lat, lon, zoom=18):
    return (
        "https://static-maps.yandex.ru/1.x/"
        f"?ll={lon},{lat}&z={zoom}&size=650,450&l=sat"
    )

if __name__ == "__main__":
    lat =  34.063402
    lon = -118.433053

    url = get_satellite_preview(lat, lon)
    print("Opening:", url)

    webbrowser.open(url)