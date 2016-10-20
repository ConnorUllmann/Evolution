import os

with open("docs.txt", "w") as output:
    filenames = os.listdir(os.getcwd())
    for filename in filenames:
        isPythonFile = filename.find(".py") != -1 and filename.find(".pyc") == -1 and filename != "class_scanner.py"
        if isPythonFile:
            with open(filename) as input:
                wrote = False
                for line in input:
                    isClassDefinition = line.find("class") != -1
                    isFunctionDefinition = line.find("def") != -1
                    if isClassDefinition or isFunctionDefinition:
                        output.write(line)
                        wrote = True
                if wrote:
                    output.write("\n")
                
                
