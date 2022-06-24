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

def BPSK_noise():
    """ Adds noise to a BPSK transmission scheme """
    # ASCII for 'w'
    character = np.array([0,1,1,1,0,1,1,1])
    nbits = len(character)
    bits = character
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

    # Now let's recieve some signals! But with noise now
    SNR = 1
    NP = NP_compute(SNR)
    rx = tx_OTA + NP * np.random.randn(nbits*num_samples)

    plt.plot(t, rx)
    plt.title("RX signal (raw) - SNR {} dB".format(SNR))
    plt.show()

    # plt.plot(t,cosine_vec)
    # plt.show()

    rxI = rx * cosine_vec
    rxQ = rx * sine_vec

    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].plot(t, rxI)
    axs[0].set_title("RX I signal - SNR {} dB".format(SNR))
    axs[1].plot(t, rxQ)
    axs[1].set_title("RX Q signal - SNR {} dB".format(SNR))
    fig.tight_layout()
    plt.show()

    rxIQ = intdump(rxI, 51) + np.multiply(1j,intdump(rxQ, 51))
    rxbits = pskdemod(rxIQ, 2)

    nerrors = sum(abs(rxbits - bits))

    # Bit error rates -> Q(sqrt(2Eb/N_0)) where Eb/No = SNR per bit
    # Thus SNR = 1 means Q(sqrt(2)) = 10**-1
    print ("The number of bit errors is %d" % nerrors)
    print( "The error rate is {}".format(nerrors/nbits))

def QPSK_noise():
    """ Modulates a set of binary values into QPSK """
    character = np.array([0, 1, 1, 1, 0, 1, 1, 1])
    nbits = len(character)
    bits = character
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

    # Now let's recieve some signals!
    NP = NP_compute(1)
    print(NP)
    rx = tx_OTA + NP * np.random.randn(nbits*num_samples)

    plt.plot(t, rx)
    plt.show()

    rxI = rx * cosine_vec
    rxQ = rx * sine_vec

    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].plot(t, rxI)
    axs[1].plot(t, rxQ)
    fig.tight_layout()
    plt.show()

    rxIQ = intdump(rxI, num_samples) + np.multiply(1j,intdump(rxQ, num_samples))
    plt.plot(rxIQ)
    plt.show()
    rxbits = pskdemod(rxIQ, 4)

    nerrors = sum(abs(rxbits - bits))

    # Bit error rates -> Q(sqrt(2Eb/N_0)) where Eb/No = SNR per bit
    # Thus SNR = 1 means Q(sqrt(2*10)) = 10**-6
    print ("The number of bit errors is %d" % nerrors)
    print( "The error rate is {}".format(nerrors/nbits))

def NP_compute(SNRdB):
    """ Computes the noise power for a desired SNR """
    return 1/(10**(SNRdB/10))

if __name__ == '__main__':
    BPSK_noise()
    #QPSK_noise()