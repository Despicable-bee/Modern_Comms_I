import numpy as np
import math
import cmath
import struct

def ismember(A, B):
    return [ np.sum(a == B) for a in A ]

def pskmod(x, M, phi=0, ctype="gray"):
    m = np.array(range(M))
   
    if sum(ismember(np.array(ismember(x, m)) == 0, True)) > 0:
        print("pskmod: all elements of X must be integers in the range [0,%d-1]" % M)
       
    constellation = np.exp(1j*2*np.pi*m/M+1j*phi)
   
    if (ctype.lower() == "bin"): # non-graycoding
        y = [constellation[xx] for xx in x]
    elif (ctype.lower() == "gray"): # graycoding
        (m ^ np.right_shift(m, 1))
        b = (m ^ np.right_shift(m, 1)).argsort()
        y = [constellation[xx] for xx in b[x]]
   
    return y

def pskdemod(x, M, phi=0, ctype="gray"):
    m = np.array(range(M))
    
    idx = np.mod(np.round((np.angle(x) - phi) * M/2/np.pi), M) + 1
    
    if (ctype.lower() == "bin"):
        y = idx-1
    elif (ctype.lower() == "gray"):
        constmap = m ^ np.right_shift(m, 1)
        y = [constmap[int(xx)] for xx in idx-1]
        
    return y

    m = np.array(range(M))
   
    if sum(ismember(np.array(ismember(x, m)) == 0, True)) > 0:
        print("qammod: all elements of X must be integers in the range [0,%d-1]" % M)
        return
    
    c = np.sqrt(M)
    if (not (c == int(c) and np.log2(c) == int(np.log2(c)))):
        print("qammod: M must be square and a power of 2")
        return
    
    b = -2 * np.mod (x, (c)) + c - 1
    a = 2 * np.floor (x / (c)) - c + 1
    y = a + 1j*b
    return (y)

def qammod(x, M):
    m = np.array(range(M))
   
    if sum(ismember(np.array(ismember(x, m)) == 0, True)) > 0:
        print("qammod: all elements of X must be integers in the range [0,%d-1]" % M)
        return
    
    c = np.sqrt(M)
    if (not (c == int(c) and np.log2(c) == int(np.log2(c)))):
        print("qammod: M must be square and a power of 2")
        return
    
    b = -2 * np.mod (x, (c)) + c - 1
    a = 2 * np.floor (x / (c)) - c + 1
    y = a + 1j*b
    return (y)

def qamdemod(y, M):
    c = np.sqrt(M)
    if (not (c == int(c) and np.log2(c) == int(np.log2(c)))):
        print("qamdemod: M must be square and a power of 2")
        return
    
    x = qammod(range(M), M)
    z = np.zeros(np.size(y))
    for k in range(np.size(y)):
        z[k] = np.argmin(abs(  y[k] - x ))
    
    return z

def intdump(x, nsamp):
    """ Integrates the signal x for one bit period then outputs the averaged one
        value into Y """
    # e.g. 51*4/51 = 4
    signalLength = int(len(x)/nsamp)
    signalPointer = 0
    Y = []
    for i in range(0, signalLength):
        bitvalue = 0
        for j in range(0, nsamp):
            bitvalue += x[signalPointer]
            signalPointer += 1
        bitvalue = bitvalue / nsamp
        Y.append(bitvalue)
    return np.array(Y)

def oversample(array, number):
    """ Takes an array and repeats each of its elements a number of times """
    newArr = []
    for item in array:
        for i in range(0,number):
            newArr.append(item)
    return newArr

def read_complex_bytev2(filename, M):
    data = np.fromfile(filename, dtype=np.dtype('B'), count=M)
    normdata=(np.array(data, dtype=float)-127)/128
    normdata.dtype=np.complex
    return normdata