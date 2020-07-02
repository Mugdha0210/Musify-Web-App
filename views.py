from django.shortcuts import render
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
			a = {"artist" : artist}
			print(a)
	else :
		a_form = ArtistForm()
	context = {'a_form' : a_form}
	#display_page(request, context)
	return render(request, 'Musify/searchpage.html', context)
	
def display_page(request, context):
	client_id = 'e1026387021c413786266d809e931ca1'
	client_secret = '6a3eb258f5b54b358860a5de726d0063'
	spotify = SpotifyAPI(client_id, client_secret)
	#template = loader.get_template('Musify/displaypage.html')
	return render(request, 'Musify/displaypage.html', context)
	
def redirect_page(request):
	#template = loader.get_template('Musify/callback.html')
	return render(request, 'Musify/callback.html')
	
	
	

