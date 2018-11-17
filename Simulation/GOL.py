import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as animation
import scipy.ndimage as ndi


def render(matrices, speedOfLife):
    f = plt.figure()
    reel = []
    for matrix in matrices:
        frame = plt.imshow(matrix,'gray_r')
        reel.append([frame])
    a = animation.ArtistAnimation(f, reel, interval=speedOfLife,blit=True,repeat_delay=1000)
    plt.show()


def initialize_life():
    width = int(input('Enter width: '))
    height = int(input('Enter height: '))
    initial_state = np.random.randint(0, 2, width * height).reshape((width, height))
    plt.imshow(initial_state, 'gray_r')
    plt.title('Initial State [GOL]')
    plt.show()
    return initial_state


def run(nGenerations, seed):
    neighbors = [[1, 1, 1],
                 [1, 0, 1],
                 [1, 1, 1]]

    generations = []
    gen = 0
    while gen <= nGenerations:
        cells = ndi.convolve(seed, neighbors)
        nextState = seed.flatten()
        II = 0
        for cell in cells.flatten():
            # Check if its alive
            if nextState[II] == 1:
                if 2 <= cell < 4:
                    nextState[II] = 1
                else:
                    nextState[II] = 0
            if nextState[II] == 0 and cell == 2:
                nextState[II] = 1
            else:
                nextState[II] = 0
            II += 1
        generations.append(nextState.reshape((seed.shape[0], seed.shape[1])))
        gen += 1
        seed = nextState.reshape((seed.shape[0], seed.shape[1]))
    # Animate the Game of Life Simulation!
    render(generations, 100)


def main():
    initial_state = initialize_life()
    run(int(input('Enter Number of Generations to Simulate: ')), initial_state)


if __name__ == '__main__':
    main()
