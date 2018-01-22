import gzip

class metadata:
    #This class stores the metadata for a given file
    # Default values are all set to -1 indicating that data is to be filled
    internal_id = -1
    docno = -1
    date = -1
    headline = -1

def convert_docno_to_date(docno):
    # This method convers a docno to its relevant date
    print('hello')
    <DOCNO> LA010189-0001 </DOCNO>



def read_gzip_file(gzip_file_path):
    #This method reads through the gzip file, and searches for doc tags
    gzip_file_path = '/Users/ayser/Dropbox/Waterloo/3A/Courses/Course_Projects/msci_541/Assignments/Data/latimes.gz'
    # 'doc_counter is used to keep track of how many documents are saved'
    doc_counter = 0
    #opening the .gz file and reading it line by line
    with gzip.open(gzip_file_path,'rt') as gz_file:
        #This variable will store the current document
        current_doc = ""
        #This variable is used to keep track of the internal_id of each doc
        current_doc_internal_id = 0
        # This dictionary is used to store the relationship between internal_id and docno
        doc_no_to_internal_id = {}
        # This dictionary is used to store the relationship between internal_id and metadata
        internal_id_to_meta_data ={}
        #This variable is used to keep track of all of the meta data
        metadata_string = ""
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
                docno  = docno[7:]
                docno = docno[0:len(docno)-8]
                docno = docno.strip(" ")
                current_doc_meta_data.docno = docno
                current_doc_meta_data.date = convert_docno_to_date(docno)

            current_doc = current_doc + line

            if line[0:5]=='</DOC>':
                doc_counter +=1
                save_doc(current_doc)
                current_doc = ""

            # If a new document is being read, clear out the variable saving the doc
            if new_file = True:
                current_doc = ""

    print(doc_counter)


readgzip('/Users/ayser/Dropbox/Waterloo/3A/Courses/Course_Projects/msci_541/Assignments/Data/latimes.gz')


"""
First generate internal_id
Next extract and store all meta Data from doc
Map internal data to docno
Next save doc as file
do while all files exist
save metadata file separately
"""
