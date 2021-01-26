from flask import Flask
from flask_restful import Resource, Api, reqparse
import pika
import redis
import sys
import secrets
import json

# Create the application instance
app = Flask(__name__)
api = Api(app)

QUEUE_NAME = 'task_queue'

extensions = {
    "cpp":"cpp",
    "c": "c",
    "java":"java",
    "python3":"py",
    "javascript":"js",
    "haskell":"hs"
}


req_args = reqparse.RequestParser()
req_args.add_argument('src', type=str, help="source code to be executed", required =True)
req_args.add_argument('stdin', type=str, help="inputs")
req_args.add_argument('lang', type=str, help="language", required=True)
req_args.add_argument('timeout', type=int, help="limit time execution", required=True)


connected = False

print("server launching")


def random(size):
    return secrets.token_hex(size)




def connect():
        connection = Connection.getInstance()
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        return channel
"""         except :
            print("error") """

#connect()


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
                pika.ConnectionParameters(host='rabbit', heartbeat=0))



class Req(Resource):
    def get(self):
        return "hello"
        

    #@app.route('/submit',methods=['POST'])    
    def post(self):
        print ("on est la")
        args = req_args.parse_args()
        #print(args)
        folder = random(5)
        channel = connect()
        body = {
            'src' : args['src'],
            'lang': args['lang'],
            'timeout' : args['timeout'],
            'stdin' : args['stdin'],
            'folder' : folder
        }
        addToQueue(json.dumps(body), channel)
        #RedisClient.getInstance().set(folder, args)
        #RedisClient.getInstance().set(folder, "coucou")
        #print(args.json())
        return folder, 200


@app.route('/get/<string:key>',methods=['GET'])
def test(key):
        status = RedisClient.getInstance().get(key)
        if (status == None):
            return {"status":"Queued"}, 202
        elif(status=={"status":"Processing"}):
            return {"status":"Processing"}, 202
        else :
            return status,200
        return {
            'src' : 'print',
            'stdin' : '',
            'lang' : 'python3',
            'timeout' : 5,
            'folder' : random(10)
        }



def addToQueue(data, channel):
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=data)
    print("data added to queue")
#connection.close()


api.add_resource(Req, '/')


# If we're running in stand alone mode, run the application

""" if __name__ == '__main__':
    app.run(debug=True, port = 5000, threaded = True) """
