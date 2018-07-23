import requests
import champList
# import tkinter
from tkinter import*
import json

def init(data):
	data.time = 0

def timerFired(data):
	# print(data.time)
	# data.time+=data.timerDelay
	pass


def redrawAll(canvas,data):
	def call():
		print("wtf")

	b = Button(canvas, text = "click me", command = call)
	b.place(x=0,y=0)
	# print(b.size)


def mousePressed(event,data):
	print(event)
def keyPressed(event,data):
	print(event)
def getChamp(apiKey):
	myChamp = input("choose your champion \n")
	yourChamp = input("choose your enemy chamipon \n")
	with open("data/champion/" + myChamp + ".json") as file:
		data = json.load(file)
	print(data["data"][myChamp]["stats"])
	baseSpeed = 0.625
	stats = data["data"][myChamp]["stats"]
	myASOffset = round(stats["attackspeedoffset"],3)
	myBaseAS = round(baseSpeed/(1+myASOffset),3)
	myASLevel = round(stats["attackspeedperlevel"],3)
	print(myASOffset,myBaseAS,myASLevel)

	

def main():
	apiKey = "RGAPI-1de6f07a-6db2-4f52-a110-1c693c6ec168"
	# summonerName, summonerID, accountID = getInput(apiKey)
	choice = input("what do you want to choose? \n")
	if choice == "1":
		try:
			getMatchHistory(accountID,apiKey)
		except:
			pass
	elif choice == "2":
		getChamp(apiKey)
		run (500,500)

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")






if __name__ == '__main__':
	main()