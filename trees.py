##############################################################
##############################################################
#Code for extracting elementary trees from the universal 
#dependency data set.
#
#Forrest Davis
#June 30, 2017
##############################################################
##############################################################
import collections, os

#Returns dictionary, key: value = dependency: 0/1
#if 0, dep represents a substitution node
#if 1, dep represents an adjunction node
def Deps(dep_file):
    deps_info = open(dep_file, 'r')
    deps = {}

    for line in deps_info:
        line = line.strip()
        if "#" not in line:
            line = line.split(' ')
            
            if len(line) == 2:
                deps[line[0]] = line[1]
            else:
                print "error with following dep: "
                print line
    
    deps_info.close()
    return deps

#Function for scraping sentence for trees and writing to file
def extract(num, trees, sentence_hash, arguments, deps, output, out):

    for word in output:

        dep = word[7]
        #Skip enhanced nodes
        if dep == "_":
            continue
        #Currently marking all punctuation with black node
        if dep == "punct":
            tree = word[3]+'\t'+'b\n'
            if tree in trees:
                tree_num = trees[tree][0]
                trees[tree][1] += 1
            else:
                tree_num = 'd'+str(num[0])
                trees[tree] = [tree_num, 1]
                num[0]+=1
            word.append(tree_num)
            out.write('\t'.join(word)+'\n')
        #Word is argument of verb, thus is only black node
        elif(word[6] in arguments and deps[dep]=='0'): #and word[3]!="VERB"):
            tree = word[3]+'\t'+ 'b\n'
            if tree in trees:
                tree_num = trees[tree][0]
                trees[tree][1] += 1
            else:
                tree_num = 'd'+str(num[0])
                trees[tree] = [tree_num, 1]
                num[0]+=1
            word.append(tree_num)
            out.write('\t'.join(word)+'\n')
        #Word is a verb or root
        elif word[0] in arguments:
            '''
            #Handle parataxis NEED TO CHECK
            if word[7] == 'root' and word[3] == "NOUN":
                if len(arguments[word[0]]) > 2:
                    print '---------------------------'
                    print arguments
                    for w in output:
                        print w
            else:
            '''
            crossed_Verb = 0
            tree = ''
            for arg in arguments[word[0]]:
                if int(arg) > int(word[0]) and not crossed_Verb:
                    tree+= '\t'+word[3]+'\t'+'b\n'
                    tree+= '  '+sentence_hash[arg][2]+'\n'
                    tree+= sentence_hash[arg][0]+'\tw\n'
                    crossed_Verb = 1
                elif crossed_Verb:
                    tree+= '  '+sentence_hash[arg][2]+'\n'
                    tree+= sentence_hash[arg][0]+'\tw\n'
                else: 
                    tree+= sentence_hash[arg][0]+'\tw\n' 
                    tree+= '  '+sentence_hash[arg][2]+'\n'
            if not crossed_Verb:
                tree+= '\t'+word[3]+'\t'+'b\n'
            if tree in trees:
                tree_num = trees[tree][0]
                trees[tree][1] += 1
            else:
                tree_num = 'd'+str(num[0])
                trees[tree] = [tree_num, 1]
                num[0]+=1
            word.append(tree_num)
            out.write('\t'.join(word)+'\n')

        #Word is a adjunct
        elif deps[dep] == '1':
            if dep == 'root':
                tree = word[3]+'\t'+'b\n'
                if tree in trees:
                    tree_num = trees[tree][0]
                    trees[tree][1] += 1
                else:
                    tree_num = 'd'+str(num[0])
                    trees[tree] = [tree_num, 1]
                    num[0]+=1
                word.append(tree_num)
                out.write('\t'.join(word)+'\n')

            else:
                head = sentence_hash[word[0]][1]
                index = word[0]
                if int(head) < int(index):
                    tree = sentence_hash[head][0]+'\t'+'w\n'
                    tree += '  '+dep+'\n'
                    tree += '\t'+word[3]+'\t'+'b\n'
                    if tree in trees:
                        tree_num = trees[tree][0]
                        trees[tree][1] += 1
                    else:
                        tree_num = 'd'+str(num[0])
                        trees[tree] = [tree_num, 1]
                        num[0]+=1
                    word.append(tree_num)
                    out.write('\t'.join(word)+'\n')
                else:
                    tree = '\t'+sentence_hash[head][0]+'\t'+'w\n'
                    tree += '  '+dep+'\n'
                    tree += word[3]+'\t'+'b\n'
                    if tree in trees:
                        tree_num = trees[tree][0]
                        trees[tree][1] += 1

                    else:
                        tree_num = 'd'+str(num[0])
                        trees[tree] = [tree_num, 1]
                        num[0]+=1
                    word.append(tree_num)
                    out.write('\t'.join(word)+'\n')
                
        else:
            print "-----------------------------------"
            print "ERROR:"
            for w in output:
                if w == word:
                    print '\t', w
                else:
                    print w

    out.write('\n')

