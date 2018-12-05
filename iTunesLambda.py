import xml.etree.ElementTree as ET
from libpytunes import Library
from collections import Counter
import musicbrainzngs
import requests
from urllib.parse import urlparse
import boto3
import botocore

musicbrainzngs.set_useragent("Artist Nationality Sorter", "a0.0.2", "alexchow.me")

s3 = boto3.resource('s3')

# l = Library('/Users/alexchow/Music/iTunes/iTunes Music Library.xml')
l= Library('iTunes Music Library.xml')
artists = []
xmls = []
countries = []
cities = []

def findArtist(library):

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

def handler(event, context):
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    s3 = boto3.client('s3')
    objs = s3.list_objects_v2(Bucket='my_bucket')['Contents']
    [obj['Key'] for obj in sorted(objs, key=get_last_modified)]
    # source_bucket = event['Records'][0]['s3']['bucket']['name']
    # key = urlparse(event['Records'][0]['s3']['object']['key'])
    try:
        s3.Bucket(my_bucket).download_file(key, 'User iTunes Music Library.xml')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    library = 'User iTunes Music Library.xml'
    count = findArtist(library)
    return count
