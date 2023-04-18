import matplotlib.pyplot as plt
import numpy as np
import statistics



def main():
    machine1()
    machine2()
    machine3()

    


def machine1():
    mainPathM1S2 = 'Path to File'
    m1s1 = 'Path to File'
    m1s3 = 'Path to File'
    m1s4 = 'Path to File'
    m1s5 = 'Path to File'
    m1s6 = 'Path to File'
    
    machineDetails('1', mainPathM1S2, m1s1, m1s3, m1s4, m1s5, m1s6)
    

    
    
def machine2():
    mainPathM2S2 = 'Path to File'
    m2s1 = 'Path to File'
    m2s3 = 'Path to File'
    m2s4 = 'Path to File'
    m2s5 = 'Path to File'
    m2s6 = 'Path to File'
    
    machineDetails('2', mainPathM2S2, m2s1, m2s3, m2s4, m2s5, m2s6)
    
    
def machine3():
    mainPathM3S2 = 'Path to File'
    m3s1 = 'Path to File'
    
    machineDetailsM3('3', mainPathM3S2, m3s1)
    





def machineDetails(machineNum, mainMPath, ms1, ms3, ms4, ms5, ms6, spindleNorm='2'):
    mainMCoords = getCoords(mainMPath)
    ms1Coords = getCoords(ms1)
    ms3Coords = getCoords(ms3)
    ms4Coords = getCoords(ms4)
    ms5Coords = getCoords(ms5)
    ms6Coords = getCoords(ms6)
    
    mAvgCoords = [np.mean(mainMCoords['X']), np.mean(mainMCoords['Y'])]    
    
    mFullCoords, mFullAvg = getFullCoords(mainMCoords, mAvgCoords, ms1Coords,  
                                 ms3Coords, ms4Coords, ms5Coords, ms6Coords)
    
    plotCoords(mFullAvg, f'M{machineNum} All Spindles (Normalized to Spindle {spindleNorm})')       # full machine with averaged values
    
    plotHistogram(mFullCoords, mAvgCoords, f'Machine {machineNum}')
    
    fig,a = plt.subplots(3,2, figsize=(10,15), dpi=140)
    plotCoords(ms1Coords, f'M{machineNum} Spindle 1', a, modifier=1, sub1=0, sub2=0, graph=0)         # spindle 1
    plotCoords(mainMCoords, f'M{machineNum} Spindle 2', a, modifier=1, sub1=0, sub2=1, graph=0)       # spindle 2
    plotCoords(ms3Coords, f'M{machineNum} Spindle 3', a, modifier=1, sub1=1, sub2=0, graph=0)         # spindle 3
    plotCoords(ms4Coords, f'M{machineNum} Spindle 4', a, modifier=1, sub1=1, sub2=1, graph=0)         # spindle 4
    plotCoords(ms5Coords, f'M{machineNum} Spindle 5', a, modifier=1, sub1=2, sub2=0, graph=0)         # spindle 5
    plotCoords(ms6Coords, f'M{machineNum} Spindle 6', a, modifier=1, sub1=2, sub2=1)         # spindle 6
    
    
    
    
    
def machineDetailsM3(machineNum, mainMPath, ms1, spindleNorm='2'):
    mainMCoords = getCoords(mainMPath)
    ms1Coords = getCoords(ms1)
    
    mAvgCoords = [np.mean(mainMCoords['X']), np.mean(mainMCoords['Y'])]    
    
    mFullCoords, mFullAvg = getFullCoordsM3(mainMCoords, mAvgCoords, ms1Coords)
    
    plotCoords(mFullAvg, f'M{machineNum} All Spindles (Normalized to Spindle {spindleNorm})')       # full machine with averaged values
    
    plotHistogram(mFullCoords, mAvgCoords, f'Machine {machineNum}')
    
    fig,a = plt.subplots(1,2, figsize=(10,5), dpi=140, squeeze=False)
    plotCoords(ms1Coords, f'M{machineNum} Spindle 1', a, modifier=1, sub1=0, sub2=0, graph=0)         # spindle 1
    plotCoords(mainMCoords, f'M{machineNum} Spindle 2', a, modifier=1, sub1=0, sub2=1, graph=1)       # spindle 2
    
    
    
    



