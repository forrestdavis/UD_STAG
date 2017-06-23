import support as s

def Trees(sentences):
    num = 1

    #key: value == tree number: tree
    trees = {}

    for sentence in sentences:
        root_loc = 0
        verb_locs = []

        #key: value == index: POS, HEAD INDEX, DEP LABEL
        sent_hash = {}

        #First pass to create hash map of sentence
        #as well as locate root child and verb locations
        for node in sentence:
            #Skipping over enchanced nodes
            if node[6] == "_":
                continue
            sent_hash[int(node[0])] = (node[3], int(node[6]), node[7])
            if node[3] == "VERB":
                verb_locs.append(int(node[0]))
            if node[7] == "root":
                root_loc = int(node[0])

        #Second pass to create trees
        verb_child = {}
        for node in sentence:

            #Skipping over enchanced nodes
            if ".1" in node[0]:
                continue
            index = int(node[0])
            head = int(node[6])
            pos = node[3]
            dep = node[7]
            
            if head in verb_locs and pos != "AUX":# and pos != "PUNCT":
                tree = pos + "(black_node)"
                if tree not in trees:
                    trees[tree] = ["d"+str(num), 1]
                    num += 1
                else:
                    trees[tree][1] += 1

                if pos != "PUNCT":
                    if head not in verb_child:
                        verb_child[head] = [[index, pos, dep]]
                    else:
                        verb_child[head].append([index, pos, dep])

            elif head in verb_locs and pos == "AUX":
                black_node = pos
                head_node = sent_hash[head]
                white_node = head_node[0]
                if index < head:
                    tree = black_node + "(black_node)----"+dep+"--->"+white_node
                else:
                    tree = white_node + '<---'+dep+'----'+black_node+"(black_node)"

                if tree not in trees:
                    trees[tree] = ["d"+str(num), 1]
                    num += 1
                else:
                    trees[tree][1] += 1

            else:
                if head != 0:
                    black_node = pos
                    head_node = sent_hash[head]
                    white_node = head_node[0]
                    if index < head:
                        tree = black_node + "(black_node)----"+dep+"--->"+white_node
                    else:
                        tree = white_node + '<---'+dep+'----'+black_node+"(black_node)"
                    if tree not in trees:
                        trees[tree] = ["d"+str(num), 1]
                        num += 1
                    else:
                        trees[tree][1] += 1
        

        for verb_index in verb_child:
            crossed_Verb = 0
            tree = ''
            for child in verb_child[verb_index]:
                if child[0] > verb_index and not crossed_Verb:
                    tree += "VERB(black_node)"
                    crossed_Verb = 1
                    tree += '----' + child[2] + '--->' + child[1] + "   "
                elif crossed_Verb:
                    tree += '----' + child[2] + '--->' + child[1] + "   "
                else:
                    tree += "   " + child[1] + '<---' + child[2] + '----   '
            if tree not in trees:
                trees[tree] = ["d"+str(num), 1]
                num += 1
            else:
                trees[tree][1] += 1

    '''
    for tree in trees:
        print trees[tree], tree
    '''
    subset = []
    global_max = 0
    global_info = []
    num = 2
    for tree in trees:
        if trees[tree][1] > num:
            subset.append([trees[tree], tree])
            if trees[tree][1] > global_max:
                global_max = trees[tree][1]
                global_info = [trees[tree],tree]

    print "total: ", len(trees)
    print "trees with > ", num, " : ", len(subset)
    print "trees with <= ", num," : ", len(trees) - len(subset)
    print "tree with largest count: ", global_info


if __name__ == '__main__':

    data_file = "./ud-treebanks-conll2017/UD_English/en-ud-train.conllu"
    #data_file = "./reduced.conllu"
    texts, sentences = s.extractSentences(data_file)
    Trees(sentences)
