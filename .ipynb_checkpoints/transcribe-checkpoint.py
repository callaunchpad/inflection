import time
import boto3

S3_BUCKET_NAME = 'patwang123bucket'
AWS_PROFILE_NAME = 'patwang123'
AWS_REGION = 'us-east-1'

recording_uri = lambda u: f"recordings/{u}"
data_uri = lambda u: f"data/{u}"
s3_recording_uri = lambda u: f"s3://{S3_BUCKET_NAME}/{recording_uri(u)}"

session = boto3.Session(profile_name=AWS_PROFILE_NAME)
s3 = session.client('s3')

filenames = ['test.mp3']

for filename in filenames:
  with open(data_uri(filename), 'rb') as f:
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
  print(status)