import xml.etree.ElementTree as ET
from libpytunes import Library
from collections import Counter
import musicbrainzngs
import requests

musicbrainzngs.set_useragent("Artist Nationality Sorter", "a0.0.2", "alexchow.me")


l = Library('iTunes Music Library.xml')
artists = []
xmls = []
countries = []
cities = []

class findArtists:
    for id, song in l.songs.items():
        if song.artist in artists:
            continue
        else:
            test = musicbrainzngs.search_artists(query=song.artist, limit = 1)
            xmls.append(test)
            artists.append(song.artist)
    print(artists)

    for item in xmls:
        if item['artist-list'][0]['area']['type'] == 'City':
            city = (item['artist-list'][0]['area']['name'])
            payload = {'q': 'foo', 'maxRows': 1, 'username': '007noon700'}
            payload['q'] = city
            r = requests.get('http://api.geonames.org/search', params=payload)
            root = ET.fromstring(r.text)
            # print(root[1][6].text)
            countries.append(root[1][6].text)
        else:
            countries.append(item['artist-list'][0]['area']['name'])
    print(countries)
    totalCount = Counter(countries)
    # print(totalCount)


