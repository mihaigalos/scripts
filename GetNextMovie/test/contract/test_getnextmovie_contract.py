import unittest
from unittest import TestCase
from getnextmovie import MovieSeasonAndEpisodeExtractor

import os
import shutil
import fnmatch
import re


class ContractBase(unittest.TestCase):
    def setUp(self):
        self.me = MovieSeasonAndEpisodeExtractor()


class NextSuggestionWorks(ContractBase):

    def test_whenTypicalFolder(self):
        self.me.last_movie = "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
        (season, episode, folder) = self.me.parseLastMovie()
        next_suggested_movie = self.me.getPotentialNextMovie()
        self.assertEqual(
            next_suggested_movie, '/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E10')

    def test_whenTypicalFolderDot(self):
        self.me.last_movie = "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06.E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
        (season, episode, folder) = self.me.parseLastMovie()
        next_suggested_movie = self.me.getPotentialNextMovie()
        self.assertEqual(
            next_suggested_movie, '/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06.E10')


if __name__ == '__main__':
    unittest.main()
