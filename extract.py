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
            sent_hash[node[0]] = (node[3], node[6], node[7])
            if node[3] == "VERB":
                verb_locs.append(node[0])
            if node[7] == "root":
                root_loc = node[0]

        #Second pass to create trees
        verb_child = {}
        placed_Verb = 0
        need_Verb = 0
        for node in sentence:
            index = node[0]
            head = node[6]
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
                    if head < index and not placed_Verb:
                        need_Verb = 1
                    if head not in verb_child:
                        if need_Verb:
                            verb_child[head] = [['VERB'],[pos, dep]]
                            placed_Verb = 1
                            need_Verb = 0
                        else:
                            verb_child[head] = [[pos, dep]]
                    else:
                        if need_Verb:
                            verb_child[head].append(['VERB'])
                            placed_Verb = 1
                            need_Verb = 0
                        verb_child[head].append([pos, dep])

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
                if head != "0":
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
        

        crossed_Verb = 0
        for verb_index in verb_child:
            tree = ''
            for child in verb_child[verb_index]:
                if child[0] != 'VERB':
                    if not crossed_Verb:
                        tree += child[0] + '<---'+child[1]+'----' 
                    else:
                        tree += '----' + child[1] + '--->' + child[0]
                else:
                    tree += "VERB"
                    crossed_Verb = 1
            if tree not in trees:
                trees[tree] = ["d"+str(num), 1]
                num += 1
            else:
                trees[tree][1] += 1

        '''
        output = []
        for tree in trees:
            if not output:
                output.append([trees[tree], tree])
            else:
                been_inserted = 0
                for x in range(len(output)):
                    if trees[tree][0] < output[x][0][0]:
                        output.insert(x, [trees[tree], tree])
                        been_inserted = 1
                        break
                if not been_inserted:
                    output.append([trees[tree], tree])
        '''

    for tree in trees:
        print trees[tree], tree


if __name__ == '__main__':

    #data_file = "./ud-treebanks-conll2017/UD_English/en-ud-train.conllu"
    data_file = "./simple_example.conllu"
    texts, sentences = s.extractSentences(data_file)
    Trees(sentences)
