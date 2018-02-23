# This method holds all the helper methods for assignment 2, pertaining to in-memory inverstion
import os,json,ast
def token_string_maker(line,token_string):
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
        if tokens_to_id.__contains__(token):
            token_ids.append(tokens_to_id[token])
        else:
            token_id = len(list(tokens_to_id.keys()))
            token_ids.append(token_id)
            tokens_to_id[token] = token_id
    return token_ids

def count_words(token_ids):
    # This method returns a dictionary of {term_id:count}
    word_counts = {}
    for token_id in token_ids:
        if word_counts.__contains__(token_id):
            word_counts[token_id] = word_counts[token_id] +1
        else:
            word_counts[token_id] =1
    return word_counts

def add_to_postings(word_count,doc_id,inverted_index):
    # This method returns the inverted_index
    for term_id in word_count:
        count = word_count[term_id]
        if inverted_index.__contains__(term_id):
            postings = inverted_index[term_id]
        else:
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
    file_path = os.path.join(save_directory_path, "inverted_index" + ".txt")
    current_file = open(file_path, "w")
    for item in inverted_index:
        current_file.write("<")
        current_file.write(str(item))
        current_file.write("$")
        current_file.write(str(inverted_index[item]))
        current_file.write(">")
    current_file.close()

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
    read_directory_path = read_directory_path+"/"+"inverted_index.txt"
    current_file  = open(read_directory_path, "r")
    dict_string = ""
    current_dict = {}
    for line in current_file:
        dict_string = dict_string +line
    print("A")
    i =0
    substring1 = '<'
    substring2 = '$'
    substring3 = '>'

    substringa = "{"
    substringb = ":"
    substringc = "}"
    while len(dict_string)>1:
        alpha = dict_string.index(substring1) +1
        beta = dict_string.index(substring2, alpha)
        gamma = dict_string.index(substring3, beta)
        key = dict_string[alpha:beta]
        value = dict_string[beta:gamma]
        j = 0
        postings_list =[]
        while len(value)>1:
            first = value.index(substringa) +1
            second = value.index(substringb, first)
            third = value.index(substringc,second)
            post_key = value[first:second]
            post_value = value[(second+1):third]
            key_value = {}
            key_value[int(post_key)] = int(post_value)
            postings_list.append(key_value)
            try:
                j = value.index(",") +1
            except:
                j = value.index("]") +1
            value = value[j:]
            j = 0
        i =dict_string.index(">")+1
        dict_string = dict_string[i:]
        i = 0
        current_dict[key] = postings_list
    return current_dict
# Assignment_2_end_d
