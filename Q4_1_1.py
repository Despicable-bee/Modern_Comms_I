# Standard libs
import numpy as np
import math
import cmath
from matplotlib import pyplot as plt

# Local Libs
from helpers import pskmod
from helpers import pskdemod
from helpers import oversample
from helpers import intdump
from helpers import qammod
from helpers import qamdemod

def BPSK():
    """Modulates a set of binary values into BPSK"""
    nbits = 4
    bits = np.random.randint(2, size=nbits)
    modbits = pskmod(bits, 2)
    print(bits)

    num_samples = 51

    t = np.linspace(0, nbits, num_samples*nbits)
    f = 4 # Rb = 25, fc = 100 - ratio of 4

    txbits = oversample(modbits, num_samples)
    cosine_vec = []
    sine_vec = []
    for i in range(0, len(t)):
        cosine_vec.append(math.cos(2*math.pi*f*t[i]))

    for i in range(0, len(t)):
        sine_vec.append(math.sin(2*math.pi*f*t[i]))
    
    txi = np.real(txbits) * cosine_vec
    txq = np.imag(txbits) * sine_vec

    #OTA = Over the air
    tx_OTA = txi + txq

    plt.plot(t, tx_OTA)
    plt.title("BPSK TX signal over the air (OTA)")
    plt.show()

    # Now let's recieve some signals!
    rx = tx_OTA

    rxI = rx * cosine_vec
    rxQ = rx * sine_vec

    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].plot(t, rxI)
    axs[0].set_title("RX I signal")
    axs[1].plot(t, rxQ)
    axs[1].set_title("RX Q signal")
    plt.show()

    rxIQ = intdump(rxI, 51) + np.multiply(1j,intdump(rxQ, 51))

    print(pskdemod(rxIQ, 2))

def QPSK():
    """ Modulates a set of binary values into QPSK """
    nbits = 4
    bits = np.array([0,1,2,3])
    modbits = pskmod(bits, 4)
    print(bits)
    num_samples = 51

    t = np.linspace(0, nbits, num_samples*nbits)
    f = 4 # Rb = 25, fc = 100 - ratio of 4

    txbits = oversample(modbits, num_samples)

    cosine_vec = []
    sine_vec = []
    for i in range(0, len(t)):
        cosine_vec.append(math.cos(2*math.pi*f*t[i]))

    for i in range(0, len(t)):
        sine_vec.append(math.sin(2*math.pi*f*t[i]))

    txi = np.real(txbits) * cosine_vec
    txq = np.imag(txbits) * sine_vec

    #OTA = Over the air
    tx_OTA = txi + txq

    plt.plot(t, tx_OTA)
    plt.title("QPSK TX signal over the air (OTA)")
    plt.show()

    # Now let's recieve some signals!
    rx = tx_OTA

    rxI = rx * cosine_vec
    rxQ = rx * sine_vec

    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].plot(t, rxI)
    axs[0].set_title("RX I signal")
    axs[1].plot(t, rxQ)
    axs[1].set_title("RX Q signal")
    fig.tight_layout()
    plt.show()

    rxIQ = intdump(rxI, num_samples) + np.multiply(1j,intdump(rxQ, num_samples))

    print(pskdemod(rxIQ, 4))

def QAM_16():
    """ Modulates a set of binary values into 16-QAM """
    nbits = 16
    bits = np.random.randint(16, size=nbits)
    modbits = qammod(bits, 16)
    num_samples = 51

    t = np.linspace(0, nbits, num_samples*nbits)
    f = 4 # Rb = 25, fc = 100 - ratio of 4

    txbits = oversample(modbits, num_samples)

    cosine_vec = []
    sine_vec = []
    for i in range(0, len(t)):
        cosine_vec.append(math.cos(2*math.pi*f*t[i]))

    for i in range(0, len(t)):
        sine_vec.append(math.sin(2*math.pi*f*t[i]))

    txi = np.real(txbits) * cosine_vec
    txq = np.imag(txbits) * sine_vec
    print(txi)
    print(txq)

    #OTA = Over the air
    tx_OTA = txi + txq

    plt.plot(t, tx_OTA)
    plt.show()

    # Now let's recieve some signals!
    rx = tx_OTA

    rxI = rx * cosine_vec
    rxQ = rx * sine_vec

    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].plot(t, rxI)
    axs[1].plot(t, rxQ)
    fig.tight_layout()
    plt.show()
    print(intdump(rxI, num_samples))
    rxIQ = intdump(rxI, num_samples) + np.multiply(1j,intdump(rxQ, num_samples))
    
    print(rxIQ)
    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].plot(np.real(rxIQ))
    axs[1].plot(np.imag(rxIQ))
    fig.tight_layout()
    plt.show()
    demod = qamdemod(2*rxIQ, 16)
    plt.plot(bits, label="bits")
    plt.plot(demod, label="demod")
    plt.legend()
    plt.show()

    print(demod)
    print(bits)

if __name__ == '__main__':
    # BPSK()
    QPSK()
    # QAM_16()