import numpy as np

def load_iq_file(path, dtype=np.complex64):
    return np.fromfile(path, dtype=dtype)
