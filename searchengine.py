# This program runs the search engine program
import ast,sys,os,json, time, re,math
from objects import *
import lexicon_engine as lexicon_engine
from snippet_engine import *

def bm25_top_10(doc_no_to_internal_id,internal_id_to_metadata,inverted_index,tokens_to_id):
    # Retrieving Query from user
    print()
    query = input("Search: ")
    c = time.time()
    query = query.lower()
    query = re.sub(r'\W+', ' ', query)
    query_list =  query.split()

    # Perform bm25 retrieval on query
    doc_id_to_bm25_score = {}
    k1 = 1.2
    k2 = 7
    b = 0.75

    for term in query_list:
        try:
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
    sorted_doc_id_to_bm25_score_keys = list(sorted_doc_id_to_bm25_score_keys[:10]) # Top 10 doc list

    rank_to_docno = {} # {rank:docno}
    rank_counter = 0
    for doc_id in sorted_doc_id_to_bm25_score_keys:
        rank_counter +=1
        docno = internal_id_to_docno[int(doc_id)]
        rank_to_docno[rank_counter] = docno
        current_file_meta_data = current_file_meta_data.create_meta_data(internal_id_to_metadata.get(int(doc_id)))
        # Print results
        headline = str(current_file_meta_data.headline).strip()
        if len(headline)<1:
            headline = first_x_characters(directory,current_file_meta_data,50)
        print_string = str(rank_counter)+". "+headline+" ("+str(current_file_meta_data.date)+")"
        print(print_string)
        print()
        snippet = top_3_lines(directory,current_file_meta_data,query_list)
        print(snippet)
        print()

    t = time.time()
    total = t - c
    print("Retrieval performed in "+str(total)+" seconds")
    return rank_to_docno

def read_doc(rank_to_docno,rank,doc_no_to_internal_id,internal_id_to_metadata,directory):
    # Print document to screan given rank
    docno = rank_to_docno[rank]
    print("Docno")
    print(docno)
    file_internal_id = doc_no_to_internal_id.get(docno)
    file_internal_id = int(file_internal_id)
    # Getting from internal_id to meta_data
    current_file_meta_data = metadata()
    current_file_meta_data = current_file_meta_data.create_meta_data(internal_id_to_metadata.get(file_internal_id))
    current_file_path = str(directory) + "/" + str(current_file_meta_data.date)+"/"+str(current_file_meta_data.internal_id)+".txt"
    # Printing out requested data
    current_file = open(current_file_path)

    print("Requested File:")
    for line in current_file:
        print(line)

print("Loading Search Engine...")

try:
    c = time.time()
    directory = "/Users/ayser/Dropbox/Waterloo/3A/Courses/Course_Projects/msci_541/la_times_files"
    # Loading all relevant information

    # Getting docno_to_internal_id
    docno_to_internal_id_file_path = directory+"/"+"doc_no_to_internal_id.txt"
    docno_to_internal_id_file  = open(docno_to_internal_id_file_path, "r")
    doc_no_to_internal_id_string = ""
    for line in docno_to_internal_id_file:
        doc_no_to_internal_id_string = doc_no_to_internal_id_string +line
    json_as_string = doc_no_to_internal_id_string.replace("'", "\"")
    doc_no_to_internal_id = json.loads(json_as_string)

    # Getting internal_id_to_docno
    internal_id_to_docno = {}
    doc_keys = list(doc_no_to_internal_id.keys())
    for key in doc_keys:
        internal_id_to_docno[doc_no_to_internal_id[key]] = key

    # Loading internal id to metadata mapping
    internal_id_to_meta_data_file_path = directory+"/"+"internal_id_to_meta_data.txt"
    internal_id_to_meta_data_file  = open(internal_id_to_meta_data_file_path, "r")
    internal_id_to_metadata_string = ""
    for line in internal_id_to_meta_data_file:
        internal_id_to_metadata_string = internal_id_to_metadata_string + line
    internal_id_to_metadata = ast.literal_eval(internal_id_to_metadata_string)

    # Loading inverted_index
    inverted_index = lexicon_engine.read_inverted_index(directory)

    # Loading tokens_to_id
    tokens_to_id = lexicon_engine.read_tokens_to_id(directory)

    #Loading collection data
    collection_data_file = directory+"/"+"collection_info.txt"
    collection_data_file = open(collection_data_file,"r")
    average_word_count = 0
    collection_size = 0

    for line in collection_data_file:
        average_word_count = int(float((line[0:line.index("_")])))
        collection_size = int(float((line[line.index("_")+1:])))

    t = time.time()
    total = t - c
    print("All data loaded in "+str(total)+" seconds")
    print("Program Ready..")

    exit = False
    rank_to_docno = bm25_top_10(doc_no_to_internal_id,internal_id_to_metadata,inverted_index,tokens_to_id)
    while exit == False:
        try:
            print("To read one of the above documents, enter the rank of the document (1-10)")
            print("To perform another search, Enter 'N' ")
            print("To exit the program, Enter 'Q' ")
            query_list = [1,2,3,4,5,6,7,8,9,10]
            command = input("Enter Command: ")
            if command == "N":
                print("Enter New Query")
                # Now retrieving documents, displaying results and creating snippets
                rank_to_docno = bm25_top_10(doc_no_to_internal_id,internal_id_to_metadata,inverted_index,tokens_to_id)
            elif command =="Q":
                exit = True
                sys.exit()
            elif int(command) in query_list:
                read_doc(rank_to_docno,int(command),doc_no_to_internal_id,internal_id_to_metadata,directory)
                print()
            else:
                print("Input incorrectly formatted, try again")
        except:
            print("Input incorrectly formatted, try again")
except:
    print("Error 1")
