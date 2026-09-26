import wave
import sys
import numpy as np

def analyze_wav(filename):
    try:
        with wave.open(filename, 'rb') as wf:
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            
            print(f"Format: PCM, Channels: {channels}, Sample Rate: {framerate}Hz, Bit Depth: {sample_width*8} bits")
            print(f"Duration: {n_frames / float(framerate):.3f} seconds")
            
            raw_data = wf.readframes(n_frames)
            
            if sample_width == 2:
                data = np.frombuffer(raw_data, dtype=np.int16)
            elif sample_width == 4:
                data = np.frombuffer(raw_data, dtype=np.int32)
            else:
                data = np.frombuffer(raw_data, dtype=np.int8)

            rms = np.sqrt(np.mean(data.astype(np.float64)**2))
            peak = np.max(np.abs(data))
            
            print(f"RMS Audio Level: {rms:.2f}")
            print(f"Peak Audio Level: {peak}")
            if rms < 10:
                print("CONCLUSION: SILENCE OR EXTREMELY LOW VOLUME")
            else:
                print("CONCLUSION: AUDIO CONTAINS SIGNAL")
    except Exception as e:
        print(f"Error analyzing WAV: {e}")

analyze_wav("local_test.wav")
