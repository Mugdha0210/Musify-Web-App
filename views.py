from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import SpotifyAPI
from .models import SpotifyAPI1
from django.shortcuts import get_object_or_404
from .forms import ArtistForm
import requests
# Create your views here.
playlist = []
recom = []
rec_pl = []

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
    a = {}
    if request.method == 'POST':
        a_form = ArtistForm(request.POST)
        if a_form.is_valid():
            artist = a_form.cleaned_data.get("artist")
            client_id = 'e1026387021c413786266d809e931ca1'
            client_secret = '6a3eb258f5b54b358860a5de726d0063'
            spotify = SpotifyAPI1(client_id, client_secret)
            r = spotify.get_artist(artist)
            artist_image_url = r['images'][2]['url']
            r = spotify.get_artist_albums(artist)
            a["artist"] = artist
            a["artist_image_url"] = artist_image_url
            for i in range(0, 5):
            	a[f"album{i}_image_url"] = spotify.get_album(r['items'][i]['id'])['images'][0]['url']

            #This image url should be used to display image on webpage
            return render(request, 'Musify/artistpage.html', a)


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
		
		z = spotify.get_rec_played()
		items1 = z["items"]
		global rec_pl

		rec_pl = items1
		print(rec_pl)		
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

	context["rec_name0"] = rec_pl[0]["track"]["name"]
	context["rec_pre0"] = rec_pl[0]["track"]["preview_url"]
	return render(request, 'Musify/displaypage.html', context)
	

