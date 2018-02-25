# Objective of this program is to return a given file after given a prompt
# First the program will load both dictinaries and the metadata file
# Next, the program will use the given prompts to find the requested file
# Finally, the program will read the file, and print it out
import sys, os,json,ast
from metadata import *

def file_finder_error():
    print("There is an error with the format of the input")
    print("please ensure the data input is accurate")
    print("If no data is returned, and the input data is correct, no files exist attached to that input")
    print("The command line arguements accepts three arguements, they are as follows:")
    print("1. The path to the folder where the files are stored. ")
    print("example: /Users/ayser/Dropbox/Waterloo/3A/Courses/Course_Projects/msci_541/test ")
    print("2. The type of id used to request the file. This can be either the 'docno' or the 'id'")
    print("3. The id of the file being requested, in the format specifide ")
    print("docno ids follow the format LAxxxxxx-xxxx")
    print("id is an integer")
#Program starts here
try:
    # Reading arguments presented from input
    input_list = sys.argv
    read_directory_path = input_list[1]
    id_type = input_list[2]

    # Loading all relevant files:
    # Loading metadata string
    metadata_file_path = read_directory_path+"/"+"metadata.txt"
    metadata_file  = open(metadata_file_path, "r")
    metadata_string = ""
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
    # Determining file_internal_id to quickly search and find the file
    file_internal_id =-1

    if(id_type == 'docno'):
        docno = input_list[3]
        docno = docno.strip(" ")
        print(len(docno))
        print(docno)
        if(len(docno)==13):
            print('b')
            file_internal_id = doc_no_to_internal_id.get(docno)
        else:
            print('c')
            file_finder_error()
            sys.exit()
    else:
        if(id_type=="id"):
            file_internal_id = input_list[3]
        else:
            file_finder_error()
            sys.exit()

    file_internal_id = int(file_internal_id)
    # Getting from internal_id to meta_data
    current_file_meta_data = metadata()
    current_file_meta_data = current_file_meta_data.create_meta_data(internal_id_to_metadata.get(file_internal_id))
    current_file_path = str(read_directory_path) + "/" + str(current_file_meta_data.date)+"/"+str(current_file_meta_data.internal_id)+".txt"
    # Printing out requested data
    current_file = open(current_file_path)
    print('4')

    print("Returning Requested File...")
    print("docno: "+str(current_file_meta_data.docno))
    print("internal id: "+ str(current_file_meta_data.internal_id))
    print("date: "+ str(current_file_meta_data.date))
    print("headline: "+ str(current_file_meta_data.headline))
    print("raw document: ")

    for line in current_file:
        print(line)
except:
    print("Error in file processing... Try again..")
    file_finder_error()

#find_internal_id(LA092390-0001)
