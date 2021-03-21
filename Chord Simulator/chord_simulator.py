
import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk    

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 0.5      # Decay time (seconds)
fA4 = 440    # Frequency (Hz)
semitone = 2**(1/12)


# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude

# Karplus-Strong paramters
K = 1
N = 64

chords = [[130.81, 164.81, 196, 261.63, 329.63],
          [146.83, 174.61, 220, 293.66, 349.23],
          [164.81, 196, 246.94, 329.63, 392],
          [174.61, 220, 261.63, 349.23, 440],
          [196, 246.94, 293.66, 392, 493.88],
          [220, 261.63, 329.63, 440, 523.25]]

global chordsn 

chordsn = chords[0]

def filterab(f):
	om1 = 2.0 * pi * float(f)/RATE
	om = [om1, 2*om1, 3*om1, 4*om1, 5*om1]
	a = [[1, -2*r*cos(omi), r**2] for omi in om]
	b = [[r*sin(omi)] for omi in om]
	return a,b

 
def set_chords():
	f1 = chordsn[0]
	a1,b1 = filterab(f1)
	f2 = chordsn[1]
	a2,b2 = filterab(f2)
	f3 = chordsn[2]
	a3,b3 = filterab(f3)
	f4 = chordsn[3]
	a4,b4 = filterab(f4)
	f5 = chordsn[4]
	a5,b5 = filterab(f5)

f1 = chordsn[0]
a1,b1 = filterab(f1)
f2 = chordsn[1]
a2,b2 = filterab(f2)
f3 = chordsn[2]
a3,b3 = filterab(f3)
f4 = chordsn[3]
a4,b4 = filterab(f4)
f5 = chordsn[4]
a5,b5 = filterab(f5)

harmonic = np.array([1, 0.7, 0.2, 0.6, 0.1])

root = Tk.Tk()

H1 = Tk.DoubleVar()
H2 = Tk.DoubleVar()
H3 = Tk.DoubleVar()
H4 = Tk.DoubleVar()
H5 = Tk.DoubleVar()

H1.set(harmonic[0])
H2.set(harmonic[1])
H3.set(harmonic[2])
H4.set(harmonic[3])
H5.set(harmonic[4])

H1scale = Tk.Scale(root, label = 'f*1', variable = H1, from_ = 0, to = 2, resolution = 0.01)
H2scale = Tk.Scale(root, label = 'f*2', variable = H2, from_ = 0, to = 2, resolution = 0.01)
H3scale = Tk.Scale(root, label = 'f*3', variable = H3, from_ = 0, to = 2, resolution = 0.01)
H4scale = Tk.Scale(root, label = 'f*4', variable = H4, from_ = 0, to = 2, resolution = 0.01)
H5scale = Tk.Scale(root, label = 'f*5', variable = H5, from_ = 0, to = 2, resolution = 0.01)


#harmonic = np.array([0, 0, 1, 0, 0])

ORDER = 2   # filter order

states1 = np.zeros((5, ORDER))
states2 = np.zeros((5, ORDER))
states3 = np.zeros((5, ORDER))
states4 = np.zeros((5, ORDER))
states5 = np.zeros((5, ORDER))

x1 = np.zeros(BLOCKLEN)
x2 = np.zeros(BLOCKLEN)
x3 = np.zeros(BLOCKLEN)
x4 = np.zeros(BLOCKLEN)
x5 = np.zeros(BLOCKLEN)

y1 = np.zeros((5, BLOCKLEN))
y2 = np.zeros((5, BLOCKLEN))
y3 = np.zeros((5, BLOCKLEN))
y4 = np.zeros((5, BLOCKLEN))
y5 = np.zeros((5, BLOCKLEN))


# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True
KEYPRESS = False

