import random

import datapreparation as dp
import numpy as np
from deap import base, creator, tools

test_roll = dp.midfile_to_piano_roll("spooky.midi")

# print(test_roll.shape)
# dp.visualize_piano_roll(test_roll)

# Deap init
IND_SIZE = 144


creator.create("Fitness", base.Fitness, weights=(1.0,1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("attr_float", lambda: random.random()*80)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)

ind1 = toolbox.individual()
print(ind1)