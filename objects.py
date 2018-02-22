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
