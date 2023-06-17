import numpy as np
import matplotlib.pyplot as plt
from random import *

#specify the objective function
def f1(x:np.ndarray)->float:
    return x[0]**2 + x[1]**2

#specify the objective function
def f2(x:np.ndarray)->float:
    return 100 * (x[0]**2 - x[1])**2 + (1 - x[0])**2

#specify the objective function
def f3(x:np.ndarray)->float:
    return 2 * (x[0] - 0.5)**2 + x[1]**2 + x[2]**2 + 1 

# get a fitness_lst from a population
def get_fitness_lst(population:list, f)->list:
    fitness_lst = []
    for individual in population:
        fitness = f(individual)
        fitness_lst.append(fitness)
    return fitness_lst

#specify the SBX(crossover)
def SBX(p:float, eta:float, x_upper:np.ndarray, x_lower:np.ndarray, parent1:np.ndarray, parent2:np.ndarray, is_crossover:bool)->np.ndarray:
    pt = random()
    is_crossover = False
    if pt < p:
        u = random()
        if u <= 0.5:
            belta = (2*u) ** (1/(eta+1))
        else:
            belta = (1/(2-2*u)) ** (1/(eta+1))
        
        offspring1 = 0.5 * ((1+belta)*parent1 + (1-belta)*parent2)
        offspring2 = 0.5 * ((1-belta)*parent1 + (1+belta)*parent2)
        if (offspring1 < x_upper).all() and (offspring1 > x_lower).all() and (offspring2 < x_upper).all() and (offspring2 > x_lower).all():
            is_crossover = True
            return offspring1, offspring2, is_crossover
        else:
            return parent1, parent2, is_crossover
    else:
        return parent1, parent2, is_crossover

#specify the highly disruptive polynomial mutation function
def poly_mutation(p:float, eta:float, x_upper:np.ndarray, x_lower:np.ndarray, xt:np.ndarray, is_mutation:bool)->np.ndarray:
    pt = random()
    is_mutation = False
    if pt < p:
        r = random()
        if r <= 0.5:
            t = (xt - x_lower) / (x_upper - x_lower)
            delta = np.power(2*r + (1-2*r) * np.power(1-t, eta+1), 1/(eta+1)) - 1
        else:
            t = (x_upper - xt) / (x_upper - x_lower)
            delta = 1 - np.power(2 * (1-r)+2 * (r-0.5) * np.power(1-t, eta+1), 1/(eta+1))
        offspring = xt + delta * (x_upper - x_lower)
        if (offspring < x_upper).all() and (offspring > x_lower).all():
            is_mutation = True
            return offspring, is_mutation
        else:
            return xt, is_mutation
    else:
        return xt, is_mutation
    
#initialize
def initialize_population(size:int, variable_size:int, x_upper:np.ndarray, x_lower:np.ndarray)->list:
    population = []
    for _ in range(size):
        individual = []
        for idx in range(variable_size):
            x = uniform(x_lower[idx], x_upper[idx])
            individual.append(x)
        population.append(np.array(individual))
    return population

#selection
def selection(size:int, new_population:list, elite_rate:float, f)->list:
    fitness_list = get_fitness_lst(new_population, f)
    sorted_fitness = sorted(enumerate(fitness_list), key = lambda x:x[1])
    idx = [i[0] for i in sorted_fitness]
    elite_num = int(elite_rate * len(new_population))
    if elite_rate > 0 and elite_num <= size:
        offspring_population =[]
        elite_idx = idx[0: elite_num]
        diverse_idx = idx[len(idx) - (size - elite_num): len(idx)]
        total_idx = elite_idx + diverse_idx
        for val in total_idx:
            offspring_population.append(new_population[val])
        shuffle(offspring_population)
        return offspring_population
    else:
        raise NameError('Error')
    
#fitness plot
def fitness_plot(population:list, save_path:str, iteration_num:int, f)->float:
    fitness_list = get_fitness_lst(population, f)
    minimum = min(fitness_list)
    maximum = max(fitness_list)
    mean = sum(fitness_list) / len(fitness_list)
    index = fitness_list.index(minimum)
    plt.scatter(range(len(fitness_list)), fitness_list, label = 'iteration_' + str(iteration_num))
    plt.xlabel('index')
    plt.ylabel('fitness')
    plt.legend()
    plt.savefig(save_path + '/result' + str(iteration_num) + '.png')
    plt.close()
    print('iteration:{}, the best individual:{}, its index:{}, the fitness:{}'.format(iteration_num, population[index], index, minimum))
    return minimum, maximum, mean

#plot the minimum in every iteration
def minimum_fitness_plot(minimum_lst:list, save_path:str)->None:
    plt.plot(range(len(minimum_lst)), minimum_lst, label = 'minimum', c = 'red')
    plt.xlabel('iteration')
    plt.ylabel('fitness')
    plt.legend()
    plt.savefig(save_path + '/min_output.png')
    plt.close()

#plot the maximum and mean in every iteration
def max_mean_fitness_plot(maximum_lst:list, mean_lst:list, save_path:str)->None:
    plt.plot(range(len(maximum_lst)), maximum_lst, label = 'maximum', c ='blue')
    plt.plot(range(len(mean_lst)), mean_lst, label = 'mean', c = 'green')
    plt.xlabel('iteration')
    plt.ylabel('fitness')
    plt.legend()
    plt.savefig(save_path + '/max_mean_output.png')
    plt.close()

#boxplot
def boxplot(box_num:int, entire_evolution:list, save_path:str, f)->None:
    entire_fitness_lst = []
    index = np.linspace(0, box_num, box_num)
    for idx in index:
        fitness_lst = get_fitness_lst(entire_evolution[int(idx)], f)
        entire_fitness_lst.append(fitness_lst)
    labels = [int(i) for i in index]
    plt.grid(True)
    plt.boxplot(entire_fitness_lst, meanline = True, showmeans = True, labels = labels, flierprops = {"marker":"+"})
    plt.xlabel('iteration')
    plt.ylabel('fitness')
    plt.savefig(save_path + '/boxplot.png')
    plt.close()

#plot the evolutionary process between one generation and another generation
#can specify any two generations in evolutionary process
def evolution_plot(population1:list, iteration1:int, population2:list, iteration2:int, save_path:str, f)->None:
    fitness_population1_lst = get_fitness_lst(population1, f)
    fitness_population2_lst = get_fitness_lst(population2, f)
    plt.scatter(range(len(fitness_population1_lst)), fitness_population1_lst, label = 'iteraton'+str(iteration1), c = 'blue')
    plt.scatter(range(len(fitness_population2_lst)), fitness_population2_lst, label = 'iteraton'+str(iteration2), c = 'red')
    plt.xlabel('index')
    plt.ylabel('fitness')
    plt.legend()
    plt.savefig(save_path + '/evolution.png')
    plt.close()