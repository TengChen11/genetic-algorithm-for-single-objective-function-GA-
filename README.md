# genetic-algorithm-for-single-objective-functions-GA-
python; GA; N decision variables; SBX; polynomial mutation; optimization

## Overview

​	This program is about how GA works in single objective functions with two decision variables. The great thing about this code is that you can specify any function with N decision variables that you want to optimize.

​	N is the number of decision variables.

​	For example, you can find three objective functions here in the file named function.py. Check them by yourself.  

## Note

### function.py

The method of crossover used here is SBX.

The method of mutation used here is highly disruptive polynomial mutation.

Elite strategy is used to select.

### GA_f1.ipynb and GA_f2.ipynb

Parameters you need to concentrate:

Crossover_p: the probability of crossover. Usually set it between 0.4 and 0.6.

Mutation_p: the probability of mutation. Usually set it to 1/population_size or between 0.001 and 0.01.

Don't set elite rate too largely because you may come across an error.

### pictures in fitness results

The pictures illustrate the fitness of every individual in the population in one iteration.

You may get confused by the x-axis. Take a simple example:

The index 0 means this is the first individual in the population, and so on.

### pictures in output

The pictures illustrate the entire process of optimization. 



#### if you want more details, dive into this program. By the way, you are allowed to specify your objective functions in function.py.

Try it.

Give the feedback if there is any issue.



### 
