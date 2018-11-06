from getnextmovie import MovieSeasonAndEpisodeExtractor

msae = MovieSeasonAndEpisodeExtractor()
(season, episode, folder) = msae.parseLastMovie()

print ("Season: " + str(season))
print ("Episode: " + str(episode))
print ("Folder: " + str(folder))

next_suggested_movie = msae.getNextMovie()

print()
print ("Next suggestion: " + str(next_suggested_movie))
