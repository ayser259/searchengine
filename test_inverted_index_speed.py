import gzip, re, sys, os,json, time, ast
from objects import *
import lexicon_engine as lexicon_engine

print("Start Saving Run")


print("Starting Serialization Read")

a = time.time()
# Reading arguments presented from input
input_list = sys.argv
read_directory_path = input_list[1]

print("Starting to read")
# Loading the inverted index
b= time.time()
inverted_index = lexicon_engine.read_inverted_index(read_directory_path)
t = time.time()
total = t-b
print("inverted_index loaded in "+str(total)+" seconds")


# Loading tokens_to_id dictionary
b= time.time()
tokens_to_id = lexicon_engine.read_tokens_to_id(read_directory_path)
t = time.time()
total = t-b
print("tokens_to_id loaded in"+str(total)+ 'Seconds')
t =time.time()
total = t-a

print("Serialzation Test Completed in "+str(total)+" seconds")








"""
Try methods:



If you want to save a dictionary to a json file


method #2

dict = {'Python' : '.py', 'C++' : '.cpp', 'Java' : '.java'}
f = open("dict.txt","w")
f.write( str(dict) )
f.close()
save dictionary to a pickle file (.pkl)

The pickle module may be used to save dictionaries (or other objects) to a file. The module can serialize and deserialize Python objects.
# Method #3
import pickle
dict = {'Python' : '.py', 'C++' : '.cpp', 'Java' : '.java'}
f = open("file.pkl","wb")
pickle.dump(dict,f)
f.close()
"""
