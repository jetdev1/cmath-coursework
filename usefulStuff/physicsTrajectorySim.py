#this approach will focus most of the calculations on vector quantities
import math
import matplotlib.pyplot as plt
import time
import sys
import traceback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#create the object shotPut to hold all the constants
#as well as the current state of the projectile

class shotPut:

    #the init function will run when the object is first created
    #variables and constants of the shot put will be defined here
    def __init__(self, launchAngle):
        #launch velocity = 13.72m/s
        #value taken from Ryan Crouser's best throw in 2017 IAAF championships
        self.u = 13.72

        #take gravitational acceleration constant as -9.82m/s^2
        self.gravityAccel = -9.82

        #take radius of men's shot put as 0.065m
        self.radius = 0.065

        #take drag coefficient of shot as 0.5
        self.dragCoeff = 0.07

        #take the density of air at sea level at 15 degrees Celsius as 1.225kg/m^3
        self.airDensity = 1.225

        #create a variable to hold the current velocity value of the shot put
        #at the point where this object is created, set the velocity to its launch velocity
        self.currentVel = 13.72

        #calulate the verticle velocity of the shot at launch put using trigonometric ratios
        #math.sin accepts values only in radians
        self.yVel = self.currentVel * math.sin(math.radians(launchAngle))

        #calulate the horizontal velocity of the shot put at launch using trigonometric ratios
        #math.cos accepts values only in radians
        self.xVel = self.currentVel * math.cos(math.radians(launchAngle))

        #set the mass(kg) of the shot put
        self.mass = 7.26

        #set the launch angle of this instance of the shot shotPut
        self.launchAngle = launchAngle

        #initialise the coordinates of the shot put to t=0
        #coordinates are in meters
        self.y = 2.1
        self.x = 0

        #create blank lists for coordinates to plot trajectory
        self.xCoordinates = []
        self.yCoordinates = []



    #this function calculates the drag of the shot put based on
    #current velocity of the shot put
    def calcDragDecel(self, currentVel):
        #using Newton's drag and taking pi = 3.14159
        self.drag = 0.5 * self.dragCoeff * self.airDensity * 3.14159 * self.radius ** 2 * currentVel ** 2

        #calculate the acceleration caused by drag based on F = ma
        self.dragAccel = - (self.drag / self.mass)

        #return the acceleration value caused by drag
        return self.dragAccel


    #decompose the diagonal motion of the shot put into its horizontal and verticle motion
    #These work in the context of each time interval

    #calculate displacement of shot put along y-axis
    def calcYDisplacement(self, elapsedTime, currentDragAccel):
        #calculate the verticle displacement of the shot put
        self.yDisplacement = self.yVel * elapsedTime + ((self.gravityAccel + currentDragAccel) * elapsedTime**2)/2

        return self.yDisplacement


    #calculate displacement of shot put along y-axis
    def calcXDisplacement(self, elapsedTime, currentDragAccel):
        #calculate the verticle displacement of the shot put
        self.xDisplacement = self.xVel * elapsedTime + ((currentDragAccel) * elapsedTime**2)/2

        return self.xDisplacement

    #update the y coordinates of the shotPut
    def updateYCoordinates(self, displacement):
        self.y += displacement
        #append the new coordinate into the list of coordinates
        self.yCoordinates.append(self.y)

    #update the x coordinates of the shotPut
    def updateXCoordinates(self, displacement):
        self.x += displacement
        #append the new coordinate into the list of coordinates
        self.xCoordinates.append(self.x)

    def updateYvel(self, currentDragAccel, elapsedTime):
        self.yVel += (currentDragAccel + self.gravityAccel) * elapsedTime

    def updateXvel(self, currentDragAccel, elapsedTime):
        self.xVel += currentDragAccel * elapsedTime




#the coordinates of the shot put can be fed into this function to plot out the graph
def plotGraph(xCoordinates, yCoordinates, *args):
    try:
        plt.plot(xCoordinates, yCoordinates, linestyle=args[0])

    except:
        #plot the graph using all the coordinates calculated previously
        plt.plot(xCoordinates, yCoordinates)

    #label the coordinates of the graph
    plt.xlabel("horizontal distance travelled by projectile")
    plt.ylabel("height of projectile")


# outfile: CSV filename; headers: 1D list; plots: 2D list

def writeCSV(outfile, headers, plots):
    with open(outfile, 'w') as outfile:
        # write headers of csv
        for header in headers:
            outfile.write(str(header))
        outfile.write('\n')

        # insert data points
        for plot in plots:
            for field in plot:
                outfile.write(str(field) + ',')

