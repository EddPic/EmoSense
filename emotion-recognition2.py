#!/usr/bin/python3.6

import os, io
from google.cloud import vision
import pandas as pd
import picamera
from time import sleep

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'pivotal-racer-373206-010f8b7eecc2.json'

def takephoto():
    camera = picamera.PiCamera()
    camera.start_preview()
    sleep(2)
    camera.capture('image.jpg')
    camera.stop_preview()

def main():
    takephoto()
    """Deteccion de emociones """
    
    client = vision.ImageAnnotatorClient()
    image_path= os.path.abspath('image3.jpg')

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    
    response = client.face_detection(image=image)
    faces = response.face_annotations
        
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('Enojo: {}'.format(likelihood_name[face.anger_likelihood]))
        print('Alegria: {}'.format(likelihood_name[face.joy_likelihood]))
        print('Sorpresa: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('Tristeza: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    """##########################"""
    txt=likelihood_name[face.anger_likelihood]
    print(txt)
    
    
    
    """##########################"""
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        

if __name__ == '__main__':

    main()
