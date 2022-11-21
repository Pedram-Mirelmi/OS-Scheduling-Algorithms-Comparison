from numpy.random import normal, uniform
import numpy as np

# Pedram - Mirelmi - 610398176

def getNormalRandomNumber(mean: int, std: int, in_range: int, shape: tuple) -> np.ndarray:
    total = normal(mean, std, size=shape[0]*shape[1])
    total = total[np.logical_and(total>0, total<=in_range)].astype(int)
    valid_count = len(total) - (len(total)%shape[1])
    total = total[:valid_count]
    return np.reshape(total, newshape=(len(total)//shape[1], shape[1]))
    

def getUniformRandomNumber(in_range, shape: tuple) -> np.ndarray:
    total = uniform(low=0, high=in_range, size=shape).astype(int)
    # valid_count = len(total) - (len(total)%shape[1])
    # total = total[:valid_count]
    # return np.reshape(total, newshape=(len(total)//shape[1], shape[1]))
    return total

