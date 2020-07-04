from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import SpotifyAPI
from django.shortcuts import get_object_or_404
from .forms import ArtistForm
import requests
# Create your views here.
playlist = []
recom = []

def index(request):
	#template = loader.get_template('Musify/index.html')
	#context = { 'latest_question_list' : "Hello World", }
	#print(request.POST)
	return render(request, 'Musify/index.html')
	


def search_page(request):
    template = loader.get_template('Musify/searchpage.html')
    #artist = request.POST['artist_name']
    #genre = request.POST['genre_name']
    #print(artist, genre)
    if request.method == 'POST':
        a_form = ArtistForm(request.POST)
        if a_form.is_valid():
            artist = a_form.cleaned_data.get("artist")
            client_id = 'e1026387021c413786266d809e931ca1'
            client_secret = '6a3eb258f5b54b358860a5de726d0063'
            spotify = SpotifyAPI(client_id, client_secret)
            r = spotify.get_artist(artist)
            artist_image_url = r['images'][2]['url']
            r = spotify.get_artist_albums(artist)
            album_id1 = r['items'][0]['id']
            r1 = spotify.get_album(album_id1)
            album1_image_url = r1['images'][0]['url']
            album_id2 = r['items'][1]['id']
            r2 = spotify.get_album(album_id2)
            album2_image_url = r2['images'][0]['url']
            album_id3 = r['items'][2]['id']
            r3 = spotify.get_album(album_id3)
            album3_image_url = r3['images'][0]['url']
            album_id4 = r['items'][3]['id']
            r4 = spotify.get_album(album_id4)
            album4_image_url = r4['images'][0]['url']
            album_id5 = r['items'][4]['id']
            r5 = spotify.get_album(album_id5)
            album5_image_url = r5['images'][0]['url']
            a = {"artist" : artist, "artist_image_url" : artist_image_url, "album1_image_url" : album1_image_url, "album2_image_url" : album2_image_url, "album3_image_url" : album3_image_url, "album4_image_url" : album4_image_url, "album5_image_url" : album5_image_url}

            #This image url should be used to display image on webpage
            return render(request, 'Musify/displaypage.html', a)


    else :
        a_form = ArtistForm()
    context = {'a_form' : a_form}
    #display_page(request, context)
    return render(request, 'Musify/searchpage.html', context)
	
def redirect_page(request):
	#template = loader.get_template('Musify/callback.html')
	client_id = 'e1026387021c413786266d809e931ca1'
	client_secret = '6a3eb258f5b54b358860a5de726d0063'
	if request.method == 'GET' :
		spotify = SpotifyAPI(client_id, client_secret)
		s = spotify.perform_auth()
		code = request.GET.urlencode()
		code1 = str(code)
		cleaned_code = code1.split('&')[0]
		cleaned_code1 = cleaned_code[5:]
		print("code is", cleaned_code1)
		s = spotify.give_code_get_token(code = cleaned_code1)
		s = spotify.base_search()
		p = spotify.get_user_playlist()
		playlist_id  = p.json()["items"][0]["id"]
		p = spotify.get_playlist_items(playlist_id)
		items = p.json()["items"]
		global playlist
		playlist = items
		
		x = spotify.get_recommend_seeds()
		y = spotify.get_recommendns()
		global recom
		recom = y["tracks"][:5]
	#else :
		#print(s)
		context = s.json()
	print(s)
	
	return render(request, 'Musify/index.html', context)
	
	
def display_page(request):
	context = {}
	for i in range(0, 5):
		context[f"url{i}"] = playlist[i]["track"]["album"]["images"][0]["url"]
		context[f"al_name{i}"] = recom[i]["album"]["name"]
		context[f"al_img{i}"] = recom[i]["album"]["images"][0]["url"]
	return render(request, 'Musify/displaypage.html', context)
	

