#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 15:02:58 2016

@author: antonyr
"""
import pandas as pd
from spotimy import Spotimy


sp = Spotimy()

# the LIKED playlist has 325 tracks
# I broke the main playlist up in to subplaylists consisting of 100 tracks or fewer  (100, 100, 100, 35)
    # as Spotify has a 100 limit for returned tracks from a playlist
sub_liked_playlist_ids = ["6VryOLabHojfgIyyKOmuEt", "1BSNZpUP6JN2jRytOcfoEk", "4RYw2n1Dfd19Emf79maPNw", "6fDgbzrQnk1CGNGBZ3rXHK"]
# I did the same thing for the 325 tracks in the REJECTED playlist
sub_rejected_playlist_ids = ["20IzzIq6R5mEKG24XsISNv", "2cV6PaCbsu0DhE4YwwBSvx", "0x0GmfReSi26ZrtWj0LftG", "4tFephURinCd9IpNE5kcK0"]

df = None

for playlist in sub_liked_playlist_ids:
    df_liked = sp.get_tracks_from_playlist(playlist)
    df = pd.concat([df,df_liked], ignore_index=True)

for playlist in sub_rejected_playlist_ids:
    df2 = sp.get_tracks_from_playlist(playlist, liked=False)  # mark playlist as not "liked"
    df = pd.concat([df,df2], ignore_index=True)

df.to_csv('spotify_liked_rejected.csv', index=False)

