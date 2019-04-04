#coding=utf-8
"""
Программа трассировки маршрутов
"""
import dwavebinarycsp
import networkx as nx
import matplotlib.pyplot as plt

import Grid


csp = dwavebinarycsp.ConstraintSatisfactionProblem('BINARY')

"""
Возвращает список битового представления числа
    bits - кол-во бит в списке
    n -     Исходное число
"""
def IntToBin(bits,n):
    l = []
    for i in range(bits):
        l.append(n & 1)
        n >>= 1
    return l

"""
Задание ребра графа.
    v1, v2 - номера вершин графа (int)
"""
def edge(v1,v2):
    return tuple(IntToBin(2,v1)+IntToBin(2,v2))

"""
Переводит список бит в число.
"""
def BinToInt(l):
    num=0
    for v in reversed(l):
        num <<= 1
        num |= v
    return num

#l = IntToBin(3,6)
#n = BinToInt(l)
#l = edge(0,3)

"""
Функция установки значения целочисленной переменной по битам
Параметры:
    cs - constrans правило
    node - имя (номер) переменной
    val - целое значение
    numbits - количество бит в битовом представлении
"""
def setIntVar(cs,node, numbits, val):
    bitl = IntToBin(numbits,val) # Переводим в список битов
    for bit in range(numbits):
        cs.fix_variable((node,bit),bitl[bit])

def setIntVar2(cs,node, numbits, val):
    n1,n2 = node
    bitl = IntToBin(numbits,val) # Переводим в список битов
    for bit in range(numbits):
        cs.fix_variable((n1,n2,bit),bitl[bit])


# Задаем топологию графа
#gr = [(0,0,0, 1,0,0),(1,0,0, 0,1,0), (0,0,0, 1,1,0),(1,1,0, 0,0,1)] # Граф цепи 0->1->2, 0->3->4
#gr = [edge(0,1),edge(1,2),edge(0,3),edge(3,4)]
#gr = [(0,0,0, 1,0,0, 1),(1,0,0, 0,1,0, 1), (0,0,0, 1,1,0, 1),(1,1,0, 0,0,1, 1)] # Граф цепи 0->1->2, 0->3->4 с результатом

""" Представляем имена переменных как tuple (name, bits)
Заменяем имена букв на цифры. x - 0 y - 1 z - 2 ...
"""

# Констраинс на соседние вершины

def neigbor(r10,r11, c10,c11, r20,r21,  c20,c21, res):
    r1 = BinToInt([r10,r11]) # индекс ряда 1 вершины
    c1 = BinToInt([c10,c11])  # индекс колонки 1 вершины
    v1 = r1,c1
    r2 = BinToInt([r20,r21]) # индекс ряда 2 вершины
    c2 = BinToInt([c20,c21])  # индекс колонки 2 вершины
    v2 = r2,c2
    if (v1,v2) in g.edges:
        return res == 1
    else:
        #return  res == 0
        return  False

def neigbor2(r10,r11, c10,c11, r20,r21, c20,c21):
    r1 = BinToInt([r10,r11]) # индекс ряда 1 вершины
    c1 = BinToInt([c10,c11])  # индекс колонки 1 вершины
    v1 = r1,c1
    r2 = BinToInt([r20,r21]) # индекс ряда 2 вершины
    c2 = BinToInt([c20,c21])  # индекс колонки 2 вершины
    v2 = r2,c2
    return v1,v2 in g.edges

"""
Формирует список параметров вида [(0,0,0),(0,0,1),(0,0,2), (0,1,0),(0,1,1),(0,1,2)]
n - номер переменной
y - (0 - ряд, 1 - колонка
x - (номер бита)
"""
def L(n):
    return  [(n,y,x)for y in range(2) for x in range(2)]


"""
num=0
kl  = sorted(res_sample.keys())

vl = []
for k in kl:
    vl.append(res_sample[k])
num = BinToInt(vl)

print(res_sample, num)
"""

"""
for sample, energy in solution.data(['sample', 'energy']):
    if energy == min_energy:
        time = 'business hours' if sample['time'] else 'evenings'
        location = 'office' if sample['location'] else 'home'
        length = 'short' if sample['length'] else 'long'
        mandatory = 'mandatory' if sample['mandatory'] else 'optional'
        print("During {} at {}, you can schedule a {} meeting that is {}".format(time, location, length, mandatory))
"""