def init():
    try:
        flag = sys.argv[1]
        if str(flag) == '-r':
            try:
                infile = str(sys.argv[2])
                if not infile.endswith('.csv') or infile.endswith('.CSV'):
                    print('The provided filename is not a CSV file.')
                    exit()

            except Exception as err:
                traceback.print_tb(err.__traceback__)
                print('No CSV file path provided!')

            infileCSV = pd.read_csv(infile)
            fig = make_subplots(rows=1, cols=1, subplot_titles=(
            "Trajectory of a shot"
            ))
            fig.add_trace(go.Scattergl(
            x = infileCSV['x'], y = infileCSV['y'],
            name = "Trajectory of shot",
            mode = 'lines'
            ), row=1, col=1)
            fig.update_xaxes(title_text="Horizontal distance", row=1, col=1)
            fig.update_yaxes(title_text="Altitude", row=1, col=1)

            global endTime
            endTime = time.time()
            fig.show()
            return True

    except Exception as err:
        traceback.print_tb(err.__traceback__)
        exit()



#main() houses core logic of the calculations
def main():
    global endTime
    #time interval between each plot
    timeInterval = 0.00001

    #create a blank list of launch angles to be written to to create legend later
    angleList = []
    counter = 0
    plots = []

    #create instances of shotPut of launch angles ranging from 1 to 89
    for angle in range(35, 46):
        shotput = shotPut(angle)

        #append the new angle into the list
        angleList.append(str(angle) + "°")

        ##INSERT LOGIC HERE
        #initialise time value
        t = 0

        #continue loop if shotput has not touched the ground yet
        while shotput.y > 0:
            #calculate the deceleration caused by drag along the y-axis
            YDragDecel = shotput.calcDragDecel(shotput.yVel)

            #update the yVel for the next calculation loop
            shotput.updateYvel(YDragDecel, timeInterval)

            #calculate the deceleration caused by drag along the y-axis
            XDragDecel = shotput.calcDragDecel(shotput.xVel)

            #update the xVel for the next calculation loop
            shotput.updateXvel(XDragDecel, timeInterval)

            #calculate the displacement of the shotPut on the Y axis
            yDisplacement = shotput.calcYDisplacement(timeInterval, YDragDecel)

            #update the Y coordinate of shotPut and append to list of coordinates
            shotput.updateYCoordinates(yDisplacement)

            #display the y coordinate
            #print(shotput.y, end="")

            #calculate the displacement of the shotPut on the X axis
            xDisplacement = shotput.calcXDisplacement(timeInterval, YDragDecel)

            #update the X coordinate of shotPut and append to list of coordinates
            shotput.updateXCoordinates(xDisplacement)

            plot = [angle, shotput.x, shotput.y]
            plots.append(plot)

            #display the x coordinate
            #print(shotput.x, end="")

            #update t value
            t += timeInterval
            counter += 1



        #plot graph for this instance of shotPut
        plotGraph(shotput.xCoordinates, shotput.yCoordinates)

    try:
        writeToCSV = sys.argv[1]
        if writeToCSV == '-c':
            try:
                outfile = str(sys.argv[2])

            except Exception as err:
                traceback.print_tb(err.__traceback__)
                print("No filename provided for dumping data to CSV file.")

            # dump the data into a CSV file
            headers = ['angle of throw', 'x', 'y']
            writeCSV(outfile, headers, plots)
            print('CSV file completed')
        else:
            print('no CSV file created')

    except Exception as err:
        print('No argument for CSV file given')
        traceback.print_tb(err.__traceback__)


    print(counter)
    #plot the ground
    plotGraph([0, 22], [0, 0])

    #Add the ground to the legend
    angleList.append("Ground")

    #plot start point
    plotGraph([0, 0], [0, 8])

    #Add the ground to the legend
    angleList.append("Start")

    #manual dotted line for explanation
    plotGraph([5, 5], [0,7], "dashed")
    plotGraph([0.5, 0.5], [0,7], "dashed")
    plotGraph([0.5, 5], [2.5384, 5.4203], "dashed")
    plotGraph([0.5, 5], [2.5384, 2.5384], "dashed")
    plt.plot(21.1621054228, 0, "ro")

    #Create the legend for the graphs
    plt.legend(angleList, loc="upper right")
    plt.subplots_adjust(left=0.025, bottom=0.05, right=0.99, top=0.99, wspace=None, hspace=None)

    endTime = time.time()
    #displays all graphs that have been plotted
    plt.show()

#call the main() function to start the program
if __name__ == "__main__":
    startTime = time.time()
    plotFromFile = init()
    if plotFromFile:
        print(endTime - startTime)
        exit()
    main()
    print(endTime - startTime)
