'each of these methods returns a dictionary with keys as topi ids and a key for average'

' each of these methods '
import ast,sys,os,json, time, re,math,  xlsxwriter
from objects import *

results_dict = {} # This holds {student_tag:results_list}
qrel_index = {} # Format: topic_id : [{docno:relevance}]

def average_precision(results_list,qrel_index):
    # This method calculates the average_precision given the results_list and qrel_index
    average_precision_dict = {}
    topic_ids = list(qrel_index.keys())
    for topic in topic_ids:
        try:
            relevant_docs = list(qrel_index[topic])
            total_files_returned = 0
            relevant_files_returned = 0
            average_precision = 0
            for result in results_list:
                if result.query_id == topic:
                    total_files_returned = total_files_returned +1
                    if result.docno in relevant_docs:
                        relevant_files_returned = relevant_files_returned +1
                        precision = float(relevant_files_returned)/float(total_files_returned)
                        average_precision = float(average_precision) + precision
                        precision = 0
            average_precision = (1/(float(len(relevant_docs))))*average_precision
            average_precision_dict[topic] = round(average_precision,4)
        except:
            print("Topic DNE")
    return average_precision_dict

def precision_at_10(results_list,qrel_index):
    # This method calculates the precision_at_10 given the results_list and qrel_index
    precision_at_10_dict = {}
    topic_ids = list(qrel_index.keys())
    for topic in topic_ids:
        try:
            relevant_docs = list(qrel_index[topic])
            total_files_returned = 0
            relevant_files_returned = 0
            average_precision = 0
            for result in results_list:
                if total_files_returned<10:
                    if result.query_id == topic:
                        total_files_returned = total_files_returned +1
                        if result.docno in relevant_docs:
                            relevant_files_returned = relevant_files_returned +1
                else:
                    break
            precision = float(relevant_files_returned)/float(total_files_returned)
            precision_at_10_dict[topic] = round(precision,4)
        except:
            print("Topic DNE")
    return precision_at_10_dict


def ndcg_at_10(results_list,qrel_index):
    # thjis method calculated the ndcg at 10
    ndcg_at_10_dict = {}
    topic_ids = list(qrel_index.keys())
    for topic in topic_ids:
        try:
            dcg = 0
            idcg = 0
            total_files_returned = 0
            relevant_files_returned = 0
            relevant_docs = list(qrel_index[topic])
            for result in results_list:
                if total_files_returned < 10:
                    if result.query_id == topic:
                        total_files_returned = total_files_returned + 1
                        if total_files_returned < len(relevant_docs):
                            idcg = idcg + (float(1)/(math.log(total_files_returned+1,2)))
                        else:
                            idcg = idcg + (float(1)/(math.log(len(relevant_docs)+1,2)))
                        if result.docno in relevant_docs:
                            relevant_files_returned = relevant_files_returned +1
                            dcg = dcg + (float(1)/(math.log(total_files_returned+1,2)))
                else:
                    break
            ndcg = round((float(dcg)/float(idcg)),4)
            ndcg_at_10_dict[topic] = ndcg
        except:
            print("Topic DNE")
    return ndcg_at_10_dict


def ndcg_at_1000(results_list,qrel_index):
    # thjis method calculated the ndcg at 10

    ndcg_at_1000_dict = {}
    topic_ids = list(qrel_index.keys())
    ndcg = 0
    for topic in topic_ids:
        try:
            dcg = 0
            idcg = 0
            ndcg = 0
            total_files_returned = 0
            relevant_files_returned = 0
            relevant_docs = list(qrel_index[topic])
            for result in results_list:
                if total_files_returned <= 1000:
                    if result.query_id == topic:
                        total_files_returned = total_files_returned + 1
                        if total_files_returned <= len(relevant_docs):
                            idcg = idcg + (float(1)/(math.log(total_files_returned+1,2)))
                        if result.docno in relevant_docs:
                            relevant_files_returned = relevant_files_returned +1
                            dcg = dcg + (float(1)/(math.log(total_files_returned+1,2)))
            if idcg == 0:
                ndcg = 0
            else:
                ndcg = round((float(dcg)/float(idcg)),4)
            ndcg_at_1000_dict[topic] = ndcg
        except:
            print("Topic DNE")
    return ndcg_at_1000_dict