"""
# Check how many solutions meet the constraints (are valid)
valid, invalid, data = 0, 0, []
for datum in response.data(['sample', 'energy', 'num_occurrences']):
    if (csp.check(datum.sample)):
        valid = valid+datum.num_occurrences
        for i in range(datum.num_occurrences):
            data.append((datum.sample, datum.energy, '1'))
    else:
        invalid = invalid+datum.num_occurrences
        for i in range(datum.num_occurrences):
            data.append((datum.sample, datum.energy, '0'))
print(valid, invalid)

print(next(response.samples()))

for datum in response.data(['sample', 'energy', 'num_occurrences', 'chain_break_fraction']):
    print(datum)
"""

"""
Получает список трассировки вершин сетки из вершины 1 к вершине 2
Реализовано для двух битового размера колонки и ряда т.е размер сетки 4x4 - вершины

Параметры:
    g - граф поля трассировки (сетка)
    v1, v2 - координаты вершин. Задаются в виде (ряд, колонка)
    
Вовращает:
    Список вершин через которые проходит трасса
    [(r0, c0),.(r1,c1)....(r2.c2)]
    
На номер вершины выделяется 2 бита т.е. 4 - бита на вершину
    

"""
def Trace(g,v1,v2):
    # cs0 =dwavebinarycsp.Constraint.from_func(neigbor2,L(0)+L(1), dwavebinarycsp.BINARY,name='cs0')
    cs0 = dwavebinarycsp.Constraint.from_func(neigbor, L(0) + L(1) + ['res0'], dwavebinarycsp.BINARY, name='cs0')
    csp.add_constraint(cs0)

    cs1 = dwavebinarycsp.Constraint.from_func(neigbor, L(1) + L(2) + ['res2'], dwavebinarycsp.BINARY, name='cs1')
    csp.add_constraint(cs1)
    r1,c1 = v1
    r2,c2 = v2
    # Устанавливаем начальную и конечную вершины
    """
    setIntVar2(cs0, (0, 0), 2, 0)  # ряд вершины 1
    setIntVar2(cs0, (0, 1), 2, 0)  # колонка вершины 1
    setIntVar2(cs1, (2, 0), 2, 0)  # ряд вершины 2
    setIntVar2(cs1, (2, 1), 2, 2)  # колонка вершины 2
    """
    setIntVar2(cs0, (0, 0), 2, r1)  # ряд вершины 1
    setIntVar2(cs0, (0, 1), 2, c1)  # колонка вершины 1
    setIntVar2(cs1, (2, 0), 2, r2)  # ряд вершины 2
    setIntVar2(cs1, (2, 1), 2, c2)  # колонка вершины 2

    bqm = dwavebinarycsp.stitch(csp, max_graph_size=8)
    #print(" Do stitch()")
    # print (bqm)

    # Проверка на локальной машине
    from dimod.reference.samplers import ExactSolver
    sampler = ExactSolver()
    solution = sampler.sample(bqm)

    """
    #Проверка на реальной машине
    from dwave.system.samplers import DWaveSampler
    from dwave.system.composites import EmbeddingComposite

    # Set up a D-Wave system as the sampler
    sampler = EmbeddingComposite(DWaveSampler())
    #sampler = EmbeddingComposite(DWaveSampler(endpoint='https://URL_to_my_D-Wave_system/', token='ABC-123456789012345678901234567890', solver='My_D-Wave_Solver'))
    solution = sampler.sample(bqm, num_reads=100)
"""

    print(solution)
    min_energy = next(solution.data(['energy']))[0]
    print(min_energy)

    res_sample = next(solution.data(['sample']))[0]
    print (res_sample)
    r1 = [res_sample[(1, 0, 0)], res_sample[(1, 0, 1)]]  # Собираем биты ряда узла 1
    res0 = res_sample['res0']
    if (not res0):
        return []
    # r1.append(res_sample[(1,0,0)])
    # r1.append(res_sample[(1,0,1)])
    nr = BinToInt(r1)  # номер ряда числом
    k = [res_sample[(1, 1, 0)], res_sample[(1, 1, 1)]]  # Собираем биты колонки узла 1
    nk = BinToInt(k)  # номер колонки числом

    return [v1,(nr,nk),v2]

#res = Trace(g, (0,0),(1,2))
#g = nx.path_graph(10) # 0 - 1 -2 ... 9
g = Grid.CreateGridGraph(4,4,[] )
#g = Grid.CreateGridGraph(4,4,[(0,0),(1,1)] )
Grid.PlotGrid(g)
#print g.edges

#Grid.plt.plot([0,nk],[0,nr],color='b')
#Grid.PlotGrid(g)
#Grid.PlotTrace(g, res)
