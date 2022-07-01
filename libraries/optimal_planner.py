import json

Operators=[] #operadores 
Priority=[]  #ordenes ordenadas por prioridad
ocupation={} #diccionario para saber si un operador esta ocupado
production={} #diccionario que contiene arreglo de operadores ordenados por prudictividad por cada operador seleccionado
Solution=[] # matriz que contiene los 3 operadores para cada orden 
time=[]# numero de turnos por orden para finalizar produccion

def ini(op:list,prio:list):
    """ Function to initialize the arrays for the optimization """
    Operators=op
    Priority=prio
    for i in range (0,len(Operators)):
        ocupation[Operators[i]]=False
    

def med(op,sch):
    """Function to calculate the mean production of a operator"""
    pass

def optimization():

    for i in range (0,len(Priority)):
        sol=[]
        for j in range (0,Operators):
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


