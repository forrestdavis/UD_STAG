data = open("./ud-treebanks-conll2017/UD_English/en-ud-train.conllu", "r")

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

num = 20

print texts[num]
for token in sentences[num]:
    print token

data.close()
