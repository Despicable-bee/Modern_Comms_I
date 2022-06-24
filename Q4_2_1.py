import numpy as np
import math
import cmath
import sys
from matplotlib import pyplot as plt
from helpers import pskmod
from helpers import pskdemod
from helpers import oversample
from helpers import intdump
from helpers import qammod
from helpers import qamdemod
from helpers import read_complex_bytev2

def freq_synchronizer():
    """ Synchronizes the signal """
    data = read_complex_bytev2("./binaries/freqA.bin", int(2e6))
    #plt.plot(data[1:5000])
    starts = time_synchronizer()
    for i in range(0,len(starts)):
        sig_start = starts[i]
        print(sig_start)
        offset = 640 - 1

        # realData = np.real(data[sig_start:sig_start+offset])
        # imagData = np.imag(data[sig_start:sig_start+offset])
        # plt.plot(realData, imagData, 'x')
        # plt.title("Signal data raw - (constellation plot)")
        # plt.xlabel("I")
        # plt.ylabel("Q")
        # plt.show()

        # fig, axs = plt.subplots(nrows=2, ncols=1)
        # axs[0].set_title("Real signal data (distorted)")
        # axs[0].plot(np.real(data[sig_start:sig_start+offset]))
        # axs[1].set_title("Imag signal data (distorted)")
        # axs[1].plot(np.imag(data[sig_start:sig_start+offset]))
        # fig.tight_layout()
        # plt.show()

        # Create the exponential vector
        exp_vec = []
        
        # Frequency information to correct the distortion
        t = np.linspace(0, len(data), len(data))
        f = 3300
        extra_rot = complex(0.939693, 0.34202)*np.exp(1j*np.pi/4)

        for i in range(0, len(t)):
            exp_vec.append(cmath.exp(2*math.pi*f*t[i]*1j))
        newData = data * exp_vec * extra_rot

        # realData = np.real(newData[sig_start:sig_start+offset])
        # imagData = np.imag(newData[sig_start:sig_start+offset])
        # plt.plot(realData, imagData, 'x')
        # plt.title("Signal data synchronised - (constellation plot)")
        # plt.xlabel("I")
        # plt.ylabel("Q")
        # plt.show()

        # Plot the corrected IQ signal data
        # fig, axs = plt.subplots(nrows=2, ncols=1)
        # axs[0].set_title("Real signal data (frequency synchronised)")
        # axs[0].plot(np.real(newData[sig_start:sig_start+offset]))
        # axs[1].set_title("Imag signal data (frequency synchronised)")
        # axs[1].plot(np.imag(newData[sig_start:sig_start+offset]))
        # fig.tight_layout()
        # plt.show()

        # Then integrate dump and demod
        IQData = intdump(newData[sig_start:sig_start+offset], 16)

        # print out the two rows

        # Rotate around to get the different values
        p1 = pskdemod(
                intdump(newData[sig_start:sig_start+offset], 16), 4, 
                        ctype='bin').astype(int)
        p2 = pskdemod(
                intdump(newData[sig_start:sig_start+offset]*1j, 16), 4, 
                        ctype='bin').astype(int)
        p3 = pskdemod(
                intdump(newData[sig_start:sig_start+offset]*-1, 16), 4, 
                        ctype='bin').astype(int)
        p4 = pskdemod(
                intdump(newData[sig_start:sig_start+offset]*-1j, 16), 4, 
                        ctype='bin').astype(int)

        phases = [p1,p2,p3,p4]
        phaseOffsets = ['None', '1j', '-1', '-1j']
        counter = 0

        # for i in range(0, len(phases)):
        #     p = phases[i]
        #     po = phaseOffsets[i]
        #     plt.title("Phase Offset: {}".format(po))
        #     print(p)
        #     print(len(p))
        #     tempX = np.linspace(0, len(p), len(p))
        #     print(tempX)
        #     plt.step(tempX, p)
        #     plt.show()

        e1 = [1, 4, 16, 64]
        e2 = [64, 16, 4, 1]
        endians = [e1, e2]

        totalbits = int(20*2)
        totalbytes = int(totalbits/8)

        # Now time to decode what the message might be
        phase_arr = []
        for j in range(0,4):
            # 4 phase combinations
            endian_arr = []
            for k in range(0, 2):
                # 2 different endians
                char_arr = []
                for i in range(0, totalbytes):
                    # 5 bytes per combo
                    num_arr = []
                    for l in range(0, 4):
                        # 4 symbols per byte
                        num_arr.append(phases[j][i*4 + l])
                    char_arr.append(chr(np.sum(np.array(num_arr) * \
                            np.array(endians[k]))))
                endian_arr.append(char_arr)
            phase_arr.append(endian_arr)
        print("----------------------------")
        counter = 0
        for i in range(0,len(phase_arr)):
            for j in range(0, 2):
                string = ""
                for k in range(0,len(phase_arr[i][j])):
                    string += phase_arr[i][j][k]
                print("{}.: {}".format(counter,string))
                counter += 1

