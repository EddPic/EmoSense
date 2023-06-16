#!/usr/bin/python3.6

import base64
import picamera
import json
import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/equipo7/Desktop/Google-Recognition-master/pivotal-racer-373206-010f8b7eecc2.json"

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')

def main():
    takephoto()
    """Deteccion de emociones """

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('image.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'FACE_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()
        print (json.dumps(response, indent=4, sort_keys=True))

if __name__ == '__main__':

    main()
