from django.contrib.auth.models import User
from movies.models import Rating, Movie
ratings = {1: [i for i in range(0,20)],
			2: [i for i in range(0,5)],
			3: [i for i in range(0,10)]}

print('adding ratings')

for i in ratings:
	u = User.objects.create_user(str(i),str(i)+'@z.com',str(i)*10)
	u.save()
	for j in ratings[i]:
		m = Movie.objects.get(movie_no = j+1)
		r = Rating(user_id = u,movie_id = m, rating = 5)
		r.save()
