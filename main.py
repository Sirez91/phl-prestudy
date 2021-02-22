import PySimpleGUI as gui
import random
import serial
import time

gloveUSB = '/dev/ttyUSB1'
serGlove = serial.Serial(gloveUSB, 9600)

totalRounds = 4
vibrations_ = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7"
]
vibrations = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "1;6",
    "2;6",
    "3;6",
    "4;6",
    "5;6",
    "1;7",
    "2;7",
    "3;7",
    "4;7",
    "5;7",
    "1",
    "2",
    "3",
    "4",
    "5",
    "1;6",
    "2;6",
    "3;6",
    "4;6",
    "5;6",
    "1;7",
    "2;7",
    "3;7",
    "4;7",
    "5;7",
]

round = 1
vibration = 0
maxRounds = 4
f = ''
id = ''

startLayout = [
    [
        gui.Column(
            [
                [
                    gui.Text("Your ID: ", key="textkey"),
                    gui.In(size=(25,1), enable_events=True, key='-ID-')
                ],
                [
                    gui.Button("START")
                ]
            ],
            key="-content-"
        )
    ]
]
fingerTest = [
    [
        gui.Column(
            [
                [
                    gui.Text("You can test the vibration on your fingers by clicking the buttons.", key="fingerText1"),
                    gui.Text("Click ready when you feel familiar with it.", key="fingerText2")

                ],
                [
                    gui.Button("Daumen"),
                    gui.Button("Zeigefinger"),
                    gui.Button("Mittelfinger"),
                    gui.Button("Ringfinger"),
                    gui.Button("Kleiner Finger"),
                    gui.Button("READY")
                ]
            ],
            key="-content-"
        )
    ]
]
vibrationTestLayout = [
    [
        gui.Text("Click if you are ready.", key="text", size=(200,1))
    ],
    [
        gui.Button("READY", key="vibrate"),
        gui.Button("DONE", key="d", visible=False),
        gui.Button("FINISH", key="end", visible=False),
        gui.Button("LEFT", key="l", visible=False),
        gui.Button("NONE", key="n", visible=False),
        gui.Button("UNDEFINED", key="u", visible=False),
        gui.Button("RIGHT", key="r", visible=False)
    ]
]

#Create the window
window = gui.Window("Prestudy", startLayout, size=(600,400))
input = []
difference = []
totalDifference = 0
roundDifference = 0


def end():
    save()
    f.close()
    window.close()

def toggleVibrationButtons(bool):
    window["l"].update(visible=bool)
    window["n"].update(visible=bool)
    window["u"].update(visible=bool)
    window["r"].update(visible=bool)


def showEnd():
    window["end"].update(visible=True)
    toggleVibrationButtons(False)
    window["d"].update(visible=False)
    window["vibrate"].update(visible=False)
    print(totalDifference)
    totalPoints = len(vibrations)*maxRounds
    window["text"].update("You passed the test with " + str(totalPoints-totalDifference) +  "/" + str(totalPoints) + " Points. Thank you for participating :D")

def save():
    global input
    global difference
    global roundDifference
    print(input)
    f.write(str(input) + "\r\n")
    input = []
    f.write(str(difference) + "\r\n")
    difference = []
    f.write(str(roundDifference) + "\r\n")
    roundDifference = 0

def showRoundEnd():
    window["d"].update(visible=True)
    toggleVibrationButtons(False)
    window["vibrate"].update(visible=False)
    window["text"].update("End of round " + str(round) + ". Glove has to be rewired, please contact the instructor.")

def isRoundEnd():
    return (len(vibrations)) <= vibration

def nextRound():
    global round
    round+=1
    save()
    startNewRound()

def startNewRound():
    random.shuffle(vibrations)
    print(vibrations)
    f.write("Round: " + str(round) + "\r\n")
    f.write(str(vibrations) + "\r\n")
    toogleButtons(False)
    global vibration
    vibration=0
    window["text"].update("Click if you are ready.")

def sendVibration():
    vibration_message = vibrations[vibration]
    print(vibration_message)
    serGlove.write(vibration_message.encode())

def toogleButtons(bool):
    window["d"].update(visible=False)
    toggleVibrationButtons(bool)
    window["vibrate"].update(visible=not bool)

def vibrate():
    sendVibration()
    toggleVibrationButtons(False)
    window["vibrate"].update(visible=False)
    window["text"].update("Vibrating...")
    window.refresh()
    time.sleep(1)
    window["text"].update("Did you feel vibration appart from the finger vibration?")
    toogleButtons(True)

def getDiff(event, vibration):
    print("event: " + event)
    if(len(vibration)>1):
        isLeft = vibration[2] == "6"
        print(isLeft)
        if(isLeft and event == "l"):
            return 0
        if((not isLeft) and event == "r"):
            return 0
        return 1
    else:
        if(event != "n"):
            return 1
        return 0

def choseVibration(event):
    global vibration
    global totalDifference
    global roundDifference
    input.append(event)
    diff = getDiff(event, vibrations[vibration])
    roundDifference+=diff
    totalDifference+=diff
    difference.append(diff)
    vibration+=1
    if(isRoundEnd()):
        if(round >= maxRounds):
            showEnd()
        else:
            showRoundEnd()
    else:
        vibrate()
        

#Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the ok button
    if event == "START":
        id = values["-ID-"]
        filename = id + ".txt"
        print(id)
        try:
            f = open(filename)
            # Do something with the file
            print("file already exists")
            f.close()
        except IOError:
            if(id):
                window.close()
                window = gui.Window("Prestudy", fingerTest, size=(600,400), finalize=True)
                f = open(filename,"w+")
                f.close()
    if event == "READY":
                window.close()
                window = gui.Window("Prestudy", vibrationTestLayout, size=(600,400), finalize=True)
                f = open(filename, "a")
                startNewRound()
    if event == "d":
            nextRound()
    if event == "end":
            end()
    if event == "l":
        choseVibration(event)
    if event == "n":
        choseVibration(event)
    if event == "u":
        choseVibration(event)
    if event == "r":
        choseVibration(event)
    if event == "vibrate":
        vibrate()
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
    if event == gui.WIN_CLOSED:
        break

end()