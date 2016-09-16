#George Stoica gis Section BB
from tkinter import *
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
import time
import threading

RunFlag = True
called = 0

"""
Manipulate the audio
"""
#read all the audio files
s1 = AudioSegment.from_file('Sounds/Mountain1.wav')
s2 = AudioSegment.from_file('Sounds/Mountain2.wav')
s3 = AudioSegment.from_file('Sounds/Tree1.wav')
s4 = AudioSegment.from_file('Sounds/Tree2.wav')
s5 = AudioSegment.from_file('Sounds/Tree3.wav')
s6 = AudioSegment.from_file('Sounds/LeftRiver.wav')
s7 = AudioSegment.from_file('Sounds/MiddleRiver.wav')
s8 = AudioSegment.from_file('Sounds/RightRiver.wav')
#put them into a list
songList = [s1, s2, s3, s4, s5, s6, s7, s8]
#if the songs segments are less than 7 seconds, keep on adding them in loop
#until they surpass 7 seconds, at which point truncate them all to be exactly
#6.5 seconds long
for i in range(len(songList)):
    song1 = songList[i]
    while len(songList[i]) < 7000:
        songList[i] += song1
    songList[i] = songList[i][:6500]

#Function to make the gain of all the sounds be the same
#taken from: "http://stackoverflow.com/questions/33720395/can-pydub-
#set-the-maximum-minimum-volume/33750619#33750619"
def mathTargetAmplitude(sound, targetAmplitude):
    changeInDBFS = abs(targetAmplitude - sound.dBFS)
    return sound.apply_gain(changeInDBFS)

#adjust max gain for all songs
for i in range(len(songList)):
    songList[i] = mathTargetAmplitude(songList[i], -20)

#Exports all the manipulated sound files into new sound files
songList[0].export('Sounds/newMountain1.wav', format='wav')
songList[1].export('Sounds/newMoutain2.wav', format='wav')
songList[2].export('Sounds/newTree1.wav', format='wav')
songList[3].export('Sounds/newTree2.wav', format='wav')
songList[4].export('Sounds/newTree3.wav', format='wav')
songList[5].export('Sounds/newRiverL.wav', format='wav')
songList[6].export('Sounds/newRiverM.wav', format='wav')
songList[7].export('Sounds/newRiverR.wav', format='wav')

"""
Creating the Mountain Class
"""
#defines the mountain class

#taken from the course notes.
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)


