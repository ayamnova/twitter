import pandas as pd
import scipy

file_in = './mat/05-31/part-00000'

with open(file_in, 'r') as fin:
    a = pd.read_table(fin, delim_whitespace=True)
    print(a)
