from django.db import models

# Create your models here.

#!/usr/bin/env python
# coding: utf-8


import datetime
import base64
from urllib.parse import urlencode

import requests


class SpotifyAPI(models.Model):
    access_token = None
    access_token_expires = datetime.datetime.now()
    client_id = None
    client_secret = None
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
    
    def get_token_data(self) :
        return {"grant_type" : "client_credentials"}  
        
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data = token_data, headers = token_headers)
        
        if r.status_code not in range(200, 299) :
            raise Exception("Could not authenticate client")
        
        now = datetime.datetime.now()
        data = r.json()
        self.access_token = data['access_token']
        expires_in = data['expires_in']    #seconds
        self.access_token_expires = now + datetime.timedelta(seconds = expires_in)
                #now = datetime.datetime.now()
        #self.access_token_did_expire = self.access_token_expires < now
        return True
      
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
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        #print("access_token", access_token)
        headers = {"Authorization" : f"Bearer {access_token}"}
        return headers
    
    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers = headers)
        print(lookup_url)
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
        #print(json_data)
        return json_data['artists']['items'][0]['id']
        
    def get_album(self, _id):
        return self.get_resource(_id, resource_type = 'albums')
    
    def get_artist(self, artist_name):
        _id = self.get_id(name = artist_name)
        return self.get_resource(_id, resource_type = 'artists')
