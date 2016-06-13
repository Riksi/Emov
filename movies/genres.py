genre_mapping_table= \
[[5, 1.0, 1.0],
[14, 0.75,0.75],
[17, 1.0, 0.25],
[18, 0.75, 0.5],
[8, 1.0, 0.5],
[11, 1.0, 0.0],
[6, 0.5, 0.25],
[9, 0.75, 0.5],
[1, 1.0, 0.5],
[12, 0.75, 0.75],
[15, 0.75, 0.5],
[16, 1.0, 0.5],
[10, 0.5,0.25],
[2, 1.0, 0.75],
[11,0.75,0.25],
[13,0.75,0.5]]

genre_nums = [[0, 'unknown'],
[1, 'Action'],
[2, 'Adventure'],
[3, 'Animation'],
[4, "Children's"],
[5, 'Comedy'],
[6, 'Crime'],
[7, 'Documentary'],
[8, 'Drama'],
[9, 'Fantasy'],
[10, 'Film-Noir'],
[11, 'Horror'],
[12, 'Musical'],
[13, 'Mystery'],
[14, 'Romance'],
[15, 'Sci-Fi'],
[16, 'Thriller'],
[17, 'War'],
[18, 'Western']]

not_included = {0,3,4,7}
genre_nums_map = dict(genre_nums)

genre_map = dict(map(lambda i: (i[0],\
	{'arousal':i[1],'valence':i[2]}),genre_mapping_table)) 

def parse_genres(gr_str):
	return list(map(lambda x: int(x),gr_str.split(',')))

def compute_scores(gr_str):
	dims = ['arousal','valence']
	genres = set(parse_genres(gr_str))
	genres = genres - genres.intersection(not_included)
	if genres:
		vals = list(map(lambda g: genre_map.get(g),genres))
		scores = [sum([i[dim] for i in vals])/len(genres) for dim in dims]
		#print(scores)
		return(scores)

def best_score(aro,val,scores):
	#print(list(map(lambda s: (aro-s[0])**2 + (val-s[1])**2 if s else 3,scores)))
	return scores.index(min(scores,key = lambda s: (aro-s[0])**2 + (val-s[1])**2 if s else 3))

