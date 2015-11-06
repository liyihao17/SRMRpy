import numpy as np
from srmrpy.segmentaxis import segment_axis

def simple_energy_vad(x, fs, framelen=0.02, theta_main=30, theta_min=-55):
    '''Simple energy voice activity detection algorithm based on energy thresholds as described in Kinnunen & Rajan '''
    # Split signal in frames
    framelen = int(framelen * fs)
    frames = segment_axis(x, length=framelen, overlap=0, end='pad')
    frames_zero_mean = frames - frames.mean(axis=0)
    frame_energy = 10*np.log10(1/(framelen-1) * (frames_zero_mean**2).sum(axis=1) + 1e-6)
    max_energy = max(frame_energy)
    speech_presence = (frame_energy > max_energy - theta_main) & (frame_energy > theta_min)
    x_vad = np.zeros_like(x)
    for idx, frame in enumerate(frames):
        if speech_presence[idx]:
            x_vad[idx*framelen:(idx+1)*framelen] = s[idx*framelen:(idx+1)*framelen]
        else:
            x_vad[idx*framelen:(idx+1)*framelen] = 0
    return x_vad, speech_presence

if __name__ == '__main__':
    from scipy.io.wavfile import read as readwav
    from matplotlib import pyplot as plt

    fs, s = readwav('/Users/jfsantos/Downloads/OUT_2015_10_29/SCwoArtifacts/Lecture_Room_2_1_FCJF0_reverb-only.wav')
    s  = s.astype('float')/np.iinfo(s.dtype).max
    s_vad, speech_presence = simple_energy_vad(s, fs)

    plt.plot(s)
    plt.plot(s_vad - 1, 'g')
    plt.show()
