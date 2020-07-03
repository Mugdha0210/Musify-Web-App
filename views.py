from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import SpotifyAPI
from django.shortcuts import get_object_or_404
from .forms import ArtistForm

# Create your views here.
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
	return render(request, 'Musify/callback.html')
	
	
	