def doc_time_function(docno,doc_no_to_internal_id,internal_id_to_metadata):
    # This method returns a value the doc_time_function
    doc_time_function = 0
    file_internal_id = doc_no_to_internal_id.get(docno)
    current_file_meta_data = metadata()
    current_file_meta_data = current_file_meta_data.create_meta_data(internal_id_to_metadata.get(file_internal_id))
    doc_time_function = 0.018*int(current_file_meta_data.doc_length) + 7.8
    return doc_time_function

def time_based_gain(results_list,qrel_index,docno_to_internal_id,internal_id_to_metadata):
    # this method calculates the time based gain
    probability_click_given_relevant = 0.64
    probability_click_given_nonrelevant = 0.39
    probability_save_given_relevant = 0.77
    probability_save_given_nonrelevant = 0.27
    gain_factor = 0
    time_to_evaluate_summary = 4.4

    time_based_gain_dict = {}
    topic_ids = list(qrel_index.keys())
    for topic in topic_ids:
        try:
            relevant_docs = list(qrel_index[topic])
            time_based_gain_value = 0
            discount_factor = 0
            time_factor = 0
            gain_factor = 0
            relevant_files_returned = 0

            for i in range(0,len(results_list)):
                result = results_list[i]
                doc_time = 0
                if result.query_id == topic:
                    if i>0:
                        prev_result = results_list[i-1]
                        doc_time = doc_time_function(prev_result.docno,docno_to_internal_id,internal_id_to_metadata)

                        if prev_result.docno in relevant_docs:
                            time_factor = time_factor + time_to_evaluate_summary + (doc_time*probability_click_given_relevant)
                        else:
                            time_factor = time_factor + time_to_evaluate_summary + (doc_time*probability_click_given_nonrelevant)

                        if result.docno in relevant_docs:
                            gain_factor = 1*(probability_click_given_relevant*probability_save_given_relevant)
                        else:
                            gain_factor = 0*probability_save_given_nonrelevant*probability_save_given_nonrelevant
                    else:
                        time_factor = 0
                    discount_factor = math.exp(float(-1)*float(time_factor)*math.log(2)*(float(1/224)))
                    time_based_gain_value =  time_based_gain_value + (gain_factor*discount_factor)
                    discount_factor = 0
            time_based_gain_dict[topic] = time_based_gain_value
        except:
            print("Topic DNE")
    return time_based_gain_dict

