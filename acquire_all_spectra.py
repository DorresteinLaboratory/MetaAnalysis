#!/usr/bin/python

import os
import sys
import csv
import urllib
import ms1_averaging
from joblib import Parallel, delayed
import multiprocessing
import subprocess
import os
import json


#Wraps the parallel job running, simplifying code
def run_parallel_job(input_function, input_parameters_list, parallelism_level):
    if parallelism_level == 1:
        output_results_list = []
        for input_param in input_parameters_list:
            result_object = input_function(input_param)
            output_results_list.append(result_object)
        return output_results_list
    else:
        results = Parallel(n_jobs = parallelism_level)(delayed(input_function)(input_object) for input_object in input_parameters_list)
        return results

def process(param, execution="remote"):
    filename = param[0]
    output_folder = param[1]

    if execution == "massive":
        massive_path = "/data/massive/%s" % (filename[2:])
        norm_vector = ms1_averaging.average_ms1(massive_path)
    else:
        ftp_filename = "ftp://massive.ucsd.edu/%s" % (filename[2:])
        print(ftp_filename)
        local_filename = os.path.join(output_folder, os.path.basename(filename))
        cmd = "wget '%s' -O %s" % (ftp_filename, local_filename)
        os.system(cmd)
        norm_vector = ms1_averaging.average_ms1(local_filename)


    output_dict = {}
    output_dict["vector"] = norm_vector.tolist()
    output_dict["filepath"] = filename

    return output_dict


def main():
    input_metadata = sys.argv[1]
    output_folder = sys.argv[2]

    output_json_filename = os.path.join(output_folder, "spectra.json")

    all_filename = []

    with open(input_metadata) as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        for row in reader:
            filename = row["filename"]
            all_filename.append(filename)

    parameters = [(param, output_folder) for param in all_filename]

    all_spectra_output = run_parallel_job(process, parameters[:2], 1)


    json.dump(all_spectra_output, open(output_json_filename, "w"))





if __name__ == "__main__":
    main()
