import unittest
from unittest import TestCase
from getnextmovie import MovieSeasonAndEpisodeExtractor

import os
import shutil
import fnmatch
import re


class FileFactory(unittest.TestCase):
    def createFolderStructure(self):
        self.kodi_test_folder = "test_MovieSeasonAndEpisodeExtractor"
        self.kodi_log_file = "kodi.log"
        location = os.path.join(self.kodi_test_folder, "media", "Seagate_2TB",
                                "Series", "Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD")
        if(os.path.isdir(location)):
            shutil.rmtree(location)
        os.makedirs(location)

        location = os.path.join(self.kodi_test_folder, "media", "Seagate_2TB",
                                "Series", "Game.of.Thrones.S07.720p.HDTV.H264.RoSubbed-playTV")
        if(os.path.isdir(location)):
            shutil.rmtree(location)
        os.makedirs(location)

    def createDemoFiles(self):
        files = [self.kodi_test_folder + "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E08.No.One.720p.BluRay.DD5.1.x264-CtrlHD.mkv",
                 self.kodi_test_folder + "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv",
                 self.kodi_test_folder + "/media/Seagate_2TB/Series/Game.of.Thrones.S07.720p.HDTV.H264.RoSubbed-playTV/Game.of.Thrones.S07E01.720p.HDTV.H264.RoSubbed-playTV.mp4"]

        for file in files:
            with open(file, "w") as f:
                f.close()

    def createLogFile(self):
        kodi_log = """19:51:50.179 T:1584132864  NOTICE: Closing stream player 3
19:51:50.184 T:1926138368  NOTICE: VideoPlayer: finished waiting
19:51:50.242 T:1926138368  NOTICE: VideoPlayer: Opening: """ + self.kodi_test_folder + """/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E08.No.One.720p.BluRay.DD5.1.x264-CtrlHD.mkv
19:51:50.243 T:1438765824  NOTICE: Creating InputStream
19:51:50.259 T:1438765824  NOTICE: Creating Demuxer
20:56:22.257 T:1387262720  NOTICE: thread end: video_thread
20:56:22.259 T:1438765824  NOTICE: deleting video codec
20:56:22.270 T:1438765824  NOTICE: Closing stream player 3
20:56:22.369 T:1926138368  NOTICE: VideoPlayer: finished waiting
20:56:22.429 T:1926138368  NOTICE: VideoPlayer::OpenFile: """ + self.kodi_test_folder + """/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"""
        with open(self.kodi_test_folder + "/" + self.kodi_log_file, "w") as f:
            f.write(kodi_log)
            f.flush()
            f.close()

    def setUp(self):
        self.me = MovieSeasonAndEpisodeExtractor()
        self.createFolderStructure()
        self.createLogFile()
        self.createDemoFiles()

    def tearDown(self):
        shutil.rmtree(self.kodi_test_folder)
        pass


class NextSemanticSuggestionWorks(FileFactory):
    def test_whenFileExists(self):
        self.me.last_movie = self.kodi_test_folder + \
            "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E08.No.One.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
        (season, episode, folder) = self.me.parseLastMovie()
        next_suggested_movie = self.me.getNextMovie()
        self.assertEqual(next_suggested_movie, self.kodi_test_folder
                         + '/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv')

    def test_whenFileDoesntExists(self):
        self.me.last_movie = self.kodi_test_folder + \
            "/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv"
        (season, episode, folder) = self.me.parseLastMovie()
        next_suggested_movie = self.me.getNextMovie()
        self.assertTrue(
            "Game.of.Thrones.S07E01.720p.HDTV.H264.RoSubbed-playTV.mp4" in next_suggested_movie)


class NextSuggestionWorks(FileFactory):

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


class ReadLogWorks(FileFactory):
    def test_whenTypical(self):
        self.me.readLog(self.kodi_test_folder + "/" + self.kodi_log_file)
        self.me.parseLastMovie()
        self.assertEqual(self.me.last_movie, self.kodi_test_folder
                         + '/media/Seagate_2TB/Series/Game.of.Thrones.S06.720p.BluRay.DD5.1.x264-CtrlHD/Game.of.Thrones.S06E09.Battle.of.the.Bastards.720p.BluRay.DD5.1.x264-CtrlHD.mkv')


if __name__ == '__main__':
    unittest.main()
