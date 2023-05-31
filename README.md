# Random-Number-Generator

This is my attempt at a random number generator, particularly one with less predictability.

This random number generator records audio (via a microphone) based on a duration you can set (default is 5). Using Short-Time Fourier Transform (STFT) or Fast Fourier Transform (FFT), the frequencies of the recording is isolated, taking the absolute values and finding the minimum and maximum values of these frequencies accordingly.

The frequencies are then normalized using:

$$\frac{f - f_\text{min}}{f_\text{max} - f_\text{min}}$$

This gives the frequencies now values between 0 and 1. The average of these frequencies are taken and the result outputted.

If you don't have a microphone, this won't work. If your recordings have only one tone, that is, the average frequency equals the individual frequencies, an error message will be produced.

In the future I hope to add more complexity, because as for now the values are typically quite low using my microphone. 

The advantage of this script is that it is very difficult to reproduce recordings, with background noise, microphone artefacts, etc. all playing a role.
