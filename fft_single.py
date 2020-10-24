import numpy as np
from queue import Queue


def norecur_FFT(x):
    """A non-recursive implementation of the 1D Cooley-Tukey FFT"""
    m = len(x)
    if m % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    else:
        loc_reverse = []
        for i in range(m):
            b = '{:0{width}b}'.format(i, width= int(np.log2(m)))
            loc_reverse.append(int(b[::-1], 2))
        x_reorder = x[loc_reverse]  # bit_reversal for the input of butterfly
        x_reorder_queue = Queue()  # queue to store all inputs of the loop(single raw input&partial result)
        for i in range(len(x_reorder)):
            x_reorder_queue.put([x_reorder[i]])  # put single elements of array
        counter = 0
        while x_reorder_queue.qsize() > 1:
            x_even = x_reorder_queue.get()
            x_odd = x_reorder_queue.get()
            n = len(x_even)
            N = 2 * n  # how many single elements involved
            factor = np.exp(-2j * np.pi * np.arange(N) / N)
            partial_result = np.concatenate([x_even+factor[:N//2]*x_odd, x_even+factor[N//2:]*x_odd])
            counter += 1
            x_reorder_queue.put(partial_result)  # put partial results as next step input
        return x_reorder_queue.get(), counter



x = np.arange(32)
#print(np.allclose(np.fft.fft(x), norecur_FFT(x)))
_, counter = norecur_FFT(x)
print(counter)