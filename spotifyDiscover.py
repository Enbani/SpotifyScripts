#Spotify Daily App v 1.0

import sys
import random
import spotipy
import spotipy.util as util
import simplejson as json



#define scope, import keys, and authenticate
scopes = "user-top-read playlist-modify-public"
clientID = '[insert client ID]'
clientSecret = '[insert client secret ID]'
redirectURI = "https://play.spotify.com/user"

#username provided as a system argument
username = sys.argv[1]

token = util.prompt_for_user_token(username, scopes, clientID, clientSecret, redirectURI)

#check to see if token is good, else exit
if token:
	sp = spotipy.Spotify(auth=token)
	sp.trace = False
	
else:
	print "Can't get token for %s" %username
	sys.exit(0)



def userTopTracks():
    '''userTopTracks() will return a dictionary of song names: song IDs.'''
    tracksDictionary = {}
    timeRange = ['short_term', 'medium_term']
	
    for period in timeRange:
	    topTracks = sp.current_user_top_tracks(limit=20, time_range=period)
	    topTracksItems = topTracks['items']

	    for item in topTracksItems:
	        songName = item['name']
	        songID = item['id']
	        tracksDictionary[songName] = songID
	  
    return tracksDictionary


def randomizer(tracksDict):
    '''randomizer() takes a dictionary as input, intended to be the return
    value of userTopTracks(). Function will output a list of Spotify song IDs.'''
    seeds = []
    i = 1
    
    while i <= 5:
        seeds.append(random.choice(tracksDict.values()))
        i += 1
        
    return seeds


def recommendations(seeds):
    '''recommendations() takes a list of seed tracks and returns a list of
    recommended songs. Max seeds = 5.'''
    playlistTracks = []
    recJson = sp.recommendations(seed_tracks=seeds, limit=15, country="US")
    recTracks = recJson['tracks']
    
    for item in recTracks:
        playlistTracks.append(item['id'])

    return playlistTracks

 
def checkPlaylist(playlistTracks, username):
    '''checkPlaylist() checks to see if a playlist with given name exists.
    If so, utilizes playlist ID and adds tracks. If not, creates playlist
    and adds tracks.'''
    playlistName = "Age of Automation" #or whatever you want to call it
    playlists = sp.user_playlists(username)
    playlistFound = False
    
    for playlist in playlists['items']:
        if playlist['name'] == playlistName:
            playlistID = playlist['id']
            playlistFound = True
            break
 
        
    if playlistFound == True:
        sp.user_playlist_replace_tracks(username, playlistID, playlistTracks)
        
    else:
        newPlaylist = sp.user_playlist_create(username, "Age of Automation")
        playlistID = newPlaylist['id']
        sp.user_playlist_add_tracks(username, playlistID, playlistTracks)
        
    print "\n\n...Playlist tracks added successfully.\n\n"


    
songs = userTopTracks()
seeds = randomizer(songs)
recommendedTracks = recommendations(seeds)
checkPlaylist(recommendedTracks, username)
    
    

		 
	