def getCoords(path):
    lines = []
    with open(path, 'r') as file:
        locs = file.readlines()
        
        
    for i in locs:
        i = i.split()
        
        try:
            if i[0] == '?':
                i.pop(0)
                i.pop(1)
                
            elif i[0] == 'Step':
                continue
                
        except IndexError:
            continue
    
        
        lines.append(i)
        
        
    coords = {'X': [], 'Y': []}
    for j in range(len(lines)):
        if (lines[j][0] == 'X') and (lines[j+1][0] == 'Y'):
            xCoord = float(lines[j][-1])
            yCoord = float(lines[j+1][-1])
            if (xCoord > 0.003) or (xCoord < -0.003) or (yCoord > 0.003) or (yCoord < -0.003):
                continue
            else:
                coords['X'].append(float(lines[j][-1]))
                coords['Y'].append(float(lines[j+1][-1]))
            
    return coords
    



def getFullCoords(mainMCoords, mAvgCoords, ms1Coords, ms3Coords, 
                  ms4Coords, ms5Coords, ms6Coords):
    mFullCoords = {'X': [], 'Y': []}
    mFullCoords['X'].extend(mainMCoords['X'])
    mFullCoords['X'].extend(ms1Coords['X'])
    mFullCoords['X'].extend(ms3Coords['X'])
    mFullCoords['X'].extend(ms4Coords['X'])
    mFullCoords['X'].extend(ms5Coords['X'])
    mFullCoords['X'].extend(ms6Coords['X'])
    
    mFullCoords['Y'].extend(mainMCoords['Y'])
    mFullCoords['Y'].extend(ms1Coords['Y'])
    mFullCoords['Y'].extend(ms3Coords['Y'])
    mFullCoords['Y'].extend(ms4Coords['Y'])
    mFullCoords['Y'].extend(ms5Coords['Y'])
    mFullCoords['Y'].extend(ms6Coords['Y'])
    
    
    fullCoords2 = {'X': [], 'Y': []}
    j = 0
    for key, value in mFullCoords.items():
        newValue = [i - mAvgCoords[j] for i in value]
        j+=1
        
        fullCoords2[key].extend(newValue)
    
    return mFullCoords, fullCoords2




def getFullCoordsM3(mainMCoords, mAvgCoords, ms1Coords):
    mFullCoords = {'X': [], 'Y': []}
    mFullCoords['X'].extend(mainMCoords['X'])
    mFullCoords['X'].extend(ms1Coords['X'])
    
    mFullCoords['Y'].extend(mainMCoords['Y'])
    mFullCoords['Y'].extend(ms1Coords['Y'])
    
    
    fullCoords2 = {'X': [], 'Y': []}
    j = 0
    for key, value in mFullCoords.items():
        newValue = [i - mAvgCoords[j] for i in value]
        j+=1
        
        fullCoords2[key].extend(newValue)
    
    return mFullCoords, fullCoords2





def plotCoords(coords, pTitle, a=0, modifier=0, sub1=0, sub2=0, graph=1):
    xAvgCoord = np.mean(coords['X'])
    yAvgCoord = np.mean(coords['Y'])
    
    meanX1, meanY1 = [xAvgCoord-0.0002, xAvgCoord+0.0002], [yAvgCoord, yAvgCoord]
    meanX2, meanY2 = [xAvgCoord, xAvgCoord], [yAvgCoord-0.0002, yAvgCoord+0.0002]
    
    bx1,by1 = [-0.0005, -0.0005], [-0.0005,0.0005]
    bx2,by2 = [-0.0005,0.0005], [0.0005, 0.0005]
    bx3,by3 = [0.0005,0.0005], [0.0005, -0.0005]
    bx4,by4 = [0.0005,-0.0005], [-0.0005, -0.0005]
    
    gx1,gy1 = [-0.001, -0.001], [-0.001,0.001]
    gx2,gy2 = [-0.001,0.001], [0.001, 0.001]
    gx3,gy3 = [0.001,0.001], [0.001, -0.001]
    gx4,gy4 = [0.001,-0.001], [-0.001, -0.001]
    
    rx1,ry1 = [-0.002, -0.002], [-0.002,0.002]
    rx2,ry2 = [-0.002,0.002], [0.002, 0.002]
    rx3,ry3 = [0.002,0.002], [0.002, -0.002]
    rx4,ry4 = [0.002,-0.002], [-0.002, -0.002]
    
    
    if modifier == 0:
        fig = plt.figure(figsize=(6,6), dpi = 150)
        ax = fig.add_axes([0,0,1,1])
        ax.set_xlim(-0.003,0.003)
        ax.set_ylim(-0.003,0.003)
        
        ax.plot(bx1, by1, bx2, by2, bx3, by3, bx4, by4, color='dodgerblue')
        ax.plot(gx1, gy1, gx2, gy2, gx3, gy3, gx4, gy4, color='limegreen', linewidth=3)
        ax.plot(rx1, ry1, rx2, ry2, rx3, ry3, rx4, ry4, color='red')
        ax.plot(meanX1, meanY1, meanX2, meanY2, color='purple', linewidth = 2)
        ax.scatter(coords['X'], coords['Y'])
        
        plt.title(pTitle)
    
    elif modifier == 1:
        a[sub1][sub2].plot(bx1, by1, bx2, by2, bx3, by3, bx4, by4, color='dodgerblue')
        a[sub1][sub2].plot(gx1, gy1, gx2, gy2, gx3, gy3, gx4, gy4, color='limegreen', linewidth=3)
        a[sub1][sub2].plot(rx1, ry1, rx2, ry2, rx3, ry3, rx4, ry4, color='red')
        a[sub1][sub2].plot(meanX1, meanY1, meanX2, meanY2, color='purple', linewidth = 2)
        a[sub1][sub2].scatter(coords['X'], coords['Y'])
        
        a[sub1][sub2].set_xlim(-0.003,0.003)
        a[sub1][sub2].set_ylim(-0.003,0.003)
        a[sub1][sub2].set_title(pTitle)
    
    if graph == 1:
        plt.show()





