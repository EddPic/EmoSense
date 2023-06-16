"""Paquetes a Instalar:
    pip install customtkinter
    sudo apt-get install python-imaging-tk
"""

import os, io
from google.cloud import vision
#import pandas as pd

from picamera import PiCamera
from time import sleep
import customtkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import paho.mqtt.client as mqtt
import time
from datetime import datetime
from os import listdir
#import numpy as np
from natsort import natsorted
import fpdf


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'pivotal-racer-373206-010f8b7eecc2.json'


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x800")
root.title("App IoT")

numdatos=5
tcaptura=5

"""MQTT"""

mqttBroker= "192.168.137.242"
max30100 = "esp32/heartrate"
gsr = "esp32/gsr"




def on_message(client, userdata, message):
    global datagsr,databpm
    if message.topic ==max30100:
        #print("BPM: " ,str(message.payload.decode("utf-8")))
        databpm=str(message.payload.decode("utf-8"))
    elif message.topic ==gsr:
        #print("GSR " ,str(message.payload.decode("utf-8")))
        datagsr=str(message.payload.decode("utf-8"))
        


client = mqtt.Client("")
client.connect(mqttBroker) 

client.loop_start()

client.subscribe([(max30100,1),(gsr,1)])
client.on_message=on_message 


global timelist, gsrlist, bpmlist, resultsensor, emotionlist, datatable


timelist=[]
gsrlist=[]
bpmlist=[]
resultsensor=[]
emotionlist=[]
datatable=[]




def Photo():    
    camera = PiCamera()
    camera.start_preview()
    for i in range(1,numdatos):
        sleep(tcaptura)
        camera.resolution = (1280, 720)
        camera.capture('/home/equipo7/Desktop/ProyectoIoT/Google-Recognition-master/Imagenes/Image%s.jpg' % i)
        timedata=datetime.now()
        registro=timedata.strftime("%H:%M:%S")
        timelist.append(registro)
        gsrlist.append(datagsr)
        bpmlist.append(databpm)
    camera.stop_preview()
    camera.close()
    
    #Carpeta Picamera
    images_dir="/home/equipo7/Desktop/ProyectoIoT/Google-Recognition-master/Imagenes"
    #Carpeta Pruebas
    #images_dir="/home/equipo7/Desktop/ProyectoIoT/Google-Recognition-master/Pruebas"

    for images in os.listdir(images_dir):
        #print(images)
        if (images.endswith(".jpg")):
            #print(images)
            dirimage=images_dir+"/"+images
#             print(type(dirimage))
#             print(dirimage)
                
            deteccion(dirimage)
            emotionlist.append(respuesta)
    print(emotionlist)
    print(gsrlist)
    print(bpmlist)
    
    for i in range(numdatos-1):
        #print(i)
        if int(bpmlist[i]) >100:
            #print("Enojado")
            resultsensor.append("Enojado")
        elif int(bpmlist[i]) >80 and int(bpmlist[i]) <100 and int(gsrlist[i]) < 1700:
            #print("Triste")
            resultsensor.append("Triste")
        elif int(gsrlist[i]) > 1700 and int(bpmlist[i]) > 80 and int(bpmlist[i]) <100:
            #print("Alegre")
            resultsensor.append("Alegre")
        else:
            #print("Neutral")
            resultsensor.append("Neutral")
            
    print(resultsensor)
    formulario()
""""""
    

def deteccion(photodir):
    """Deteccion de emociones """
    global respuesta
    
    client = vision.ImageAnnotatorClient()
    image_path= os.path.abspath(photodir)

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    
    response = client.face_detection(image=image)
    faces = response.face_annotations
        
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    #print('Deteccion de Emocion:')
    
    
    d_emociones={'Enojo':'','Alegria':'','Sorpresa':'', 'Tristeza':''}
    respuesta=''

    for face in faces:
#         print('Enojo: {}'.format(likelihood_name[face.anger_likelihood]))
#         print('Alegria: {}'.format(likelihood_name[face.joy_likelihood]))
#         print('Sorpresa: {}'.format(likelihood_name[face.surprise_likelihood]))
#         print('Tristeza: {}'.format(likelihood_name[face.sorrow_likelihood]))
        
        d_emociones['Enojo']=likelihood_name[face.anger_likelihood]
        d_emociones['Alegria']=likelihood_name[face.joy_likelihood]
        d_emociones['Sorpresa']=likelihood_name[face.surprise_likelihood]
        d_emociones['Tristeza']=likelihood_name[face.sorrow_likelihood]
    


        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

#         print('face bounds: {}'.format(','.join(vertices)))
        
    for key, value in d_emociones.items():
        if(str(value)=='UNLIKELY' or str(value)=='POSSIBLE' or str(value)=='LIKELY' or str(value)=='VERY_LIKELY' ):
            respuesta=key
        
    """
    response = service_request.execute()
        print (json.dumps(response, indent=4, sort_keys=True))
    """    
#     emotion=customtkinter.CTkLabel(master=frame,text=respuesta,width=100,height=30,fg_color=("transparent"))
#     emotion.place(relx=0.5, rely=0.8, anchor="center")

    #print(respuesta)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(response.error.message))


def login():
    #main()
#     cameraresult=customtkinter.CTkImage(Image.open("/home/Equipo7/Desktop/ProyectoIoT/Google-Recognition-master/image2.jpg"),size=(300,300))
#     label = customtkinter.CTkLabel(master=frame,image=cameraresult,text="",width=300,height=300,fg_color=("transparent"))
#     label.place(relx=0.5, rely=0.55, anchor="center")

    """emotion=customtkinter.CTkLabel(master=frame,text=respuesta,width=100,height=30,fg_color=("transparent"))
    emotion.place(relx=0.5, rely=0.8, anchor="center")"""
    

