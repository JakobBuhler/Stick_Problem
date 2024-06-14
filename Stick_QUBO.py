import numpy as np 

class StickMaxLength():
    def __init__(self):
        self.p = None
        self.ndc = None 
        self.nsv = None
        self.tv = None
        self.pv = None
        self.dc = None
    
    def gen_problems(self, length, max_length):
        self.p = {"length": length, "max_length": max_length}
        self.ndc = len(self.p["length"])
        self.nsv = self.p["max_length"]
        self.tv = self.ndc + self.nsv
        self.pv = sum(self.p["length"])
        self.dc = self.p["length"]

    def gen_qubo_matrix(self): 
        Q = np.zeros((self.tv, self.tv),dtype = int)
        #First Hamiltonian
        for i in range(len(self.dc)):
            Q[i,i] += -self.dc[i]  
        #Second Hamiltonian
        sac = [-1 for _ in range(self.nsv)]
        c = self.tv - self.nsv
        for idx, val in enumerate(sac):
            if c + idx < self.tv:
                Q[c + idx,c +idx] +=  self.pv * val
        for i in range(c,self.tv): 
            for j in range(c,self.tv):
                if i==j:
                    continue
                Q[i,j] += self.pv * 1
        #Third Hamiltonian
        slc = [-1 * i for i in range(1,self.nsv +1)]
        ac = self.dc + slc
        for i in range(len(ac)):
            Q[i,i] += self.pv * ac[i]**2
        for i in range(self.tv):
            for j in range(self.tv):
                if i==j:
                    continue
                Q[i,j] += self.pv * ac[i]*ac[j]
        
        return Q