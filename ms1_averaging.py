import scipy
import numpy as np
from pyteomics import mzxml
from line_profiler import LineProfiler
import copy 
import pandas as pd
from itertools import izip
import os
from __future__ import division
%reload_ext line_profiler%reload_ext line_profiler

mass_list = []
intensity_list = []

path = (r'H:\Chrissy\Averaging_Study\mzXML\101_Prebiotic_CDR_SD_1.mzXML')
spectra = mzxml.read(path, read_schema = True) #type is pyteomics mzxml   

def timing_stuff():
    inten2 = list() 
    mlist2 = list()
    mlist = np.array([])
    inten = np.array([])
    final_mlist = np.array([])
    final_inten = np.array([])
    
    for element in spectra:
        mlist = copy.deepcopy(element['m/z array']) 
        inten = copy.deepcopy(element ['intensity array'])
              
        if mlist[0] >= 99:
            mlist = mlist.tolist() 
            inten = inten.tolist()
        
            mlist2.extend(mlist)
            inten2.extend(inten)
        mlist = []
        inten = []
        
    final_mlist = np.unique(mlist2, return_inverse = True)
    length = final_mlist[0].shape[0]
    
    final_inten = np.zeros(length) 
    
    final_inten = final_inten.tolist()
    indices = list(final_mlist[1])
    
    for intensity, index in zip(inten2, indices): #time heavy processes
        final_inten[index] += intensity 
        
    final_mlist = final_mlist[0]
    
    for counter, item2 in enumerate(final_inten):
        if item2 == 0:
            final_mlist[counter] = 0
        
    final_mlist = [value for value in final_mlist if value != 0]
    final_inten = [value for value in final_inten if value != 0]
    d = {'mlist':final_mlist, 'inten': final_inten}
    df = pd.DataFrame(data = d)
    df.to_csv(r'H:\Chrissy\Averaging_Study\OUTPUT_mzXML_file_process_code\OUTPUT_101_Prebiotic_CDR_SD_1.csv')
%lprun -f timing_stuff timing_stuff()
