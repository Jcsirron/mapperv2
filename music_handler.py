#!/usr/bin/env python
"""
music_handler.py
Created by Chandler Norris May 2, 2020

This is a basic pygame music handling program to ease using the music module.
"""
from pygame import mixer
from os import path


MUSIC_FOLDER = "data\\Music"
MUSIC_VOLUME = 1.0
# This is the dictionary where you can refer to songs without needing to know the exact song name
# play_song() only needs a string reference to the song, since it will load it before playing it.
# EX: songs = {"test": "The_Horde_Sample.mp3"}
songs = {}


def play_song(song=None, loops=0, queue=False):
    if song in songs:
        mixer.music.set_volume(MUSIC_VOLUME)
        if queue is True:
            queue_file = path.join(MUSIC_FOLDER, songs[song])
            # music.queue() will only work if there is a song playing.
            if mixer.music.get_busy():
                mixer.music.queue(queue_file)
            else:
                mixer.music.load(path.join(MUSIC_FOLDER, songs[song]))
        else:
            mixer.music.load(path.join(MUSIC_FOLDER, songs[song]))
            if mixer.music.get_busy():
                mixer.music.stop()
            mixer.music.play(loops)


def set_song_volume(volume=1.0):
    global MUSIC_VOLUME
    if volume > 1.0:
        MUSIC_VOLUME = 1.0
    elif 1.0 > volume > 0.0:
        MUSIC_VOLUME = volume
    else:
        MUSIC_VOLUME = 0


def add_song(song_name, song_filename):
    global songs
    if song_name not in songs:
        songs[song_name] = song_filename
    else:
        print(str(song_name) + " is already in the song list!")


def remove_song(song_name):
    global songs
    if song_name in songs:
        del songs[song_name]
    else:
        print(str(song_name) + " is not in the song list!")
