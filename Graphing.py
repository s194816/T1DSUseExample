import tkinter 
from paho.mqtt import client as mqtt_client
from paho import mqtt
import json
import csv
from datetime import datetime
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

broker = '4af60bec82144872a35cde8b4ad13058.s1.eu.hivemq.cloud'
port = 8883
#topic = "test"
topic_sub = input("Enter topic to subscribe to: ")
filename = topic_sub+".csv"
print(topic_sub)

username = 'DEM-T1DS'
password = 'Thesis1234'
deviceId = "your deviceId"

def getDataAndPlotIt():
    file = open(filename,'r')
    
    file = csv.DictReader(file)
    
    date = []
    BG = []
    
    for col in file:
        date.append(col['Lines'])
        BG.append(col['BG'])
        
    f = Figure(figsize=(15,10), dpi=100)
    a = f.add_subplot(221,title = topic_sub)
    a.plot(date,BG)
    
    
    f.subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9, top = 0.9, wspace = 0.4, hspace=0.4)
    
    canvas = FigureCanvasTkAgg(f,window)
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=0)
    
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    toolbar.place(x=0, y= 480)
    
    window.after(5000,getDataAndPlotIt)
        
    

def AddHeader():
    try:
        with open(filename,'r') as csv_file:
            pass
        
    except:
        with open (filename, mode = 'w', newline = '') as csv_file:
            fieldnames = ['Lines','BG',"Date and Time"]
            writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            writer.writeheader()
            
            
            
def writedata(a):
    file = open(filename)
    reader = csv.reader(file)
    lines = len(list(reader))
    lines+=1
    
    now = datetime.now()
    with open(filename,mode='a',newline='')as csv_file:
        csv_file_writer=csv.writer(csv_file,delimiter=',',quotechar='"')
        csv_file_writer.writerow([lines,a,now.strftime("%d/%m/%Y %H:%M:%S")])
        

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
    client = mqtt_client.Client()
    #client.tls_set(ca_certs='isrgrootx1.pem',tls_version=mqtt.client.ssl.PROTOCOL_TLS) 
    client.tls_set(ca_certs="isrgrootx1.pem")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        y = json.loads(msg.payload.decode())
        writedata(y)
        print(y)
        print(msg.topic)

    client.subscribe(topic_sub)
    client.on_message = on_message       
    

                
window = tkinter.Tk()
window.title("Patient status")
window.geometry('960x540')
window.resizable(False,False)
window.configure(bg="white")
            

client = connect_mqtt()
subscribe(client)
client.loop_start()
AddHeader()
getDataAndPlotIt()

window.mainloop()
client.loop_stop()            