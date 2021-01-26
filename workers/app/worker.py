import pika
import redis
import sys
from flask import Flask
import time
import os
import subprocess
import json
from run import execute
from shutil import rmtree 



app = Flask(__name__)


QUEUE_NAME = 'task_queue'


codes = {200:'success',404:'file not found',400:'error',408:'timeout'}



print("worker launching")


extensions = {
    "cpp":"cpp",
    "c": "c",
    "java":"java",
    "python3":"py",
    "javascript":"js",
    "haskell":"hs"
}


""" def connect():
        print("trying to connect")
        try:
            connection = Connection.getInstance()
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)
            return channel
        except :
            print("error")

connect() """


class RedisClient:
   __instance = None
   @staticmethod 
   def getInstance():
      """ Static access method. """
      if RedisClient.__instance == None:
         RedisClient()
      return RedisClient.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if RedisClient.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         print ("creating a singleton")
         RedisClient.__instance = redis.Redis(host='redis', port=6379)



class Connection:
   __instance = None
   @staticmethod 
   def getInstance():
      """ Static access method. """
      if Connection.__instance == None:
         Connection()
      return Connection.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if Connection.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         print ("creating a singleton")
         Connection.__instance = pika.BlockingConnection(
                pika.ConnectionParameters(host='rabbit'))



def runCode(ch, body):
    # print(json.dumps(x))
    try:
        # outputFile = os.path.join("../temp", body['folder'], "output.txt")
        # RedisClient.getInstance().set(body['folder'], "created output")
        # f = open(outputFile, "w+")
        # f.close()
        file = os.path.join("../temp", body['folder'], "source."+extensions[body['lang']])
        # command = 'run.py ../temp/' + body['folder'] +'/source.' + extensions[body['lang']] + ' ' + body['lang'] + ' '  + body['timeOut']
        RedisClient.getInstance().set(body['folder'], "command ran")
        res = execute(file, body['lang'], body['timeout'])
        RedisClient.getInstance().set(body['folder'], res[0])
        # infile = open(outputFile, 'r', encoding='utf8')
        # data = infile.read()
        # infile.close()

        result = {
                    'output':res[0],
                    'code':res[1],
                    'status':codes[res[1]],
                    'submission_id':body['folder']
                }
        result = json.dumps(result)

        try : 
            dir_path = os.path.join("../temp", body['folder'])
            rmtree(dir_path)
            RedisClient.getInstance().set(body['folder'], result)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
            RedisClient.getInstance().set(body['folder'], "Error: %s : %s" % (dir_path, e.strerror))
    except:
        print("err")


def createFile(ch, body):
    #path = "/temp/" + body['folder']
    path = os.path.join("../temp", body["folder"])
    RedisClient.getInstance().set(body['folder'], 'create file function')
    try:
        os.mkdir(path)
        RedisClient.getInstance().set(body['folder'], 'dir created')
        try :
            filepath = os.path.join(path, "input.txt")
            #i = open(path +"/input.txt", "w+")
            i = open(filepath, "w+")
            RedisClient.getInstance().set(body['folder'], 'input file')
            #i.write(body['input'])
            i.write("test")
            try :
                RedisClient.getInstance().set(body['folder'], 'more')
                f = open(path +'/source.'+ extensions[body['lang']], "w")
                f.write(body['src'])
                f.close()
                runCode(ch,body)
            except :
                print ("Creation of the directory %s failed" % path)                
        except :
            print ("Creation of the directory %s failed" % path)
            #RedisClient.getInstance().set(body['folder'], 'input file failed to create')
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)
    


def updateRedis(key, newContent):
        RedisClient.getInstance().set(key, newContent)



def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    #time.sleep(body.count(b'.'))
    print(" [x] Done")
    content = json.loads(body.decode())
    #print("Content : ")
    #print(content['folder'])
    createFile(ch, content)
    #updateRedis(content['folder'], "depuis le worker")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel = Connection.getInstance().channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
channel.start_consuming()




# If we're running in stand alone mode, run the application

if __name__ == '__main__':
  app.run(host='localhost', debug=True, port = 5001, threaded = True) 