def time_synchronizer():
    """ 
        Synchronizes the value in time using the energy synchronization method. 
    """
    data = read_complex_bytev2("./binaries/freqA.bin", int(2e6))
    #plt.plot(data[1:5000])
    offset = 640 - 1
    numSamples = 100000
    sample = data[0:numSamples]
    averagingNum = 25       # Tune this variable to get the correct value

    # Now we want to create a energy detection system
    # We're going to do with with a moving average
    synchronized = []
    avg = []
    for i in range(0, len(sample)):
        movAvg = 0
        # Sample within +/- averagingNum/2 from the current point
        if(i - (averagingNum/2)-1 < 0  or i + (averagingNum/2)-1 > numSamples -1):
            
            # Edge case 1 - left side constrained
            if i - (averagingNum/2)-1 < 0:
                offset = abs(i - averagingNum/2 - 1)
                for j in range(0,averagingNum):
                    movAvg = movAvg + abs(sample[int(i-averagingNum/2-1 + j + offset)])
            
            # Edge case 2- right side constrained
            elif i + (averagingNum/2)-1 > numSamples -1:
                offset = abs(i + averagingNum/2 - numSamples - 1)
                for j in range(0,averagingNum):
                    movAvg = movAvg + abs(sample[int(i-averagingNum/2-1 + j - offset)])
                
        else:
            # Sample normally
            for j in range(0,averagingNum):
                movAvg = movAvg + abs(sample[int(i-averagingNum/2-1 + j)])
        movAvg = movAvg / averagingNum
        avg.append(movAvg)

        if(movAvg > 0.5):      # Tune this to get a better reading
            # This point is a 1
            synchronized.append(1)
        else:
            synchronized.append(0)
    
    # okay, let us find all of the start points
    start_indexes = []

    plt.plot(synchronized)
    plt.title("Signal data (raw synchronised)")
    plt.plot(abs(sample))
    plt.show()

    # Now to gather all the values where it starts off as 1
    globalPtr = 0
    copySync = synchronized
    print(len(synchronized))
    while(globalPtr < len(synchronized)):
        try:
            syncSample = 0
            syncPtr = 0
            # Iterate until we find the first 1
            while(syncSample == 0):
                syncSample = copySync[syncPtr]
                syncPtr += 1
            #  Append that value
            start_indexes.append(syncPtr - 1 + globalPtr)
            # Iterate until we find the first 0
            while syncSample == 1:
                syncSample = copySync[syncPtr]
                syncPtr += 1
            
            # update the global value
            globalPtr += syncPtr - 1
            copySync = synchronized[globalPtr:]
        except IndexError as ie:
            print(ie)
            print(syncPtr)
            print(globalPtr)
            break

    # while(pointer < numSamples):
    #     try: 
    #         indexer += synchronized.index(1)
    #         pointer = synchronized.index(1) + \
    #                 synchronized[synchronized.index(1):].index(0) + 200
    #         start_indexes.append(indexer)
    #         synchronized = synchronized[pointer:]
    #     except ValueError as ve:
    #         print(ve)
    #         print(pointer)
    #         break
    print("Indexes: {}".format(start_indexes))
    
    plt.plot(avg)
    plt.title("Input data filtered (SMA)")
    plt.show()

    # plt.plot(np.array(synchronized))
    # plt.show()
    return start_indexes



if __name__ == '__main__':
    freq_synchronizer()