#!/usr/bin/python

import os
import shutil
import fnmatch
import re
import unittest
import glob

from os.path import expanduser
from subprocess import Popen, PIPE

kodi_log = expanduser("~") + "/.kodi/temp/kodi.log"


class MovieSeasonAndEpisodeExtractor(object):
    def __init__(self):
        self.last_movie = ""

    def readLog(self, kodi_log_file=kodi_log):
        last_movies = []
        with open(kodi_log_file) as f:
            for line in f.readlines():
                m = re.search('.*VideoPlayer::OpenFile: (.*)', line)
                if m is not None:
                    last_movies.append(str(m.group(1)))
        self.last_movie = last_movies[-1]

    def parseLastMovie(self):
        m = re.search('(.*)([sS][0-9]+)(\.*)([eE][0-9]+)(.*)', self.last_movie)
        if m is not None:
            self.prefix = m.group(1) + m.group(2) + m.group(3) + m.group(4)
            (self.season, self.episode, self.folder) = (
                m.group(2), m.group(4), m.group(1))
            self.folder = self.folder[:self.folder.rfind('/')]
            return (self.season, self.episode, self.folder)

    def reset(self, season, folder, prefix):
        self.season = season
        self.folder = folder
        self.prefix = prefix
        self.episode = "E00"

    def getNextMovie(self, debug=False):
        full_suggestion = self.getPotentialNextMovie()

        folder_suggestion = full_suggestion[:full_suggestion.rfind("/")]
        file_suggestion = full_suggestion[full_suggestion.rfind("/") + 1:]

        if (debug):
            print("")
            print("Folder Suggestion:" + folder_suggestion)
            print("File   Suggestion:" + file_suggestion + "*.*")

        for file in os.listdir(folder_suggestion):
            if fnmatch.fnmatch(file, file_suggestion + "*.*"):
                return folder_suggestion + "/" + file
        if (debug):
            print("No match found, seeking to next season..")

        (next_season, next_season_folder) = self.getNextSeasonFolder()
        if (debug):
            print("\nseeking in: " + next_season_folder)

        if next_season is not None and next_season_folder is not None:
            if(debug):
                print("\nresetting season to: " + next_season)
            next_prefix = next_season_folder + "/*" + next_season + "*E00*.*"
            self.reset(next_season, next_season_folder, next_prefix)
            return self.getNextMovie(debug)

    def getNextSeasonFolder(self):
        potential_next_season = self.getPotentialNextSeason()

        next_season_folder_list = glob.glob(
            self.folder + "/../*" + potential_next_season + "*")
        if next_season_folder_list is not None:
            return (potential_next_season, os.path.abspath(next_season_folder_list[0]))
        return (None, None)

    def getPotentialNextSeason(self):
        prefix = "S"
        next_season = int(self.season[1:]) + 1
        if(next_season < 10):
            next_season = "0" + str(next_season)
        return prefix + next_season

    def getPotentialNextMovie(self):
        next_episode = int(self.episode[1:]) + 1
        if(next_episode < 10):
            next_episode = "0" + str(next_episode)

        pos_episode = self.prefix.find(self.episode) + 1
        head = self.prefix[:pos_episode]

        return head + str(next_episode)