class Mountain(object):
    def __init__(self, x, y, r):
        self.x, self.y, self.r = x, y, r
        #base is twice the size of the radius
        self.baseLength = self. r + self.r
        #height is four times the size of the radius
        self.height = self.baseLength + self.baseLength
        self.yMin, self.yMax = self.y + self.height//2, self.y - self.height//2
        #initialize the "bottom or base" of rectangle. First bottom right, 
        #then bottom left
        self.xBL, self.yBL = self.x-3*self.baseLength//4, self.y+self.height//2
        self.xBR, self.yBR = self.x+9*self.baseLength//10, self.y+self.height//2
        #add more to the base
        self.xB0, self.yB0 = self.xBL - self.r/4, self.yBL + self.r/4
        self.xB1, self.yB1 = self.x, self.yBL
        self.xB2, self.yB2 = self.xBR - self.r/4, self.yBR + self.r * 3/16
        #initialize the top of the "hitbox" also equals the 
        #center of the rectangle
        self.xT, self.yT = self.x, self.y
        #initialize the next four peak/trough points
        self.x0, self.y0 = self.x - self.r // 3 * 2, self.y - self.r // 3 * 2
        self.x1, self.y1 = self.x - self.r //3 , self.y - self.r // 5 * 4
        self.x2, self.y2 = self.x + self.r // 3, self.y - self.height // 2
        self.x3, self.y3 = self.x + self.r // 3 * 2, self.y - self.r
        #put the peak/troughs in an animation list
        self.PTCoords = ([[self.x0, self.y0], [self.x1, self.y1], 
            [self.x2, self.y2], [self.x3, self.y3]])
        #print(self.PTCoords)
        #print(self.yT)
        self.count = 0
        #specify if it's clicked
        self.clicked = False
        def rgbString(red, green, blue):
            return "#%02x%02x%02x" % (red, green, blue)
        self.color = rgbString(96, 0, 0)
        #originial color to revert back to once mouse is moved out of the object
        self.origColor = rgbString(96, 0, 0)
        self.p0Dir = 1
        self.p1Dir = 1
        self.p2Dir = 1
        self.p3Dir = 1
        self.p4Dir = 1
        self.p0Speed = 5
        self.p1Speed = 3
        self.p2Speed = 5
        self.p3Speed = 6
    
    #draws the mountain
    def draw(self, canvas):
        def rgbString(red, green, blue):
            return "#%02x%02x%02x" % (red, green, blue)
        
        # canvas.create_polygon(self.xBL, self.yBL, self.xB0, self.yB0, 
        #     self.xB1, self.yB1, self.xB2, self.yB2, self.xBR, self.yBR, 
        #     fill=rgbString(39, 27, 12))
        #draw hitbox
        #canvas.create_polygon(self.xBL, self.yBL, self.xT, 
         #   self.yT, self.xBR, self.yBR, fill="green")
        canvas.create_polygon(self.xBL, self.yBL, self.xB0, self.yB0, 
            self.xB1, self.yB1, self.xB2, self.yB2, self.xBR, self.yBR, 
            fill=rgbString(39, 27, 12))
        #I used poly art to draw my objects, which means drawing the mountains
        #with different polygons and shading them in different ways. 
        #My mountains have five such regions, outlined below.
        #Region 1
        canvas.create_polygon(self.PTCoords[1][0], self.PTCoords[1][1], 
            self.PTCoords[2][0], self.PTCoords[2][1], self.xT, self.yT, 
            fill=rgbString(207, 159, 99))
        #Region 2
        canvas.create_polygon(self.PTCoords[0][0], self.PTCoords[0][1], 
            self.xBL, self.yBL, self.xT, self.yT, fill=rgbString(201, 146, 80))
        #Region 3
        canvas.create_polygon(self.PTCoords[0][0], self.PTCoords[0][1], 
            self.PTCoords[1][0], self.PTCoords[1][1], self.xT, self.yT, 
            fill=rgbString(117, 81, 36))
        #Region 4
        canvas.create_polygon(self.PTCoords[2][0], self.PTCoords[2][1], 
            self.xT, self.yT, self.xBR, self.yBR, self.PTCoords[3][0], 
            self.PTCoords[3][1], fill=rgbString(58, 40, 18))
        #Region 5 51, 25, 0
        canvas.create_polygon(self.xBL, self.yBL, self.xT, self.yT, 
            self.xBR, self.yBR, fill=rgbString(39, 27, 12))

    #checks to see if the mouse pressed is within a certain boundary
    def containsPoint(self, pointX, pointY):
        slopeLeft = abs(self.yBL - self.yT)//abs(self.xBL - self.xT)
        slopeRight = abs(self.yBR - self.yT)//abs(self.xBR - self.xT)
        if pointX >= self.xBL and pointX <= self.xT:
            if pointY >= self.yBL - slopeLeft * abs(pointX - self.xBL):
                if pointY <= self.yBL:
                    return True
        elif pointX >= self.xT and pointX <= self.xBR:
            if pointY >= self.yBR - slopeRight * abs(self.xBR - pointX): 
                if pointY <= self.yBL:
                    return True
        else:
            return False

    #Timer Fired animates the mountain. 
    #There are four helper functions:
    #The four helper function move four vertices of my mountain object up and
    #down at different length and speeds, giving it a soothing effect.
    def onTimerFired(self):
        if self.clicked:
            self.moveP0()
            self.moveP1()
            self.moveP2()
            self.moveP3()

    #mvoes the first point
    def moveP0(self):
        if self.p0Dir == 1:
            #moving Up!
            self.PTCoords[0][1] -= self.p0Speed
            if self.PTCoords[0][1] <= self.y1:
                self.p0Dir = 0
                self.PTCoords[0][1] -= self.p0Speed
        elif self.p0Dir == 0:
            #moving Down!
            self.PTCoords[0][1] += self.p0Speed
            if self.PTCoords[0][1] >= self.yT:
                self.p0Dir = 1
                self.PTCoords[0][1] -= self.p0Speed

    #moves the second point
    def moveP1(self):
        if self.p1Dir == 1:
            #moving Up!
            self.PTCoords[1][1] -= self.p1Speed
            if self.PTCoords[1][1] <= (self.y1 + self.y2)/2:
                self.p1Dir = 0
                self.PTCoords[1][1] -= self.p1Speed
        elif self.p1Dir == 0:
            #moving Down!
            self.PTCoords[1][1] += self.p1Speed
            if self.PTCoords[1][1] >= self.y1:
                self.p1Dir = 1
                self.PTCoords[1][1] -= self.p1Speed

    #moves the third point
    def moveP2(self):
        if self.p2Dir == 1:
                #moving Up!
            self.PTCoords[2][1] -= self.p2Speed
            if self.PTCoords[2][1] <= self.y2 - 20:
                self.p2Dir = 0
                self.PTCoords[2][1] -= self.p2Speed
        elif self.p2Dir == 0:
            #moving Down!
            self.PTCoords[2][1] += self.p2Speed
            if self.PTCoords[2][1] >= (self.y1 + self.y2)/2:
                self.p2Dir = 1
                self.PTCoords[2][1] -= self.p2Speed

    #moves the fourth point
    def moveP3(self):
        if self.p3Dir == 1:
            #moving Up!
            self.PTCoords[3][1] -= self.p3Speed
            if self.PTCoords[3][1] <= self.x1:
                self.p3Dir = 0
                self.PTCoords[3][1] -= self.p3Speed
        elif self.p3Dir == 0:
            #moving Down!
            self.PTCoords[3][1] += self.p3Speed
            if self.PTCoords[3][1] >= self.y:
                self.p3Dir = 1
                self.PTCoords[3][1] -= self.p3Speed


"""
Creating the Tree Class
"""

