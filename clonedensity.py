import sys
import math
import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

plotly.tools.set_credentials_file(username='natpie1',
                                  api_key='bjhv6wPhJexpjfwUExkJ')
file_path = "/Users/Nat/Dropbox/Williams Lab/4. Data Collection/***K14-CreER; Confetti_Sagittal_Palate_Lineage_Analysis_180929_AvP.xlsx"

"""
--File Setup--

The file should have, at the minimum, a column for basal cell count ('Basal'),
suprabasal cell count ('Suprabasal'), and the mouse ID ('Mouse'). Additional
columns for topography ('Topography') or area ('Area') can be used as well.
All relevant data points should be accesible on one excel sheet.

--Execution--

1. Set plotly credentials
2. Assign file path for excel sheet to object 'file_path'
3. Assign appropriate sheet number to object 'sheet_name'
4. Select data by topography or location if necessary
5. Use command prompt 'python clonedensity.py graphname'

"""

xl = pd.read_excel(file_path, sheet_name=0)
basal = np.array(xl.loc[:, "Basal"]).astype(int)
suprabasal = np.array(xl.loc[:, "Suprabasal"]).astype(int)
mouse = np.array(xl.loc[:, "Mouse"])

"""
#--Optional Modifiers--

#Topography

topo = np.array(xl.loc[:, "Topography"])
basal = basal[topo == 'R']
suprabasal = suprabasal[topo == 'R']
mouse = mouse[topo == 'R']

#Location

area = np.array(xl.loc[:, "Area"])
basal = basal[area == 'Ant']
suprabasal = suprabasal[area == 'Ant']
mouse = mouse[area == 'Ant']
"""

def clone_array(b, sb, d):
    """
    This function accepts a 1d array of basal cells (b), a 1d array of
    suprabasal cells (sb), and an integer dimension (d).

    The function returns a 2d array:

        axis0 = suprabasal cells, length d + 1
        axis1 = basal cells, length d

    Each element in the array is the counts of occurences of a clone with
    associated dimensions. Clones with zero basal cells will be assumed
    delaminated clones and will not be included in the array.
    """
    b[b > d] = d
    sb[sb > d] = d
    output = np.zeros((d + 1, d))
    for index, bcells in enumerate(b):
        if bcells != 0:
            output[sb[index], bcells - 1] += 1
    return output

def sample_arrays(b, sb, m, d):
    """
    This function and all following functions accept a 1d array of basal cells
    (b), a 1d array of suprabasal cells (sb), a 1d array of mice IDs (m), and
    an integer dimension (d).

    The function returns a 3d array:

        axis0 = samples in data set
        axis1 = suprabasal cells, length d + 1
        axis2 = basal cells, length d

    Each element in the array is the count sfor each occurence for a clone of the
    associated size. Each mouse is considered one sample.
    """
    mice = set(m)
    output = [clone_array(b[m==i], sb[m==i], d) for i in mice]
    return output

def percent_arrays(b, sb, m, d):
    """
    This function returns a 3d array:

        axis0 = samples in data set
        axis1 = suprabasal cells, length d + 1
        axis2 = basal cells, length d

    Each element in the array is a percentage of clones of the associated size
    for a single sample.
    """
    mice_arrays = sample_arrays(b, sb, m, d)
    sums = np.array([np.sum(array).astype(int) for array in mice_arrays])
    output = []
    for index, array in enumerate(mice_arrays):
        output.append(np.divide(array, sums[index]))
    return output

def normalized_array(b, sb, m, d):
    """
    This function returns a 2d array:

        axis0 = suprabasal cells, length d + 1
        axis1 = basal cells, length d

    Each element in the array is a normalized percentage of clones of the
    associated size within the entire data set.
    """
    percentage_arrays = percent_arrays(b, sb, m, d)
    output = sum(percentage_arrays)/len(percentage_arrays)
    return output

def error_text(b, sb, m, d):
    """
    This function returns a 2d list:
