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

recording_uri = lambda u: f"recordings/{u}"
data_uri = lambda u: f"data/{u}"
transcription_uri = lambda u: f"transcriptions/{u}"
s3_recording_uri = lambda u: f"s3://{S3_BUCKET_NAME}/{recording_uri(u)}"

session = boto3.Session(profile_name=AWS_PROFILE_NAME)
s3 = session.client('s3')

filenames = ['test.mp3']

for filename in filenames:
  with closing(open(data_uri(filename), 'rb')) as f:
      p = s3.upload_fileobj(f, S3_BUCKET_NAME, recording_uri(filename))
  
transcribe = session.client('transcribe')
for filename in filenames:
  job_name = filename
  job_uri = s3_recording_uri(filename) # s3://DOC-EXAMPLE-BUCKET1/key-prefix/file.file-extension"

  transcribe.start_transcription_job(
      TranscriptionJobName=job_name,
      Media={'MediaFileUri': job_uri},
      MediaFormat='mp3',
      LanguageCode='en-US'
  )

  while True:
      status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
      if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
          break
      print(f"Transcription job '{job_name}' is not ready yet...")
      time.sleep(5)
  assert status['ResponseMetadata']['HTTPStatusCode'] == 200
  sample_rate = status['TranscriptionJob']['MediaSampleRateHertz']
  transcribe_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
  opened = urlopen(transcribe_url)
  data_json = json.loads(opened.read())
  print(data_json)
  transcribe.delete_transcription_job(TranscriptionJobName=job_name)
  with closing(open(transcription_uri(f"{os.path.splitext(filename)[0]}.json"), 'w')) as f:
    json.dump(data_json, f)
  


polly = session.client("polly")

try:
    # Request speech synthesis
    response = polly.synthesize_speech(Text="Hello world!", OutputFormat="mp3",
                                        VoiceId="Joanna")
except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)

if 'AudioStream' in response:
    with closing(response["AudioStream"]) as stream:
        save_path = os.path.join(os.getcwd(), 'data', 'test.mp3')
        file = open(save_path, 'wb')
        file.write(stream.read())