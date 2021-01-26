import os, filecmp ,sys, subprocess

codes = {200:'success',404:'file not found',400:'error',408:'timeout'}

def compile(file,lang):

    if((lang =='python3') or (lang =='javascript')):
        return 200
    

    if (os.path.isfile(file)):
        if lang=='c':
            os.system('gcc ' + file)
        elif lang=='cpp':
            os.system('g++ ' + file)
        elif lang=='java':
            os.system('javac ' + file)
        elif lang=='haskell':
            os.system('ghc -o main ' + file )
        if (os.path.isfile('a.out')) or (os.path.isfile('main.class') or (os.path.isfile('main'))):
            return 200
        else:
            return 400
    else:
        return 404

def run(file,timeOut,lang):
    #cmd='sudo -u task_queue '
    cmd=''
    cm = os.path.join("temp", 'folder', "source.py")
    if lang == 'java':
        cmd += 'java main'
    elif lang=='c' or lang=='cpp':
        cmd += './a.out'
    elif lang=='python3':
        cmd += 'python3 '+ file
    elif lang=='javascript':
        cmd += 'node '+ file
    elif lang=='haskell':
        cmd += './main'

    try : 
        process = subprocess.run(['python3', file],
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         timeout = timeOut,
                         universal_newlines=True)
        print ("stdout : " , process.stdout)
        print ("stderr : " , process.stderr)
        if (process.stderr == ''):
            return process.stdout, 200
        else :
            return process.stderr, 400
    except subprocess.TimeoutExpired as err :
        print("TimeoutExpired error: {0}".format(err))
        return err, 408
    os.system("python3 " + cm)

    r = os.system('timeout '+timeOut+' '+cmd+' < '+input + ' > '+testout)

    if r==0:
        return 200
    #TIMEOUT
    elif r==31744:
        return 408
    else:
        return 400

def match(output):
    if os.path.isfile('out.txt') and os.path.isfile(output):
        b = filecmp.cmp('out.txt',output)
        os.remove('out.txt')
        return b
    else:
        return 404

def execute(file, lang, timeout):
    timeout = min(15,int(timeout))
    status=compile(file,lang)
    if status == 200:
        status=run(file,timeout,lang)
        return status
    return status