class Tree(object):
    def __init__(self, x, y, r):
        self.x, self.y, self.r = x, y, r
        #define the trunk
        self.xTL, self.yTL = self.x - self.r/3, self.y - self.r
        self.xTR, self.yTR = self.x + self.r/3, self.y - self.r
        self.xBL, self.yBL = self.x - self.r/3, self.y + self.r * 2
        self.xBR, self.yBR = self.x + self.r/3, self.y + self.r * 2
        self.color = rgbString(96, 0, 0)
        self.origColor = rgbString(96, 0, 0)
        self.count = 0
        self.clicked = False
        #Here I define the parts of my tree
        self.bottomThird()
        self.middleThird()
        self.topThird()

    #defines the first third
    def bottomThird(self):
        self.bttX, self.bttY = self.x, self.y 
        self.btR = [[self.x + self.r/6, self.y + self.r/4], 
                    [self.x + self.r/3, self.y], 
                    [self.x + self.r, self.y + self.r * 3/2],
                    [self.x + self.r/2, self.y + self.r * 7/6],
                    [self.x + self.r/3, self.y + self.r * 3/2]]
        self.btbX, self.btbY = self.x, self.y + self.r
        #Left side of the first third!
        self.btL = [[self.x - self.r/3, self.y + self.r * 3/2],
                    [self.x - self.r/2, self.y + self.r * 7/6],
                    [self.x - self.r, self.y + self.r * 3/2],
                    [self.x - self.r/3, self.y],
                    [self.x - self.r/6, self.y + self.r/4]]

    #define the middle third of the tree!
    def middleThird(self):
        self.mttX, self.mttY = self.x, self.y - self.r
        #shove the right part into a list
        self.mtR = [[self.x + self.r/12, self.y - self.r *6/5],
                    [self.x + self.r/3, self.y - self.r *6/5],
                    [self.x + self.r *5/6, self.y + self.r/3],
                    [self.x + self.r/3, self.y], 
                    [self.x + self.r/6, self.y + self.r/4]]
        self.mtbX, self.mtbY = self.x, self.y
        self.mtL = [[self.x - self.r/6, self.y + self.r/4],
                    [self.x - self.r/3, self.y],
                    [self.x - self.r *5/6, self.y + self.r/3],
                    [self.x - self.r/3, self.y - self.r *6/5],
                    [self.x - self.r/12, self.y - self.r *6/5]]

    #define the top 
    def topThird(self):
        self.tttX, self.tttY = self.x, self.y - self.r * 2
        self.ttR = [[self.x + self.r/2, self.y - self.r * 10/9],
                    [self.x + self.r/3, self.y - self.r * 6/5],
                    [self.x + self.r/12, self.y - self.r * 6/5]]
        self.ttbX, self.ttbY = self.x, self.y - self.r
        self.ttL = [[self.x - self.r/12, self.y - self.r * 6/5],
                    [self.x - self.r/3, self.y - self.r * 6/5],
                    [self.x - self.r/2, self.y - self.r * 10/9]]

    def draw(self, canvas):
        #draws the trunk
        self.drawTrunk(canvas)
        #draws the right side of the tree leaves
        self.drawRight(canvas)
        #draws the middle of the tree leaves
        self.drawMiddle(canvas)
        #draws the left of the tree leaves
        self.drawLeft(canvas)

    def drawTrunk(self, canvas):
        canvas.create_rectangle(self.xTL + self.r/5, self.yTL,
            self.xBR - self.r/5, self.yBR, fill=rgbString(77, 51, 0), width=0)
        canvas.create_polygon(self.xBL+self.r/5, self.yBL, self.xBR-self.r/5, 
            self.yBR, self.x + self.r/30, self.yBR + self.r *1/10, 
            self.x - self.r/30, self.yBR + self.r * 1/10, 
            fill=rgbString(77, 51, 0), width=0)

    def drawRight(self, canvas):
        #draw Top Right Third
        canvas.create_polygon(self.tttX, self.tttY, 
            self.ttR[0][0], self.ttR[0][1], self.ttR[1][0], self.ttR[1][1],
            self.ttR[2][0], self.ttR[2][1], fill=rgbString(0, 51, 0), width=0)
        #draw Middle Right Third
        canvas.create_polygon(self.mtR[0][0], self.mtR[0][1], 
            self.mtR[1][0], self.mtR[1][1],self.mtR[2][0], self.mtR[2][1], 
            self.mtR[3][0], self.mtR[3][1], self.mtR[4][0], self.mtR[4][1],
            fill=rgbString(0, 26, 0), width=0)
        #draw Bottom Right Third
        canvas.create_polygon(self.btR[0][0], self.btR[0][1], 
            self.btR[1][0], self.btR[1][1], self.btR[2][0], self.btR[2][1], 
            self.btR[3][0], self.btR[3][1],self.btR[4][0], self.btR[4][1],
            fill=rgbString(0, 10, 0), width=0)

    def drawMiddle(self, canvas):
        #draw Top Middle Third
        canvas.create_polygon(self.tttX, self.tttY, 
            self.ttR[2][0], self.ttR[2][1], self.ttbX, self.ttbY, 
            self.ttL[0][0], self.ttL[0][1], fill=rgbString(0, 128, 0), width=0)
        #draw Middle Middle Third
        canvas.create_polygon(self.ttbX, self.ttbY, 
            self.ttR[2][0], self.ttR[2][1], self.mtR[4][0], self.mtR[4][1],
            self.mtbX, self.mtbY, self.mtL[0][0], self.mtL[0][1],
            self.ttL[0][0], self.ttL[0][1], fill=rgbString(0, 102, 0), width=0)
        #draw Middle Bottom Third
        canvas.create_polygon(self.mtbX, self.mtbY, 
            self.mtR[4][0], self.mtR[4][1], self.btR[4][0], self.btR[4][1],
            self.btbX, self.btbY, self.btL[0][0], self.btL[0][1],
            self.btL[4][0], self.btL[4][1], fil=rgbString(0, 77, 0), width=0)

    def drawLeft(self, canvas):
        #draw Top Right Third
        canvas.create_polygon(self.tttX, self.tttY, 
            self.ttL[0][0], self.ttL[0][1], self.ttL[1][0], self.ttL[1][1],
            self.ttL[2][0], self.ttL[2][1], fill=rgbString(0, 204, 0), width=0)
        #draw Middle Right Third
        canvas.create_polygon(self.mtL[0][0], self.mtL[0][1], self.mtL[1][0], 
            self.mtL[1][1], self.mtL[2][0], self.mtL[2][1], self.mtL[3][0], 
            self.mtL[3][1], self.mtL[4][0], self.mtL[4][1], 
            fill=rgbString(0, 179, 0), width=0)
        #draw Bottom Right Third
        canvas.create_polygon(self.btL[0][0], self.btL[0][1], self.btL[1][0], 
            self.btL[1][1], self.btL[2][0], self.btL[2][1], self.btL[3][0], 
            self.btL[3][1], self.btL[4][0], self.btL[4][1], 
            fill=rgbString(0, 153, 0), width=0)

    def onTimerFired(self):
        if self.clicked:
            if self.count < 5:
                #calles helper function that moves the trees right if count is
                #less than 5
                self.timerFiredLessThan5()
            elif self.count < 10:
                #calls helper function that moves the trees left if count is
                #greater than 5
                self.timerFiredGreaterThan5()
            else:
                #sets the count back to 0
                 self.count = 0

    def timerFiredLessThan5(self):
        for i in range(len(self.btR)):
            self.btR[i][0] += 2
            self.btR[i][1] += 2
            self.btL[i][0] += 2
            self.btL[i][1] += 2
            self.mtL[i][0] += 2
            self.mtL[i][1] += 2
            self.mtR[i][0] += 2
            self.mtR[i][1] += 2
        for i in range(len(self.ttR)):
            self.ttR[i][0] += 2
            self.ttR[i][1] += 2
            self.ttL[i][0] += 2
            self.ttL[i][1] += 2
        self.count += 1

    def timerFiredGreaterThan5(self):
        for i in range(len(self.btR)):
            self.btR[i][0] -= 2
            self.btR[i][1] -= 2
            self.btL[i][0] -= 2
            self.btL[i][1] -= 2
            self.mtL[i][0] -= 2
            self.mtL[i][1] -= 2
            self.mtR[i][0] -= 2
            self.mtR[i][1] -= 2
        for i in range(len(self.ttR)):
            self.ttR[i][0] -= 2
            self.ttR[i][1] -= 2
            self.ttL[i][0] -= 2
            self.ttL[i][1] -= 2
        self.count += 1

    def containsPoint(self, x, y):
        if x >= self.xBL - self.r/3 and x <= self.xBR + self.r/3:
            if y >= self.yTL - self.r/3 and y <= self.yBR + self.r/3:
                return True
        return False

