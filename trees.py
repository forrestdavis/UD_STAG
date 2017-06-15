
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


def buildUp(text, sentence, num):

    print text, "\n"

    for node_number in xrange(len(sentence)):
        node = sentence[node_number]
        print node
        while node[6] != "0":
            parent_index = int(node[6])
            node = sentence[parent_index-1]
            print node

        print "------------------------------------------------------\n"

def buildDown(text, sentence, num):
    
    print text, "\n"
    children = {}
    for node in sentence:
        parent_index = node[6]
        child_index = node[0]
        if parent_index in children:
            l = children[parent_index]
            l.append(child_index)
            children[parent_index] = l
        else:
            children[parent_index] = [child_index]

    for key in children:
        if key == "0":
            print "\troot"
            for child_index in children[key]:
                print sentence[int(child_index)-1]
            print "--------------------------------------------------\n"
        else:
            print "\t",sentence[int(key)-1]
            for child_index in children[key]:
                print sentence[int(child_index)-1]
            print "--------------------------------------------------\n"


if __name__ == '__main__':

    data_file = "./ud-treebanks-conll2017/UD_English/en-ud-train.conllu"
    texts, sentences = extractSentences(data_file)

    num = 20
    text = texts[num]
    sentence = sentences[num]
    buildUp(text, sentence, num)
    buildDown(text, sentence, num)

