import numpy as np
import math
import cmath
from matplotlib import pyplot as plt
from helpers import pskmod
from helpers import pskdemod
from helpers import oversample
from helpers import intdump
from helpers import qammod
from helpers import qamdemod
from helpers import read_complex_bytev2

def correlation_sync():
    """ Computes the autocorrelation of the signal to synchronize """
    data = read_complex_bytev2("./binaries/freqB.bin", int(2e6))
    sample = data
    exp_vec = []
    num_samples = 16
    
    t = np.linspace(0, len(data), len(data))
    
    f = 3465
    samplesize= int(10e3)
    extra_rot = complex(0.573576, 0.819152)*np.exp(1j*np.pi/4)

    for i in range(0, len(t)):
        exp_vec.append(cmath.exp(2*math.pi*f*t[i]*1j))

    newSample = sample * exp_vec * extra_rot

    realData = np.real(newSample[0:samplesize])
    imagData = np.imag(newSample[0:samplesize])
    plt.plot(realData, imagData, 'x')
    plt.title("Signal data (frequency sync) - Constellation diagram")
    plt.xlabel("I")
    plt.ylabel("Q")
    plt.show()

    # We need to encode the binary sequence 1111 0011 1010 0000
    bpskSync = [1,1,1,1, 0,0,1,1, 1,0,1,0, 0,0,0,0]
    # Now we module to BPSK
    modbits = pskmod(bpskSync, 2)
    # Oversample
    oversampleSync = oversample(modbits, 8)

    # Flip the oversample
    for i in range(0,len(oversampleSync)):
        oversampleSync[i] = -1 * oversampleSync[i]
    
    plt.plot(oversampleSync)
    plt.title("Synchronisation BPSK waveform")
    plt.show()

    # Now we need to correlate the sync waveform with the signal

    # Original waveform
    # fig, axs = plt.subplots(nrows=2, ncols=1)
    # axs[0].plot(np.real(data[sig_start:sig_start+offset]))
    # axs[1].plot(np.imag(data[sig_start:sig_start+offset]))
    # fig.tight_layout()
    # plt.show()

    # Now let's correlate
    sig_start_2 = 0
    offset_2 = 2000
    realCorr = np.correlate(oversampleSync, newSample[sig_start_2:sig_start_2+offset_2])
    # imagCorr = np.correlate(imagSym, newSample[sig_start_2:sig_start_2+offset_2])

    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].set_title("I signal data (frequency sync)")
    axs[0].plot(np.real(newSample[sig_start_2:sig_start_2+offset_2]))
    axs[1].set_title("Q signal data (frequency sync)")
    axs[1].plot(np.imag(newSample[sig_start_2:sig_start_2+offset_2]))
    fig.tight_layout()
    plt.show()

    plt.plot(realCorr)
    plt.title("Correlation with BPSK waveform plot (real)")
    plt.show()

    # So the first frame starts at sample 301
    sig_start_3 = 350
    offset_3 = 320

    # Now let's find the words
    # Rotate around to get the different values
    p1 = pskdemod(
            intdump(newSample[sig_start_3:sig_start_3+offset_3], 
                    num_samples), 4, ctype='bin').astype(int)
    p2 = pskdemod(
            intdump(newSample[sig_start_3:sig_start_3+offset_3]*1j, 
                    num_samples), 4, ctype='bin').astype(int)
    p3 = pskdemod(
            intdump(newSample[sig_start_3:sig_start_3+offset_3]*-1, 
                    num_samples), 4, ctype='bin').astype(int)
    p4 = pskdemod(
            intdump(newSample[sig_start_3:sig_start_3+offset_3]*-1j, 
                    num_samples), 4, ctype='bin').astype(int)
    phases = [p1,p2,p3,p4]

    fig, axs = plt.subplots(nrows=4, ncols=1)
    axs[0].step(np.linspace(0, len(p1), len(p1)), p1)
    axs[1].step(np.linspace(0, len(p2), len(p2)), p2)
    axs[2].step(np.linspace(0, len(p3), len(p3)), p3)
    axs[3].step(np.linspace(0, len(p4), len(p4)), p4)
    fig.tight_layout()
    plt.show()

    # for i in range(0, len(phases)):
    #     print(phases[i][0:19])
    #     print(phases[i][20:39])

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
                char_arr.append(chr(np.sum(np.array(num_arr) * np.array(endians[k]))))
            endian_arr.append(char_arr)
        phase_arr.append(endian_arr)
    for i in range(0,len(phase_arr)):
        for j in range(0, 2):
            string = ""
            for k in range(0,len(phase_arr[i][j])):
                string += phase_arr[i][j][k]
            print(string)

if __name__ == '__main__':
    correlation_sync()

