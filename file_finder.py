# Objective of this program is to return a given file after given a prompt
# First the program will load both dictinaries and the metadata file
# Next, the program will use the given prompts to find the requested file
# Finally, the program will read the file, and print it out
import sys, os,json,ast
class metadata:
    #This class stores the metadata for a given file
    # Default values are all set to -1 indicating that data is to be filled
    internal_id = -1
    docno = -1
    date = -1
    headline = -1

    def __str__(self):
        return '<'+'internal_id'+str(self.internal_id) + 'docno'+str(self.docno) +'date'+str(self.date)+'headline'+str(self.headline)+'>'

    def create_meta_data(self,meta_data_string):
        #Extracting internal_id from saved string
        substring1 = '<internal_id'
        substring2 = 'docno'
        self.internal_id = meta_data_string[(meta_data_string.index(substring1)+len(substring1)):meta_data_string.index(substring2)]
        #Extracting docno from saved string
        substring1 = 'docno'
        substring2 = 'date'
        self.docno = meta_data_string[(meta_data_string.index(substring1)+len(substring1)):meta_data_string.index(substring2)]
        #Extracting date from saved string
        substring1 = 'date'
        substring2 = 'headline'
        self.date = meta_data_string[(meta_data_string.index(substring1)+len(substring1)):meta_data_string.index(substring2)]
        #Extracting headline from saved string
        substring1 = "headline"
        substring2 = ">"
        self.headline = meta_data_string[(meta_data_string.index(substring1)+len(substring1)):meta_data_string.index(substring2)]

        return self

#Program starts here
try:
    print("trying")
    # Reading arguments presented from input
    '''
    input_list = sys.argv
    read_directory_path = input_list[1]
    id_type = input_list[2]
    '''
    read_directory_path = "/Users/ayser/Dropbox/Waterloo/3A/Courses/Course_Projects/msci_541/test"
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
    '''
    if(id_type == 'docno'):
        docno = input_list[3]
        file_internal_id = doc_no_to_internal_id.get(docno)
    else:
        file_internal_id = input_list[3]
    '''
    # Finding internal_id based on docno
    docno = "LA092390-0001"
    file_internal_id = doc_no_to_internal_id.get(docno)
    file_internal_id = int(file_internal_id)
    # Getting from internal_id to meta_data
    current_file_meta_data = metadata()
    current_file_meta_data = current_file_meta_data.create_meta_data(internal_id_to_metadata.get(file_internal_id))
    current_file_path = str(read_directory_path) + "/" + str(current_file_meta_data.date)
    'get file, open and print'
except:
    print("Error in file processing... Try again..")

#find_internal_id(LA092390-0001)
