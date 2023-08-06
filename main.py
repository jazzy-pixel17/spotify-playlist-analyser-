import spot
from flask import Flask, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def display_stats():
    # getting user data
    playlist_link = input("\nHello there!\n\nThis is a little program built to analyse your Spotify playlists. One thing to note is that this program can't analyse more than 100 songs in a playlist so it is recommended to use shorter playlists. Also, this program only works on user-made playlists and hence won't work for Spotify Blend playlist links.\n\nEnter playlist link: ")
    spot.get_playlistcsv(playlist_link)

    # implementing
    spot.piechart()
    spot.horbarchart()
    owner = spot.playlistowner(playlist_link)
    name = spot.playlistname(playlist_link)
    song_count = spot.songcount()
    length = spot.duration()
    average_time = spot.averagetime()
    art_freq = spot.artfreq()
    time_period = spot.timeperiod()
    pie_chart = 'static/pie_chart.png'
    bar_chart = 'static/bar_chart.png'
    cover = 'static/cover.png'
    pop1 = 'static/pop1.png'
    pop2 = 'static/pop2.png'
    pop3 = 'static/pop3.png'
    l1 = spot.pop1(playlist_link)
    l2 = spot.pop2(playlist_link)
    l3 = spot.pop3(playlist_link)
    pop1_name = l1[1]
    pop1_artist = l1[2]
    pop1_rating = l1[0]
    pop2_name = l2[1]
    pop2_artist = l2[2]
    pop2_rating = l2[0]
    pop3_name = l3[1]
    pop3_artist = l3[2]
    pop3_rating = l3[0]

    return render_template('stats.html',pop3_name=pop3_name, pop3_artist=pop3_artist, pop3_rating=pop3_rating, pop2_name=pop2_name, pop2_artist=pop2_artist, pop2_rating=pop2_rating, pop1_name=pop1_name, pop1_artist=pop1_artist, pop1_rating=pop1_rating, owner=owner, name=name, song_count=song_count, length=length, average_time=average_time, art_freq=art_freq, time_period=time_period, pie_chart=pie_chart, bar_chart=bar_chart, cover=cover, pop1=pop1, pop2=pop2, pop3=pop3)

if __name__ == '__main__':
    app.run(debug=True)