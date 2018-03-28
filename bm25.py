import ast,sys,os,json, time, re,math,operator, xlsxwriter
from objects import *
import lexicon_engine as lexicon_engine
from nltk.stem import PorterStemmer

class results:
    # This object stores the qrel data
    query_id = -1
    student_tag = ""
    docno = ""
    rank = -1
    score = -1

def json_read(filepath):
    return_dict = {}
    data = json.load(open(filepath))
    return return_dict

def bm25(directory,query_dict,k1,k2,b,output_filename):
    a = time.time()
    # This method takes in a query list, inverted index, returns a dictionary {rank:result}
    c = time.time()
    # Getting docno_to_internal_id_file
    docno_to_internal_id_file_path = directory+"/"+"doc_no_to_internal_id.txt"
    docno_to_internal_id_file  = open(docno_to_internal_id_file_path, "r")
    doc_no_to_internal_id_string = ""
    for line in docno_to_internal_id_file:
        doc_no_to_internal_id_string = doc_no_to_internal_id_string +line
    json_as_string = doc_no_to_internal_id_string.replace("'", "\"")
    doc_no_to_internal_id = json.loads(json_as_string)

    internal_id_to_docno = {}
    doc_keys = list(doc_no_to_internal_id.keys())
    for key in doc_keys:
        internal_id_to_docno[doc_no_to_internal_id[key]] = key

    # Loading internal id to metadata mapping
    internal_id_to_meta_data_file_path = read_directory_path+"/"+"internal_id_to_meta_data.txt"
    internal_id_to_meta_data_file  = open(internal_id_to_meta_data_file_path, "r")
    internal_id_to_metadata_string = ""
    for line in internal_id_to_meta_data_file:
        internal_id_to_metadata_string = internal_id_to_metadata_string + line
    internal_id_to_metadata = ast.literal_eval(internal_id_to_metadata_string)

    # Loading inverted_index
    inverted_index = lexicon_engine.read_inverted_index(read_directory_path)
    trial = list(inverted_index.values())

    # Loading tokens_to_id
    tokens_to_id = lexicon_engine.read_tokens_to_id(read_directory_path)

    #Loading collection data
    collection_data_file = read_directory_path+"/"+"collection_info.txt"
    collection_data_file = open(collection_data_file,"r")
    average_word_count = 0
    collection_size = 0

    for line in collection_data_file:
        average_word_count = int(float((line[0:line.index("_")])))
        collection_size = int(float((line[line.index("_")+1:])))

    t = time.time()
    total = t - c
    c = time.time()
    print("All data loaded in "+str(total)+" seconds")

    query_ranked_dict = {} # this is {query_id:[ordered_result_list]}
    query_list = list(query_dict.keys())
    stemmer = PorterStemmer()
    for query in query_list:
        term_list = query_dict[query] # these are the terms in the query
        doc_id_to_bm25_score = {}
        bm25_score = 0
        sorted_doc_id_to_bm25_score_keys = []
        for term in term_list:
            try:
                #term = stemmer.stem(term)
                term_id = int(tokens_to_id[term])
                postings_list = inverted_index[term_id] # [{doc_id:count}]
                no_of_rel_documents = len(postings_list)/2
                for i in range(0,len(postings_list)):
                    posting = postings_list[i] # {doc_id:count}
                    doc_id = list(postings_list[i].keys())
                    doc_id = doc_id[0]
                    term_count_in_doc = int(posting[doc_id])
                    current_file_meta_data = metadata()
                    qf = 1
                    current_file_meta_data = current_file_meta_data.create_meta_data(internal_id_to_metadata.get(int(doc_id)))
                    k = k1*((1-b)+b*(float(current_file_meta_data.doc_length)/float(average_word_count)))
                    try:
                        bm25_score = doc_id_to_bm25_score[int(doc_id)]
                    except:
                        bm25_score = bm25_score
                    bm25_score = bm25_score + ((((k1+1)*term_count_in_doc)/float((k+term_count_in_doc))*(((k2+1)*qf)/(k2+qf)))*(math.log((collection_size-no_of_rel_documents+0.5)/(no_of_rel_documents+0.5))))
                    doc_id_to_bm25_score[int(doc_id)] = bm25_score
                    bm25_score = 0
            except:
                bm25_score = 0

        sorted_doc_id_to_bm25_score_keys = sorted(doc_id_to_bm25_score,key=doc_id_to_bm25_score.get,reverse=True)
        sorted_doc_id_to_bm25_score_keys = list(sorted_doc_id_to_bm25_score_keys[:1000])

        ranked_result_list = []
        rank_counter = 0
        for doc_id in sorted_doc_id_to_bm25_score_keys:
            rank_counter= rank_counter+1
            current_score = doc_id_to_bm25_score[doc_id]
            current_result = results()
            current_result.score = current_score
            current_result.docno = internal_id_to_docno[int(doc_id)]
            current_result.query_id = query
            current_result.student_tag = "bm25"
            current_result.rank = rank_counter
            ranked_result_list.append(current_result)
        query_ranked_dict[query] = ranked_result_list
        t = time.time()
        total = t - c
        print("BMScore & Ranking Complete for "+str(query)+" in "+str(total)+" seconds")

    inverted_index = None
    internal_id_to_metadata = None
    docno_to_internal_id = None
    tokens_to_id = None

    #########################################################

    save_string = directory+"/"+output_filename+".xlsx"
    book = xlsxwriter.Workbook(save_string)
    sheet1 = book.add_worksheet()
    sheet1.write(0, 0, "Query")
    sheet1.write(0, 1, "q0")
    sheet1.write(0, 2, "docno")
    sheet1.write(0, 3, "rank")
    sheet1.write(0, 4, "score")
    sheet1.write(0, 5, "a25choudBM25")


    #########################################################
    counter = 0
    write_string = ""
    for query in query_list:
        ranked_list = list(query_ranked_dict[query])
        for result in ranked_list:
            write_string = write_string + str(query)+" "+"q0 "+str(result.docno)+" "+str(result.rank)+" "+str(result.score)+" a25choudBM25"+'\n'
            counter = counter+1
            sheet1.write(counter,0, str(query))
            sheet1.write(counter,1, "q0")
            sheet1.write(counter,2, result.docno)
            sheet1.write(counter,3, result.rank)
            sheet1.write(counter,4, result.score)
            sheet1.write(counter,5, "a25choudBM25")

    book.close()
    output_path = directory+"/"+output_filename
    current_file = open(output_path,"w")
    current_file.write(write_string)
    t= time.time()
    total = t- a
    print("Finished in "+str(total)+" seconds")
    print("BM25 Complete")

#Program starts here
print("Running bm25.py")

input_list = sys.argv
read_directory_path = input_list[1]
query_path = input_list[2]

query_doc = open(query_path,"r")
# intializing query dict {query_no:[query_list]}
query_dict = {}

# The following segment will return a populated query_list
query_id = -1
query_string = ""
query_list = []
add_dict = False
for line in query_doc:
    line = line.lower()
    try:
        query_id = int(line)
        add_dict = False
    except:
        query_string = str(line)
        query_list = re.sub("[^\w]", " ",  query_string).split()
        for item in query_list:
            if item.isalnum()==False:
                query_list.remove(item)
        add_dict = True
    if add_dict:
        query_dict[query_id]=query_list

bm25(read_directory_path,query_dict,1.2,7,0.75,"a25choud-hw4-bm24-baseline.txt")
