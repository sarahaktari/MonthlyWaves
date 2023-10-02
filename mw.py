#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 22:49:01 2023

@author: student
"""
# imports for important things 

import datetime
import spotipy 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from spotipy.oauth2 import SpotifyOAuth


# requested credentials based on Spotify API
clientID = 'a992bbc06e644f7eb5400d39585c458f' #enter client ID
clientSecret = '3817178c33d54ee988f798fdee4ed7a6' #enter client secret
redirectURI = 'http://localhost:8888/callback' #enter redirect uri 
scopesUsed = 'playlist-modify-public playlist-modify-private user-top-read user-library-read user-library-modify user-read-recently-played'

# initialize your data with spotifyOAuth
spotOA = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI, scope=scopesUsed))

# access the user's display name to personalize playlists
userInfo = spotOA.me()
userName = userInfo['display_name']



# current and end dates
end_date = datetime.now()
dateToday = end_date - relativedelta(months=1)

#dictionary for month name to correspond to 
months = {
    1: "january", 2: "february", 3: "march", 4: "april",
    5: "may", 6: "june", 7: "july", 8: "august",
    9: "september", 10: "october", 11: "november", 12: "december"
}

currentMonth = months[dateToday.month]
#playlistDate = dateToday.strftime('%b %y')

# convert to unix time stamps
#start_timestamp = int(start_date.timestamp()) * 1000
#end_timestamp = int(end_date.timestamp()) * 1000


#gives top tracks from the past 4 weeks
topTracks = spotOA.current_user_top_tracks(time_range='short_term', limit=50)

# see if top 20 exists 
if topTracks['items']:
    trackURI = [track['uri'] for track in topTracks['items']]
    trackList = [track['name'] for track in topTracks['items']]
    
    # playlist with description
    playlistTitle = f"{currentMonth} {dateToday.year}!!!"
    playlistDes = f"{userName}'s monthly playlist for {currentMonth} {dateToday.year}"
    
    #playlist starts off as private, change settings later 
    playlistCreate = spotOA.user_playlist_create(user=spotOA.me()['id'],
                                              name=playlistTitle,
                                              public=False,
                                              description=playlistDes)['id']
    
    # puts in top 20
    spotOA.playlist_add_items(playlistCreate, trackURI)
    
    print("playlist made!")
    
    