"""
Calculating the River Classes
"""
class LeftRiver(object):
    def __init__(self, x, y, r):
        self.x, self.y, self.r = x, y, r
        self.x0, self.y0 = self.x, self.y
        self.x1, self.y1 = self.x + self.r*3/4, self.y
        self.x2, self.y2 = self.x + 2 * self.r, self.y + self.r/4
        self.x3, self.y3 = self.x + self.r * 9/4, self.y + self.r
        self.x4, self.y4 = 1280//3, self.y + self.r * 2
        self.x5, self.y5 = 1280//3, 800
        self.x6, self.y6 = self.x + self.r * 2, self.y + self.r * 2
        self.x7, self.y7 = self.x + self.r *3/4, self.y + self.r/2   
        self.clicked = False
        #there are 4 sets of animation points.
        #Set 1
        self.set1 = [[1280//12, 49900/117], [1280//12, 49900/117]]
        #Set 2
        self.set2 = [[1280//6, 20200/39 - 70], [1280//6, 20200/39 + 70]]
        #Set 3
        self.set3 = [[1280//4, 71300/117 - 5], [1280//4, 71300/117 + 5]]
        #Set 4
        self.set4 = [[1280//3 - 20, 700], [1280//3 - 20, 700]]
        self.speed1 = 2
        self.speed2 = 4
        self.speed3 = 6
        self.speed4 = 8
        self.dir1 = 0
        self.dir2 = 1
        self.dir3 = 0
        self.dir4 = 1

    #draws the river
    def draw(self, canvas):
        canvas.create_polygon(self.x0, self.y0, self.x1, self.y1,
            self.x2, self.y2, self.x4, self.y4, 
            self.x5, self.y5, self.x6, self.y6, self.x7, self.y7, 
            fill=rgbString(179, 240, 255))
        canvas.create_polygon(self.set1[0][0], self.set1[0][1], self.set2[0][0],
            self.set2[0][1], self.set2[1][0], self.set2[1][1], self.set1[1][0],
            self.set1[1][1], fill=rgbString(153, 221, 255), width=0)
        canvas.create_polygon(self.set2[0][0], self.set2[0][1], self.set3[0][0],
            self.set3[0][1], self.set3[1][0], self.set3[1][1], self.set2[1][0],
            self.set2[1][1], fill=rgbString(153, 221, 255), width=0)
        canvas.create_polygon(self.set3[0][0], self.set3[0][1], self.set4[0][0],
            self.set4[0][1], self.set4[1][0], self.set4[1][1], self.set3[1][0],
            self.set3[1][1], fill=rgbString(153, 221, 255), width=0)

    #defines the region over which points are contained. 
    #Works over the whole river
    def containsPoint(self, x, y):
        # 3 cases
        #First:
        if self.x2 <= x and x <= self.x4:
            yA = (self.y4 - self.y2)/(self.x4 - self.x2)*(x-self.x2) + self.y2
            yB = (self.y5 - self.y6)/(self.x5 - self.x6)*(x-self.x6) + self.y6
            if yA <= y and y <= yB:
                #self.clicked = True
                return True
        #Second:
        elif self.x1 <= x and x <= self.x2:
            yA = (self.y2 - self.y1)/(self.x2 - self.x1)*(x - self.x1) + self.y1
            yB = (self.y6 - self.y7)/(self.x6 - self.x7)*(x - self.x6) + self.y6
            if yA <= y and y <= yB:
                return True
        elif self.x0 <= x and x <= self.x1:
            yA = self.y0
            yB = (self.y7 - self.y0)/(self.x7 - self.x0)*(x - self.x0) + self.y0
            if yA <= y and y <= yB:
                return True
        return False


    def onTimerFired(self):
        if self.clicked == True:
            #performs the animation of the river
            #moves three sets of points in different directions
            #to make different polygons
            self.doDir1()
            self.doDir2()
            self.doDir3()

    def doDir1(self):
        if self.dir1 == 0:
            #going out
            self.set1[0][1] -= self.speed1
            self.set1[1][1] += self.speed1
            if self.set1[0][1] <= 49900/117 - 15:
                self.dir1 = 1
        elif self.dir1 == 1:
            #going in
            self.set1[0][1] += self.speed1
            self.set1[1][1] -= self.speed1
            if self.set1[0][1] >= 49900/117:
                self.dir1 = 0

    def doDir2(self):
        if self.dir2 == 0:
            #going out
            self.set2[0][1] -= self.speed2
            self.set2[1][1] += self.speed2
            if self.set2[0][1] <= 20200/39 - 50:
                self.dir2 = 1
        elif self.dir2 == 1:
            #going in
            self.set2[0][1] += self.speed2
            self.set2[1][1] -= self.speed2
            if self.set2[0][1] >= 20200/39:
                self.dir2 = 0

    def doDir3(self):
        if self.dir3 == 0:
            #going out
            self.set3[0][1] -= self.speed3
            self.set3[1][1] += self.speed3
            if self.set3[0][1] <= 71300/117 - 80:
                self.dir3 = 1
        elif self.dir3 == 1:
            #going in
            self.set3[0][1] += self.speed3
            self.set3[1][1] -= self.speed3
            if self.set3[0][1] >= 71300/117 - 10:
                self.dir3 = 0

class MiddleRiver(object):
    def __init__(self, x, y, r):
        self.x , self.y, self.r = x, y, r
        self.x0, self.y0 = self.x, self.y
        self.x1, self.y1 = 731, 400
        self.x2, self.y2 = 639, 510
        self.x3, self.y3 = 426, self.y + self.r * 2
        self.x4, self.y4 = 426, 800
        self.x5, self.y5 = 640, 800
        self.x6, self.y6 = 640, 400 + 700/3
        #5 sets
        self.set1 = [[731, 400 + 400/6], [731, 400 + 400/6]]
        self.set2 = [[670, 400 + 400/3 - 40], [670, 400 + 400/3 + 40]]
        self.set3 = [[609, 600], [609, 600]]
        self.set4 = [[548, 400 + 800/3 - 90], [548, 400 + 800/3 + 90]]
        self.set5 = [[487, 400 + 2000/6], [487, 400 + 2000/6]]
        self.speed1 = 2
        self.speed2 = 4
        self.speed3 = 6
        self.speed4 = 8
        self.dir1 = 0
        self.dir2 = 1
        self.dir3 = 0
        self.dir4 = 1
        self.clicked = False

    def onTimerFired(self):
        if self.clicked == True:
            #changes the position of the animation points to generate shifting
            #images
            self.doDir1()
            self.doDir2()
            self.doDir3()
            self.doDir4()

    def doDir1(self):
        if self.dir1 == 0:
            #going out
            self.set1[0][1] -= self.speed1
            self.set1[1][1] += self.speed1
            if self.set1[0][1] <= 400 + 400/6 - 10:
                self.dir1 = 1
        elif self.dir1 == 1:
            #going in
            self.set1[0][1] += self.speed1
            self.set1[1][1] -= self.speed1
            if self.set1[0][1] >= 400 + 400/6:
                self.dir1 = 0

    def doDir2(self):
        if self.dir2 == 0:
            #going out
            self.set2[0][1] -= self.speed2
            self.set2[1][1] += self.speed2
            if self.set2[0][1] <= 400 + 400/3 - 40:
                self.dir2 = 1
        elif self.dir2 == 1:
            #going in
            self.set2[0][1] += self.speed2
            self.set2[1][1] -= self.speed2
            if self.set2[0][1] >= 400 + 400/3:
                self.dir2 = 0

    def doDir3(self):
        if self.dir3 == 0:
            #going out
            self.set3[0][1] -= self.speed3
            self.set3[1][1] += self.speed3
            if self.set3[0][1] <= 600 - 70:
                self.dir3 = 1
        elif self.dir3 == 1:
            #going in
            self.set3[0][1] += self.speed3
            self.set3[1][1] -= self.speed3
            if self.set3[0][1] >= 600 - 10:
                self.dir3 = 0

    def doDir4(self):
        if self.dir4 == 0:
            #going out
            self.set4[0][1] -= self.speed4
            self.set4[1][1] += self.speed4
            if self.set4[0][1] <= 400 + 800/3 - 90:
                self.dir4 = 1
        elif self.dir4 == 1:
            #going in
            self.set4[0][1] += self.speed4
            self.set4[1][1] -= self.speed4
            if self.set4[0][1] >= 400 + 800/3 - 10:
                self.dir4 = 0

    #draws the river
    def draw(self, canvas):
        canvas.create_polygon(self.x0, self.y0, self.x1, self.y1, 
            self.x2, self.y2, self.x3, self.y3, 
            self.x4, self.y4, self.x5, self.y5, 
            self.x6, self.y6,
            fill=rgbString(179, 240, 255))
        #Draws the animation polygons
        #Drawing 2 polygons
        canvas.create_polygon(self.set1[0][0], self.set1[0][1], self.set2[0][0],
            self.set2[0][1], self.set3[0][0], self.set3[0][1],  self.set3[1][0], 
            self.set3[1][1], self.set2[1][0], self.set2[1][1], self.set1[1][0], 
            self.set1[1][1], fill=rgbString(153, 221, 255), width=0)
        canvas.create_polygon(self.set3[0][0], self.set3[0][1], self.set4[0][0],
            self.set4[0][1], self.set5[0][0], self.set5[0][1], self.set4[1][0],
            self.set4[1][1], self.set3[1][0], self.set3[1][1], 
            fill=rgbString(153, 221, 255), width=0)

    def containsPoint(self, x, y): 
        if self.x3 <= x and x <= self.x2:
            yA = (self.y3 - self.y2)/(self.x3 - self.x2)*(x - self.x2) + self.y2
            yB = 800
            if yA <= y and y <= yB:
                return True
        elif self.x2 <= x and x <= self.x0:
            yA = (self.y2 - self.y1)/(self.x2 - self.x1)*(x - self.x1) + self.y1
            yB = (self.y6 - self.y0)/(self.x6 - self.x0)*(x - self.x0) + self.y0
            if yA <= y and y <= yB and 400 <= y:
                return True
        return False


class RightRiver(object):
    def __init__(self, x, y, r):
        self.x, self.y, self.r = x, y, r
        self.x0, self.y0 = self.x, self.y
        self.x1, self.y1 = 1240, 400
        self.x2, self.y2 = 914, 700
        self.x3, self.y3 = 640, 400 + 1000/3
        self.x4, self.y4 = 640, 800
        self.x5, self.y5 = 1280, 800
        #need 3 sets
        self.set1 = [[1186.667, 400 + 400/3], [1186.667, 400 + 400/3]]
        self.set2 = [[1093.337, 400 + 800/3 - 70], [1093.337, 400+800/3 + 70]]
        self.set3 = [[1000, 800], [1000, 800]]
        self.speed1 = 2
        self.speed2 = 4
        self.dir1 = 0
        self.dir2 = 1
        self.clicked = False

    #animates the rivers
    def onTimerFired(self):
        if self.clicked == True:
            if self.dir1 == 0:
                #going out
                self.set1[0][1] -= self.speed1
                self.set1[1][1] += self.speed1
                if self.set1[0][1] <= 400 + 400/3 - 20:
                    self.dir1 = 1
            elif self.dir1 == 1:
                #going in
                self.set1[0][1] += self.speed1
                self.set1[1][1] -= self.speed1
                if self.set1[0][1] >= 400 + 400/3 - 5:
                    self.dir1 = 0

            if self.dir2 == 0:
                #going out
                self.set2[0][1] -= self.speed2
                self.set2[1][1] += self.speed2
                if self.set2[0][1] <= 400 + 800/3 - 90:
                    self.dir2 = 1
            elif self.dir2 == 1:
                #going in
                self.set2[0][1] += self.speed2
                self.set2[1][1] -= self.speed2
                if self.set2[0][1] >= 400 + 800/3 - 10:
                    self.dir2 = 0

    #draws the river
    def draw(self, canvas):
        canvas.create_polygon(self.x0, self.y0, self.x1, self.y1, 
            self.x2, self.y2, self.x3, self.y3, self.x4, self.y4, 
            self.x5, self.y5, fill=rgbString(179, 240, 255))
        canvas.create_polygon(self.set1[0][0], self.set1[0][1], self.set2[0][0],
            self.set2[0][1], self.set3[0][0], self.set3[0][1], self.set3[1][0],
            self.set3[1][1], self.set2[1][0], self.set2[1][1], self.set1[1][0],
            self.set1[1][1], fill=rgbString(153, 221, 255), width=0)


    def containsPoint(self, x, y):
        if self.x3 <= x and x <= self.x2:
            yA = (self.y3 - self.y2)/(self.x3 - self.x2)*(x - self.x2) + self.y2
            yB = 800
            if yA <= y and y <= yB:
                return True
        elif self.x2 <= x and x <= self.x0:
            yA = (self.y2 - self.y1)/(self.x2 - self.x1)*(x - self.x1) + self.y1
            if yA <= y and 400 <= y:
                return True
        return False

#creates a Sun object, who's purpose is to stop all the sounds from playing
class Sun(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.cR, self.cG, self.cB = 230, 185, 0

    def draw(self, canvas):
        for i in range(50):
            canvas.create_oval(self.x - self.r*(50-i)/50, 
                self.y - self.r *(50-i)/50, 
                self.x + self.r*(50-i)/50, 
                self.y + self.r*(50-i)/50, 
                fill=rgbString(self.cR, self.cG + 1*i, self.cB + i*2), width=0)

    def containsPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y -y)**2)**.5
        return d <= self.r

    def onTimerFired(self): pass


class PlaySongThread (threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data
    def run(self):
        soundPlay(self.data)

def soundPlay(data):
    CHUNK = 1024
    global RunFlag
    while (RunFlag):

        song = data.wf.readframes(CHUNK)
        # draw in canvas
        while len(song) > 0:
            data.stream.write(song)
            song = data.wf.readframes(CHUNK)
        # check whether we need to update the song-mix    
        if (data.songUpdate):
            #print("here")
            data.songUpdate = False
            data.wf = data.new_wf
            data.stream = data.new_stream    
        data.wf.rewind()

class updateSongThread (threading.Thread):
    def __init__(self, data, delay):
        threading.Thread.__init__(self)
        # The function will sleep for a specified delay
        self.delay = delay  
        # data: contains all song related info
        self.data = data
    def run(self):
        global RunFlag
        while (RunFlag):
            # sleep for "delay"
            time.sleep(self.delay)
            if (self.data.selectionUpdate):
                updateSongMix(self.data)

class updateCanvasThread (threading.Thread):
    def __init__(self, canvas, data, delay):
        threading.Thread.__init__(self)
        self.canvas = canvas 
        self.data = data
        self.delay = delay
    def run(self):
        global RunFlag
        while (RunFlag):
            time.sleep(self.delay)
            updateCanvas(self.canvas, self.data)

def toggleSong(data, idx):
    data.songSelected[idx] = not data.songSelected[idx]
    data.selectionUpdate = True

def updateSongMix(data):
    if (not data.selectionUpdate):
        return
    data.selectionUpdate = False
    song = AudioSegment.silent(duration=6500)
    for i in range(len(data.songName)):
        if data.songSelected[i]:
            #print("ovrelayd song name : ", data.songName[i])
            song = song.overlay(data.songName[i])
    song.export('Sounds/newSound.wav', format='wav')
    data.new_wf = wave.open('Sounds/newSound.wav', 'rb')
    data.new_stream = data.p.open(
                format=data.p.get_format_from_width(data.new_wf.getsampwidth()),
                channels=data.new_wf.getnchannels(),
                rate=data.new_wf.getframerate(),
                output=True)

    data.songUpdate = True

def init(data):
    #initialize pyaudio
    data.p = pyaudio.PyAudio()
    #import all the songs
    data.songName = ([AudioSegment.from_file('Sounds/newRiverL.wav'),
                      AudioSegment.from_file('Sounds/newRiverM.wav'),
                      AudioSegment.from_file('Sounds/newRiverR.wav'),
                      AudioSegment.from_file('Sounds/newTree1.wav'),
                      AudioSegment.from_file('Sounds/newTree2.wav'),
                      AudioSegment.from_file('Sounds/newTree3.wav'),
                      AudioSegment.from_file('Sounds/newMountain1.wav'),
                      AudioSegment.from_file('Sounds/newMoutain2.wav')])
    
    data.objects = [LeftRiver(0, 400, 100), MiddleRiver(792, 400, 100),
                    RightRiver(1280, 400, 100), Tree(435, 500, 40), 
                    Tree(320, 430, 30), Tree(570, 400, 20), 
                    Mountain(970, 190, 120), Mountain(840, 380, 100),
                     Sun(50, 60, 100)]

    #assign is on/off on list
    data.songSelected = [False, False, False, False, False, False, False, False, 
                         False]
    data.selectionUpdate = True
    data.songUpdate = False
    #toggleSong(data, 0)
    updateSongMix(data)
    data.wf = data.new_wf
    data.stream = data.new_stream
    data.songUpdate = False
    #Initialize the mountain objects
    data.on = False
    data.startScreen = False
    #Sky Gradient
    data.rgbR, data.rgbG, data.rgbB = 229, 246, 255
    #Ground Gradient
    data.rgbR1, data.rgbG1, data.rgbB1 = 155, 255, 51
    initStartScreen(data)
    data.startScreen = "Start"
    initIntroScreen(data)

#initializes the start screen
def initStartScreen(data):
    #These 20 points are calculated to draw the river in my initial start screen
    #the river is curvy.
    data.rX0, data.rY0 = 900, 400
    data.rX1, data.rY1 = 800, 400
    data.rX2, data.rY2 = 750, 425
    data.rX3, data.rY3 = 700, 435
    data.rX4, data.rY4 = 600, 450
    data.rX5, data.rY5 = 550, 465
    data.rX6, data.rY6 = 500, 500
    data.rX7, data.rY7 = 510, 520
    data.rX8, data.rY8 = 525, 550
    data.rX9, data.rY9 = 550, 700
    data.rX10, data.rY10 = 575, 750
    data.rX11, data.rY11 = 590, 790
    data.rX12, data.rY12 = 600, 800
    data.rX13, data.rY13 = 1100, 800
    data.rX14, data.rY14 = 1000, 720
    data.rX15, data.rY15 = 900, 650
    data.rX16, data.rY16 = 800, 575
    data.rX17, data.rY17 = 700, 500
    data.rX18, data.rY18 = 750, 480
    data.rX19, data.rY19 = 850, 460
    data.rX20, data.rY20 = 1150, 400
    data.color = rgbString(153, 221, 255)
    #creates the starting objects/scenery around the river
    data.startObjects =[Mountain(1110, 400, 110), Mountain(970, 280, 115), 
    Mountain(1150, 150, 150), Tree(420, 600, 60), Tree(120, 580, 50), 
    Tree(250, 490, 40), Tree(500, 410, 35)]

def initIntroScreen(data):
    #draw the gradient for the sky
    data.rgbRT, data.rgbGT, data.rgbBT = 79, 227, 212
    #draw the gradient for the bottom
    data.rgbRB, data.rgbGB, data.rgbBB = 255, 224, 179
    data.introColor = rgbString(255, 179, 179)

def mousePressed(event, data):
    # use event.x and event.y3
    if data.startScreen =="Start":
        if event.x > 550 and event.x < 980 and event.y > 500 and event.y < 780:
            data.startScreen = "Intro"
    elif data.startScreen == "Intro":
        if event.x > 570 and event.x < 700 and event.y > 680 and event.y < 720:
            data.startScreen = "Play"
    else:
        for i in range(len(data.objects)-1, -1, -1):
            #if the sun is clicked, all the sound stops
            if (isinstance(data.objects[i], Sun) and 
                data.objects[i].containsPoint(event.x, event.y)):
                for j in range(len(data.songSelected)):
                    data.songSelected[j] = False
                data.selectionUpdate = True
                for j in range(len(data.objects)):
                    data.objects[j].clicked = False
            #The sun was not clicked, something else was
            elif data.objects[i].containsPoint(event.x, event.y):
                data.on = True
                data.objects[i].clicked = not data.objects[i].clicked
                toggleSong(data, i)
                if data.on == True:
                    data.on = False
                    break

def updateCanvas(canvas, data):
    canvas.delete(ALL)
    if data.startScreen == "Start":
        drawStartScreen(canvas, data)
    elif data.startScreen == "Intro":
        drawIntroScreen(canvas, data)
    elif data.startScreen == "Play":
        for i in range(100):
            canvas.create_rectangle(0,4*i, 1280, 4*(i+1), 
                fill=rgbString(data.rgbR-2*i, data.rgbG - 1*i, data.rgbB), 
                width=0)
        for i in range(90):
            canvas.create_rectangle(0, 400 + 4*i, 1280, 400+4*(i+1), 
                fill=rgbString(data.rgbR1 -1*i, data.rgbG1-2*i, data.rgbB1), 
                width=0)
        for i in range(len(data.objects)):
            if data.songSelected[i] == True: 
                data.objects[i].onTimerFired()
            data.objects[i].draw(canvas)
        canvas.update()

def drawStartScreen(canvas, data):
    #create the gradients for the sky
    for i in range(100):
            canvas.create_rectangle(0,4*i, 1280, 4*(i+1), 
                fill=rgbString(data.rgbR-2*i, data.rgbG - 1*i, data.rgbB), 
                width=0)
    #create the gradients for the ground
    for i in range(90):
        canvas.create_rectangle(0, 400 + 4*i, 1280, 400+4*(i+1), 
            fill=rgbString(data.rgbR1 -1*i, data.rgbG1-2*i, data.rgbB1), 
            width=0)
    #create the river
    canvas.create_polygon(data.rX0, data.rY0, data.rX1, data.rY1, 
        data.rX2, data.rY2, data.rX3, data.rY3, data.rX4, data.rY4, 
        data.rX5, data.rY5, data.rX6, data.rY6, data.rX7, data.rY7, 
        data.rX8, data.rY8, data.rX9, data.rY9, data.rX10, data.rY10, 
        data.rX11, data.rY11, data.rX12, data.rY12, data.rX13, data.rY13, 
        data.rX14, data.rY14, data.rX15, data.rY15, data.rX16, data.rY16, 
        data.rX17, data.rY17, data.rX18, data.rY18, data.rX19, data.rY19, 
        data.rX20, data.rY20, fill=data.color, width=0)
    #create the scenery objects
    for obj in range(len(data.startObjects)-1, -1, -1):
        data.startObjects[obj].draw(canvas)
    #writing the text
    canvas.create_text(120, 90, text="Light", font="Helvetica 60 bold", 
        fill=rgbString(128, 213, 255))
    canvas.create_text(270, 150, text="Your", font="Helvetica 60 bold", 
        fill=rgbString(255, 213, 153))
    canvas.create_text(420, 220, text="Life", font="Helvetica 60 bold", 
        fill=rgbString(224, 128, 255))
    #intializing the begin "button"
    canvas.create_text(760, 700, text="BEGIN", font="Helvetica 40 bold", 
        fill=rgbString(102, 216, 255))

def drawIntroScreen(canvas, data):
    # draw in canvas
    for i in range(58):
        canvas.create_rectangle(0, 13*i, 1280, 13*i + 13, 
            fill=rgbString(data.rgbRT + 3*i, data.rgbGT, 
                data.rgbBT), width=0)
    canvas.create_text(640, 87, text="Music Mixer Instructions: ", 
        font="Helvetica 50 bold", fill=rgbString(77, 165, 255))
    canvas.create_text(640, 174, text="Make Your Own Music", 
        font="Helvetica 20", fill=rgbString(51, 152, 255))
    canvas.create_text(640, 261, 
        text="Click on Mountains, Rivers and Trees to Generate Sound", 
        font="Helvetica 20" , fill=rgbString(26, 139, 255))
    canvas.create_text(640, 348, 
        text="Click on Multiple Objects to Create Mixes", 
        font="Helvetica 20" , fill=rgbString(0, 126, 255))
    canvas.create_text(640, 431, text="Click the Sun to Stop All Music", 
        font="Helvetica 20", fill=rgbString(0, 113, 230))
    canvas.create_text(640, 518, 
        text="Press I For Instructions or Escape to Go Back", 
        font="Helvetica 20", fill=rgbString(0, 100, 205))
    canvas.create_text(640, 605, text="Have Fun!", font="Helvetica 20" , 
        fill=rgbString(0, 87, 180))
    canvas.create_text(640, 692, text="Proceed", font="Helvetica 30", 
        fill=data.introColor)
    
def mouseMotion(event, data):
    if data.startScreen == "Start":
    #print ("moved", event.x, event.y)
        if event.x > 550 and event.x < 980 and event.y > 500 and event.y < 780:
            data.color = rgbString(77, 210, 255)
        else:
           data.color = rgbString(153, 221, 255)
    elif data.startScreen == "Intro":
        if event.x > 570 and event.x < 700 and event.y > 680 and event.y < 720:
            data.introColor = rgbString(255, 128, 128)
        else:
           data.introColor = rgbString(255, 179, 179)

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "i":
        data.startScreen = "Intro"
    elif event.keysym == "Escape":
        data.startScreen = "Start"
        
def run(width=300, height=300):
    global RunFlag
    def redrrawAllWrapper(canvas, data):
        #only deletes the objects that are currently running
        for i in range(len(data.songSelected)):
            if data.songSelected[i] == True:
                canvas.delete(data.objects[i])
        #canvas.delete(ALL)
        canvas.update()

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)

    def mouseMotionWrapper(event, canvas, data):
        mouseMotion(event, data)

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    init(data)
    threadUpdateSong = updateSongThread(data, .1)
    threadUpdateSong.start()
    threadPlaySong = PlaySongThread(data)
    threadPlaySong.start()

    root = Tk()    
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))

    root.bind("<Motion>", lambda event: mouseMotionWrapper(event, canvas, data))
    threadUpdateCanvas = updateCanvasThread(canvas, data, .05)
    threadUpdateCanvas.start()
    root.mainloop()
    print('bye!')
    RunFlag = False
    time.sleep(10)
run(1280, 800)


















