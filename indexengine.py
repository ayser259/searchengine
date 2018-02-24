# This file holds all the helper methods for the 'gzip_reader_methods.py' file
import gzip, re, sys, os,json, time
from objects import *
import lexicon_engine as lexicon_engine

def gzip_reader_error():
    print("There has been an error with your request")
    print("Please ensure that the path for the both the gzip file and the saving directory is accurate. ")
    print("This program is run from the command line and accepts two arguements in specific formats")
    print("They are as follows: ")
    print("1. The gziped file that is to be read. The full path to the file should be provided. For example: ")
    print("Users/ayser/Dropbox/Waterloo/3A/Courses/Course_Projects/msci_541/Assignments/Data/latimes.gz")
    print("2. The destination directory shoudl not exist and should be provided in the following format, such that the folder 'test' does not exist:")
    print("Users/ayser/Dropbox/Waterloo/3A/Courses/Course_Projects/msci_541/test")
    sys.exit()

def convert_docno_to_date(docno):
    # This method convers a docno to its relevant date
    month = docno[2:4]
    day = docno[4:6]
    year = docno[6:8]

    if month =='01':
        month = "January"
    if month =='02':
        month = "February"
    if month =='03':
        month = "March"
    if month =='04':
        month = "April"
    if month =='05':
        month = "May"
    if month =='06':
        month = "June"
    if month =='07':
        month = "July"
    if month =='08':
        month = "August"
    if month =='09':
        month = "September"
    if month =='10':
        month = "October"
    if month =='11':
        month = "November"
    if month =='12':
        month = "December"
    date = month + " " + day + " "+ "19"+year
    return date

def extract_headline(headline):
    # This method extracts the headline from the given headline text
    try:
        substring1 = "<P>"
        substring2 = "</P>"
        headline = headline[(headline.index(substring1)+len(substring1)):headline.index(substring2)]
        return str(headline)
    except:
        headline = ""
        return headline

def save_doc(current_doc,current_doc_meta_data,save_directory_path):
    # This method is used to save the current document
    date = current_doc_meta_data.date
    save_directory_path = save_directory_path+"/"+date
    # Search for folder based on date, if it doesn't exist, create it
    if (os.path.exists(save_directory_path)) == False:
        os.makedirs(save_directory_path)
    # Save file to preexisting or created folder
    file_path = os.path.join(save_directory_path, str(current_doc_meta_data.internal_id) + ".txt")
    current_file = open(file_path, "w")
    current_file.write(current_doc)
    current_file.close()

def save_docno_to_internal_id(doc_no_to_internal_id,save_directory_path):
    # This method is used to save the docno to internal id mapping
    if (os.path.exists(save_directory_path)) == False:
        os.makedirs(save_directory_path)
    file_path = os.path.join(save_directory_path, "doc_no_to_internal_id" + ".txt")
    current_file = open(file_path, "w")
    current_file.write(str(doc_no_to_internal_id))
    current_file.close()

def save_internal_id_to_metadata(internal_id_to_meta_data,save_directory_path):
    # This method is used to sasve the internal id to metadata mapping
    if (os.path.exists(save_directory_path)) == False:
        os.makedirs(save_directory_path)
    file_path = os.path.join(save_directory_path, "internal_id_to_meta_data" + ".txt")
    current_file = open(file_path, "w")
    current_file.write(str(internal_id_to_meta_data))
    current_file.close()

def save_meta_data(meta_data_list,save_directory_path):
    # This method is used to sasve the internal id to metadata mapping
    if (os.path.exists(save_directory_path)) == False:
        os.makedirs(save_directory_path)
    file_path = os.path.join(save_directory_path, "metadata" + ".txt")
    current_file = open(file_path, "w")
    for item in meta_data_list:
        current_file.write(str(item))
    current_file.close()

def read_gzip_file(gzip_file_path,save_directory_path):
    #This method reads through the gzip file, and searches for doc tags
    # 'doc_counter is used to keep track of how many documents are saved'
    doc_counter = 0
    #opening the .gz file and reading it line by line
# Assignment_2_start_a
    # This string is used to store tokenizable string, not full document
    token_string = ""
    # This boolean value keeps track of whether or not we are reading valid tokens
    is_token_tag = False
    # This dictionary is part_1 of lexicon: token --> token_ids
    tokens_to_id = {}
    # This dictionary is the inverted index
    inverted_index = {}
