from django.shortcuts import render
from django.http import HttpResponse 
from django import forms
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import random
class MakeanArtistForm(forms.Form):
    artist_name = forms.CharField(label = 'Artist Name', widget=forms.TextInput(attrs= {'class': 'artist_name'}))
    year = forms.IntegerField(label = 'Year of Release', required= False, max_value= 2023, min_value= 2000, widget=forms.NumberInput(attrs= {'class': 'year'}))


def getSongs(artist_name, year):
    client_id = 'f6635de84ba24b4cb25638b9d6095c3d'                #enter the client ID from the Settings menu in Spotify
    client_secret = '94936c10c5424335acfe9a72f52d961a'        #enter the client secret from the Settings menu in Spotify

    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    access_token=client_credentials_manager.get_access_token()
    #print(access_token)
    spotify=spotipy.Spotify(auth=access_token['access_token'])
                            #Use the search method to search for the artist by name, and retrieve their id.
            #---------------REMEMBER TO SET THE ARTIST NAME TO WHATEVER THE USER ENTERS ON THE WEBPAGE-----------------
    # artist_name = input("Enter the name of the artist: ")

    def same_artist_list():
        tracks = []
        track_names = []
        search_offset = 0
        name_of_artist = artist_name
        results = spotify.search(q='artist:' + artist_name, type='track', limit = 50)
        tracks = results['tracks']['items']
        while len(tracks) < 151:
            search_offset += 50  # Increment the offset to retrieve the next page
            results = spotify.search(q='artist:' + name_of_artist, type='track', limit=50, offset=search_offset)
            tracks += results['tracks']['items']
        random.shuffle(tracks)
        for track in tracks:
            if track['name'] not in track_names and len(track_names) < 10:
                track_names.append(track['name'])
        if len(track_names) < 10:
            track_names.append("Couldn't find any more songs.")
        return track_names
    
    def same_year_list():
        track = []
        track_names = []
        name_of_artist = artist_name
        search_offset = 0
        results = spotify.search(q='artist:' + name_of_artist, type='track', limit = 50, offset = search_offset)
        tracks = results['tracks']['items']

# Loop through the pages of results
        while len(tracks) < 151:
            search_offset += 50  # Increment the offset to retrieve the next page
            results = spotify.search(q='artist:' + name_of_artist, type='track', limit=50, offset=search_offset)
            tracks += results['tracks']['items']
        random.shuffle(tracks)
        for track in tracks:
            if (track['album']['release_date'].split('-')[0]) == year:
                if track['name'] not in track_names:
                    track_names.append(track['name'])
            if len(track_names) >= 10:
                break

        if len(track_names) < 10:
            track_names.append("Couldn't find any more songs.")
        return track_names
    
    if year == None:
        nameOfTracks = same_artist_list()
    else:
        nameOfTracks = same_year_list()

    return nameOfTracks
    
def index (request):
    return render(request, 'playpal/index.html', {
        'form' : MakeanArtistForm()
    })

def printSongs(request):
    if request.method == 'POST':
        form = MakeanArtistForm(request.POST)
        if form.is_valid():
            artistName = form.cleaned_data['artist_name']
            yearOfRelease = form.cleaned_data['year']
            listOfTracks = getSongs(artistName, yearOfRelease)
            
            return render(request, "playpal/songs.html", {'listOfTracks': listOfTracks})
        else:
            return render(request, 'playpal/index.html', {
                'form': form
            })

    return render(request, 'playpal/index.html', {
            form: MakeanArtistForm()
        })