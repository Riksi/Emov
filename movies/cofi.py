import numpy as np

#A further pre-processing using data to include only those movies
#with at least 10 ratings i.e. indices given by np.where(np.sum(R,axis=1)>=10)

class Cofi:
    def __init__(self,
                Y_data, 
                R_data,
                num_features,
                num_recms = 10,
                lmd = 10,
                alpha=0.001,
                num_iters = 500,
                       user = None,
                       debug = False,
                       normalize = True, 
                       debugGD = False):
            self.num_features = num_features
            self.Y = np.loadtxt(Y_data)
            self.R = np.loadtxt(R_data)
            self.num_movies,self.num_users = self.Y.shape
            self.Y_mean = np.zeros((self.num_movies,1))
            if debug:
                self.X = np.loadtxt('x_test.txt')
                self.T = np.loadtxt('t_test.txt')
            else:
                self.X = np.random.randn(self.num_movies,self.num_features)
                self.T = np.random.randn(self.num_users,self.num_features)
            self.lmd = lmd
            self.alpha = alpha
            self.num_recms = num_recms
            self.num_iters = num_iters
            self.normalize = normalize
            self.debugGD = debugGD
            self.user = user or self.num_users

    def compute_cost(self,params):
        X,T= self.reshape_params(params)
        J = 0.5*self.sum2(self.cost_term(X,T,2))\
            +0.5*self.lmd*(self.sum2(T**2)
                        +self.sum2(X**2))
        return J

    def sum2(self,M):
        return np.sum(np.sum(M))

    def cost_term(self,X,T,power=1):
        return ((X.dot(T.T) - self.Y)**power)*self.R

    def cost_grad(self,params):
        X,T = self.reshape_params(params)
        grad_term = self.cost_term(X,T)
        grad_X = grad_term.dot(T) + self.lmd*X
        grad_T = (grad_term.T).dot(X) + self.lmd*T
        return self.unroll_params(grad_X,grad_T)

    def reshape_params(self,params):
        m,u,f = self.num_movies,self.num_users,self.num_features
        x = params[0:m*f].reshape((m,f),order='F');
        t = params[m*f:].reshape((u,f),order='F');
        return x,t

    def unroll_params(self,x,t):
        return np.concatenate((x.flatten(order='F'),t.flatten(order='F')),axis=0)

    def mean_normalize(self):
        for i in range(0,self.num_movies):
            idx = np.where(self.R[i,:]==1)
            self.Y_mean[i,:] = np.mean(self.Y[i,idx])
            self.Y[i,idx]-=self.Y_mean[i,:]
   
    def grad_desc(self,params):
        for i in range(0,self.num_iters):
            if self.debugGD:
                print('Iteration: %s, Cost: %s'%(str(i),str(self.compute_cost(params))))
            params = params - self.alpha*self.cost_grad(params)
        return params

    def calculate_params(self):
            if self.normalize:
                self.mean_normalize()
            params = self.grad_desc(self.unroll_params(self.X,self.T))
            self.X,self.T = self.reshape_params(params)

    def predict(self):
        self.predictions = self.X.dot(self.T.T) + self.Y_mean
        
    def recommend(self):
        self.calculate_params()
        self.predict()
        real_preds = self.predictions[:,self.user-1:self.user]*(self.R[:,self.user-1:self.user]!=1)
        movie_inds = [i for i in range(0,self.num_movies)]
        movie_inds.sort(key = lambda ind: real_preds[ind,:], reverse = True)
        return (real_preds[movie_inds],movie_inds[:self.num_recms])
        
