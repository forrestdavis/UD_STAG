def extractSentences(data_file):

    data = open(data_file, "r")
    sentences = []

    sentence = []
    texts = [] 

    end = 0

    for line in data:
        line = line.strip("\n")
        if not line:
            end = 1
        if line and line[0] != "#":
            line = line.split()
            sentence.append(line)
        if end:
            end = 0
            sentences.append(sentence)
            sentence = []
        elif line and line[0] == "#" and "text" in line:
            texts.append(line[9:])

    data.close()
    return texts, sentences


def buildUp(sentence, text):

    print text, "\n"

    for node_number in xrange(len(sentence)):
        node = sentence[node_number]
        print node
        while node[6] != "0":
            parent_index = int(node[6])
            node = sentence[parent_index-1]
            print node

        print "------------------------------------------------------\n"

def buildDown(sentence, text, verbose=True):
    
    if verbose:
        print text, "\n"

    children = {}
    for node in sentence:
        parent_index = node[6]
        child_index = node[0]
        if parent_index == "_":
            print text
            print node
        elif parent_index in children:
            l = children[parent_index]
            l.append(child_index)
            children[parent_index] = l
        else:
            children[parent_index] = [child_index]

    if verbose:
        for key in children:
            if key == "0":
                print "\tROOT"
                for child_index in children[key]:
                    print sentence[int(child_index)-1]
                print "--------------------------------------------------\n"
            else:
                print "\t",sentence[int(key)-1]
                for child_index in children[key]:
                    print sentence[int(child_index)-1]
                print "--------------------------------------------------\n"
    return children

def makeTrees(sentences):

    trees = []
    counts = {}

    num = 0
    for sentence in sentences:
        children_dict = buildDown(sentence, '', False)
        num +=1

        #Key sorting work around
        for key in children_dict:
            tmp = []
            notAdded = 1
            for child in children_dict[key]:
                if int(key) < int(child) and notAdded:
                    tmp.append(key)
                    notAdded = 0
                tmp.append(child)

        #Create proto-trees with POS
        for key in children_dict:
            tree = []
            if key == "0":
                tree.append("ROOT")
            else:
                tree.append(sentence[int(key)-1][3])

            for child_index in children_dict[key]:
                tree.append(sentence[int(child_index)-1][3])
            if tree not in trees:
                trees.append(tree)
            if tuple(tree) not in counts:
                counts[tuple(tree)] = 1
            elif tuple(tree) in counts:
                counts[tuple(tree)] = counts[tuple(tree)]+1

    return trees, counts
            
def checkProjective(texts, sentences):

    location = 0

    return texts

if __name__ == '__main__':

    data_file = "./ud-treebanks-conll2017/UD_English/en-ud-train.conllu"
    texts, sentences = extractSentences(data_file)


    num = 1027
    text = texts[num]
    sentence = sentences[num]
    #buildUp(sentence, text)
    #buildDown(sentence, text)

    trees, counts = makeTrees(sentences)

    print "Number of sentences: ", len(sentences)
    print "Number of trees: ", len(trees)

    threshold = 1
    freq_tags = []
    for key in counts:
        if counts[key] > threshold:
            freq_tags.append(key)
    print "Number of trees with occcurence greater than ", threshold, " : ", len(freq_tags)

    print "Number of trees with occurence less than ", threshold, " : ", len(trees) - len(freq_tags)
