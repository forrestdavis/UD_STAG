data = open("./ud-treebanks-conll2017/UD_English/en-ud-train.conllu", "r")

sentences = []

sentence = []

for line in data:
    line = line.strip("\n")
    if line and line[0] != "#":
        tokens = line.split()
        if tokens[0] == "1" and sentence:
            sentences.append(sentence)
            sentence = []
        else:
            sentence.append(tokens)

print sentences[0]
