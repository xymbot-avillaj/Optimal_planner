import json
import numpy as np

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.optimize import minimize
import requests

ORION_URL = ''

Operators=[] #operadores 
Orders=[]  #ordenes  
ocupation={} #diccionario para saber si un operador esta ocupado
production={} #diccionario que contiene arreglo de operadores ordenados por prudictividad por cada operador seleccionado
product=[]
Solution=[] # matriz que contiene los 3 operadores para cada orden 
time=[]# numero de turnos por orden para finalizar produccion

epch=200

class Solve(Problem):

    def __init__(self, c):
        super().__init__(n_var=np.shape(c)[0]*np.shape(c)[1], n_obj=1,n_eq_constr=np.shape(c)[1], n_ieq_constr=np.shape(c)[0], xu=1,
        xl=0)
        self.C=c

    def _evaluate(self, x, out, *args, **kwargs):
        num_rows, num_cols = self.C.shape
        x = np.reshape(x, (epch, num_rows, num_cols))
        D = np.multiply(self.C, x)
        out["F"] = -1 * np.sum(np.sum(D,axis=2), axis=1)
        g1=np.sum(x, axis=1)-3
        g2=np.sum(x, axis=2)-1
        out['H']=g1
        out["G"] =g2

def postResult(path, data, headers={'Content-Type': 'application/json'}):
    x = requests.post(path, headers=headers, json=data)
    return x.text

def ini(op:list,prio:list,prod:list):
    """ Function to initialize the arrays for the optimization """
    global Orders, Operators, product
    Operators=op
    Orders=prio
    product= prod
    for i in range (0,len(Operators)):
        ocupation[Operators[i]]=False
    

def med(op,sch):
    """Function to calculate the mean production of a operator"""
    pass

def optimization_Orders():
    """Function optimization with Orders"""
    for i in range (0,len(Orders)):
        sol=[]
        for j in range (0,len(Operators)):
            if not ocupation [production[Orders[i]][j]]:
                sol.append(production[Orders[i]][j])
                ocupation [production[Orders[i]][j]]=True
            if len (sol) == 3:
                break
        Solution.append[sol]
        total=100 # numero total de piezas a producir
        toper=0 #
        turns=0
        op=0
        while total > toper:
            turns=turns+1
            toper = med (Solution[i][op]) + toper
            op = op +1
            if op == 3:
                op =0
        time.append(turns)
    # send the solutions back to Orion

def optimization ():
    """Function optimization without Orders"""
    algorithm = GA(pop_size=epch,sampling=BinaryRandomSampling(),crossover=TwoPointCrossover(),mutation=BitflipMutation(),
    eliminate_duplicates=True)
    C=np.array(product)
    solv=Solve(C)
    res = minimize(solv,algorithm,('n_gen', 200),verbose=False)
    num_rows, num_cols = C.shape
    solut=np.reshape(res.X,num_rows, num_cols)
    Oper=[]
    Mach=[]
    for i in range (0,len(Orders)):
        O=[]
        Mach.append(Orders[i])
        for j in range (0,len(Operators)):
            if solut[i][j]:
                O.append(Operators[j])
        Oper.append(O)
    entity = {'id': 'urn:ngsi:OptimalPlanner:001', 'type': 'Optimal_Planner', 'Equipment':{'value':[]} ,'Operators':{'value':[]}}
    entity["Equipment"]['value'].append(Orders)
    entity["Operators"]['value'].append(Oper)
    try:
            print(postResult(ORION_URL +'/v2/entities?options=upsert', entity, {'Content-Type': 'application/json',}))
            return
    except requests.exceptions.ConnectionError:
            print('Unable to stablish connection to FIWARE-Orion for entity update. Please, contact the developer team')
            return
    
    




    