def my_function(event):
    global CONTINUE
    global KEYPRESS
    global xn
    global f1,f2,f3,f4,f5
    global a1,b1
    global a2,b2
    global a3,b3
    global a4,b4
    global a5,b5
    
    chordsn = chords[0]
  
    print('You pressed ' + event.char)
    
    if event.char == "1":
        chordsn = chords[0]
        f1 = chordsn[0]
        a1,b1 = filterab(f1)
        f2 = chordsn[1]
        a2,b2 = filterab(f2)
        f3 = chordsn[2]
        a3,b3 = filterab(f3)
        f4 = chordsn[3]
        a4,b4 = filterab(f4)
        f5 = chordsn[4]
        a5,b5 = filterab(f5)
        
    if event.char == "2":
        chordsn = chords[1]
        f1 = chordsn[0]
        a1,b1 = filterab(f1)
        f2 = chordsn[1]
        a2,b2 = filterab(f2)
        f3 = chordsn[2]
        a3,b3 = filterab(f3)
        f4 = chordsn[3]
        a4,b4 = filterab(f4)
        f5 = chordsn[4]
        a5,b5 = filterab(f5)
        
    if event.char == "3":
        chordsn = chords[2]
        f1 = chordsn[0]
        a1,b1 = filterab(f1)
        f2 = chordsn[1]
        a2,b2 = filterab(f2)
        f3 = chordsn[2]
        a3,b3 = filterab(f3)
        f4 = chordsn[3]
        a4,b4 = filterab(f4)
        f5 = chordsn[4]
        a5,b5 = filterab(f5)
    
    if event.char == "4":
        chordsn = chords[3]
        f1 = chordsn[0]
        a1,b1 = filterab(f1)
        f2 = chordsn[1]
        a2,b2 = filterab(f2)
        f3 = chordsn[2]
        a3,b3 = filterab(f3)
        f4 = chordsn[3]
        a4,b4 = filterab(f4)
        f5 = chordsn[4]
        a5,b5 = filterab(f5)
    
    if event.char == "5":
        chordsn = chords[4]
        f1 = chordsn[0]
        a1,b1 = filterab(f1)
        f2 = chordsn[1]
        a2,b2 = filterab(f2)
        f3 = chordsn[2]
        a3,b3 = filterab(f3)
        f4 = chordsn[3]
        a4,b4 = filterab(f4)
        f5 = chordsn[4]
        a5,b5 = filterab(f5)
    
    if event.char == "6":
        chordsn = chords[5]
        f1 = chordsn[0]
        a1,b1 = filterab(f1)
        f2 = chordsn[1]
        a2,b2 = filterab(f2)
        f3 = chordsn[2]
        a3,b3 = filterab(f3)
        f4 = chordsn[3]
        a4,b4 = filterab(f4)
        f5 = chordsn[4]
        a5,b5 = filterab(f5)
        
    
    if event.char == 'a':
        xn = 1

    if event.char == 's':
        xn = 2
        
    if event.char == 'd':
        xn = 3
        
    if event.char == 'f':
        xn = 4
        
    if event.char == ' ':
        xn = 5
    
    if event.char not in ['a','s','d','f',' ']:
        xn = 6  
    
    
    if event.char == 'q':
      print('Good bye')
      CONTINUE = False
      
    KEYPRESS = True


root.bind("<Key>", my_function)

s1 = Tk.StringVar()
s1.set('press 1~6 to select chords')

s2 = Tk.StringVar()
s2.set('1=C  2=Dm  3=Em  4=F  5=G  6=Am')

s3 = Tk.StringVar()
s3.set('press a,s,d,f,space to play')

s4 = Tk.StringVar()
s4.set('use sliders to adjust the amplitude of harmonic waves')

s5 = Tk.StringVar()
s5.set('press Q to quit')

L1 = Tk.Label(root, textvariable = s1)
L2 = Tk.Label(root, textvariable = s2)
L3 = Tk.Label(root, textvariable = s3)
L4 = Tk.Label(root, textvariable = s4)
L5 = Tk.Label(root, textvariable = s5)

L1.pack()
L2.pack()
L3.pack()
L4.pack()
L5.pack()
H1scale.pack(side = Tk.LEFT)
H2scale.pack(side = Tk.LEFT)
H3scale.pack(side = Tk.LEFT)
H4scale.pack(side = Tk.LEFT)
H5scale.pack(side = Tk.LEFT)



print('Press keys for sound.')
print('Press "q" to quit')

while CONTINUE:
    root.update()
    
    harmonic = np.array([H1.get(), H2.get(), H3.get(), H4.get(), H5.get()])

    if KEYPRESS and CONTINUE:
        # Some key (not 'q') was pressed
        
        if xn == 1:
            x1[0] = 10000.0
        
        if xn ==2 :
            x2[0] = 10000.0 
            
        if xn ==3 :
            x3[0] = 10000.0 
        
        if xn == 4:
            x4[0] = 10000.0
        
        if xn == 5:
            x5[0] = 10000.0
        
            
        if xn == 6:
            x1[0] = 0
            x2[0] = 0
            x3[0] = 0
            x4[0] = 0
            x5[0] = 0
    
    for i in range(5):
        [y1[i], states1[i]] = signal.lfilter(b1[i], a1[i], x1, zi = states1[i])
        [y2[i], states2[i]] = signal.lfilter(b2[i], a2[i], x2, zi = states2[i])
        [y3[i], states3[i]] = signal.lfilter(b3[i], a3[i], x3, zi = states3[i])
        [y4[i], states4[i]] = signal.lfilter(b4[i], a4[i], x4, zi = states4[i])
        [y5[i], states5[i]] = signal.lfilter(b5[i], a5[i], x5, zi = states5[i])

    x1[0] = 0.0
    x2[0] = 0.0
    x3[0] = 0.0
    x4[0] = 0.0
    x5[0] = 0.0
    
    y1out = np.sum(y1*harmonic[:,None],axis = 0)
    y2out = np.sum(y2*harmonic[:,None],axis = 0)
    y3out = np.sum(y3*harmonic[:,None],axis = 0)
    y4out = np.sum(y4*harmonic[:,None],axis = 0)
    y5out = np.sum(y5*harmonic[:,None],axis = 0)
    
    yout = y1out + y2out + y3out + y4out + y5out
    

    KEYPRESS = False

    yout = np.clip(yout.astype(int), -MAXVALUE, MAXVALUE)     # Clipping

    binary_data = struct.pack('h' * BLOCKLEN, *yout);    # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
