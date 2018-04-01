from objects import *
import sys,os, re
import lexicon_engine as lexicon_engine

def top_3_lines(directory,current_file_meta_data,query_list):
    current_file_path = str(directory) + "/" + str(current_file_meta_data.date)+"/"+str(current_file_meta_data.internal_id)+".txt"
    # Printing out requested data
    current_file = open(current_file_path)
    line_to_score ={}
    is_token_tag = False
    current_doc = ""
    current_doc_string = ""
    for line in current_file:
        token_string = ""
# The following code is used to extract the part of the document that should be within the tokens
        if (line[0:6] =='<TEXT>') or (line[0:10] =='<HEADLINE>') or (line[0:0] =='<GRAPHIC>'):
            is_token_tag = True
        elif line[0:7] =='</TEXT>' or line[0:11] =='</HEADLINE>' or (line[0:10] =='</GRAPHIC>'):
            is_token_tag = False
        if is_token_tag == True:
            token_string = lexicon_engine.token_string_maker(line,token_string)
        # Storing all the relevant lines for a document within a variable
        current_doc = current_doc + token_string
        current_doc_string = current_doc_string + token_string
        # Saving singular document after encountering the end document tag
        if line[0:6]=='</DOC>':
            current_doc = re.split('(?<=[.!?]) +',current_doc)

    for line in current_doc:
        line_list = list(line.split())
        score = 0
        for item in query_list:
            if item in line_list:
                score = score+ 1
        line_to_score[line] = score

    sorted_line_to_score = sorted(line_to_score,key=line_to_score.get,reverse=True)
    sorted_line_to_score = list(sorted_line_to_score[:3])
    return_string = ""
    for item in sorted_line_to_score:
        return_string = return_string.strip()+item

    if len(return_string)<10:
        return_string= current_doc_string[0:300].strip()+"..."
    return return_string

def first_x_characters(directory,current_file_meta_data,chars):
    # Returns first x characters
    current_file_path = str(directory) + "/" + str(current_file_meta_data.date)+"/"+str(current_file_meta_data.internal_id)+".txt"
    # Printing out requested data
    current_file = open(current_file_path)
    line_to_score ={}
    is_token_tag = False
    current_doc = ""
    current_doc_string = ""
    for line in current_file:
        token_string = ""
# The following code is used to extract the part of the document that should be within the tokens
        if (line[0:6] =='<TEXT>') or (line[0:10] =='<HEADLINE>') or (line[0:0] =='<GRAPHIC>'):
            is_token_tag = True
        elif line[0:7] =='</TEXT>' or line[0:11] =='</HEADLINE>' or (line[0:10] =='</GRAPHIC>'):
            is_token_tag = False
        if is_token_tag == True:
            token_string = lexicon_engine.token_string_maker(line,token_string)
        # Storing all the relevant lines for a document within a variable
        current_doc = current_doc + token_string
        current_doc_string = current_doc_string +token_string
        # Saving singular document after encountering the end document tag
        if line[0:6]=='</DOC>':
            current_file = re.split('(?<=[.!?]) +',current_doc)

    return_string= str(current_doc_string[0:chars]).strip()+"..."
    return return_string
