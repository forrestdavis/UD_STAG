import collections, os, sys

#Returns dictionary, key: value = dependency: 0/1
#if 0, dep represents a substitution node
#if 1, dep represents an adjunction node
def Deps(dep_file):
    deps_info = open(dep_file, 'r')
    deps = {}

    for line in deps_info:
        line = line.strip()
        if "#" not in line and line:
            line = line.split(' ')
            
            if len(line) == 2:
                deps[line[0]] = line[1]
            else:
                print "error with following dep: "
                print line
    
    deps_info.close()
    return deps

#Function for scraping sentence for trees and writing to file
def srl_extract(num, trees, sentence_hash, arguments, deps, output, out):

    for word in output:

        dep = word[10]
        pos = word[4]

        #Currently marking all punctuation with black node
        if dep == "P":
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
        elif(word[8] in arguments and deps[dep]=='0'): #and word[3]!="VERB"):
            tree = pos +'\t'+ 'b\n'
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
            crossed_Verb = 0
            tree = ''
            for arg in arguments[word[0]]:
                if int(arg) > int(word[0]) and not crossed_Verb:
                    tree+= '\t'+pos+'\t'+'b\n'
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
                tree+= '\t'+pos+'\t'+'b\n'
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
            '''
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
            '''
            head = sentence_hash[word[0]][1]
            index = word[0]
            if int(head) < int(index):
                tree = sentence_hash[head][0]+'\t'+'w\n'
                tree += '  '+dep+'\n'
                tree += '\t'+pos+'\t'+'b\n'
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
                tree += pos+'\t'+'b\n'
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

#For conll09 SRL Task
def SRL_Trees(data_file, dep_file, output_file, trees=None):
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
            srl_extract(num, trees, sentence_hash, arguments, 
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
            #Currently using gold deprel 
            #change line[10] to line[11] for pred
            sentence_hash[line[0]] = (line[4], line[8], line[10])

            if deps[line[10]]=='0':
                if line[8] not in arguments:
                    arguments[line[8]] = [line[0]]
                else:
                    arguments[line[8]].append(line[0])

    data.close()
    out.close()
    return trees

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print "Usage: python srl_trees.py conll09 files"
        print "All files listed in command line will use", 
        print " the same elementary trees"
        print "output is filename.tag"
        sys.exit(1)

    dep_file = "srl_deps.txt"
    grammar_file = open("srl_grammar.txt", "w")
    trees = None

    for x in range(1, len(sys.argv)):
        data_file = sys.argv[x]
        output_file = sys.argv[x].split('.')[0]+".tag"
        trees = SRL_Trees(data_file, dep_file, output_file)

    
    for tree in trees:
        grammar_file.write(trees[tree][0]+":\n")
        grammar_file.write(tree)

    grammar_file.close()
