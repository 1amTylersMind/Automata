import numpy as np, matplotlib.pyplot as plt, matplotlib. animation as animation
import sys, os, time
import scipy.ndimage as ndi


def render(matrices, speedOfLife, isColor):
    f = plt.figure()
    reel = []
    for matrix in matrices:
        if isColor:
            frame = plt.imshow(matrix)
        else:
            frame = plt.imshow(matrix,'gray_r')
        reel.append([frame])
    a = animation.ArtistAnimation(f, reel, interval=speedOfLife,blit=True,repeat_delay=1000)
    plt.show()


def simulate(ngen, seed, conv):
    gen = 0
    generations = []
    neural = []
    while gen <= ngen:
        generations.append(seed)
        world = ndi.convolve(seed, conv).flatten()
        nextstate = seed.flatten()
        land = np.zeros(world.shape)
        II = 0
        for cell in world:
            """
            RULES THAT MODIFY NEXT_STATE
            """
            II += 1
        neural.append(world.reshape((seed.shape[0],seed.shape[1])))
        gen += 1
        seed = nextstate.reshape((seed.shape[0],seed.shape[1]))
    return generations, neural


def main():

    
    
if __name__ == '__main__':
    main()

