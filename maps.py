from tweets import get_locations
from geolocation.main import GoogleMaps

google_maps = GoogleMaps("AIzaSyCOjJ-Nqa8NZQ3ti7SQ7_IE1HohSZaJunk")

locations = get_locations("./data/25crisis/")
for loc in locations.keys():
    print(loc)
    print(google_maps.search(location=loc).first().lat)

