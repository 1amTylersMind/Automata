import os, sys, time, resource, numpy as np, scipy.ndimage as ndi
import matplotlib.pyplot as plt, matplotlib.animation as animation


class Utils:

    @staticmethod
    def swap(fname, destroy):
        data = []
        for line in open(fname, 'r').readlines():
            data.append(line.replace('\n', ''))
        if destroy:
            os.system('rm ' + fname)
        return data

    @staticmethod
    def check_mem_usage():
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return mem

    @staticmethod
    def filter_preview(matrix, conv, isColor):
        fig, ax = plt.subplots(1,2, figsize=(10,5))
        if isColor:
            ax[0].imshow(matrix)
            ax[1].imshow(ndi.convolve(matrix,conv,origin=0))
        else:
            ax[0].imshow(matrix, 'gray_r')
            ax[1].imshow(ndi.convolve(matrix,conv,origin=0),'gray_r')
        plt.show()


class AutomataImageProcessing:

    mask = [[]]
    state = [[]]
    ngen = 0
    simulation = []
    medians = []

    def __init__(self,initial_state,filta,depth):
        self.state = initial_state
        self.mask = filta
        self.ngen = depth

    def run(self, MODE):
        modes = {'mavg':0}
        gen = 0
        data = []
        while gen < self.ngen:
            data.append(self.state)
            world = ndi.convolve(self.state, self.mask).flatten()
            nextstate = np.zeros(self.state.shape).flatten()
            if modes[MODE] == 0:
                self.state = self.knowutiMeans(world,nextstate)
            gen += 1
        return data

    def knowutiMeans(self,world,nextstate):
        avg = world.mean()
        ii = 0
        for cell in world:
            if cell >=avg:
                nextstate[ii] += 1
            else:
                nextstate[ii] -= 1
            ii += 1
        return nextstate.reshape(self.state.shape[0],self.state.shape[1])

    @staticmethod
    def render(matrices, speedOfLife, isColor):
        f = plt.figure()
        reel = []
        for matrix in matrices:
            if isColor:
                frame = plt.imshow(matrix)
            else:
                frame = plt.imshow(matrix, 'gray_r')
            reel.append([frame])
        a = animation.ArtistAnimation(f, reel, interval=speedOfLife, blit=True, repeat_delay=1000)
        plt.show()


def preview():
    # test image (random seed)
    test_seed = np.random.randint(0, 2, 100).reshape((10, 10))
    # test filter
    simple_box = [[0, 1, 1, 1, 0],
                  [1, 2, 2, 2, 1],
                  [1, 2, 3, 2, 1],
                  [1, 2, 2, 2, 1],
                  [0, 1, 1, 1, 0]]
    # take a peek
    Utils.filter_preview(test_seed, simple_box, False)


def main():
    aip = AutomataImageProcessing(test_seed, simple_box, 10)
    film = aip.run('mavg')
    aip.render(film, 200, True)


if __name__ == '__main__':
    main()