# Assignment_2_end_a
    with gzip.open(gzip_file_path,'rt') as gz_file:
        #This variable will store the current document
        current_doc = ""
        #This variable is used to keep track of the internal_id of each doc
        current_doc_internal_id = 0
        # This dictionary is used to store the relationship between internal_id and docno
        docno_to_internal_id = {}
        # This dictionary is used to store the relationship between internal_id and metadata
        internal_id_to_metadata ={}
        # Used to keep track of whether the line being read is part of the headline
        is_headline = False
        headline = ""
        # Used to keep track of all metadata
        metadata_list =[]
        # Starting to read through the file
# Assignment_2_start_a
        # This string is used to store tokenizable string, not full document
        token_string = ""
        # This boolean value keeps track of whether or not we are reading valid tokens
        is_token_tag = False
        # This dictionary is part_1 of lexicon: token --> token_ids
        tokens_to_id = {}
        # This dictionary is the inverted index
        inverted_index = {}
        t = time.time()
# Assignment_2_end_a
        for line in gz_file:

# Assignment_2_start_b

            if (line[0:6] =='<TEXT>') or (line[0:10] =='<HEADLINE>') or (line[0:0] =='<GRAPHIC>'):
                is_token_tag = True
            elif line[0:7] =='</TEXT>' or line[0:11] =='</HEADLINE>' or (line[0:10] =='</GRAPHIC>'):
                is_token_tag = False
            if is_token_tag == True:
                token_string = lexicon_engine.token_string_maker(line,token_string)
# Assignment_2_end_b
            # If a <DOC> tag is detected,internal_id,new meta data are initialized
            if line[0:5]=='<DOC>':
                current_doc_internal_id += 1
                doc_counter += 1
                current_doc_meta_data = metadata()
                current_doc_meta_data.internal_id = current_doc_internal_id
            # if a <DOCNO> tag is detected, docno is stored in metadata, date is extracted
            if line[0:7]=='<DOCNO>':
                # Extracting the docno from the string
                docno = line
                docno = docno[7:]
                docno = docno[0:14]
                docno = docno.strip(" ")
                # Saving docno and date to metadata
                current_doc_meta_data.docno = docno
                current_doc_meta_data.date = convert_docno_to_date(docno)
            # Storing headline values within a singular value

            if line[0:10]=="<HEADLINE>" or is_headline == True :
                is_headline = True
                headline =  headline + line

            # Extracting headlines, which are a multline value
            if line[0:11]=="</HEADLINE>":
                headline = headline + line
                is_headline = False
                current_doc_meta_data.headline = str(extract_headline(headline))
                headline = ""
            # Storing all the relevant lines for a document within a variable
            current_doc = current_doc + line
            # Saving singular document after encountering the end document tag
            if line[0:6]=='</DOC>':
# Assignment_2_start_c

                tokens = lexicon_engine.tokenize(current_doc)
                token_ids = lexicon_engine.convert_tokens_to_ids(tokens,tokens_to_id)
                word_count = lexicon_engine.count_words(token_ids)
                lexicon_engine.add_to_postings(word_count,current_doc_internal_id,inverted_index)
                current_doc_meta_data.doc_length = len(token_ids)

# Assignment_2_end_c
                docno_to_internal_id.update({current_doc_meta_data.docno:current_doc_meta_data.internal_id})
                internal_id_to_metadata.update({current_doc_meta_data.internal_id:str(current_doc_meta_data)})
                save_doc(current_doc,current_doc_meta_data,save_directory_path)
                metadata_list.append(current_doc_meta_data)
                current_doc = ""
                token_string = ""
                tokens = ""
                token_ids =""
        # Saving dictionaries and metadata to file
# Assignment_2_start_d

        id_to_tokens = lexicon_engine.convert_ids_to_tokens(tokens_to_id)
        lexicon_engine.save_tokens_to_id(tokens_to_id,save_directory_path)
        lexicon_engine.save_id_to_tokens(id_to_tokens,save_directory_path)
        lexicon_engine.save_inverted_index(inverted_index,save_directory_path)

# Assignment_2_end_d
        save_docno_to_internal_id(docno_to_internal_id,save_directory_path)
        save_internal_id_to_metadata(internal_id_to_metadata,save_directory_path)
        save_meta_data(metadata_list,save_directory_path)
        print(str(doc_counter)+" documents located, processed, and saved.")
        print(doc_counter)
