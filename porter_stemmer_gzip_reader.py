import gzip, re, sys, os,time
from porter_stemmer_index_engine import *
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
