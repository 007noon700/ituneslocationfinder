import xml.etree.ElementTree as ET
from libpytunes import Library
from collections import Counter
import musicbrainzngs
import requests
import boto3
import pycountry
import pygal
import pygal_maps_world

musicbrainzngs.set_useragent("Artist Nationality Sorter", "a0.0.2", "alexchow.me")


# l = Library('/Users/alexchow/Music/iTunes/iTunes Music Library.xml')
l= Library('iTunes Music Library.xml')
artists = []
xmls = []
countries = []
cities = []

def findArtist():
    # get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    # s3 = boto3.client('s3')
    # objs = s3.list_objects_v2(Bucket='itunesartistlocationmapper')['Contents']
    # last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][0]
    # print(last_added)
    # l=Library(last_added)
    for id, song in l.songs.items():
        if song.artist is None:
            continue
        if song.artist in artists:
            continue
        else:
            test = musicbrainzngs.search_artists(query=song.artist, limit = 1)
            xmls.append(test)
            artists.append(song.artist)
    print(artists)

    for item in xmls:
        if 'area' not in item['artist-list'][0]:
            countries.append('Unknown')
        elif item['artist-list'][0]['area']['type'] == 'City':
            city = (item['artist-list'][0]['area']['name'])
            payload = {'q': 'foo', 'maxRows': 1, 'username': '007noon700'}
            payload['q'] = city
            r = requests.get('http://api.geonames.org/search', params=payload)
            root = ET.fromstring(r.text)
            # print(root[1][6].text)
            countries.append(root[1][6].text)
        elif item['artist-list'][0]['area']['type'] == 'Subdivision':
            city = (item['artist-list'][0]['area']['name'])
            payload = {'q': 'foo', 'maxRows': 1, 'username': '007noon700'}
            payload['q'] = city
            r = requests.get('http://api.geonames.org/search', params=payload)
            root = ET.fromstring(r.text)
            # print(root[1][6].text)
            countries.append(root[1][6].text)
        elif item['artist-list'][0]['area']['type'] == 'Municipality':
            city = (item['artist-list'][0]['area']['name'])
            payload = {'q': 'foo', 'maxRows': 1, 'username': '007noon700'}
            payload['q'] = city
            r = requests.get('http://api.geonames.org/search', params=payload)
            root = ET.fromstring(r.text)
            # print(root[1][6].text)
            countries.append(root[1][6].text)
        elif item['artist-list'][0]['area']['type'] == 'District':
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
    return totalCount

def mapper():
    countrycodes = []
    for country in countries:
        if country is not 'Unknown':
            country = pycountry.countries.get(name=country)
        else:
            continue
        countrycodes.append(country.alpha_2.lower())
    print(countrycodes)
    totalCount = Counter(countrycodes)
    return totalCount

class tester:
    findArtist()
    count=dict(mapper())
    print(count)
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = 'Concentration of Artists in your iTunes Library'
    worldmap_chart.add('Number of Artists', count)
    worldmap_chart.render_to_file('chart.svg')




