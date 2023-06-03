import sounddevice as sd
import numpy as np
import librosa
import sys
import secrets

def randomGenerator(verbose=None,method=None,duration=None,sampling_rate=None,frame_size=None,hop_length=None):
    # verbose can either be 0 or 1.
    # If 0, nothing is printed. If 1, you are informed when recording starts.
    
    # Set the frame size and hop length (adjust these values as needed)
    if frame_size == None:
        frame_size = 2048
    if hop_length == None:
        hop_length = 512

   # Set the duration of the audio recording (in seconds)
    if duration == None:
       duration = 5

   # Set the sampling rate
    if sampling_rate == None:
        sampling_rate = 44100

   # Choose the Fourier Transform method (FFT or STFT)
    if method == None:
        method = "STFT"

    if verbose == None or verbose != 1:
        verbose = 0

   # Record audio
    if verbose == 1:
        print("Recording Audio!")
    audio = sd.rec(int(duration * sampling_rate), channels=1)
    sd.wait()

    # Convert audio to mono and normalize the amplitude
    audio = audio.squeeze()
    audio /= np.max(np.abs(audio))
    
    # Noise is generated using the cryptographically secure secrets method. Even if this eventually becomes biased, the average user will struggle to bias the rest of the work.
    noise = secrets.randbits(53) / (2 ** 53)
    noise_sign = round(secrets.randbits(53) / (2 ** 53))
 
   # If STFT is chosen, we normalized the absolute values of the frequencies and then take the average
    if method == "STFT" or method == "stft":
        # Apply the Short-Time Fourier Transform (STFT) to obtain frequency components
        stft = librosa.stft(audio, n_fft=frame_size, hop_length=hop_length)
 
        # Calculate the magnitudes of frequency components
        magnitude = np.abs(stft)

        Max_Value = -1*sys.float_info.max
         
        for i in range(len(magnitude)):
            for j in range(len(magnitude[i])):
                if magnitude[i][j] > Max_Value:
                    Max_Value = magnitude[i][j]

        Min_Value = sys.float_info.max
        for i in range(len(magnitude)):
            for j in range(len(magnitude[i])):
                if magnitude[i][j] < Min_Value:
                    Min_Value = magnitude[i][j]   

        normalized_frequencies = []
        for i in range(len(magnitude)):
            frequencies = []
            for j in range(len(magnitude[i])):
                frequencies.append((magnitude[i][j] - Min_Value)/(Max_Value - Min_Value))
            normalized_frequencies.append(frequencies)
         
        # Calculate the average frequency values for each frame
        average_frequency = np.mean(np.mean(np.array(normalized_frequencies), axis=0))

        if np.abs(np.mean(np.mean(np.array(normalized_frequencies/average_frequency), axis=0))) < 0.001:
            print("Audio is one/no tone, so it would make the number generation predictable. Try again!")
            return randomGenerator(verbose,method,duration,sampling_rate,frame_size,hop_length)
        else:
            if noise_sign == 0:
                if average_frequency + noise >= 0 or average_frequency + noise <= 1:
                    return average_frequency + noise
                else:
                    return randomGenerator(verbose,method,duration,sampling_rate,frame_size,hop_length)
            elif noise_sign == 1:
                if np.abs(average_frequency - noise) >= 0 or np.abs(average_frequency + noise) <= 1:
                    return np.abs(average_frequency - noise)
                else:
                    return randomGenerator(verbose,method,duration,sampling_rate,frame_size,hop_length)
 
   # If FFT is chosen, we normalized the absolute values of the frequencies and then take the average    
    else:
        # Apply the Fast Fourier Transform (FFT) to obtain frequency components
        fft_result = np.fft.fft(audio, n=frame_size)
        frequencies = np.fft.fftfreq(frame_size, d=1.0/sampling_rate)

        # Calculate the magnitudes of frequency components
        magnitude = np.abs(fft_result)

        Max_Value = max(magnitude)
        Min_Value = min(magnitude)

        normalized_frequencies = []
        for i in range(len(magnitude)):
            normalized_frequencies.append((magnitude[i] - Min_Value)/(Max_Value - Min_Value))

        average_frequency = np.mean(normalized_frequencies)

        if np.abs(np.mean(np.array(normalized_frequencies/average_frequency))) < 0.001:
            print("Audio is one/no tone, so it would make the number generation predictable. Try again!")
            return randomGenerator(verbose,method,duration,sampling_rate,frame_size,hop_length)
        else:
            if noise_sign == 0:
                if average_frequency + noise >= 0 or average_frequency + noise <= 1:
                    return average_frequency + noise
                else:
                    return randomGenerator(verbose,method,duration,sampling_rate,frame_size,hop_length)
            elif noise_sign == 1:
                if np.abs(average_frequency - noise) >= 0 or np.abs(average_frequency + noise) <= 1:
                    return np.abs(average_frequency - noise)
                else:
                    return randomGenerator(verbose,method,duration,sampling_rate,frame_size,hop_length)
