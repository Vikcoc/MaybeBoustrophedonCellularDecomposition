from turtle import color
import matplotlib.pyplot as plt
import numpy as np

class Map:
    freq = 0.25
    obstacles = []

    @staticmethod
    def __init__():
        plt.figure(figsize=(13, 7))
        #ax = fig.add_subplot(111)
        x = np.arange(-5, 6, 0.5)
        y = np.arange(-10, 11, 1)
        plt.xticks(x)
        plt.yticks(y)
        
    @staticmethod
    def BuildLayout(corners):
        plt.plot([[corners[0][0], corners[1][0]],
                  [corners[1][0], corners[3][0]],
                  [corners[3][0], corners[2][0]],
                  [corners[2][0], corners[0][0]]],
                 [[corners[0][1], corners[1][1]],
                  [corners[1][1], corners[3][1]],
                  [corners[3][1], corners[2][1]],
                  [corners[2][1], corners[0][1]]], color = "Black")
        
    @staticmethod
    def MapPoints(points):
        Map.obstacles = points.copy()
        for i in range(len(points)):
            plt.plot([points[i][0], points[(i+1)%len(points)][0]], [points[i][1], points[(i+1)%len(points)][1]], color = "Red")
        plt.pause(1)

    @staticmethod
    def PlotCells(points):
        plt.plot([points[0][0], points[1][0]],
                 [points[0][1], points[1][1]],
                   color = "Purple")
        plt.plot([points[2][0], points[3][0]],
                 [points[2][1], points[3][1]],
                   color = "Purple")
        for i in np.arange(points[0][0] + Map.freq/2, points[2][0], Map.freq):
            x = i
            y1 = points[0][1] + ((x - points[0][0])*(points[2][1] - points[0][1]))/(points[2][0] - points[0][0])
            y2 = points[1][1] + ((x - points[1][0])*(points[3][1] - points[1][1]))/(points[3][0] - points[1][0])
            plt.plot([x, x],
                    [y1, y2],
                    color = "Green", linestyle = "dashed")
            # plt.plot([x, x],
            #          [points[2][1], points[3][1]],
            #            color = "Green", linestyle = "dashed")
        Map.freq = Map.freq*3/4 
    
    @staticmethod
    def PlotFromCells(pointsList):
        for points in pointsList:
            plt.scatter(points[0][0], points[0][1], color = "purple")
            plt.scatter(points[1][0], points[1][1], color = "purple")
            plt.scatter(points[2][0], points[2][1], color = "purple")
            plt.scatter(points[3][0], points[3][1], color = "purple")
            plt.plot([points[0][0], points[1][0]],
                    [points[0][1], points[1][1]],
                    lw = 3,
                    color = "Purple")
            plt.plot([points[2][0], points[3][0]],
                    [points[2][1], points[3][1]],
                    lw = 2,
                    color = "Purple")
            for i in np.arange(points[0][0] + Map.freq/2, points[2][0], Map.freq):
                x = i
                y1 = points[0][1] + ((x - points[0][0])*(points[2][1] - points[0][1]))/(points[2][0] - points[0][0])
                y2 = points[1][1] + ((x - points[1][0])*(points[3][1] - points[1][1]))/(points[3][0] - points[1][0])
                plt.plot([x, x],
                        [y1, y2],
                        color = "Green", linestyle = "dashed")
                # plt.plot([x, x],
                #          [points[2][1], points[3][1]],
                #            color = "Green", linestyle = "dashed")
            Map.freq = Map.freq*3/4 
            #plt.draw()
            plt.pause(1)

    @staticmethod
    def Show():
        plt.show()
