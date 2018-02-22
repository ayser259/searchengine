# This method holds all the helper methods for assignment 2, pertaining to in-memory inverstion

def token_string_maker(line,token_string):
    if line[0:3]!='<P>' and line[0:4] !='</P>' and (line[0:6] !='<TEXT>') and (line[0:10] !='<HEADLINE>') and (line[0:0] !='<GRAPHIC>'):
        token_string = token_string + line
    return token_string

def tokenize(doc_string):
    # This method tokenizes the document string and returns a list of all the tokens
    tokens = []
    start = 0
    index = -1
    while i < len(doc_string):
        i = i+1
        current_term = doc_string[index:index+1]
        if (current_term.isalnum() == False):
            if (start!= token_counter):
                token = doc_string[start:index]
                tokens.append(token)
            start = index + 1
    if(start!=index):
        tokens.append(doc_string[start:index])
    return tokens

def convert_tokens_to_ids(tokens,tokens_to_id):
    # This method returns a list of token_ids
    print('placeholder')
    a = []
    return a

def count_words(token_ids):
    # This method returns a dictionary of {term_id:count}
    print('placeholder')
    a = {}
    return a

def add_to_postings(word_count,doc_id,inverted_index):
    # This method returns the inverted_index
    print('placeholder')
    a = []
    return a

def convert_ids_to_tokens(tokens_to_id):
    # This method returns a dictionary of token ids to the token
    print('placeholder')
    a = []
    return a    
