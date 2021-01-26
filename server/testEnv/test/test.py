import requests
import os
import json
import subprocess
from run import execute
import shutil


# BASE = "http://127.0.0.1:5000/"
response = requests.post(BASE, {"src":"print(\"Hello World\")","stdin":"","lang":"python3","timeout":5})
# print(response.json())


codes = {200:'success',404:'file not found',400:'error',408:'timeout'}


extensions = {
    "cpp":"cpp",
    "c": "c",
    "java":"java",
    "python3":"py",
    "javascript":"js",
    "haskell":"hs"
}

def test():
    # path = os.path.join("../temp", "folder")
    # os.mkdir(path)
    # filepath = os.path.join(path, "input.txt")
    #         #i = open(path +"/input.txt", "w+")
    # i = open(filepath, "w+")
    # i.write('input')
    # outputFile = os.path.join("temp", 'folder', "output.txt")
    # f = open(outputFile, "w+")
    # f.close()
    # command = 'run.py ../temp/' + 'folder' +'/source.' + 'py' + ' ' + 'python3' + ' '  + '5'
    path = os.path.join("../temp", 'folder')
    f = open(path +'/source.'+ extensions['python3'], "w")
    f.write('print(\"hello world\")')
    f.close()
    cm = os.path.join("../temp", 'folder', "source.py")
    file = os.path.join("../temp", 'folder', "source."+ extensions['python3'])
    res = execute(file, 'python3', 5)
    result = {
                    'output':res[0],
                    'code':res[1],
                    'status':codes[res[1]],
                    'submission_id':'jkfnrdj99'
                }
    result = json.dumps(result)
    print (result)
    #shutil.rmtree(os.path.join("../temp", "folder"))


    #os.system("python3 " + cm)

test()



 