import gzip, re, sys, os

class metadata:
    #This class stores the metadata for a given file
    # Default values are all set to -1 indicating that data is to be filled
    internal_id = -1
    docno = -1
    date = -1
    headline = -1

    def __str__(self):
        return '<'+'internal_id'+internal_id + 'docno'+docno +'date'+date+'headline'+headline+'>'

    def create_meta_data(self,meta_data_string):
        #Extracting internal_id from saved string
        internal_id_start = '<internal_id'
        internal_id_end = 'docno'
        self.internal_id = re.search('%s(.*)%s' % (internal_id_start, internal_id_end), meta_data_string).group(1)
        #Extracting docno from saved string
        docno_start = 'docno'
        docno_end = 'date'
        self.docno = re.search('%s(.*)%s' % (docno_start, docno_end), meta_data_string).group(1)
        #Extracting date from saved string
        date_start = 'date'
        date_end = 'headline'
        self.date = re.search('%s(.*)%s' % (date_start, date_end), meta_data_string).group(1)
        #Extracting headline from saved string
        headline_start = "headline"
        headline_end = ">"
        self.headline = re.search('%s(.*)%s' % (headline_start, headline_end), meta_data_string).group(1)
        return self

def convert_docno_to_date(docno):
    # This method convers a docno to its relevant date
    month = docno[2:4]
    day = docno[4:6]
    year = docno[6:9]

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
        headline_start = '<P>'
        headline_end = '</P>'
        headline = re.search('%s(.*)%s' % (headline_start, headline_end), headline).group(1)

        headline = re.sub('[</P>]', '', headline)
        headline = re.sub('[<P>]', '', headline)
    except:
        headline = ""

    return headline

def save_doc(current_doc):
    # This method is used to save the current document
    print('entered save_doc method')

def save_docno_to_internal_id(doc_no_to_internal_id):
    # This method is used to save the docno to internal id mapping
    print('entered save_docno_to_internal_id method')

def save_internal_id_to_metadata(internal_id_to_meta_data):
    # This method is used to sasve the internal id to metadata mapping
    print('entered save_internal_if_to_metadata')

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
        # Used to keep track of whether the line being read is part of the headline
        is_headline = False
        headline = ""
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
                docno = docno[0:len(docno)-8]
                docno = docno.strip(" ")
                # Saving docno and date to metadata
                current_doc_meta_data.docno = docno
                current_doc_meta_data.date = convert_docno_to_date(docno)

            if line[0:10]=="<HEADLINE>" or is_headline == True :
                is_headline = True
                healine = headline + line

            if line[0:11]=="</HEADLINE>":
                healine = headline + line
                is_headline = False
                current_doc_meta_data.headline = extract_headline(headline)
                headline = ""

            current_doc = current_doc + line

            if line[0:5]=='</DOC>':
                doc_counter +=1
                docno_to_internal_id.update({current_doc_meta_data.docno:current_doc_meta_data.internal_id})
                internal_id_to_metadata.update({current_doc_meta_data.internal_id:current_doc_meta_data})
                save_doc(current_doc)
                current_doc = ""


        save_docno_to_internal_id(doc_no_to_internal_id)
        save_internal_id_to_metadata(internal_id_to_meta_data)

    print(doc_counter)


read_gzip_file('/Users/ayser/Dropbox/Waterloo/3A/Courses/Course_Projects/msci_541/Assignments/Data/latimes.gz')


"""
First generate internal_id
Next extract and store all meta Data from doc
Map internal data to docno
Next save doc as file
do while all files exist
save metadata file separately
"""
