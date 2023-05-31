# Random-Number-Generator

This is my attempt at a random number generator, particularly one with less predictability.

This random number generator records audio (via a microphone) based on a duration you can set (default is 5 s). Using Short-Time Fourier Transform (STFT) or Fast Fourier Transform (FFT), the frequencies of the recording are isolated, taking the absolute values and finding the minimum and maximum values of these frequencies accordingly.

The frequencies are then normalized using:

$$f_\text{N} = \frac{f - f_\text{min}}{f_\text{max} - f_\text{min}}$$

This gives the frequencies now values between 0 and 1, exclusive. The average of these frequencies are taken and the result outputted.

If you don't have a microphone, this won't work. If your recordings have only one tone, that is, the average frequency equals the individual frequencies, an error message will be produced and this won't work.

In the future I hope to add more complexity, because as for now the values are typically quite low using my microphone. 

The advantage of this script is that it is very difficult to reproduce recordings, with background noise, microphone artefacts, etc. all playing a role.

## Arguments:
verbose : Either 0 or 1. 0 means nothing is printed, 1 means that a message is printed stating when recording starts.

method : What Fourier Transform method do you want to use, STFT or FFT?

duration : (in seconds). How long should the recording be? The longer, the better.

sampling_rate : The sample rate of the recording.

frame_size : The frame_size of the recording.

hop_length : The hop length of the recording.
