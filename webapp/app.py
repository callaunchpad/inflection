import torch

import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, n_mfcc=40):
        super(MLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(n_mfcc, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64,128),
            nn.BatchNorm1d(128),
        )
        
        self.rnn = nn.LSTM(128, 64, 2, batch_first = True, bidirectional = True)
        
        self.lin = torch.nn.Linear(128, n_mfcc)
        
        self.h0 = torch.randn(4, 1, 64).to(device)
        self.c0 = torch.randn(4, 1, 64).to(device)
        
    def forward(self, x):
        x = self.layers(x)
        x = x.view(1, -1, *x.shape[1:])
        x, _ = self.rnn(x, (self.h0, self.c0))
        x = x.squeeze()
        x = self.lin(x)
        return x

from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS

from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import time
import boto3
import json

from ml import convert

#AWS Constants
AWS_PROFILE_NAME = 'patwang123'
AWS_REGION = 'us-east-1'

BOT_NAME = 'BookTrip'
BOT_ALIAS = 'test'
USER_ID = 'pat'

# Start Lex session
session = boto3.Session(profile_name=AWS_PROFILE_NAME, region_name=AWS_REGION)
lex = session.client('lex-runtime')

try:
    lex.delete_session(botName=BOT_NAME, botAlias=BOT_ALIAS, userId=USER_ID)
except:
    pass

bot_session = lex.put_session(botName=BOT_NAME, botAlias=BOT_ALIAS, userId=USER_ID) # bot alias/ name are required,,?
def get_bot_output(text):
	response = lex.post_content(botName='BookTrip',
                                botAlias='test', 
                                userId='pat',
                                contentType='text/plain; charset=utf-8',
                                inputStream=text)
	message = response["ResponseMetadata"]["HTTPHeaders"]["x-amz-lex-message"]
	audioStream = response["audioStream"]
	return message, audioStream

app = Flask(__name__)
CORS(app)

@app.route('/', methods= ['GET', 'POST'])
def get_message():
	print("Got request in main function")
	return render_template("index.html")

@app.route('/speak', methods=['GET'])
def speak():
	text = request.args['text']
	print("RECEIVED TEXT: ", text)
	message, stream = get_bot_output(text)
	print("RESPONDING WITH", message)
	file = open('response.wav', 'wb')
	file.write(stream.read())
	file.close()
	os.system('ffmpeg -i response.wav response2.wav -y')
	convert()

	path_to_file = 'output.wav'
	return send_file(
		path_to_file, 
		mimetype="audio/wav", 
		as_attachment=True, 
		attachment_filename="test.wav"
	)
 
if __name__ == "__main__":
	app.run(debug=True, ssl_context="adhoc")