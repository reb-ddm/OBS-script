import simpleobsws
import asyncio
from tkinter import *
from tkinter.font import BOLD, Font
from PIL import ImageTk, Image
import cv2
import os
import time
from threading import Timer
root = Tk()

# settings
cameraID = 3
camera_name = "Video Capture Device"
backgrounds = ["Berg", "Strand", "Lissabon"]
actual_width = 3840
actual_height = 2160
display_width = 192
# actualWidth/20
display_height = 108
default_font = Font(size=18)
button_font = Font(size=16)

def resize_to_diplay_size(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, display_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, display_height)

def resize_to_picture_size(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, actual_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, actual_height)

# obs setup
# import logging
# logging.basicConfig(level=logging.DEBUG)
serverIP = "192.168.56.1"
serverPort = "4455"
serverPassword = "CJ6kMU1YRr0IkEYo"
sceneName = "Scena"
ws = simpleobsws.WebSocketClient(
    url='ws://localhost:' + serverPort, password=serverPassword)


async def make_request(requestType, requestData=None):
    await ws.connect()  # Make the connection to obs-websocket
    # Wait for the identification handshake to complete
    await ws.wait_until_identified()
    request = simpleobsws.Request(
        requestType, requestData)  # Build a Request object
    ret = await ws.call(request)  # Perform the request
    response_data = None
    if ret.ok():  # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))
        response_data = ret.responseData
    await ws.disconnect()  # Disconnect from the websocket server cleanly
    return response_data

# obs requests


def get_items():
    loop = asyncio.get_event_loop()
    item_list = loop.run_until_complete(make_request('GetInputList'))
    return item_list.get("inputs")


def get_item_id(item_name):
    loop = asyncio.get_event_loop()
    item_id = loop.run_until_complete(make_request('GetSceneItemId', {"sceneName": sceneName,
                                                                      "sourceName": item_name}))
    print(item_id)
    if item_id != None:
        return item_id.get("sceneItemId")
    else:
        return None


def enable_background(item_id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_request('SetSceneItemEnabled', {"sceneName": sceneName,
                                                                 "sceneItemId": item_id,
                                                                 "sceneItemEnabled": True}))


def disable_background(item_id):
    loop = asyncio.get_event_loop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_request('SetSceneItemEnabled', {"sceneName": sceneName,
                                                                 "sceneItemId": item_id,
                                                                 "sceneItemEnabled": False}))


# photo naming
photoIndex = 0

# GUI
video = Frame(root, bg="white", width=display_width, height=display_height)
video.grid(column=1)
lmain = Label(video)
lmain.grid()
# Capture from camera
cap = cv2.VideoCapture(cameraID)
resize_to_diplay_size(cap)

# function for video streaming


def video_stream():
    try:
        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img, height=display_height, width=display_width)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk, height=display_height, width=display_width)
    except:
        print("An exception occurred in video_stream")
    lmain.after(3, video_stream)


video_stream()

# backgrounds
change_background_frame = Frame(root)
change_background_frame.grid(column=0, row=0)
change_background_text = Label(
    change_background_frame, text="Hintergrund ändern", font=default_font)
change_background_text.grid()


def change_background(background_name):
    print("Enabling background: " + background_name)
    item_list = get_items()
    for item in item_list:
        name = item.get("inputName")
        item_id = get_item_id(name)
        if item_id != None:
            if name == background_name:
                enable_background(item_id)
            elif name != camera_name:
                disable_background(item_id)


background_buttons = []
for background in backgrounds:
    background_button = Button(
        change_background_frame, text=background, font=button_font)
    background_button.bind("<Button-1>", lambda event,
                           bg=background: change_background(bg))
    background_button.grid()
    background_buttons.append(background_button)


# take pictures
take_pictures_frame = Frame(root)
take_pictures_frame.grid(column=1, row=1)
take_pictures_label = Label(
    take_pictures_frame, text="Name des Bildes", font=default_font)
take_pictures_label.grid()
picture_name_entry = Entry(take_pictures_frame)
picture_name_entry.grid()


def get_picture_name():
    typed_name = picture_name_entry.get()
    if typed_name == "":
        picture_name = str(photoIndex)
    else:
        picture_name = str(photoIndex) + " - " + typed_name
    picture_name_entry.delete(0, END)
    return picture_name + ".jpg"


def get_new_picture_name():
    global photoIndex
    name = get_picture_name()
    photoIndex += 1
    while os.path.exists("img/" + name):
        name = get_picture_name()
        photoIndex += 1
    return name


button = Button(take_pictures_frame, text="Foto aufnehmen!", font=button_font)
success_text = Label(take_pictures_frame)
success_text.grid()


def take_picture(event):
    global photoIndex
    resize_to_picture_size(cap)
    _, frame = cap.read()
    resize_to_diplay_size(cap)
    name = get_new_picture_name()
    if cv2.imwrite("img/" + name, frame):
        success_text.config(
            text="Bild erfolgreich gespeichert unter " + os.getcwd() + "\\img\\" + name)
    else:
        success_text.config(text="Fehler beim speichern des Bildes.")


button.bind("<Button-1>", take_picture)
button.grid()

five_sec_button = Button(
    take_pictures_frame, text="Foto aufnehmen in 5 Sekunden", font=button_font)
five_sec_frame = Frame(root)
five_sec_frame.grid(column=2, row=0)
five_sec_label = Label(five_sec_frame, font=("Arial", 35, BOLD))
five_sec_label.grid()


def take_picture_in_n_sec(event, n):
    for i in range(n, 0, -1):
        five_sec_label.config(text=str(i))
        print(i)
        time.sleep(1)
    five_sec_label.config(text="0")
    take_picture(event)
    five_sec_label.config(text="")


def take_picture_in_5_sec_in_new_thread(event):
    t = Timer(0, take_picture_in_n_sec, args=[None, 5], kwargs=None)
    t.start()


five_sec_button.bind("<Button-1>", take_picture_in_5_sec_in_new_thread)
five_sec_button.grid()


# start GUI
root.mainloop()
