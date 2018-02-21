import gzip, re, sys, os,time
from metadata import *


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
    print("test")

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
        for line in gz_file:
            # If a <DOC> tag is detected,internal_id,new meta data are initialized
            if line[0:5]=='<DOC>':
                current_doc_internal_id += 1
                doc_counter += 1
                current_doc_meta_data = metadata()
                current_doc_meta_data.internal_id = current_doc_internal_id
            # if a <DOCNO> tag is detected, docno is stored in metadata, date is extracted
            if line[0:7]=='<DOCNO>':
                # Extracting the docno from the string
                docno=line
                docno  = docno[7:]
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
                docno_to_internal_id.update({current_doc_meta_data.docno:current_doc_meta_data.internal_id})
                internal_id_to_metadata.update({current_doc_meta_data.internal_id:str(current_doc_meta_data)})
                save_doc(current_doc,current_doc_meta_data,save_directory_path)
                metadata_list.append(current_doc_meta_data)
                current_doc = ""
        # Saving dictionaries and metadata to file
        save_docno_to_internal_id(docno_to_internal_id,save_directory_path)
        save_internal_id_to_metadata(internal_id_to_metadata,save_directory_path)
        save_meta_data(metadata_list,save_directory_path)
    print(str(doc_counter)+" documents located, processed, and saved.")

# Program Starts Here
try:
    # Retrieving arguments from command line
    t = time.time()
    directory_list = sys.argv
    gzip_file_path = directory_list[1]
    save_directory_path = directory_list[2]
    #Checking to see if the destination directory exits, creating it if it doesn't
    if (os.path.exists(save_directory_path))==False:
        os.makedirs(save_directory_path)
    else:
        print("Error: Direcotry Already Exists")
        sys.exit()
    #Reading from gzip'd file:
    read_gzip_file(gzip_file_path,save_directory_path)
    a = time.time()
    total = a-t
    print("Program ran in approximately "+str(total)+" seconds.")
except:
    gzip_reader_error()
    sys.exit()
