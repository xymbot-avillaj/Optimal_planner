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
Priority=[]  #ordenes ordenadas por prioridad
ocupation={} #diccionario para saber si un operador esta ocupado
production={} #diccionario que contiene arreglo de operadores ordenados por prudictividad por cada operador seleccionado
product=[]
Solution=[] # matriz que contiene los 3 operadores para cada orden 
time=[]# numero de turnos por orden para finalizar produccion

class Solve(Problem):

    def __init__(self, c):
        super().__init__(n_var=np.shape(c)[0]*np.shape(c)[1], n_obj=1, n_ieq_constr=1, xl=np.zeros(np.shape(c)[0]*np.shape(c)[1]),
        xl=np.ones(np.shape(c)[0]*np.shape(c)[1]))
        self.C=c

    def _evaluate(self, x, out, *args, **kwargs):
        num_rows, num_cols = self.C.shape
        out["F"] = - np.sum(np.dot(-1,np.multiply(self.C,np.reshape(x,num_rows,num_cols))))
        g1=3-np.reshape(x,num_rows,num_cols).sum(axis=1)
        g2=1-np.reshape(x,num_rows,num_cols).sum(axis=0)
        G = np.column_stack([g1, g2])
        out["G"] = G

def postResult(path, data, headers={'Content-Type': 'application/json'}):
    x = requests.post(path, headers=headers, json=data)
    return x.text

def ini(op:list,prio:list,prod:list):
    """ Function to initialize the arrays for the optimization """
    global Priority, Operators, product
    Operators=op
    Priority=prio
    product= prod
    for i in range (0,len(Operators)):
        ocupation[Operators[i]]=False
    

def med(op,sch):
    """Function to calculate the mean production of a operator"""
    pass

def optimization_priority():
    """Function optimization with priority"""
    for i in range (0,len(Priority)):
        sol=[]
        for j in range (0,len(Operators)):
            if not ocupation [production[Priority[i]][j]]:
                sol.append(production[Priority[i]][j])
                ocupation [production[Priority[i]][j]]=True
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
    """Function optimization without priority"""
    algorithm = GA(pop_size=200,sampling=BinaryRandomSampling(),crossover=TwoPointCrossover(),mutation=BitflipMutation(),
    eliminate_duplicates=True)
    C=np.array(product)
    solv=Solve(C)
    res = minimize(solv,algorithm,('n_gen', 200),verbose=False)
    num_rows, num_cols = C.shape
    solut=np.reshape(res,num_rows, num_cols)
    Oper=[]
    Mach=[]
    for i in range (0,len(Priority)):
        O=[]
        Mach.append(Priority[i])
        for j in range (0,len(Operators)):
            if solut[i][j]:
                O.append(Operators[j])
        Oper.append(O)
    entity = {'id': 'urn:ngsi:OPS:001', 'type': 'Optimal_Planner', 'Equipment':{'value':[]} ,'Operators':{'value':[]}}
    entity["Equipment"]['value'].append(Priority)
    entity["Operators"]['value'].append(Oper)
    try:
            print(postResult(ORION_URL +'/v2/entities?options=upsert', entity, {'Content-Type': 'application/json',}))
            return
    except requests.exceptions.ConnectionError:
            print('Unable to stablish connection to FIWARE-Orion for entity update. Please, contact the developer team')
            return
    
    




    



