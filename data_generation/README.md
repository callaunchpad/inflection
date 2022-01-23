# Data Generation

## Setup

Make sure to set up the AWS CLI on your device and update S3_BUCKET_NAME, AWS_PROFILE_NAME, and AWS_REGION to match an S3 bucket you create. 

## Code

Begin by adding your input file (10-15 minutes of speaker speaking with minimal background noise and other voices) to this folder 
with the file name `[NAME].mp3` replacing [NAME] with the name of your speaker.

Then split it by running:

`python split.py [NAME]`

Last, generate pairs by running:

`python pair.py [NAME]`

The final pairs will be stored with the human voice in `recordings/[NAME]/human` and the Amazon voice in `recordings/[NAME]/joanna`. 

## Method

Our input to the system is just someone talking, however this form of voice conversion uses parallel utterances from two speakers. For example:

Input: [Alexa]
Output: [Trump]

To create these pairs, we implement the following process. 

1. Split the original file into 15 second segments. This is to reduce the impact of any alignment issues in the future
2. Transcribe (Speech-to-Text) each of the segments using Amazon Transcribe
3. Run Text-to-Speech on each of the transcriptions using Amazon Polly

Especially since speakers talk at different speeds, there will still be alignment issues. However, these are addressed using Dynamic Time Warping in [Spectral Analysis](https://github.com/mraheja/inflection/tree/main/spectral_analysis).
