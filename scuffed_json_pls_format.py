"""
Please format this
"""
import datetime
import tzlocal
status = {'TranscriptionJob':
        {'TranscriptionJobName': 'test.mp3',
        'TranscriptionJobStatus': 'COMPLETED',
        'LanguageCode': 'en-US',
        'MediaSampleRateHertz': 22050,
        'MediaFormat': 'mp3',
        'Media': {'MediaFileUri': 's3://patwang123bucket/recordings/test.mp3'},
        'Transcript': {'TranscriptFileUri': 'https://s3.us-east-1.amazonaws.com/aws-transcribe-us-east-1-prod/923775399665/test.mp3/b86f6774-9302-4a2a-b222-f8cd293275ff/asrOutput.json?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEoaCXVzLWVhc3QtMSJHMEUCIQCJIC8b9jWg2Pw9bClWgdiHsVh%2BHsnr7BrocXpx252EdQIgVzWP9HwxDjnJjIx%2FmZVeB0%2B0J5LL9aff0fEDpUepJkkqgwQIw%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARADGgwyNzY2NTY0MzMxNTMiDOm2VbBLGicNhKzPFCrXA3UHjfAC8lS8YYbYwVtIpy3ZeqHWKEZ1dw9Ug4Suck%2Bw%2FPVIVRx1CrFixjoz%2BAy1KSvurKY6Rs8homTKH1z5jwdvwW8Oxrq9Jpx9uKixAfBxCc%2F9AiZg7mwbSXyhbcCN8baO5eUqMzc0u5MVOQxGRWYgoSHD%2BTuz7YEzRurrNzSR6pRFLNP5XRiCksllt%2FuuzMwSZre8yTDUYXKSG0zSTKQ6g4pPhmWak2sFcY2L14SYW%2BiHuWSM0wV2b1pNBTn2P8PN543md2Cn0xUYaPMUCVdOgxXavlIYzYFo8niu0OjkzVj2%2BA3acjho2K3NOBCNtamUEP8vIB8%2FdG97%2Bo4XZr4hjrrMX9ENRZK1mCcU5AL96IEwvmBJdkymQoU9B1M1WpqvFtRWIZtS5VyD8Ux4qrFhNarI%2FyChe0TYQl5JnhYH1%2BcOF0kxIl21A3c4BdI8u9wzXHTEGxANd1JYljtSD8xH44hzVO%2F6mxeZCwBnkoFjVpUIJ0j7YN%2BYpxKI7AWiLUAJtzAwMxQ8RmncDB2Mnb5z5Dl5NONj6CS%2BYjkJmbrjJD19jGMywdvK1sbpllWj8Gx2KSelNlRexxV95LkLs10Ur6evbjMEXM13e0ZWrHC3mkzvuV9O4DDGqYeLBjqlAYBkU6tAjiqguoUHt5Z1tLC6qqrsay0BQ4fbfZLYJ2Lx5juh%2BYJ%2BDMP3ON4MDjLL18%2FIAMX1sIytzAaQy9IipMSMOcjmEAzX%2Fq2BHJfStLyJ5a%2BAFPMCQmcxqSxisbZ928wShkucDoMuf1ITpVaw7E8qoEkJlCey3T2tqURQ7MIolbauhVoj0KNc8UjL5zN04e%2B6eXmpZg%2BgbiZ5cusVx1iKRswxeQ%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20211009T184231Z&X-Amz-SignedHeaders=host&X-Amz-Expires=899&X-Amz-Credential=ASIAUA2QCFAA2QWXXDTH%2F20211009%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=ce0d837236366ba085825b3954a398ca011c4377405388b8d7a7d8f8496ce300'},
        'StartTime': datetime.datetime(2021, 10, 9, 11, 42, 16, 144000, tzinfo=tzlocal()),
        'CreationTime': datetime.datetime(2021, 10, 9, 11, 42, 16, 109000, tzinfo=tzlocal()),
        'CompletionTime': datetime.datetime(2021, 10, 9, 11, 42, 29, 88000, tzinfo=tzlocal()),
        'Settings': {'ChannelIdentification': False, 'ShowAlternatives': False}
        },
    'ResponseMetadata': {'RequestId': 'e5124763-1064-4479-a8e7-4f8b4dfe054f',
                        'HTTPStatusCode': 200,
                        'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1',
                                        'date': 'Sat, 09 Oct 2021 18:42:31 GMT',
                                        'x-amzn-requestid': 'e5124763-1064-4479-a8e7-4f8b4dfe054f',
                                        'content-length': '1993',
                                        'connection': 'keep-alive'},
                        'RetryAttempts': 0
                        }
    }

example = {
            "jobName": "test.mp3", 
            "accountId": "923775399665",
            "results": {
                        "transcripts": [
                                        {"transcript": "Hello World."}
                                       ],
                        "items": [
                                  {
                                    "start_time": "0.04", 
                                    "end_time": "0.39",
                                    "alternatives": [
                                                      {"confidence": "0.9976", "content": "Hello"}
                                                    ],
                                    "type": "pronunciation"
                                  },
                                  {
                                    "start_time": "0.39",
                                    "end_time": "0.83",
                                    "alternatives": [
                                                      {"confidence": "1.0", "content": "World"}
                                                    ],
                                    "type": "pronunciation"
                                  },
                                  {
                                    "alternatives": [
                                                      {"confidence": "0.0", "content": "."}
                                                    ],
                                    "type": "punctuation"
                                  }
                                ]
                        },
            "status": "COMPLETED"
          }
