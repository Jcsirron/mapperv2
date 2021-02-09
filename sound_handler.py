#!/usr/bin/env python
"""
sound_handler.py
Created by Chandler Norris May 2, 2020

This is a basic sound handler to consolidate all sounds into one place.
"""
from pygame import mixer
from os import path

if not mixer.get_init():
    mixer.init()

SOUND_FOLDER = "data\\Sounds"
SOUND_VOLUME = 1.0
MAX_SOUNDS = 2
# This is the sound list that you will add sounds to.  It needs to load
# EX: SOUND_LIST = {"test": mixer.Sound(path.join(SOUND_FOLDER, "horn.mp3"))}
SOUND_LIST = {}


def play_sound(sound, loops=1):
    if sound in SOUND_LIST:
        if SOUND_LIST[sound].get_num_channels() < MAX_SOUNDS:
            SOUND_LIST[sound].set_volume(SOUND_VOLUME)
            SOUND_LIST[sound].play(loops)


def stop_sound(sound):
    if sound in SOUND_LIST:
        SOUND_LIST[sound].stop()


def set_sound_volume(volume):
    global SOUND_VOLUME
    if volume > 1.0:
        SOUND_VOLUME = 1.0
    elif 1.0 > volume > 0.0:
        SOUND_VOLUME = volume
    else:
        SOUND_VOLUME = 0


def add_sound(sound_name, sound_filename):
    global SOUND_LIST
    global SOUND_FOLDER
    if sound_name not in SOUND_LIST:
        SOUND_LIST[sound_name] = mixer.Sound(path.join(SOUND_FOLDER, sound_filename))
    else:
        print(str(sound_name) + " is already in the song list!")


def remove_sound(sound_name):
    global SOUND_LIST
    if sound_name in SOUND_LIST:
        del SOUND_LIST[sound_name]
    else:
        print(str(sound_name) + " is not in the song list!")
