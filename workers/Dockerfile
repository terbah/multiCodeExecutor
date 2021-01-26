FROM ubuntu:16.04
RUN apt-get update -y
RUN apt-get install curl vim sudo build-essential -y
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
RUN apt-get install nodejs -y
#flask
RUN apt install python3-pip -y
RUN pip3 install flask
COPY app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#haskell
#RUN apt-get install haskell-platform -y
RUN curl -sSL https://get.haskellstack.org/ | sh
RUN apt-get install ghc -y
RUN node -v
RUN npm -v

COPY . .
RUN mkdir temp
RUN chmod 700  /
RUN chmod 755 -R temp/
RUN adduser --disabled-password --gecos "" task_queue
# RUN cd app && npm install
# CMD cd app &&  npm start 

CMD ["python3", "app/worker.py"]