def verificacion():
    
    global datausername,datalastname,datasession
    
    datausername=usernameentry.get()
    datalastname=lastnameentry.get()
    datasession=sessionentry.get()
    
    if datausername !="" and datalastname !="" and datasession !="":
        screen2()
    else:
        messagebox.showwarning(title="Error", message="Ingrese Datos de Sesion")
        
    
    
def formulario():
    
    global datatable
    datatable=[timelist,gsrlist,bpmlist,resultsensor,emotionlist]
    newdatauser=zip(*datatable)
    print(newdatauser)
    
    pdf = fpdf.FPDF(orientation="portrait",format='A4')

    pdf.add_page()
    pdf.set_font("Arial", size=18, style="B")
    pdf.image("UTN.png", x=10, y=8, w=30)
    pdf.cell(200, 10, txt="UNIVERSIDAD TÉCNICA DEL NORTE", ln=1, align="C")
    pdf.set_font("Arial", size=15, style="B")
    pdf.cell(200, 10, txt="Dirección de Bienestar Universitario", ln=2, align="C")
    pdf.cell(80)
    pdf.set_font("Arial", size=12)
    pdf.cell(30, 10, txt="Fecha: 2021-05-05", ln=3, align="C")
    pdf.ln(10)

    img_list=[x for x in os.listdir('Imagenes')]

    img_list=natsorted(img_list)

    cont=1
    for index,img in enumerate(img_list):
        im_w=pdf.w -2*pdf.l_margin
        i_width=im_w/3
        i_height=50
        pos_x=pdf.get_x()
        pos_y=pdf.get_y()

        #print(pos_y)
        if pos_y>250:
            pdf.add_page()
            pos_y=20
        if (index+1) % 3 == 0:
            cont=+1
            pdf.set_xy(pos_x+i_width,cont*pos_y+i_height)
            pdf.ln(10)
        else:
            pdf.set_xy(pos_x+i_width,cont*pos_y)

        pdf.image('Imagenes//'+img,pos_x,pos_y,i_width-5,i_height-5)
        
    
        #datausername,datalastname,datasession
    pdf.output("Formularios/"+datausername+datalastname+"sesion_"+datasession+".pdf")


def screen2():
    
    global frame2;
    frame.destroy()
    frame2 = customtkinter.CTkFrame(master=root,fg_color=("#222222"))
    frame2.pack(pady=20, padx=20, fill="both", expand=True)
    btnTerapia = customtkinter.CTkButton(master=frame2, text="Iniciar Sensores", command=Photo, fg_color=("#f25042"),hover_color=("#e45858"))
    btnTerapia.place(relx=0.5, rely=0.9, anchor="center")



"""Configuración de la ventana"""

frame = customtkinter.CTkFrame(master=root,fg_color=("#222222"))
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Universidad Técnica del Norte\n Facultad de Ingenieria en Ciencias Aplicadas\n Internet de las Cosas",fg_color=("#f25042"),width=550,height=60,corner_radius=10)
label.pack(pady=12, padx=10)

"""Logo de la Universidad"""""

logo=customtkinter.CTkImage(Image.open("/home/equipo7/Desktop/ProyectoIoT/Google-Recognition-master/UTN.png"),size=(150,150))
label = customtkinter.CTkLabel(master=frame,image=logo,text="",width=200,height=200,fg_color=("transparent"))
label.place(relx=0.5, rely=0.23, anchor="center")

"""Titulo Proyecto"""
projlabel=customtkinter.CTkLabel(master=frame,text="Sistema de Monitoreo de Salud Emocional",text_color=("#FFFFFF"))
projlabel.place(relx=0.5, rely=0.5, anchor="center")


"""Datos Usuario"""

usernamelabel=customtkinter.CTkLabel(master=frame,text="Nombre",text_color=("#FFFFFF"))
usernamelabel.place(relx=0.3, rely=0.6, anchor="center")
lastnamelabel=customtkinter.CTkLabel(master=frame,text="Apellido",text_color=("#FFFFFF"))
lastnamelabel.place(relx=0.3, rely=0.65, anchor="center")
sessionlabel=customtkinter.CTkLabel(master=frame,text="Numero de Sesion",text_color=("#FFFFFF"))
sessionlabel.place(relx=0.3, rely=0.7, anchor="center")

dusername=StringVar()
dlastname=StringVar()
dsession=StringVar()

usernameentry=customtkinter.CTkEntry(master=frame,text_color=("#000000"),fg_color=("#FFFFFF"),textvariable=dusername)
usernameentry.place(relx=0.7, rely=0.6, anchor="center")
lastnameentry=customtkinter.CTkEntry(master=frame,text_color=("#000000"),fg_color=("#FFFFFF"),textvariable=dlastname)
lastnameentry.place(relx=0.7, rely=0.65, anchor="center")
sessionentry=customtkinter.CTkEntry(master=frame,text_color=("#000000"),fg_color=("#FFFFFF"),textvariable=dsession)
sessionentry.place(relx=0.7, rely=0.7, anchor="center")



"""Botón Terapia"""

#cameraicon=customtkinter.CTkImage(Image.open("/home/Equipo7/Desktop/ProyectoIoT/Google-Recognition-master/icon-camera.png"),size=(40,40))
button = customtkinter.CTkButton(master=frame, text="Iniciar Terapia", command=verificacion, fg_color=("#f25042"),hover_color=("#e45858"))
button.place(relx=0.5, rely=0.9, anchor="center")





root.mainloop()