def plotHistogram(coordinates, avgCoordinates, machine):   
    xhistpts1 = np.array([-0.0015,-0.0015])
    xhistpts2 = np.array([0.0015,0.0015])
    yhistpts = np.array([0,35])
    
    
    outside = 0
    for i in range(len(coordinates['X'])):
        if (coordinates['X'][i] > 0.0015) or (coordinates['Y'][i] > 0.0015):
            outside += 1
        elif (coordinates['X'][i] < -0.0015) or (coordinates['Y'][i] < -0.0015):
            outside += 1
            
    outPct = round(outside / len(coordinates["X"]) * 100, 1)
            
    
    plt.figure(figsize=(8,4), dpi=150)
    
    plt.subplot(1,2,1)
    plt.hist(coordinates['X'], range=[-0.005,0.005], bins='auto')
    plt.plot(xhistpts1, yhistpts, color='red', linewidth=0.75)
    plt.plot(xhistpts2, yhistpts, color='red', linewidth=0.75)
    plt.title(f'{machine} X-Axis Histogram')
    
    plt.subplot(1,2,2)
    plt.hist(coordinates['Y'], range=[-0.005,0.005], bins='auto')
    plt.plot(xhistpts1, yhistpts, color='red', linewidth=0.75)
    plt.plot(xhistpts2, yhistpts, color='red', linewidth=0.75)
    plt.title(f'{machine} Y-Axis Histogram')
    
    plt.text(-0.0135,-8, 'Mean')
    plt.text(-0.0105,-8, 'Sigma')
    plt.text(-0.0075,-8, 'Max')
    plt.text(-0.0045,-8, 'Min')
    plt.text(-0.0015,-8, 'Cpk')
    
    plt.text(-0.017,-12, 'X Axis')
    plt.text(-0.017,-16, 'Y Axis')

 
    
    xAvg = avgCoordinates[0] * 1000
    yAvg = avgCoordinates[1] * 1000
    xSig = statistics.pstdev(coordinates['X']) * 1000
    ySig = statistics.pstdev(coordinates['Y']) * 1000
    xMax = max(coordinates['X']) * 1000
    yMax = max(coordinates['Y']) * 1000
    xMin = min(coordinates["X"]) * 1000
    yMin = min(coordinates['Y']) * 1000
    xCPK = min((1.5 - xAvg) / (3*xSig), (xAvg + 1.5) / (3*xSig))
    yCPK = min((1.5 - yAvg) / (3*ySig), (yAvg + 1.5) / (3*ySig))
    
    plt.text(-0.0135,-12, f'{round(xAvg,3)}')     # x average
    plt.text(-0.0135,-16, f'{round(yAvg,3)}')     # y average
    
    plt.text(-0.0105,-12, f'{round(xSig,3)}')   # x sigma
    plt.text(-0.0105,-16, f'{round(ySig,3)}')   # y sigma
    
    plt.text(-0.0075,-12, f'{round(xMax,3)}')     # x max
    plt.text(-0.0075,-16, f'{round(yMax,3)}')     # y max
    
    plt.text(-0.0045,-12, f'{round(xMin,3)}')   # x min
    plt.text(-0.0045,-16, f'{round(yMin,3)}')   # y min
    
    plt.text(-0.0015,-12, f'{round(xCPK,3)}')     # x cpk
    plt.text(-0.0015,-16, f'{round(yCPK,3)}')     # y cpk
    
    
    plt.text(-0.017,-21, f'{outPct}% of points are outside the specification limits of ±0.0015')
 
    plt.show()
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()
