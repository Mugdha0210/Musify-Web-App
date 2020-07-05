import webbrowser

url = "https://accounts.spotify.com/authorize?client_id=e1026387021c413786266d809e931ca1&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2FMusify%2Findex.html&scope=user-read-private+user-read-email+user-read-recently-played&state=34fFs29kd09"
webbrowser.open(url, new=0)
