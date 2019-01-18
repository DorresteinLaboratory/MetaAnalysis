#!/usr/bin/python
import numpy as np
from pyteomics import mzxml
import pandas as pd
import copy
import os
import sys
import getopt
import os

#Bucket Spectra into a vector
#Norms it too
def vectorize_peaks(peaks, max_mass, bin_size, normalize=False, sqrt_peaks=True):
    number_of_bins = int(max_mass / bin_size)
    peak_vector = [0.0] * number_of_bins

    for peak in peaks:
        mass = peak[0]
        bin_index = int(mass/bin_size)
        if bin_index > number_of_bins - 1:
            continue
        peak_vector[bin_index] += peak[1]

    np_array = np.array(peak_vector)

    if sqrt_peaks == True:
        np_array = np.sqrt(np_array)

    if normalize:
        np_array = np.true_divide(np_array, np.linalg.norm(np_array))

    return np_array

def average_ms1(input_filename, output_filename=None, bin_width=1.0, format="csv"):
    mass_list = []
    intensity_list = []

    spectra = mzxml.read(input_filename, read_schema = True) #type is pyteomics mzxml

    peaks_list = []

    for element in spectra:
        mlist = copy.deepcopy(element['m/z array'])
        inten = copy.deepcopy(element ['intensity array'])
        mslevel = element["msLevel"]
        if mslevel != 2:
            continue

        peaks_list += zip(mlist, inten)

    numpy_vector = vectorize_peaks(peaks_list, 2000, bin_width)

    if output_filename != None:
        dt = pd.DataFrame(data=numpy_vector)
        dt.to_csv(output_filename, mode='a', index=True)

    return numpy_vector

def main():
    average_ms1(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
