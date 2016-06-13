from movies.models import Genres, Movie
file = open('c:/users/anush/web_dev/emov/mysite/allmovies.txt','rb')
m = file.readlines()
m2 = [i.replace(b'\r\n',b'') for i in m]
m3 = [i[-38:] for i in m2]
g = [i.split(b'|')[1:] for i in m3]
gr = [[j for j in range(19) if i[j] == b'1'] for i in g]
gr_str = [','.join(map(str,i)) for i in gr]
for i in range(len(gr_str)):
	gnr = Genres(movie= Movie.objects.get(id=i+1),genres=gr_str[i])
	gnr.save()
