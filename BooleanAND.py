import lexicon_engine as lexicon_engine
import ast,sys,os,json, time
from objects import *

a = time.time()
# Reading arguments presented from input
input_list = sys.argv
read_directory_path = input_list[1]
query_doc = input_list[2]
output_doc = input_list[3]

# Loading the internal_id_to_meta_data Object
query_doc_path = read_directory_path+query_doc
query_doc = open(query_doc_path,"r")

print("Starting Program")
# Loading the intenal_id to metadatafile
internal_id_to_meta_data_file_path = read_directory_path+"internal_id_to_meta_data.txt"
internal_id_to_meta_data_file  = open(internal_id_to_meta_data_file_path, "r")
internal_id_to_metadata_string = ""
for line in internal_id_to_meta_data_file:
    internal_id_to_metadata_string = internal_id_to_metadata_string + line
internal_id_to_metadata = ast.literal_eval(internal_id_to_metadata_string)
print("line 24 internal_id_to_metadata complete")

# Loading the inverted index
b= time.time()
inverted_index = lexicon_engine.read_inverted_index(read_directory_path)
t = time.time()
total = t-b
print("line 30 inverted_index loaded in "+str(total)+" seconds")


# Loading tokens_to_id dictionary
b= time.time()
tokens_to_id = lexicon_engine.read_tokens_to_id(read_directory_path)
t = time.time()
total = t-b
print("tokens_to_id loaded in"+str(total)+ 'Seconds')
# initialixng results dictionary {docno: results_list[]}
results_dict = {}

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
        query_list = list(query_string.split())
        for item in query_list:
            if item.isalnum()==False:
                query_list.remove(item)
        add_dict = True
    if add_dict:
        query_dict[query_id]=query_list

# This segment of the code will return a query_id_to_valid_terms[query_id]=valid_term_list
# This will return all the valid docs for every query
query_id_to_valid_docs = {}
for query_id in query_dict:
    query_list = query_dict[query_id]
    valid_doc_list = []
    no_of_queries = len(query_list)
    query_counter = {} # {doc_id:count_of_term_id_in_current_loop}
    for query in query_list:
        try:
            token_id = tokens_to_id[query]
            postings_list = inverted_index[token_id] # list of all docs with term
            for i in range(0,len(postings_list)):
                post = list(postings_list[i].keys())
                post = post[0]
                # post is the doc_id
                try:
                    query_counter[post] = query_counter[post] +1
                except:
                    query_counter[post] = 1
            query_counter_keys = list(query_counter.keys())
            for doc in query_counter_keys:
                if query_counter[doc] == no_of_queries:
                    valid_doc_list.append(doc)
            query_id_to_valid_docs[query_id] = valid_doc_list
        except:
            # Do nothing
            x=1

            # Now we have to find docno, rank, score and save to string
write_string = ""
for query_id in list(query_id_to_valid_docs.keys()):
    doc_list = query_id_to_valid_docs[query_id]
    rank = 0
    for doc in doc_list:
        rank = rank +1
        current_result_metadata = metadata()
        current_result_metadata = current_result_metadata.create_meta_data(internal_id_to_metadata.get(int(doc)))
        docno = current_result_metadata.docno
        score = len(doc_list)-rank
        write_string = write_string + str(query_id)+" "+"q0 "+str(docno)+" "+str(rank)+" "+str(score)+" a25choudAND"+'\n'
# Writing to file
if (os.path.exists(read_directory_path)) == False:
        os.makedirs(read_directory_path)
save_directory_path = read_directory_path + "/" + output_doc

current_file = open(save_directory_path, "w")
current_file.write(str(write_string))
current_file.close()
t =time.time()
total = t-a
print("BooleanAND retrieval completed in "+str(total)+" seconds")
