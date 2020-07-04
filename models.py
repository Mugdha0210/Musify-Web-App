from django.db import models

# Create your models here.

#!/usr/bin/env python
# coding: utf-8


import datetime
import base64
from urllib.parse import urlencode

import requests
import json
import random

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    client_id = None
    client_secret = None
    response_type = 'code'
    redirect_uri = 'http://127.0.0.1:8000/Musify/index.html'
    scope = 'user-read-private user-read-email'
    state = '34fFs29kd09'
    authorize_url = 'https://accounts.spotify.com/authorize'
    
    token_url = 'https://accounts.spotify.com/api/token'
    access_token_did_expire = True
    
    def __init__(self, client_id, client_secret, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        
    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        
        if client_id == None or client_secret == None :
            raise Exception("You need to set client_id and client_secret")
            
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return { "Authorization" : f"Basic {client_creds_b64}" }
    
    def get_token_data(self, code) :
        return {"redirect_uri" : self.redirect_uri, "grant_type" : "authorization_code", "code" : code}
    
    def perform_auth(self):
        url = urlencode({"client_id" : self.client_id, "response_type" : self.response_type, "redirect_uri" : self.redirect_uri, "scope" : self.scope,"state" : self.state})
        authorize_url = f"{self.authorize_url}?{url}"
        print(authorize_url)
        r = requests.get(authorize_url)
        if r.status_code not in range(200, 299) :
            raise Exception("Could not authenticate client")
        
        return r
    
    def give_code_get_token(self, code) :
        token_data = self.get_token_data(code)
        token_headers = self.get_token_headers()
        r = requests.post(self.token_url, data = token_data, headers = token_headers)

        now = datetime.datetime.now()
        data = r.json()
        self.access_token = data['access_token']
        expires_in = data['expires_in']    #seconds
        self.access_token_expires = now + datetime.timedelta(seconds = expires_in)
                #now = datetime.datetime.now()
        self.access_token_did_expire = self.access_token_expires < now
        return r
      
    def get_access_token(self):
        token = self.access_token 
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None :
            self.perform_auth()
            return self.get_access_token()
        return token
    
    #def refresh_token(self):
        #pass 
    
    def get_resource_header(self):
        access_token = self.access_token 
        #print("access_token", access_token)
        headers = {"Authorization" : f"Bearer {access_token}"}
        return headers
    
    def base_search(self):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/me"
        #ookup_url = f"{endpoint}?{query_params}"
        r = requests.get(endpoint, headers = headers)
        #print(lookup_url)
        print(r.status_code)
        if r.status_code not in range(200, 299):
            return ""
        return r
    
    def search(self, query = None, operator = None, operator_query = None, search_type = "track"):
        if query == None :
            raise Exception("A query is required")    #possibly changed for musify app
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None :
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q" : query, "type" : search_type.lower()})
        #print(query_params)
        return self.base_search(query_params)
        
    def get_resource(self, lookup_id, resource_type = 'artists', version = 'v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(url = endpoint, headers= headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_id(self, name, search_type = 'artist') :
        response = self.search(query = name, search_type = search_type)
        json_data = json.loads(response.text)
        print(json_data)
        return json_data['artists']['items'][0]['id']
        
    def get_album(self, _id):
        return self.get_resource(_id, resource_type = 'albums')
    
    def get_artist(self, artist_name):
        _id = self.get_id(name = artist_name)
        return self.get_resource(_id, resource_type = 'artists')
    
    def get_user_playlist(self):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/me/playlists"
        #ookup_url = f"{endpoint}?{query_params}"
        r = requests.get(endpoint, headers = headers)
        #print(lookup_url)
        print(r.status_code)
        if r.status_code not in range(200, 299):
            return ""
        return r
        
    def get_playlist_items(self, _id):
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/playlists/{_id}/tracks"
        r = requests.get(endpoint, headers = headers)
        #print(lookup_url)
        print(r.status_code)
        if r.status_code not in range(200, 299):
            return ""
        return r
        
    def get_recommend_seeds(self):
        access_token = self.access_token
        url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        headers = {"Accept": "application/json" , "Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        r = requests.get(url = url, headers = headers)
        print(r)
        if r.status_code not in range(200, 299):
            return {}
        self.recom_seed_genre = r.json()
        return r.json()
    
    def get_recommendns(self):
        recom_list = self.recom_seed_genre["genres"]
        random_5 = random.sample(recom_list, 5)
        print(random_5)
        endpoint = "https://api.spotify.com/v1/recommendations"
        headers = self.get_resource_header()
        query_params = urlencode({"seed_genres" : random_5, "limit" : 5}, doseq = True)
        url = f"{endpoint}?{query_params}"
        print("url is ", url)
        r = requests.get(url = url, headers = headers)
        print(r)
        if r.status_code not in range(200, 299):
            return {}
        self.recom_seed_genre = r.json()
        return r.json()
