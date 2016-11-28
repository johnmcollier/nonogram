#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the nonogram models.  

'''
Construct and return nonogram CSP models.
'''

from cspbase import *
import itertools

def nonogram_csp_model(nonogram_rows, nonogram_columns):
    '''Return a CSP object representing a nonogram CSP problem along 
       with an array of variables for the problem. That is return

       nonogram_csp, variable_array

       where nonogram_csp is a csp representing the nonogram game and
       variable_array is an n by n matrix representing each cell in the
       game.
       
       The input rows and columns specify which cells in each row or column
       that need to be coloured in.
       
       This routine returns a model which consists of a variable for
       each cell of the board, with domain equal to {0,1}, with 0 being
       not coloured and 1 being coloured.
    '''

##IMPLEMENT



##############################

