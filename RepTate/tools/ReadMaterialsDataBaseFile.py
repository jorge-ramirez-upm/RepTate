import numpy as np
from polymer_data import polymer

read_dictionary = np.load('materials_database.npy').item()
for k in read_dictionary.keys():
    print(k, ': ', read_dictionary[k].data, '\n')
