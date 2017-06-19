import trees as t

def Trees(sentences):
    sentence = sentences[0]

    root_loc = 0
    verb_locs = []
    num = 1

    #key: value == tree number: tree
    trees = {}

    #key: value == index: POS, HEAD INDEX, DEP LABEL
    sent_hash = {}

    #First pass to create hash map of sentence
    #as well as locate root child and verb locations
    for node in sentence:
        sent_hash[node[0]] = (node[3], node[6], node[7])
        if node[3] == "VERB":
            verb_locs.append(node[0])
        if node[7] == "root":
            root_loc = node[0]

    #Second pass to create trees
    verb_child = []
    for node in sentence:
        index = node[0]
        head = node[6]
        pos = node[3]
        dep = node[7]

        if head in verb_locs: #and pos != "AUX":
            print node

        elif pos != "PUNCT":
            if head != "0":
                head_node = sent_hash[head]
                print head_node
                black_node = 


if __name__ == '__main__':

    #data_file = "./ud-treebanks-conll2017/UD_English/en-ud-train.conllu"
    data_file = "./simple_example.conllu"
    texts, sentences = t.extractSentences(data_file)
    Trees(sentences)
