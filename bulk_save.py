import csv
from movies.models import Movie

print('saving')
movies = csv.reader(open('./movie_data.csv'))
movies_to_save = []

for m in movies:
	movie = Movie(movie_no = int(m[0]),name = m[1])
	movies_to_save.append(movie)

Movie.objects.bulk_create(movies_to_save)