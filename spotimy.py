# -*- coding: utf-8 -*-

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd


class Spotimy():

    def __init__(self):
        scope = 'user-library-read playlist-read-private'
        self.username = "hisbiz"
        
        #### my login credentials ####
        my_client_id = '22aa229b6d674b0c908efac5542e23a9'
        my_client_secret = '008a67ef1fb14ab3b6a2fe2d786c4a8e'
        my_redirect_url='http://localhost/~antonyr/spotimy/callback'
        
        token = util.prompt_for_user_token(self.username, scope, client_id=my_client_id, client_secret=my_client_secret, redirect_uri=my_redirect_url)
        client_credentials_manager = SpotifyClientCredentials(my_client_id, my_client_secret) 
        
        

        try:
            if token:
                self.spotify = spotipy.Spotify(auth=token, client_credentials_manager=client_credentials_manager)  # spotify object
            else:
                raise ValueError("Token not returned.")
        except ValueError:
            print("Can't get token for {}".format(self.username))
            raise
    
    def get_track_data(self, track_id, liked = True):
        self.track = self.spotify.track(track_id)
        self.track_features = self.spotify.audio_features([track_id])[0]  # <-- returns a list with one element (a dict) so '[0]' is used to access the dict with the track's features
        self.track_analysis = self.spotify._get(self.track_features['analysis_url'])  # 'analysis_url' is the location of the specific audio analysis; returns the analysis fetaures
        
        seg_duration, pitches_array, timbre_array, loudness_max, loudness_max_time = self.get_segments_arrays()
        sect_duration, sect_tempo, sect_loudness, sect_key  = self.get_sections_arrays()
        sect_key_count_array, sect_key_percentage_array = self.get_sections_key_percentage(sect_key)
        print(sect_key)
        #print(sect_key_count_array)
        track_data = []

        # 275 features
        cols1 = ["Song", "ID", "Popularity", "Duration(ms)", "Duration", "Artist", "Artist ID", "Artist Popularity", "Artist Genres"]
        cols2 = ["Album", "Album ID", "Album Popularity", "Loudness", "Time Signature", "Tempo"]
        cols3 = ["Mode", "Danceability", "Energy", "Valence", "Key"]
        cols4 = ["#Segments", "Seg Dur Mean", "Seg Dur Var", "Seg Dur Med", "Seg Dur Min", "Seg Dur Max", "Seg Dur Rng", "Seg Dur Skew", "Seg Dur Kurt"]
        cols5 = ["P0_Mn","P1_Mn","P2_Mn","P3_Mn","P4_Mn","P5_Mn","P6_Mn","P7_Mn","P8_Mn","P9_Mn","P10_Mn", "P11_Mn"]
        cols6 = ["P0_Vr","P1_Vr","P2_Vr","P3_Vr","P4_Vr","P5_Vr","P6_Vr","P7_Vr","P8_Vr","P9_Vr","P10_Vr", "P11_Vr"]
        cols7 = ["P0_Med","P1_Med","P2_Med","P3_Med","P4_Med","P5_Med","P6_Med","P7_Med","P8_Med","P9_Med","P10_Med", "P11_Med"]  
        cols8 = ["P0_Min","P1_Min","P2_Min","P3_Min","P4_Min","P5_Min","P6_Min","P7_Min","P8_Min","P9_Min","P10_Min", "P11_Min"]
        cols9 = ["P0_Max","P1_Max","P2_Max","P3_Max","P4_Max","P5_Max","P6_Max","P7_Max","P8_Max","P9_Max","P10_Max", "P11_Max"]
        cols10 = ["P0_Rng","P1_Rng","P2_Rng","P3_Rng","P4_Rng","P5_Rng","P6_Rng","P7_Rng","P8_Rng","P9_Rng","P10_Rng", "P11_Rng"]
        cols11 = ["P0_Skw","P1_Skw","P2_Skw","P3_Skw","P4_Skw","P5_Skw","P6_Skw","P7_Skw","P8_Skw","P9_Skw","P10_Skw", "P11_Skw"]
        cols12 = ["P0_Krt","P1_Krt","P2_Krt","P3_Krt","P4_Krt","P5_Krt","P6_Krt","P7_Krt","P8_Krt","P9_Krt","P10_Krt", "P11_Krt"]
        cols13 = ["T0_Mn","T1_Mn","T2_Mn","T3_Mn","T4_Mn","T5_Mn","T6_Mn","T7_Mn","T8_Mn","T9_Mn","T10_Mn", "T11_Mn"]
        cols14 = ["T0_Vr","T1_Vr","T2_Vr","T3_Vr","T4_Vr","T5_Vr","T6_Vr","T7_Vr","T8_Vr","T9_Vr","T10_Vr", "T11_Vr"]
        cols15 = ["T0_Med","T1_Med","T2_Med","T3_Med","T4_Med","T5_Med","T6_Med","T7_Med","T8_Med","T9_Med","T10_Med", "T11_Med"]
        cols16 = ["T0_Min","T1_Min","T2_Min","T3_Min","T4_Min","T5_Min","T6_Min","T7_Min","T8_Min","T9_Min","T10_Min", "T11_Min"]
        cols17 = ["T0_Max","T1_Max","T2_Max","T3_Max","T4_Max","T5_Max","T6_Max","T7_Max","T8_Max","T9_Max","T10_Max", "T11_Max"]
        cols18 = ["T0_Rng","T1_Rng","T2_Rng","T3_Rng","T4_Rng","T5_Rng","T6_Rng","T7_Rng","T8_Rng","T9_Rng","T10_Rng", "T11_Rng"]
        cols19 = ["T0_Skw","T1_Skw","T2_Skw","T3_Skw","T4_Skw","T5_Skw","T6_Skw","T7_Skw","T8_Skw","T9_Skw","T10_Skw", "T11_Skw"]
        cols20 = ["T0_Krt","T1_Krt","T2_Krt","T3_Krt","T4_Krt","T5_Krt","T6_Krt","T7_Krt","T8_Krt","T9_Krt","T10_Krt", "T11_Krt"]
        cols21 = ["LoudMax Mn", "LoudMax Var", "LoudMax Med", "LoudMax Min", "LoudMax Max", "LoudMax Rng", "LoudMax Skew", "LoudMax Kurt"]
        cols22 = ["LoudMaxTime Mn", "LoudMaxTime Var", "LoudMaxTime Med", "LoudMaxTime Min", "LoudMaxTime Max", "LoudMaxTime Rng", "LoudMaxTime Skew", "LoudMaxTime Kurt"]    
        cols23 = ["#Sections", "Sect Dur Mean", "Sect Dur Var", "Sect Dur Med", "Sect Dur Min", "Sect Dur Max", "Sect Dur Rng", "Sect Dur Skew", "Sect Dur Kurt"]
        cols24 = ["Sect Tmpo Mean", "Sect Tmpo Var", "Sect Tmpo Med", "Sect Tmpo Min", "Sect Tmpo Max", "Sect Tmpo Rng", "Sect Tmpo Skew", "Sect Tmpo Kurt"]
        cols25 = ["Sect Loud Mean", "Sect Loud Var", "Sect Loud Med", "Sect Loud Min", "Sect Loud Max", "Sect Loud Rng", "Sect Loud Skew", "Sect Loud Kurt"]
        cols26 = ["C", "C#/Df", "D", "D#/Ef", "E", "F", "F#/Gf", "G", "G#/Af", "A", "A#/Bf", "B", "Liked"]
        self.column_names = cols1 + cols2 + cols3 + cols4 + cols5 + cols6 + cols7 + cols8 + cols9 + cols10 + cols11 + cols12 + cols13
        self.column_names += cols14 + cols15 + cols16 + cols17 + cols18 + cols19 + cols20 + cols21 + cols22 + cols23 + cols24 + cols25 + cols26
        
        # mean, variance, median, min, max, value range, skewness, kurtosis
        
        
        # FEATURES (248): Segments Timbre, Pitches, Loudness Max, Loudness Max Time, Duration
                    # Sections Duration, Loudness, Tempo, Key
        # STATISTICAL MEASURES: mean, median, variance, min, max, value range, skewness, kurtosis
        
        track_data.append(self.track["name"])
        track_data.append(self.track["id"])
        track_data.append(self.track["popularity"])
        track_data.append(self.track["duration_ms"])
        track_data.append(self.ms_to_minutes(self.track["duration_ms"]))
        track_data.append(self.track["artists"][0]["name"])
        track_data.append(self.track["artists"][0]["id"])
        track_data.append(self.spotify._get(self.track["artists"][0]["href"])["popularity"])    # 'href' will return a full artist object (which contains popularity/genres)
        track_data.append(self.spotify._get(self.track["artists"][0]["href"])["genres"])
        track_data.append(self.track["album"]["name"])
        track_data.append(self.track["album"]["id"])
        track_data.append(self.spotify._get(self.track["album"]["href"])["popularity"])
        track_data.append(self.track_features["loudness"])
        track_data.append(self.track_features["time_signature"])
        track_data.append(self.track_features["tempo"])
        track_data.append(self.track_features["mode"])
        track_data.append(self.track_features["danceability"])
        track_data.append(self.track_features["energy"])
        track_data.append(self.track_features["valence"])
        track_data.append(self.track_features["key"])
        
        track_data.append(len(self.track_analysis["segments"]))
        track_data.extend(self.get_statistical_measures(seg_duration))
        track_data.extend(self.get_statistical_measures(pitches_array))
        track_data.extend(self.get_statistical_measures(timbre_array))
        track_data.extend(self.get_statistical_measures(loudness_max_time))
        track_data.extend(self.get_statistical_measures(loudness_max))
        
        track_data.append(len(self.track_analysis["sections"]))
        track_data.extend(self.get_statistical_measures(sect_duration))
        track_data.extend(self.get_statistical_measures(sect_tempo))
        track_data.extend(self.get_statistical_measures(sect_loudness))
        track_data.extend(sect_key_percentage_array)

        if liked:
            track_data.append(1)
        else:
            track_data.append(0)
            
        return track_data  # returns a list: the track/song "data" in a list

    def get_segments_arrays(self):
        segment_pitches = []   # returns a list of lists(12 items per list per segment)
        segment_timbre = []    # returns a list of lists (12 items per list per segment)
        segment_durations = []
        segment_loudness_max = []
        segment_loudness_max_time = []
        for segment in self.track_analysis["segments"]:
            segment_pitches.append(segment["pitches"]) # appending a 12-d array
            segment_timbre.append(segment["timbre"])   # appending a 12-d array
            segment_durations.append(segment["duration"])  
            segment_loudness_max.append(segment["loudness_max"]) 
            segment_loudness_max_time.append(segment["loudness_max_time"])  
        return  np.array(segment_durations), np.array(segment_pitches), np.array(segment_timbre), np.array(segment_loudness_max), np.array(segment_loudness_max_time)
              
    def get_sections_arrays(self):
        section_loudness = []
        section_tempos = []
        section_keys = []
        section_durations = []
        for section in self.track_analysis["sections"]:
            section_loudness.append(section["loudness"])
            section_tempos.append(section["tempo"])
            section_keys.append(section["key"])
            section_durations.append(section["duration"])
        return np.array(section_durations), np.array(section_tempos), np.array(section_loudness), np.array(section_keys)
          

    def get_sections_key_percentage(self, sections_key):     # returns a numpy array
        number_of_different_keys = 12  # counting from 0 through 11, C = 0 ... B = 11       # example input: [6, 6, 6, 10, 10, 6, 10, 1, 10, 6, 3]  <-- 11 sections with key per section
        key_count_array = np.bincount(sections_key, minlength=number_of_different_keys) # e.g., [0, 1, 0, 1, 0 , 0, 5, 0, 0, 0, 4, 0]   /  11
        key_percentage_array = key_count_array/len(sections_key)  # e.g., (?)[ 0., 0.08333333, 0., 0.08333333, 0., 0., 0.41666667, 0., 0., 0., 0.33333333, 0.]
        #[0, .09090909, 0, .09090909, 0, 0, 0.36363636, 0, 0, 0, .45454545]
        return key_count_array, key_percentage_array     # counting from index 0 as the keys being 1 through 12 (not 0 through 11)
        
    def get_statistical_measures(self, arr):
        from scipy.stats import skew, kurtosis
        functions = [np.mean, np.var, np.median, np.min, np.max, np.ptp, skew, kurtosis]
        if arr.ndim > 1:   
            array_of_arrays = []
            for f in functions:
                array_of_arrays.append(f(arr, axis=0))  # 2d array aggregated to a 1d array, then appended to an array
            return np.concatenate(array_of_arrays)  # return a "flattened" 1d array
        # 1d array aggregated to a tuple of scalars
        return arr.mean(axis=0), arr.var(axis=0), np.median(arr, axis=0), arr.min(axis=0), arr.max(axis=0), arr.ptp(axis=0), skew(arr, axis=0), kurtosis(arr, axis=0)
        # mean, variance, median, min, max, value range, skewness, kurtosis
        
    def min_max_mean_mode(self, arr):
        from scipy.stats.mstats import mode
        mode, mode_cnt = mode(arr)  # mode returns the mode and the number of occurences of the mode item as singleton arrays
        return arr.min(), arr.max(), arr.mean(), arr.std(), mode[0], mode_cnt[0]    
    
    def ms_to_minutes(self, ms):
        total_secs = ms/1000
        minutes = int(total_secs//60)
        seconds = round(total_secs%60)
        return str(minutes) + ":" + '{:02}'.format(seconds)    
    
    def get_tracks_from_playlist(self, playlist_id, liked=True):
        playlist_obj = self.spotify.user_playlist(self.username, playlist_id, fields="tracks, next" )
        playlist_track_object = playlist_obj["tracks"]
        playlist_tracks_data = []
        for item in playlist_track_object["items"]:
            playlist_tracks_data.append(self.get_track_data(item["track"]["id"], liked=liked))
        playlist_tracks_dataframe = pd.DataFrame(playlist_tracks_data, columns=self.column_names)
        return playlist_tracks_dataframe   # returns a pandas DataFrame containing the data from each track in the given playlist (Spotify imposes a limit of returning only 100 tracks)
    
    def get_genres(self, dataframe, genres_column):
        import collections
        df = dataframe[genres_column].values
        genres_count = collections.Counter(np.concatenate(df, axis=1)) #flattens the array of arrays and gets the frequency count of the genres
        return genres_count


        
        
        
       
        
        
        