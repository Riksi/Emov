from .models import Rating, Movie, Genres
from .pnn import PNN
from .cofi import Cofi
from django.db.models import Count,Avg
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from .mock_database import mock_db,small_mock_db
import movies.genres as genres
import random
import os
import json
import requests 
import re

NUM_MOVIES = 1682
PNN_SIGMA = {'arousal': 1,'valence':9}

def eeg_handler(request):
	if request.method == 'POST':
		data = json.loads(request.POST.get('data'))
		if data['simulate']:
				example = fetch_mock_eeg()
		else:
			example = request.POST['eeg']
		return JsonResponse(obtain_predictions(example,True))

def static_data_path(filename):
	return os.path.join(os.getcwd(),'movies/static/%s'%filename)

def fetch_mock_eeg():
	eegfile = open(static_data_path('psd_test.txt'))
	eeg = np.loadtxt(eegfile)
	row = random.randrange(0,eeg.shape[0])
	return np.array([eeg[row,:]])

def obtain_predictions(example,simulate=False):
	if simulate:
		ex = example
	else:
		ex = process_data(example)
	cats = ['arousal','valence']
	return dict(zip(cats,[int(predict_emot(cat,load_eeg_data(cat),ex)) for cat in cats]))

def predict_emot(category,data,example):
	features,labels = data
	p = PNN(2,PNN_SIGMA[category],example,features,labels+1)
	pred = p.predict()[0][0]
	return pred

def process_data(data):
	return(np.array(data))

def load_eeg_data(category):
	features = np.loadtxt(static_data_path('psd_train.txt'))
	labels = np.loadtxt(static_data_path('%s_train.txt'%category[:3]))
	return features,labels

def retrieve_movies(request):
	return JsonResponse(mock_db)

def main_page(request):
	return render(request,'movies/front_end.html')

def prediction_handler(request):
	if request.method == 'POST':
		eeg = request.POST['eeg']
		return JsonResponse({'arousal':1,'valence':1})

def receive_ratings(request):
	if request.method == 'POST':
		data = json.loads(request.POST.get('data'))
		ratingsData = data['ratings']
		r = fetch_recms(ratingsData)
		movie_id = filter_by_genre(r,*emo_values([data['arousal'],data['valence']],data['match']))
		movie = Movie.objects.get(id = movie_id)
		return JsonResponse({'data':fetch_movie_api_data(movie.name)});

def emo_values(dims,match):
	vals = list(map(lambda x:1*(x>=5) if match else 1*(x<5),dims))
	return vals

def fetch_movie_api_data(name):
	name = name[:name.find('(19')]
	s = re.search(r', [A|The|An]', name)
	if s:
		st = s.start()
		name = name[st+2:s.endpos] + ' '+ name[:st]
	data = requests.get("http://www.omdbapi.com/?t=%s&y=&plot=short&r=json"%name)
	return data.json()


def process_ratings(data):
	intkeys = map(lambda i: int(i),data.keys())
	return dict(zip(intkeys,data.values()))

def vectorize_ratings(ratings):
	y = np.array([[ratings.get(i+1) or 0 for i in range(NUM_MOVIES)]],dtype='int32')
	r = 1*(y>0)
	return y.T,r.T

def load_ratings_data():
	Y = np.loadtxt(static_data_path('Ymatrix.txt'))
	R = np.loadtxt(static_data_path('Rmatrix2.txt'))
	return Y,R

def add_user_ratings(Y,R,y,r):
	Y2 = np.concatenate((Y,y),axis=1)
	R2 = np.concatenate((R,r),axis=1)
	return Y2, R2

def fetch_recms(data):
	ratings_dict = process_ratings(data)
	Y,R = add_user_ratings(*load_ratings_data(),*vectorize_ratings(ratings_dict))
	return compute_recms(Y,R)

def compute_recms(Y,R):
	cf = Cofi(Y,R,10,num_recms=20,num_iters=20)
	r = cf.recommend()
	return r

def filter_by_genre(r,aro,val):
	gnr = [Genres.objects.get(movie__id = i).genres for i in r]
	scores = [genres.compute_scores(g) for g in gnr]
	#print(r)
	best= r[genres.best_score(aro,val,scores)]
	#print(best)
	return	best

def filter_by_decade(r):
	movies = Movie.objects.get(id__in = r)

def save_recms(recms,row_id_map):
	for r in recms:
		rm = Recm(row_id_map[i],)

def read_ratings(id):
	users = Rating.objects.values_list('user',flat = True)\
		.annotate(num_ratings = Count('user'))\
		.filter(num_ratings__gte = 10)
	return Rating.objects.filter(user_id__in = list(users)),users

def form_matrix(id):
	num_movies = Movie.objects.all().count()
	ratings, users = read_ratings(id)
	return insert_into_mat(num_movies,ratings,users,id)