def save_student_data(student, average_precision_dict, precision_at_10_dict, ndcg_at_10_dict, ndcg_at_1000_dict, time_based_gain_dict,read_directory_path):
    if (os.path.exists(read_directory_path)) == False:
        os.makedirs(read_directory_path)
    averages_list = []
    key_list = list(average_precision_dict.keys())
    mean_average_precision = 0
    mean_precision_at_10 = 0
    mean_ndcg_at_10 = 0
    mean_ndcg_at_1000 = 0
    mean_time_based_gain = 0
    counter = 0
    save_string = read_directory_path+"/"+student + "_evaluation_results.xlsx"
    book = xlsxwriter.Workbook(save_string)
    sheet1 = book.add_worksheet()
    sheet1.write(0, 0, "Student")
    sheet1.write(1, 0, "Topic_ID")
    sheet1.write(2, 0, "precision_at_10")
    sheet1.write(3, 0, "average_precision")
    sheet1.write(4, 0, "ndcg_at_10")
    sheet1.write(5, 0, "ndcg_at_1000")
    sheet1.write(6, 0, "time_based_gain")
    for i in range(0,len(key_list)):
        key = key_list[i]
        counter = counter+1
        mean_average_precision = mean_average_precision + average_precision_dict.get(key)
        mean_precision_at_10 = mean_precision_at_10 + precision_at_10_dict.get(key)
        mean_ndcg_at_10 = mean_ndcg_at_10 + ndcg_at_10_dict.get(key)
        mean_ndcg_at_1000 = mean_ndcg_at_1000 + ndcg_at_1000_dict.get(key)
        mean_time_based_gain = mean_time_based_gain + time_based_gain_dict.get(key)
        sheet1.write(0,counter,student)
        sheet1.write(1,counter,key)
        sheet1.write(2,counter,precision_at_10_dict[key])
        sheet1.write(3,counter,average_precision_dict[key])
        sheet1.write(4,counter,ndcg_at_10_dict[key])
        sheet1.write(5,counter,ndcg_at_1000_dict[key])
        sheet1.write(6,counter,time_based_gain_dict[key])
    counter = float(counter)
    mean_average_precision = float(mean_average_precision)/counter
    mean_precision_at_10 = float(mean_precision_at_10)/counter
    mean_ndcg_at_10 = float(mean_ndcg_at_10)/counter
    mean_ndcg_at_1000 = float(mean_ndcg_at_1000)/counter
    mean_time_based_gain = float(mean_time_based_gain)/counter
    book.close()
    averages_list = [mean_average_precision,mean_precision_at_10,mean_ndcg_at_10,mean_ndcg_at_1000,mean_time_based_gain]
    return averages_list

def save_average_dict(averages_dictionary,read_directory_path):
    if (os.path.exists(read_directory_path)) == False:
        os.makedirs(read_directory_path)
    save_string = read_directory_path+"/"+"average_evaluation_results.xlsx"
    book = xlsxwriter.Workbook(save_string)
    sheet1 = book.add_worksheet()
    sheet1.write(0, 0, "Student")
    sheet1.write(1, 0, "mean_precision_at_10")
    sheet1.write(2, 0, "mean_average_precision")
    sheet1.write(3, 0, "mean_ndcg_at_10")
    sheet1.write(4, 0, "mean_ndcg_at_1000")
    sheet1.write(5, 0, "mean_time_based_gain")

    counter = 0
    students = list(averages_dictionary.keys())
    bad = "BAD FORMATTING"
    for student in students:
        counter = counter+1
        results_list = averages_dictionary[student]
        if results_list[0]== bad:
            sheet1.write(0, counter, student)
            sheet1.write(1, counter, bad)
            sheet1.write(2, counter, bad)
            sheet1.write(3, counter, bad)
            sheet1.write(4, counter, bad)
            sheet1.write(5, counter, bad)
        else:
            sheet1.write(0, counter, student)
            sheet1.write(1, counter, results_list[1])
            sheet1.write(2, counter, results_list[0])
            sheet1.write(3, counter, results_list[2])
            sheet1.write(4, counter, results_list[3])
            sheet1.write(5, counter, results_list[4])
    book.close()



def evaluate_measures(results_dict,qrel_index,docno_to_internal_id,internal_id_to_metadata,read_directory_path):
    # this method runs all the evaluations and saves to disk
    student_tags = list(results_dict.keys())
    averages_dict = {} # Student:[mean results]
    for student in student_tags:
        try:
            print(student)
            results_list = results_dict[student]
            average_precision_dict = average_precision(results_list,qrel_index)
            precision_at_10_dict = precision_at_10(results_list,qrel_index)
            ndcg_at_10_dict = ndcg_at_10(results_list,qrel_index)
            ndcg_at_1000_dict = ndcg_at_1000(results_list,qrel_index)
            time_based_gain_dict = time_based_gain(results_list,qrel_index,docno_to_internal_id,internal_id_to_metadata)
            averages_dict[student] = save_student_data(student, average_precision_dict, precision_at_10_dict, ndcg_at_10_dict, ndcg_at_1000_dict, time_based_gain_dict,read_directory_path)
        except:
            averages_dict[student] = ["BAD FORMATTING"]
    save_average_dict(averages_dict,read_directory_path)
