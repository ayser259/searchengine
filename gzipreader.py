import sys, os, gzip
"""
    Methods to be created:
    - Convering Document number to Date
    - Saving Meta Data
"""
class metadata:
    #This class stores the metadata for a given file
    # Default values are all set to -1 indicating that data is to be filled
    internal_id = -1
    docno = -1
    date = -1
    headline = -1

def readgzip(gzfile):
    #This method reads through the gzip file, and searches for doc tags
    counter = 0
    print("readgzip method started")
    f=gzip.open(gzfile,'rb')
    file_content=f.read()
    print(file_content)
    """
    with gzip.open(gzfile,'rt') as f:
        print(f)
        for line in f:
            print('got line', line)
            #This is to prevent reading the entire file, which would be too large
            if (counter ==100):
                print("D")
                break
            counter+= 1
    """
    print("readgzip Method Finished")


def convert_date(docno):
    # This method convers a docno to its relevant date
    print('hello')

# Program Starts Here
try:
    # Retrieving arguments from command line
    directory_list = sys.argv
    gzip_file_path = directory_list[1]
    save_directory_path = directory_list[2]
    print(gzip_file_path)
    print(save_directory_path)

    #Checking to see if the destination directory exits, creating it if it doesn't
    if (os.path.exists(save_directory_path))==False:
        os.makedirs(save_directory_path)
        print('directory created')
    else:
        print("Error: Direcotry Already Exists")



except:
    print("No Arguements Provided. Provide Path To File And Saving Directory")

#Reading from gzip'd file:
readgzip(gzip_file)
