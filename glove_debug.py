import PySimpleGUI as gui
import random
import serial
import time

gloveUSB = '/dev/ttyUSB1'
serGlove = serial.Serial(gloveUSB, 9600)

fingerTest = [
    [
        gui.Column(
            [
                [
                    gui.Button("Daumen"),
                    gui.Button("Zeigefinger"),
                    gui.Button("Mittelfinger"),
                    gui.Button("Ringfinger"),
                    gui.Button("Kleiner Finger"),
                ],
                [
                    gui.Button("Links"),
                    gui.Button("Rechts"),
                ]
            ],
            key="-content-"
        )
    ]
]
#Create the window
window = gui.Window("Prestudy", fingerTest, size=(600,400))

#Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the ok button
    if event == "Daumen":
        serGlove.write("1".encode())
    if event == "Zeigefinger":
        serGlove.write("2".encode())
    if event == "Mittelfinger":
        serGlove.write("3".encode())
    if event == "Ringfinger":
        serGlove.write("4".encode())
    if event == "Kleiner Finger":
        serGlove.write("5".encode())
    if event == "Links":
        serGlove.write("6".encode())
    if event == "Rechts":
        serGlove.write("7".encode())
    if event == gui.WIN_CLOSED:
        break

window.close()