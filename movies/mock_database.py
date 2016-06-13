


movies = ['Singin\' in the Rain (1952)','His Girl Friday (1938)', 'The Philadelphia Story (1940)', 'Vertigo (1958)', 'The Godfather: Part II (1974)', 'Blade Runner (1982)', 'GoodFellas (1990)',
'The Maltese Falcon (1941)', 'The Apartment (1960)', 'Schindler\'s List (1993)' ]

ids = [705,494, 478, 479, 187, 89, 182, 484, 1079, 318]

urls = [
"https://upload.wikimedia.org/wikipedia/en/f/f9/Singing_in_the_rain_poster.jpg",
"https://upload.wikimedia.org/wikipedia/en/1/1a/His_Girl_Friday_poster.jpg",
"https://upload.wikimedia.org/wikipedia/en/5/54/The-Philadelphia-Story-%281940%29.jpg",
"https://upload.wikimedia.org/wikipedia/commons/7/75/Vertigomovie_restoration.jpg",
"https://upload.wikimedia.org/wikipedia/en/0/03/Godfather_part_ii.jpg",
"https://upload.wikimedia.org/wikipedia/en/5/53/Blade_Runner_poster.jpg",
"https://upload.wikimedia.org/wikipedia/en/7/7b/Goodfellas.jpg",
"https://upload.wikimedia.org/wikipedia/en/9/99/Falconm.JPG",
"https://upload.wikimedia.org/wikipedia/en/b/bb/Apartment_60.jpg",
"https://upload.wikimedia.org/wikipedia/en/3/38/Schindler%27s_List_movie.jpg"
]

urls2 = ['http://ia.media-imdb.com/images/M/MV5BMTUxMTIyNTI4Nl5BMl5BanBnXkFtZTcwNTk1ODQyMg@@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BMTI3ODM3MDkzNl5BMl5BanBnXkFtZTcwMzgwNDUyMQ@@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BMjA2NzYzMjE3MF5BMl5BanBnXkFtZTgwNDExMDY0MzE@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BNzY0NzQyNzQzOF5BMl5BanBnXkFtZTcwMTgwNTk4OQ@@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BNDc2NTM3MzU1Nl5BMl5BanBnXkFtZTcwMTA5Mzg3OA@@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BMTA4MDQxNTk2NDheQTJeQWpwZ15BbWU3MDE2NjIyODk@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BMTY2OTE5MzQ3MV5BMl5BanBnXkFtZTgwMTY2NTYxMTE@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BMTc4MDEzOTMwMl5BMl5BanBnXkFtZTgwMTc2NjgyMjE@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BMTM1OTc4MzgzNl5BMl5BanBnXkFtZTcwNTE2NjgyMw@@._V1_SX300.jpg',
'http://ia.media-imdb.com/images/M/MV5BMzMwMTM4MDU2N15BMl5BanBnXkFtZTgwMzQ0MjMxMDE@._V1_SX300.jpg']

ratings = [4,4,4,4,5,4,5,4,4,5]

def make_dict(stuff):
	names = ['id','avgRating','title','url']
	return dict(zip(names,stuff))

mock_db = {'movies': [make_dict(i) for i in\
	zip(ids,ratings,movies,urls2)]}

small_mock_db = {'movies': [make_dict(i) for i in\
	zip(ids[:3],ratings,movies,urls2)]}

#print(mock_db)
