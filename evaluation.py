'''
This program takes in 3 arguments:
    1) location of qrels file
    2) location of results files
    3) save directory for this program

This program ouputs saves to the save_directory:
    1) the per topic evaluation score for each student
    2) the average evalution score for each student
'''
import ast,sys,os,json, time, re
from objects import *
from evaluation_measures import *

a = time.time()
# Reading arguments presented from input
input_list = sys.argv
qrels_file = input_list[1]
results_files = input_list[2]
save_directory_path = input_list[3]
read_directory_path = input_list[4]

# This portion of the code stores the qrels files as a dictionary with lists of relvancy
# we only need to keep track of the relvant documents, if not in dict, not relevant
qrel_index = {} # Format: topic_id : [qrel]
try:
    # This following code has been adapted from code provided by Prof. Smucker
    with open(qrels_file) as qrels_file:
        for line in qrels_file:
            line_list = line.strip().split()
            if (len(line_list)==4):
                query_id = int(line_list[0])
                docno = line_list[2]
                if int(line_list[3]) == 0:
                    relevance = False
                else:
                    relevance = True
                    try:
                        qrel_list = qrel_index[query_id]
                    except:
                        qrel_list =[]
                    qrel_list.append(docno)
                    qrel_index[query_id] = qrel_list
    qrels_file.close()
except:
    print("Error Reading Qrels File")
# Next we need to iterate through the results files
# The following code is adapted from code provided by Prof. Smucker
'''
We need to store the following information:
    For each file,
'''
results_dict = {} # This holds {student_tag:results_list}
try:
    for filename in os.listdir(results_files):
        if filename.endswith(".results"):
            if(filename=='msmuckerAND.results'):
                print("GET BACK TO SMUCKER's BOOLEAN AND")
            else:
                student_tag = filename[:filename.find(".")]
                results_file = results_files+'/'+filename
                with open(results_file) as results_file:
                    result_list = []
                    for line in results_file:
                        line_list = line.strip().split()
                        if(len(line_list)==6):
                            try:
                                result = results()
                                result.student_tag = student_tag
                                result.query_id = int(line_list[0])
                                result.docno = line_list[2]
                                result.rank = line_list[3]
                                result.score = line_list[4]
                                result_list.append(result)
                            except:
                                print(student_tag+"'s results file is incorrectly formatted'")
                    results_dict[student_tag] = result_list
    try:
        # Loading all relevant files:
        # Loading metadata string
        # Loading docno to internal id mapping
        docno_to_internal_id_file_path = read_directory_path+"/"+"doc_no_to_internal_id.txt"
        docno_to_internal_id_file  = open(docno_to_internal_id_file_path, "r")
        doc_no_to_internal_id_string = ""
        for line in docno_to_internal_id_file:
            doc_no_to_internal_id_string = doc_no_to_internal_id_string +line
        json_as_string = doc_no_to_internal_id_string.replace("'", "\"")
        doc_no_to_internal_id = json.loads(json_as_string)
        # Loading internal id to metadata mapping
        internal_id_to_meta_data_file_path = read_directory_path+"/"+"internal_id_to_meta_data.txt"
        internal_id_to_meta_data_file  = open(internal_id_to_meta_data_file_path, "r")
        internal_id_to_metadata_string = ""
        for line in internal_id_to_meta_data_file:
            internal_id_to_metadata_string = internal_id_to_metadata_string + line
        internal_id_to_metadata = ast.literal_eval(internal_id_to_metadata_string)
        evaluate_measures(results_dict,qrel_index,doc_no_to_internal_id,internal_id_to_metadata,save_directory_path)
    except:
        print("ERROR FOR FILE WRITE METHOD")

except:
    print("error reading results files")
    print(student_tag)
    print(result)

t =time.time()
total = t-a
print("evaluations.py ran in "+str(total)+" seconds")
