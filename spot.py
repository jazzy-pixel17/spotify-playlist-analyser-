#imports
import spotipy
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import math
import matplotlib.pyplot as plt
import urllib.request

# authentication
client_credentials_manager = SpotifyClientCredentials(client_id='59cfcf2856a549b2987d8c098d401af9', client_secret='f8d1d3106e5a4ae0bb8290c158ab4f29')
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# setting the style for matplotlib
plt.style.use('seaborn-v0_8-muted')

def get_playlistcsv(playlist_link):
    # get uri from playlist link
    playlist_uri = ''
    for i in playlist_link[34::]:
        if i=='?':
            break
        else:
            playlist_uri+=i

    tracks = session.playlist_tracks(playlist_uri)["items"]
    playlist_cover = session.playlist_cover_image(playlist_uri)[0]['url']
    urllib.request.urlretrieve(playlist_cover, "static/cover.png")


    with open('playlistdata.csv','w') as f:
        writer=csv.writer(f)
        # headers
        writer.writerow(['Track', 'Artist', 'Album', 'Release Date', 'Date Added', 'Duration (ms)'])

        # extract the data
        for track in tracks:
            # artists = ''
            name = track['track']['name']
            artists = ",".join([artist['name'] for artist in track['track']['artists']])
            album = track['track']['album']['name']
            releasedate = track['track']['album']['release_date']
            adddate = track['added_at'][:10]
            length = track['track']['duration_ms']

            #write
            writer.writerow([name, artists, album, releasedate, adddate, length])

#WORKING WITH THE CSV FILE

def playlistname(playlist_link):
    playlist_uri = ''
    for i in playlist_link[34::]:
        if i=='?':
            break
        else:
            playlist_uri+=i

    return session.playlist(playlist_uri)['name']

def playlistowner(playlist_link):
    playlist_uri = ''
    for i in playlist_link[34::]:
        if i=='?':
            break
        else:
            playlist_uri+=i

    return session.playlist(playlist_uri)['owner']['display_name']


def songcount():
    with open('playlistdata.csv','r') as f:
        count = 0
        data = csv.reader(f)
        for row in data:
            if row[0]=='Track':
                continue
            else:
                count += 1
        return str("No. of songs in playlist: "+str(count))


def duration():
    with open('playlistdata.csv','r') as f:
        count = 0
        time = 0
        data = csv.reader(f)
        for row in data:
            if row[0]=='Track':
                continue
            else:
                time += int(row[5])
                count += 1
        hours = math.floor(time/3600000)
        mins = math.floor((time - hours*3600000)/60000)
        sec = math.floor((time - hours*3600000 - mins*60000)/1000)
        
        return str("Total duration of playlist: "+str(hours)+" hours "+str(mins)+" mins "+str(sec)+" secs")


def averagetime():
    with open('playlistdata.csv','r') as f:
        count = 0
        time = 0
        data = csv.reader(f)
        for row in data:
            if row[0]=='Track':
                continue
            else:
                time += int(row[5])
                count += 1
        avgms = time/count
        mins = math.floor(avgms/60000)
        sec = math.floor((avgms - mins*60000)/1000)
        
        return str("Average song length: "+ str(mins)+" mins "+str(sec)+" secs")


def artfreq():
    with open('playlistdata.csv','r') as f:
        l1 = []
        dict = {}
        data = csv.reader(f)
        for row in data:
            if row[0]=='Track':
                continue
            else:
                if ',' in row[1]:
                    artists = row[1].split(',')
                    l1.extend(artists)
                else:
                    l1.append(row[1])

        # making a dictionary of artists and no. of tracks
        for i in l1:
            dict[i] = l1.count(i)
        
        # looking for most occurring artist in playlist
        count = 0
        key = ''
        for items in dict:
            if dict[items] > count:
                count = dict[items]
                key = items

        return str("The most occurring artist in this playlist is "+str(key)+" who has appeared on "+str(dict[key])+" tracks.")


