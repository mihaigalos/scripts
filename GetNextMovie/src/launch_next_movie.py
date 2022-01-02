#!/usr/bin/python

import subprocess
from getnextmovie import MovieSeasonAndEpisodeExtractor


def get_next_movie():
    msae = MovieSeasonAndEpisodeExtractor()
    msae.readLog()
    (season, episode, folder) = msae.parseLastMovie()
    next_suggested_movie = msae.getNextMovie()
    return next_suggested_movie


next_movie = get_next_movie()

args = ["kodi-send", "--action=PlayMedia(" + next_movie + ")"]
#print(" ".join(args))
subp = subprocess.Popen(args)
out = subp.communicate()[0]