def Trees(data_file, dep_file, output_file, trees=None):
    #List to be mutable
    if not trees:
        num = [1]
    #If using set of trees start count from last tree
    else:
        num = [len(trees)+1]
    deps = Deps(dep_file)
    data = open(data_file, 'r')
    out = open(output_file, 'w')

    #Dictionary for trees, key: value = tree: [tree number, count]
    if not trees:
        trees = collections.OrderedDict()
    #key: value == index: POS, HEAD INDEX, DEP LABEL
    sentence_hash = {}
    #For writing to file
    output = []
    #Dictionary marking arguments, key: value = head: arg1, arg2, etc
    arguments = {}

    for line in data:
        line = line.strip()
        if not line:

            #Extract trees
            extract(num, trees, sentence_hash, arguments, 
                    deps, output, out)

            #Reset variables for next sentence
            sentence_hash = {}
            output = [] 
            arguments = {}

        #Create hash map with words in sentence and 
        #add arguments to seperate hash map
        elif line and line[0] != "#":
            line = line.split('\t')
            output.append(line)
            if line[6] != "_":
                sentence_hash[line[0]] = (line[3], line[6], line[7])

                if line[7]!='root' and line[7]!='punct' and deps[line[7]]=='0':
                    if line[6] not in arguments:
                        arguments[line[6]] = [line[0]]
                    else:
                        arguments[line[6]].append(line[0])

    data.close()
    out.close()
    return trees

def create_All_UD(root_file, dep_file):

    names = []
    for root, dirs, files in os.walk(root_file):
        for name in dirs:
            names.append(name)

    for name in names:
        print name
        if len(name.split('_')) != 2:
            temp = name.split('_')
            out = ''
            for x in xrange(1, len(temp)):
                out += temp[x]+"_"
            out = out[:len(out)-1]
            directory = "./output/"+out
            grammar = "./grammars/"+out
        else:
            directory = "./output/"+name.split('_')[1]
            grammar = "./grammars/"+name.split('_')[1]
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(grammar):
            os.makedirs(grammar)

        info = open(directory+"/info.txt", "w")
        for root, dirs, files in os.walk(os.path.join(root_file, name)):
            for f in files:
                if "train.conllu" in f:
                    train_file = os.path.join(root, f)
                    train_output_file = directory+"/"
                    train_output_file += f.split(".")[0]+".conll16"
                if "dev.conllu" in f:
                    dev_file = os.path.join(root, f)
                    dev_output_file = directory+"/"
                    dev_output_file += f.split(".")[0]+".conll16"

        trees = Trees(train_file, dep_file, train_output_file)
        print len(trees)
        info.write("Number of trees in train: ")
        info.write(str(len(trees))+'\n')

        trees = Trees(dev_file, dep_file, dev_output_file, trees)
        print len(trees)
        info.write("Number of trees in dev and train: ")
        info.write(str(len(trees))+'\n')

        info.close()
        g = open(grammar+"/trees.txt", 'w')
        for tree in trees:
            g.write(trees[tree][0]+":\n")
            g.write(tree)

        g.close()

if __name__ == '__main__':

    #dep_file = "./deps.txt"
    #root_file = "./ud-treebanks-conll2017"
    #create_All_UD(root_file, dep_file)

