import os, sys

def importSearch(lines):
    result = []
    for line in lines:
        lineParts = line.split(" ")
        if "import" in line:
            if lineParts[0] == "import":
                if lineParts[1].endswith(","):
                    for i, word in enumerate(lineParts):
                        if i == 0:
                            continue
                        if i != len(lineParts)-1:
                            result.append(word.replace(",",""))
                        else:
                            result.append(word.replace("\n",""))
                else:
                    result.append(lineParts[1].split("\n")[0])
            else:
                if line.startswith("#"):
                    continue
                else:
                    if '__import__("' in line:
                        lineimp = line.split('"')
                        for i, element in enumerate(lineimp):
                            if element == '__import__(':
                                result.append(lineimp[i+1])
                                break
                    elif "__import__('" in line:
                        lineimp = line.split("'")
                        for i, element in enumerate(lineimp):
                            if element == '__import__(':
                                result.append(lineimp[i+1])
                                break
                    else:
                        result.append(lineParts[1])

    return result

def dirSearch(folder, found=[]):
    contents = os.listdir(folder)
    for instance in contents:
        if os.path.isdir(f"{folder}/{instance}"):
            dirSearch(f"{folder}/{instance}", found)
        else:
            if instance.endswith(".py") and instance != os.path.basename(__file__):
                with open(f"{folder}/{instance}") as f:
                    found.append(importSearch(f.readlines()))

    imports = []
    for ii in found:
        for i in ii:
            imports.append(i)
    return imports



if len(sys.argv) == 2:
    folder = sys.argv[1]
else:
    folder = os.getcwd()


imports = dirSearch(folder)

with open(f"{folder}/requirements.txt") as f:
    libs = f.readlines()
towrite = []
for i, lib in enumerate(libs):
    li = lib.split("==")[0]
    for imp in imports:
        if li.lower() == imp.lower():
            towrite.append(lib)

towrite = set(towrite)
towrite = list(towrite)
with open(f"{folder}/requirements.txt", 'w') as f:
    f.writelines(towrite)