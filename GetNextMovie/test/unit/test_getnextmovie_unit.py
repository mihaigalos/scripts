import unittest
from unittest import TestCase
from getnextmovie import MovieSeasonAndEpisodeExtractor

class ParsingWorks(unittest.TestCase):
     def setUp(self):
         self.me = MovieSeasonAndEpisodeExtractor()

     def test_whenTypicalFolder(self):
         self.me.last_movie = "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
         (season, episode, folder) = self.me.parseLastMovie()
         self.assertEqual(folder,'/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD')

     def test_whenTypicalUppercase(self):
        self.me.last_movie = "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
        (season, episode, folder) = self.me.parseLastMovie()
        self.assertEqual(season,'S06')
        self.assertEqual(episode,'E09')

     def test_whenTypicalLowercase(self):
        self.me.last_movie = "/media/Seagate_2TB/Series/Game.of.Thrones.s06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.s06e09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
        (season, episode, folder) = self.me.parseLastMovie()
        self.assertEqual(season,'s06')
        self.assertEqual(episode,'e09')

     def test_whenTypicalWithDotUppercase(self):
         self.me.last_movie = "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06.E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
         (season, episode, folder) = self.me.parseLastMovie()
         self.assertEqual(season,'S06')
         self.assertEqual(episode,'E09')

     def test_whenTypicalWithDotLowercase(self):
         self.me.last_movie = "/media/Seagate_2TB/Series/Game.of.Thrones.s06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.s06.e09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
         (season, episode, folder) = self.me.parseLastMovie()
         self.assertEqual(season,'s06')
         self.assertEqual(episode,'e09')

if __name__ == '__main__':
    unittest.main()
