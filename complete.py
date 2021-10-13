from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import time
import boto3
from urllib.request import urlopen
import json


S3_BUCKET_NAME = 'patwang123bucket'
AWS_PROFILE_NAME = 'patwang123'
AWS_REGION = 'us-east-1'

SUPPORTED_FORMATS = ['.wav', '.mp3']

recording_uri = lambda u: f"recordings/{u}"
data_uri = lambda u: f"data/{u}"
transcription_uri = lambda u: f"transcriptions/{u}"
s3_recording_uri = lambda u: f"s3://{S3_BUCKET_NAME}/{recording_uri(u)}"

session = boto3.Session(profile_name=AWS_PROFILE_NAME)
s3 = session.client('s3')
polly = session.client("polly")

# list of file names that should be located in the data/
filenames = os.listdir(os.path.join(os.getcwd(), 'data'))

for filename in filenames:
  with closing(open(data_uri(filename), 'rb')) as f:
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
      MediaFormat='wav',
      LanguageCode='en-US'
  )

  while True:
      status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
      if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
          break
      print(f"Transcription job '{job_name}' is not ready yet...")
      time.sleep(5)
  assert status['ResponseMetadata']['HTTPStatusCode'] == 200
  transcribe_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
  opened = urlopen(transcribe_url)
  data_json = json.loads(opened.read())
  transcribe.delete_transcription_job(TranscriptionJobName=job_name)
  with closing(open(transcription_uri(f"{os.path.splitext(filename)[0]}.json"), 'w')) as f:
    json.dump(data_json, f)
  try:
    # Request speech synthesis
    response = polly.synthesize_speech(Text=data_json['results']['transcripts'][0]['transcript'],
                                       OutputFormat="mp3",
                                       VoiceId="Joanna")
  except (BotoCoreError, ClientError) as error:
      # The service returned an error, exit gracefully
      print(error)
      continue

  if 'AudioStream' in response:
    with closing(response["AudioStream"]) as stream:
      save_path = os.path.join(os.getcwd(), 'data', filename)
      file = open(save_path, 'wb')
      file.write(stream.read())
