# Modern Communication systems I

This is 1/3 in a series of projects which is designed to act as a reference
    for modern communication systems.

Since this is the first of the 3, it will be the simplest and focusing on
    some of the simple modulation schemes (like BPSK, QPSK and 16-QAM).

We'll also look at some basic synchronisation techniques, and finish off with 
    a timing recovery example

## A Brief history
The first radio stations that could carry signals did not emerge until the 
    invention of the [thermionic valve](https://en.wikipedia.org/wiki/Vacuum_tube),
    (or 'vacuum tube'), which provided functionality similar to modern 
    transistors, however they were much larger.
    
Prior to this, the only means of communicating via radio was through 
    [wireless telegraphy](https://en.wikipedia.org/wiki/Wireless_telegraphy). 
    [This video](https://www.youtube.com/watch?v=YPsgEdmlUf0) shows a highly 
    skilled operator transmitting a message at a decent speed (likely a few
    characters per second). 

Wireless telegraphy had only two modes of transmitting, 'on' and 'off', and thus
    did not require any complex amplification scheme for modulation / 
    demodulation.

With the introduction of the vacuum tube, signals could now be "mixed" on the
    broadcasting side (i.e. the audio signal mixed with a 
    **carrier frequency**), and "un-mixed" on the receiving side (leaving only
    the audio signal).

## Amplitude Shift Keying (ASK)
The first, and indeed the oldest, means of encoding information and broadcasting
    it via radio waves is **Amplitude Modulation** (AM).

<img src="https://4.bp.blogspot.com/-Ban4dsr2vdA/XLlcGEKERDI/AAAAAAAABuI/1yXgH6UKoXkAqcLMobYX0xTNdKq8eCtcACLcBGAs/s1600/Amplitude%2BModulation.png"
    style="border-radius:3px"
    width="500px">

Here an **analog carrier wave** is multiplied (or 'mixed') with an analog 
    audio signal and broadcasted (via some antenna) into the open air.

Low frequency radio waves typically can't make it through the ionosphere, 
    and are thus reflected back down towards the ground, creating an area of 
    reception around the broadcast tower.

<img src="https://www.swpc.noaa.gov/sites/default/files/styles/medium/public/Ionosphere.gif?itok=79nWQYW9"
    style="border-radius:3px"
    width="500px">

**Amplitude Shift Keying** (ASK) is very similar to AM, the key difference being
    that rather than encoding analog signals, digital signals are encoded.

<img src="https://i.stack.imgur.com/NT3K0.jpg"
    style="border-radius:3px"
    width="500px">

The key reason for this, as you'll see in future parts, is because digital
    signals can employ **error correction techniques** if corrupted by
    atmospheric conditions (such as rain-fade or distortion).

A prominant variant of ASK is QAM, which we'll discuss more a bit later

## Frequency Shift keying (FSK)

Similar to ASK, **Frequency Shift Keying** (FSK) uses the same underlying idea
    as Frequncy Modulation (FM), but encodes digital signals, rather than
    analog signals.

FM is less susceptible to noise and distortion when compared to AM, and as such
    empirically has a longer range.

## Phase Shift Keying (PSK)

Finally we get to **Phase Shift Keying** (PSK), and the core focus of this repo.

<img src="https://cdn.britannica.com/18/4618-004-219D9B97/signal-modulation-methods-binary-digits-amplitudes-series.jpg"
    style="border-radius:3px"
    width="500px">

Same as before, its analog cousin is Phase Modulation (PM), but we're encoding
    digital signals rather than analog ones.

There are many variants of PSK, two very prominant forms is BPSK and QPSK, 
    which we'll discuss more a bit later.

## IQ signals
One of the first things young comms engineers encounter is the IQ signal.

[This video](https://www.youtube.com/watch?v=LpCBxDVwS_8) does a good job 
    explaining why its important to use such a technique, but in a nutshell,
    it is very uncommon for a local oscillator to exactly match the 
    carrier frequency of the carrier wave you're trying to receive.

For example, if your local oscillator is 180MHz, and there are two
    incoming signals, 179MHz and 181MHz, a simple demodulator wouldn't be
    able to tell them apart.

### Why are IQ signals important?
---
The primary use for IQ signals can best be explained through the use 
    of **constellation diagrams**.

Since the I signal is real, and the Q signal is imaginary, we can plot the 
    output on the complex plane.

Now let's have a look at some constellation diagrams under a few modulation 
    schemes.

### Binary Phase Shift Keying (BPSK)
---
First of all let's have a look at BPSK.

Running the script with the `BPSK` option uncommented

```
python3 Q4_1_1.py
```

Will produce the following output:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_1.png"
    style="background-color:white;padding:5px;border-radius:3px"
    width="500px">

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_1_2.png"
    style="background-color:white;padding:5px;border-radius:3px"
    width="500px">

The 4 bit series that was encoded for me was `1010` (yours might be slightly
    different since the sequence is randomly generated).

We can see that for the I signal (real) data, the average value of the signal is
    either:

- -0.5, or
- 0.5

The Q signal (Imag) data on the other hand always has an average value of zero.

If we combine these two signals into a complex number series, and plot them on
    the complex plane, we'd get the following constellation diagram:

<img src="https://shopdelta.eu/obrazki_art/dpsk_img2_d.jpg"
    style="background-color:white;padding:5px;border-radius:3px"
    width="500px">

So we have a way to recover binary data from a carrier wave signal, and graph 
    it, nice.

You might be wondering, why do all of this? Trust me, it'll be a life saver 
    in the future.

### Quadrature Phase Shift Keying (QPSK)
---
Next let's have a look at QPSK

Running the script with the `QPSK` option uncommented

```
python3 Q4_1_1.py
```

Will produce the following results:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_1_3.png"
    style="border-radius:3px"
    width="500px">

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_1_4.png"
    style="border-radius:3px"
    width="500px">

The 4 bit series that was encoded for me was `0123`.

You might be thinking "what? there's no such thing as a 2 or 3 bit, what gives?"

To that I'd say, yes indeed you're correct. However, consider the following
    coversion:

| Decimal | Binary |
| :---: | :---: |
| 0 | 00 |
| 1 | 01 |
| 2 | 10 |
| 3 | 11 |

"Ah!" I hear you say, "We're not just encoding binary bits anymore, we're 
    encoding two bits at a time".

Pretty much, technically you can break any sequence of bits of an even length
    into a number of two bit groups. If you've got an odd number of bits, just
    pad with zeros or something (after all, the interpretation of data is
    up to the receiving end, and we have protocols for that!).

The astute engineer will probably have guessed that QPSK has double the bitrate
    of BPSK, and again you'd be correct, however we'll discuss that in more
    depth in a future part.

Using the same logic as above, and plotting this on a constellation diagram
    (and phase shifting the entire signal by 45 degrees counter-clockwise), 
    will give us the following constellation diagram (the bit positions are 
    not exactly correct, just ignore that for now).

<img src="https://shopdelta.eu/obrazki_art/dpsk_img3_d.jpg"
    style="background-color:white;padding:5px;border-radius:3px"
    width="500px">

## Noise in signals

We can simulate noise in our signal by adding some random value multiplied by
    some noise power value during the RX phase of our code.

The noise power is computed from a desired SNR value in dB. Here are some 
    examples of varying SNR for the BPSK signal `0111 0111`

### SNR = 20dB
<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_2_1.png"
    style="border-radius:3px"
    width="500px">

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_2_2.png"
    style="border-radius:3px"
    width="500px">

### SNR = 10dB
<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_2_3.png"
    style="border-radius:3px"
    width="500px">

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_2_4.png"
    style="border-radius:3px"
    width="500px">

### SNR = 1dB
<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_2_5.png"
    style="border-radius:3px"
    width="500px">

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/q4_1_2_6.png"
    style="border-radius:3px"
    width="500px">

Despite this, none of the different SNR values produced any biterrors in the 
    decoder. As you'll see in later parts, BPSK is more robust against noise 
    than QPSK or QAM, and the 802.11 spec takes full advantage of this.

You can uncomment the `QPSK()` function in `Q4_1_2.py` if you're interested in
    seeing a QPSK modulated waveform corrupted by noise.

## Synchronisation and decoding

Now let's have a look at some synchronisation exercises. This binary, 
    `freqA.bin`, is from one of my university courses. The goal was to construct
    a script that could be used to extract the binary information out a QPSK
    data packet, using **energy detection**

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_1.PNG"
    style="border-radius:3px"
    width="500px">

Energy detection is probably the simplest synchronisation technique.

Every data packet has a 4ms (8000 sample) null space prepended to it, allowing
    a receiver to determine where the start of the data packet is.

It's not the most robust or efficient synchronisation scheme, but it will work
    for our purposes.

If we run the following command

```
python3 Q4_2_1.py
```

We should get the following output:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_2.png"
    style="border-radius:3px"
    width="500px">

Let's zoom in to the first segment (first 'blip' from the left)

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_3.png"
    style="border-radius:3px"
    width="500px">

Here the blue lines represent where the synchroniser thinks the data segment is,
    and the orange is the actual QPSK data (non-decoded).

The next step is to filter our data to get rid of the high frequency noise.

Since this is a digital radio, we can simply apply a **simple moving average** 
    (SMA), which acts as a low pass filter. We will need to tune the averaging
    period however, I've set it as 25 for now.

If we do this, we should see the following:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_4.png"
    style="border-radius:3px"
    width="500px">

Now that looks more like our QPSK waveform, but it looks as if it's distorted
    somewhat. To fix this, we'll have to apply some frequency synchronisation
    processing to our signal.

If we demodulate our signal into an IQ signal, we should see the following.

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_5.png"
    style="border-radius:3px"
    width="500px">

Since this IQ signal has real and imaginary components, we can plot this
    data on a constellation diagram

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_7.png"
    style="border-radius:3px"
    width="500px">

We can also multiply each sample by a rotation vector (since each sample in
    the combined IQ signal has both a real and imaginary component)

```
np.exp(1j*np.pi/4)
```

to undistort the signal.

Graphically speaking, this has the effect of 'unwinding' the distortion in the
    constellation diagram, leaving us with the following plot:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_8.png"
    style="border-radius:3px"
    width="500px">

Which would give us the following averaged QPSK signal data:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_6.png"
    style="border-radius:3px"
    width="500px">

The next step is to decode the message and figure out what data is being
    transmitted.

However, there are no other signals included in the segment to assist with
    frequency synchronisation (i.e.  We don't know the endianness for the data,
        what symbols correspond to what IQ signal combo, etc). 

Hence, the best we can do is simply to rotate
    the signal data around to all 4 orientations, and then try to visually
    extract that data using our intuition (I'll explain how SDRs do this 
    automatically a bit further on).

Performing these combinations:
- 4 x phase combinations
- 2 x Endianness
- 5 x bytes per combo
- 4 x symbols per byte

We get the following output for our data

```
Frequency Synchronisation Output:
----------------------------
0.: ∟L♀\8
1.: 4105,   <--- Word
2.: aQ¡M
3.: IFEJq
4.: ¶æ¦ö
5.:   
6.: Ë;û♂ç
7.: ãìïàÛ
10113    
----------------------------
0.: ∟∟P¼ 
1.: 44♣> 
2.: aa¥UÁ
3.: IIZUC
4.: ¶¶úª▬
5.: ª
6.: ËË☼ÿk
7.: ããðÿé
18755    
----------------------------
0.: ~ªNN♫
1.: ½ª±±°
2.: ÿS
3.: ÂÿÆÆÅ
4.: Ôää¤
5.: ↨→
6.: )U99ù
7.: hUllo
27394
----------------------------
0.: ▲♫↕
1.: ´°²²

2.: cSÓÓg
3.: ÉÅÇÇÙ
4.: ´¤$$¸
5.: ▲→↑↑.
6.: ÉùyyÍ
7.: comms   <--- Word
36035
----------------------------
0.: ¥¥¥µ
1.: ZZZ^
2.: úúúÊç
3.: ¯¯¯£Û
4.: ☼☼☼▼8
5.: ðððô,
6.: PPP`M
7.: ♣♣♣ q
44676
----------------------------
0.: v¶æ¦↕
1.: 

2.: Ë;ûg
3.: âãìïÙ
4.: Ü∟L♀¸
5.: 7410.   <--- Word
6.: !aQÍ
7.: HIFEs
53316
----------------------------
0.: ÀðääT
1.: ♥☼§
.: §♣99©
3.: TPllj
4.: jZNNþ
5.: ©¥±±¿
6.: ¿¯♥
7.: þúÆÆÀ
61958
----------------------------
0.: ¤¤$$¨
1.: →→↑↑*
2.: ùùyyý
3.: oomm⌂
4.: ♫♫☻
5.: °°²²
6.: SSÓÓW
7.: ÅÅÇÇÕ
70597
----------------------------
0.: Ë;û♂ç
1.: ãìïàÛ
2.: ∟L♀\8
3.: 4105,  <--- Word
4.: aQ¡M
5.: IFEJq
6.: ¶æ¦ö
7.: 
79238
----------------------------
0.: ËË☼ÿk
1.: ããðÿé
2.: ∟∟P¼
3.: 44♣>
4.: aa¥UÁ
5.: IIZUC
6.: ¶¶úª▬
7.: ª
87880
----------------------------
0.: )U99¹
1.: hUlln
2.: ~ªNNÎ
3.: ½ª±±³
4.: ÿ‼
5.: ÂÿÆÆÄ
6.: Ôääd
7.: ↨↓
6519
----------------------------
0.: ÉùyyÍ
1.: comms   <--- Word
2.: ▲♫↕
3.: ´°²²

4.: cSÓÓg
5.: ÉÅÇÇÙ
6.: ´¤$$¸
7.: ▲→↑↑.
 ```

The words we get out is `comms4105,` (the undergraduate course code)
    and `comms7410.` (the postgraduate course code).

## How do SDR's do time synchronisation automatically?

As you might have guessed, the time synchronisation for radio data is not done
    by humans.

Using this energy scheme, it is indeed possible, but there are other, much 
    faster ways of doing so.

Instead of using energy detection, we can prepend every QPSK data segment with
    a known BPSK segment like so:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_9.PNG"
    style="border-radius:3px"
    width="500px">

Then, using a simple technique like autocorrelation on incoming data, we can
    find the start of the data sequence.

For example, if we run the following command

```
python3 Q4_2_2.py
```

We should get the following (manually tuned) constellation diagram:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_10.png"
    style="border-radius:3px"
    width="500px">

We'll assume that each QPSK data segment has the following BPSK waveform
    prepended to it.

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_11.png"
    style="border-radius:3px"
    width="500px">

Looking at a segment of incoming data, we can see the following:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_12.PNG"
    style="border-radius:3px"
    width="500px">

We can quite easily see the BPSK segments from the IQ signal view.

Performing the autocorrelation gives us the following waveform:

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_13.png"
    style="border-radius:3px"
    width="500px">

The peaks represent when the BPSK synchronisation waveform is most correlated 
    with the signal data waveform.

Knowing that this would technically mean that the peak lies at the centre of the
    BPSK sync waveform, we can offset the sample data by a known amount to
    put us at the start of the QPSK data sequence.

If we then decode this QPSK signal data, using the same guess and check 
    technique we performed previously, we get the following:

```
QPSK decoded data:

_·Ãg
õÞÂÃÙ
 ÈÔ¶¸
     
#↨¶. 
õ↔)iÍ
_this   <--- Word
     
b~¾↕ 
 ½¾
```

## How do SDR's do frequency synchronisation automatically?

Similar to how time synchronisation works, We can include a segment of
    frequency synchronisation (or "training") data that is known by the 
    receiver.

<img src="https://storage.googleapis.com/starfighter-public-bucket/wiki_images/resume_photos/ModernComms/Prac1/sync_14.PNG"
    style="border-radius:3px"
    width="500px">

The receiver would then use this information to perform the frequency 
    synchronisation. There are many ways to do this, a popular method is 
    **course-fine synchronisation**.

### Course Synchronisation
---
This technique uses an auto-correlation index to detect peaks and some
    characteristic jumps in amplitude or phase curves.

### Fine Synchronisation
---
This technique uses a cross-correlation indicator of the received signal with 
    the training sequence, and by detection of some characteristic patterns in 
    amplitude of the resulting waveform.

## Closing comments

Well I hope you learned something about the basics of modern communication
    systems. There will be more to come with the next couple repos coming out
    in the near future.

Until then, stay tuned!

- Despicable-bee