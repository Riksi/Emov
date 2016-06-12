from .models import Rating, Movie
from .pnn import PNN
from django.db.models import Count,Avg
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
MIN_COUNT = 5
Y_FILE_PATH = ''
R_FILE_PATH = ''
PNN_SIGMA = {'arousal': 1,'valence':9}
MOVIES = []
import random
def eeg_handler(request):
	if request.method == 'POST':
		if request.POST['simulate']:
			return JsonResponse(obtain_predictions(SIMULATED,True))

def retrieve_movies(request):
	return JsonResponse({
		'movies':MOVIES
		})
	
def main_page(request):
	return render(request,'movies/front_end.html')

def prediction_handler(request):
	if request.method == 'POST':
		eeg = request.POST['eeg']
		return JsonResponse({'predictions':obtain_predictions()})

def receive_rating(request):
	user = request.user
	
	count = Count.objects.get(user=user)
	if count == MIN_COUNT:
		return compute_recms(user)

def fetch_recms(uid):
	Recm.objects.values_list('user',flat=True)\
	.aggregate(Max('timestamp'))\
	.filter(user_id= uid)

def compute_recms(user):
	#Cofi object
	#run Cofi.predict()
	pass

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

def insert_into_mat(num_movies,ratings,users,user_id):
	print(users)
	num_users = len(users)
	Y = np.zeros((num_users,num_movies))
	R = np.array(Y)
	row_id_map = {}
	start = ratings[0].user.id
	ind = 0
	for r in ratings:
		uid = r.user.id
		if uid != start:
			ind+=1
			start = uid
		row_id_map[ind] = uid
		colm = r.movie.id-1
		Y[ind,colm] = r.rating
		R[ind,colm]  = 1
	return Y,R, row_id_map
	
def save_mat(mat,filepath):
	f = open(filepath,'a')
	f.writelines(mat)

def process_data(data):
	return(np.array(data))


def load_data(category):
	features = np.loadtxt('c:/users/anush/web_dev/emov/mysite/movies/psd_train.txt')
	labels = np.loadtxt('c:/users/anush/web_dev/emov/mysite/movies/%s_train.txt'%category[:3])
	return features,labels

def predict_emot(category,data,example):
	features,labels = data
	ex_feat = process_data(example)
	p = PNN(2,PNN_SIGMA[category],ex_feat,features,labels+1)
	return p.predict()[0][0]

SIMULATED = np.array([[-1.702,-1.398,-1.3422,-1.5464,-1.5345,-1.7486,-1.6709,-1.9506,-1.7256,-2.277,-1.1031,-1.481,-1.3798,-1.4612,-1.2354,-2.1266,-1.583,-1.5248,-1.4193,-1.1367,-1.6672,-1.8083,-1.3734,-1.8768,-1.41,-1.6154,-1.9256,-2.2608,-1.2727,-1.8074,-1.4219,-1.5362,-1.741,-1.4685,-1.4649,-1.362,-1.4336,-1.8358,-1.5443,-1.8571,-1.259,-1.7944,-1.0321,-1.109,-0.91514,-1.1002,-1.0697,-1.6415,-1.73,-1.4843,-1.5686,-1.3158,-1.6102,-1.6187,-1.4889,-1.9175,-1.3138,-1.4474,-1.653,-1.9828,-1.4421,-1.6237,-1.2669,-1.1705,-1.6988,-1.156,-0.94572,-1.2485,-1.465,-1.3481,-1.2582,-1.3887,-1.2058,-1.4515,-0.89946,-1.1998,-1.0541,-1.0652,-1.1238,-1.4865,-1.3985,-1.3284,-1.0714,-1.064,-1.144,-1.4723,-1.1485,-1.2037,-0.99343,-1.2407,-1.4666,-1.6717,-0.99962,-1.706,-1.1913,-1.2514,-2.4483,-1.7559,-1.4293,-1.8215,-1.5875,-1.3548,-1.4684,-1.3427,-1.48,-2.0401,-1.0101,-1.224,-1.1238,-0.99413,-1.2247,-1.8884,-1.8907,-1.5166,-1.5631,-1.3996,-1.7774,-2.0046,-1.4337,-1.8288,-1.2631,-1.3931,-1.7502,-2.0971,-1.1243,-1.6736,-1.5267,-1.6792,0.017154,0.061592,-0.050175,-0.086969,0.20785,-0.17444,-0.2322,0.030483,0.32591,0.086958,0.25562,0.20158,0.28576,-0.32264,0.39336,-0.063327,-0.023719,-0.028433,0.032818,-0.22029,-0.2435,0.031133,0.41609,0.26663,0.56979,0.46966,0.66319,-0.30784,0.29735,0.043178,0.084503,-0.20775,-0.18608,-0.1823,-0.32848,0.19422,0.29027,0.36056,0.18274,0.45623,0.29635,-0.091253,0.13367,-0.52768,-0.073411,-0.16664,0.24565,-0.019563,-0.297,0.37524,0.35174,0.25662,0.2096,0.42418,0.491,0.64051,1,1,4][:128]])

def obtain_predictions(example,simulate=False):
	if simulate:
		ex = example
	else:
		ex = process_data(example)
	cats = ['arousal','valence']
	return dict(zip(cats,[int(predict_emot(cat,load_data(cat),ex)) for cat in cats]))


#print(obtain_predictions([],True))








#users = Rating.objects.values_list('user',flat = True)\
	#.annotate(num_ratings = Count('user'))\
	#.filter(num_ratings__gte = 10)
#ratings = Rating.objects.filter(user_id__in = list(users))
#print(users)
#a = insert_into_mat(25,ratings,users,5)
#print(a)
#print(a[0])
#print(a[1])
#print(a[2])

#y1 = [1*(i<10) for i in range(1682)]
#y2 = [1*(i<20) for i in range(1682)]
#R_test = np.array([y1,y2])
#Y_test = R_test*5

#print(np.sum(abs(Y_test - a[0])))
#print(np.sum(abs(R_test - a[1])))

#Save some ratings to db
#Read from db
#Form matrix - first in a list form, then as numpy array 

#r = Rating(user_id=user_id, rating=rating)
#r.save()


#Add rating to DB
#Select the ratings for each movie from each user who has at least 5 ratings 

#Rating.objects.annotate(num_ratings = Count('user_id')).filter(num_ratings__gte = 10, user_id)

#select * from movies as m1 where (select count(user_id) from movies where user_id = m1.user_id) > 10 and user_id != this_user_id order by user_id
#users = select count(user_id) from movies where (select count(user_id) from movies where user_id = m1.user_id) > 10
#l = zeros((users,movies))
#p = zeros((users,movies))
#Create rating vector
#start = 0
#prev = user_id_0
#for rating in ratings:
#	if (present_id - prev) != 0:
	#	start+=1
	#l[present_movie-1] = present_rating
	#p[present_movie-1] = 0
#select * from ratings where user_id = this_user_id
#make_vector(results)
#call_cofi(l,p,results)
# Create your views here.