def timeperiod():
    with open('playlistdata.csv','r') as f:
        upper = 0
        lower = 3000
        data = csv.reader(f)
        for row in data:
            if row[0]=='Track':
                continue
            else:
                if int(row[3][:4]) > upper:
                    upper = int(row[3][:4])
                if int(row[3][:4]) < lower:
                    lower = int(row[3][:4])

        return str("The music in this playlist was released in the years "+str(lower)+" to "+str(upper)+".")


def piechart(): # recommended with playlists with fewer no. of artists present
    with open('playlistdata.csv','r') as f:
        l1 = []
        dict = {}
        data = csv.reader(f)
        for row in data:
            if row[0]=='Track':
                continue
            else:
                if ',' in row[1]:
                    artists = row[1].split(',')
                    l1.extend(artists)
                else:
                    l1.append(row[1])

        # making a dictionary of artists and no. of tracks
        for i in l1:
            dict[i] = l1.count(i)
        
        # making 2 lists with artist names and percentages
        l2 = []
        l3 = []
        for i in dict:
            l2.append(i)
            per = dict[i]
            per = (dict[i]/len(l1))*100
            l3.append(per)
        
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.pie(l3, labels=l2, textprops={'fontsize': 8}, radius=1)
        plt.savefig('static/pie_chart.png')
        

def horbarchart():
    with open('playlistdata.csv','r') as f:
        l1 = []
        dict = {}
        data = csv.reader(f)
        for row in data:
            if row[0]=='Track':
                continue
            else:
                if ',' in row[1]:
                    artists = row[1].split(',')
                    l1.extend(artists)
                else:
                    l1.append(row[1])

        # making a dictionary of artists and no. of tracks
        for i in l1:
            dict[i] = l1.count(i)
        
        # making 2 lists with artist names and percentages
        l2 = []
        l3 = []
        for i in dict:
            l2.append(i)
            per = dict[i]
            l3.append(per)
        
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.barh(l2, l3, align='center')
        plt.yticks(fontsize=8)
        plt.savefig('static/bar_chart.png')


def pop1(playlist_link):
    playlist_uri = ''
    for i in playlist_link[34::]:
        if i=='?':
            break
        else:
            playlist_uri+=i

    tracks = session.playlist_tracks(playlist_uri)["items"]

    l=[]
    for track in tracks:
        name = track['track']['name']
        pop = track['track']['popularity']
        cover = track['track']['album']['images'][0]['url']
        artists = ", ".join([artist['name'] for artist in track['track']['artists']])
        tup = (pop,name,cover,artists)
        l.append(tup)
    l.sort(reverse=True)

    pop1 = l[0][2]
    urllib.request.urlretrieve(pop1, "static/pop1.png")

    return [l[0][0], l[0][1], l[0][3]]


def pop2(playlist_link): 
    playlist_uri = ''
    for i in playlist_link[34::]:
        if i=='?':
            break
        else:
            playlist_uri+=i

    tracks = session.playlist_tracks(playlist_uri)["items"]

    l=[]
    for track in tracks:
        name = track['track']['name']
        pop = track['track']['popularity']
        cover = track['track']['album']['images'][0]['url']
        artists = ", ".join([artist['name'] for artist in track['track']['artists']])
        tup = (pop,name,cover, artists)
        l.append(tup)
    l.sort(reverse=True)

    pop2 = l[1][2]
    urllib.request.urlretrieve(pop2, "static/pop2.png")

    return [l[1][0], l[1][1], l[1][3]]


def pop3(playlist_link): 
    playlist_uri = ''
    for i in playlist_link[34::]:
        if i=='?':
            break
        else:
            playlist_uri+=i

    tracks = session.playlist_tracks(playlist_uri)["items"]

    l=[]
    for track in tracks:
        name = track['track']['name']
        pop = track['track']['popularity']
        cover = track['track']['album']['images'][0]['url']
        artists = ", ".join([artist['name'] for artist in track['track']['artists']])
        tup = (pop,name,cover, artists)
        l.append(tup)
    l.sort(reverse=True)

    pop3 = l[2][2]
    urllib.request.urlretrieve(pop3, "static/pop3.png")

    return [l[2][0], l[2][1], l[2][3]]
