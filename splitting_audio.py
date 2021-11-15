import pyworld
from scipy.io import wavfile

import IPython
from IPython.display import Audio

import matplotlib.pyplot as plt
import numpy as np
import pysptk

sampling_frequency, data = wavfile.read("steph.wav")
IPython.display.display(Audio(data.T, rate = sampling_frequency))
plt.plot(data)
print("Sampling Frequency: ", sampling_frequency)

from pydub import AudioSegment
import math
class SplitWavAudioMubin():
    def __init__(self, filename):
        self.filename = filename
        self.filepath = filename
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 1000
        t2 = to_min * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(split_filename, format="wav")
        
    def multiple_split(self, secs_per_split):
        total_secs = math.ceil(self.get_duration())
        for i in range(0, total_secs, secs_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+secs_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_secs - secs_per_split:
                print('All splited successfully')

file = 'steph.wav'
split_wav = SplitWavAudioMubin(file)
split_wav.multiple_split(secs_per_split=15)

from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import time
import boto3
from urllib.request import urlopen
import json


S3_BUCKET_NAME = 'inflectionbucket123'
AWS_PROFILE_NAME = 'amudhasairam'
AWS_REGION = 'us-east-1'

SUPPORTED_FORMATS = ['.wav', '.mp3']

recording_uri = lambda u: f"recordings/{u}"
data_uri = lambda u: f"data/{u}"
transcription_uri = lambda u: f"transcriptions/{u}"
s3_recording_uri = lambda u: f"s3://{S3_BUCKET_NAME}/{recording_uri(u)}"

session = boto3.Session(profile_name=AWS_PROFILE_NAME, region_name = AWS_REGION)
s3 = session.client('s3')
polly = session.client("polly")

try:
    s3.create_bucket(Bucket = S3_BUCKET_NAME)
except:
    pass

# list of file names that should be located in the data/
filenames = os.listdir(os.path.join(os.getcwd(), 'recordings'))

for filename in filenames:
  with closing(open(recording_uri(filename), 'rb')) as f:
      p = s3.upload_fileobj(f, S3_BUCKET_NAME, recording_uri(filename))
  
transcribe = session.client('transcribe')
for filename in filenames:
  job_name = filename
  job_uri = s3_recording_uri(filename) # s3://DOC-EXAMPLE-BUCKET1/key-prefix/file.file-extension"
  
  print(f"Starting transcription job for {filename}")
  if filename[-4:] not in SUPPORTED_FORMATS:
      print(f"File does not end with one of {SUPPORTED_FORMATS}, skipping...")
 
  transcribe.start_transcription_job(
      TranscriptionJobName=job_name,
      Media={'MediaFileUri': job_uri},
      MediaFormat=filename[-3:],
      LanguageCode='en-US'
  )

  while True:
      status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
      if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
          break
      print(f"Transcription job '{job_name}' is not ready yet...")
      time.sleep(5)

  assert status['ResponseMetadata']['HTTPStatusCode'] == 200

  # Get location of data from transcription job and read in json
  transcribe_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
  opened = urlopen(transcribe_url)
  data_json = json.loads(opened.read())

  # Delete transcription job to clean up AWS or whatever
  transcribe.delete_transcription_job(TranscriptionJobName=job_name)

  # Save file to transcription folder
  with closing(open(transcription_uri(f"{os.path.splitext(filename)[0]}.json"), 'w')) as f:
    json.dump(data_json, f)

  # Using polly to synthesize speech based on transcript
  try:
    # Request speech synthesis
    response = polly.synthesize_speech(Text=data_json['results']['transcripts'][0]['transcript'],
                                       OutputFormat="mp3",
                                       VoiceId="Joanna")
  except (BotoCoreError, ClientError) as error:
      # The service returned an error, exit gracefully
      print(error)
      continue
  
  # Save polly response to data
  if 'AudioStream' in response:
    with closing(response["AudioStream"]) as stream:
      save_path = os.path.join(os.getcwd(), 'data', filename)
      file = open(save_path, 'wb')
      file.write(stream.read())
