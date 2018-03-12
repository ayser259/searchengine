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
a = time.time()
# Reading arguments presented from input
input_list = sys.argv
qrels_file = input_list[1]
results_files = input_list[2]
save_directory_path = input_list[3]

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
                    qrel = {docno:relevance}
                    qrel_list.append(qrel)
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
                    print(filename)
                    results_dict[student_tag] = result_list
                    average_precision_dict = average_precision(results_list,qrel_index)
                    precision_at_10_dict = precision_at_10(results_list,qrel_index)
                    ndcg_at_10_dict = ndcg_at_10(results_list,qrel_index)
                    ndcg_at_1000_dict = ndcg_at_1000(results_list,qrel_index)
                    time_based_gain_dict = time_based_gain(results_list,qrel_index)
                    save_files()
                    # Now we need to run the evaluations on the
except:
    print("error reading results files")
    print(student_tag)
    print(resul)

'''
class ResultsParser:
    class ResultsParseError(Exception):
        pass

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        global_run_id = None
        history = set()
        results = Results()
        with open(self.filename) as f:
            for line in f:
                line_components = line.strip().split()
                if len(line_components) != 6:
                    raise ResultsParseError('lines in results file should have exactly 6 columns')

                query_id, _, doc_id, rank, score, run_id = line_components
                rank = int(rank)
                score = float(score)

                if global_run_id is None:
                    global_run_id = run_id
                elif global_run_id != run_id:
                    raise ResultsParseError('Mismatching runIDs in results file')

                key = query_id + doc_id
                if key in history:
                    raise ResultsParseError('Duplicate query_id, doc_id in results file')
                history.add(key)

                results.add_result(query_id, Result(doc_id, score, rank))

        return global_run_id, results


    class Result:
        def __init__(self, doc_id, score, rank):
            self.doc_id = doc_id
            self.score = score
            self.rank = rank

        def __lt__(self, x):
            return (self.score, self.doc_id) > (x.score, x.doc_id)

    class Results:
        def __init__(self):
            self.query_2_results = defaultdict(list)

        def add_result(self, query_id, result):
            self.query_2_results[query_id].append(result)

        def get_result(self, query_id):
            return self.query_2_results.get(query_id, None)

'''

t =time.time()
total = t-a
print("evaluations.py ran in "+str(total)+" seconds")


'''
import xlwt

x=1
y=2
z=3

list1=[2.34,4.346,4.234]

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Sheet 1")

sheet1.write(0, 0, "Display")
sheet1.write(1, 0, "Dominance")
sheet1.write(2, 0, "Test")

sheet1.write(0, 1, x)
sheet1.write(1, 1, y)
sheet1.write(2, 1, z)

sheet1.write(4, 0, "Stimulus Time")
sheet1.write(4, 1, "Reaction Time")

i=4

for n in list1:
    i = i+1
    sheet1.write(i, 0, n)



book.save("trial.xls")

'''
