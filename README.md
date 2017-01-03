# Spectrometer

The code is able to analyse the sound spectrum.
We obtain two plots
1. Energy Vs Frequency
2. Amplitude Vs Time
The sound frequency is altered to obtain different band spectrum plots.




Futher Work :
Turning a normal headphone into a Noise-Cancellation Headphone.
The main idea is to use multiple microphones with multiple channels near the listener's ear, that will capture the surrounding noise. Then on the data obtained I will do the signal processing, and produce 180 degree phase-shifted signal, which will then be channeled into the headphones.

The beauty as well as the intimidating fact about it is to do all these things "synchronously" with "minimum latency", else the waves won't super-impose properly to produce 0 dB sound. And of-course the signal processing should be intelligent enough to distinguish between white noise and actual sound.

So before I could design Second Phase of Signal Processing, I need a lot of analysis and understanding on the nature of noise and how it manifests itself and distorts the actual sound waves during transmission. Therefore without the perfection of this Signal Processing part, the quality of noise-cancellation would be compromised.

So for the past week I was hell-bent to make the tool to assist me in this analysis.
As we know that actual sound wave is Analog, so its converted by the sound-card into Digital and then encoded through Pulse Coded Modulation (PCM). So the per second data obtained is large because the sound is sampled at a minimum 44100 times / sec for good quality.

Thus my Tool takes the raw data from the PCM Encoded sound coming from the input stream of the sound-card (microphone) and regenerates graphically the corresponding wave for my analysis.
It was completed just now, and this baby generated the graph on my 5 second stereo recorded sound. Totally excited and attaching the Snapshot for the very first Plot ever made by it.
This part of application is entirely coded in Python and depicts the data coming from both the channels of the microphone.

Tools like this exist in the major studio quality editing softwares used by professionals. However I wanted to make my own, so that I can have full flexibility in bending it's properties as per my requirements.

Now using this home-brewed tool I would be designing the Signal Processing Algorithm
