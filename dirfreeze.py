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


# choose root folder (default is the folder the script is being run in)
if len(sys.argv) == 3:
    folder = sys.argv[1]
    req = sys.argv[2]
elif len(sys.argv) == 2:
    if sys.argv[1] == "-H" or sys.argv[1] == "--help":
        print("usage: python3 dirfreeze.py Optional[root_dir_path] Optional[requirements_file_path]\n"
              "dirfreeze takes an existing requirements.txt file and clears up any unnecessary libraries from there depending on imports found in all python files inside the specified root dir (the directory where it's being run from by default)")
        quit()
    folder = sys.argv[1]
    req = folder
else:
    folder = os.getcwd()
    req = folder

# clean up requirements file
imports = dirSearch(folder)

if os.path.exists(f"{req}/requirements.txt"):
    with open(f"{req}/requirements.txt") as f:
        libs = f.readlines()
else:
    print("no requirements file found\nplease make sure it's inside the folder dirfreeze is being run on OR specify its path as the second argument")
    print("usage: python3 dirfreeze.py Optional[root_dir_path] Optional[requirements_file_path]")
    quit()
towrite = []
for i, lib in enumerate(libs):
    li = lib.split("==")[0]
    for imp in imports:
        if li.lower() == imp.lower():
            towrite.append(lib)

towrite = set(towrite)
towrite = list(towrite)
with open(f"{req}/requirements.txt", 'w') as f:
    f.writelines(towrite)