# This method holds all the helper methods for assignment 2, pertaining to in-memory inverstion
import os,json,ast,re

def json_save(save_dict,filename):
    file_n = json.dumps(save_dict)
    f = open(filename,"w")
    f.write(file_n)
    f.close()

def json_read(filepath):
    return_dict = {}
    data = json.load(open(filepath))
    return return_dict

def token_string_maker(line,token_string):
    # This method "cleans" the token string and removes html tags
    if line[0:3]!='<P>' and line[0:4] !='</P>' and (line[0:6] !='<TEXT>') and (line[0:10] !='<HEADLINE>') and (line[0:0] !='<GRAPHIC>'):
        token_string = token_string + line
    return token_string

def tokenize(doc_string):
    # This method tokenizes the document string and returns a list of all the tokens
    tokens = []
    start = 0
    index = -1
    doc_string= doc_string.lower()
    while index < len(doc_string):
        index = index+1
        current_term = doc_string[index:index+1]
        if (current_term.isalnum() == False):
            if (start!= index):
                token = doc_string[start:index]
                tokens.append(token)
            start = index + 1
    if(start!=index):
        tokens.append(doc_string[start:index])
    return tokens

def convert_tokens_to_ids(tokens,tokens_to_id):
    # This method returns a list of token_ids
    token_ids = []
    for token in tokens:
        try:
            token_ids.append(tokens_to_id[token])
        except:
            token_id = len(list(tokens_to_id.keys()))
            token_ids.append(token_id)
            tokens_to_id[token] = token_id
    return token_ids

def count_words(token_ids):
    # This method returns a dictionary of {term_id:count}
    word_counts = {}
    for token_id in token_ids:
        try:
            dict_item = {token_id:word_counts[token_id] +1}
            word_counts.update(dict_item)
        except:
            dict_item = {token_id:1}
            word_counts.update(dict_item)
    return word_counts

def add_to_postings(word_count,doc_id,inverted_index):
    # This method returns the inverted_index
    for term_id in word_count:
        count = word_count[term_id]
        try:
            postings = inverted_index[term_id]
        except:
            postings = []
        posting = {doc_id:count}
        postings.append(posting)
        inverted_index[term_id] = postings

def convert_ids_to_tokens(tokens_to_id):
    # This method returns a dictionary of token ids to the token
    id_to_tokens ={}
    tokens = tokens_to_id.keys()
    for token in tokens:
        id_to_tokens[tokens_to_id[token]] = token
    return id_to_tokens

def save_tokens_to_id(tokens_to_id,save_directory_path):
    # This method read the tokens to id dictionary to file
    if (os.path.exists(save_directory_path)) == False:
        os.makedirs(save_directory_path)
    file_path = os.path.join(save_directory_path, "tokens_to_id" + ".txt")
    current_file = open(file_path, "w")
    current_file.write(str(tokens_to_id))
    current_file.close()

def save_id_to_tokens(id_to_tokens,save_directory_path):
    # This method writes the id to tokens dictionary to file
    if (os.path.exists(save_directory_path)) == False:
        os.makedirs(save_directory_path)
    file_path = os.path.join(save_directory_path, "id_to_tokens" + ".txt")
    current_file = open(file_path, "w")
    current_file.write(str(id_to_tokens))
    current_file.close()

def save_inverted_index(inverted_index,save_directory_path):
    # This method saves the inverted index to file
    if (os.path.exists(save_directory_path)) == False:
        os.makedirs(save_directory_path)
    save_directory_path = save_directory_path+"/"+"inverted_index.json"
    json_save(inverted_index,save_directory_path)

def read_tokens_to_id(read_directory_path):
    # This method reads the tokens to id dictionary from file
    read_directory_path = read_directory_path+"/"+"tokens_to_id.txt"
    current_file  = open(read_directory_path, "r")
    dict_string = ""
    for line in current_file:
        dict_string = dict_string +line
    json_as_string = dict_string.replace("'", "\"")
    current_dict = {}
    current_dict = json.loads(json_as_string)
    return current_dict

def read_id_to_tokens(read_directory_path):
    # This method reads the id to tokens dictionary from file
    read_directory_path = read_directory_path+"/"+"id_to_tokens.txt"
    current_file  = open(read_directory_path, "r")
    dict_string = ""
    for line in current_file:
        dict_string = dict_string +line
    current_dict = ast.literal_eval(dict_string)
    return current_dict

def read_inverted_index(read_directory_path):
    # This method reads the inverted index from file
    read_directory_path = read_directory_path+"/"+"inverted_index.json"
    data = json.load(open(read_directory_path))
    int_key_data = {}
    for key in data:
        int_key = int(re.sub("[^0-9]", "", key))
        int_key_data[int_key] = data[key]

    return int_key_data
