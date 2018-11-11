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
        land = np.zeros(world.shape).flatten()
        II = 0
        for cell in world:
            """
            RULES THAT MODIFY NEXT_STATE
            """
            if cell >= 20:
                nextstate[II] = 1
                land[II] = 0
            if cell <= 5 or land[II] > 10:
                nextstate[II] = 0
                land[II] +=1
            if cell > 27 and np.sin(II/360) > 1:
                nextstate[II] = 1
            if nextstate[II] == 1 and cell == 32 and np.sin(II/270) >0:
                land[II] += 1
                nextstate[II] = 0
            II += 1
        gen += 1
        neural.append(world.reshape((seed.shape[0],seed.shape[1])))
        seed = nextstate.reshape((seed.shape[0],seed.shape[1]))
    return generations, neural


def galactic(epochs, space, lens):
    gen = 0
    generations = []
    neural = []
    while gen <= epochs:
        generations.append(space)
        universe = ndi.convolve(space,lens).flatten()
        step = space.flatten()
        ii = 0
        for position in universe:
            ''' Rules to Modify '''
            if position >= 12:
                step[ii] -= 1
            elif step[ii] == 0:
                step[ii] += 1
            if position == 8:
                step[ii] -= 1
            if position == 3 and step[ii] == 0:
                step[ii] += 1
            if step[ii] == 255 or step[ii] == 22:
                step[ii] -= 1

            ii += 1
        gen += 1
        neural.append(universe.reshape((space.shape[0], space.shape[1])))
        space = step.reshape((space.shape[0], space.shape[1]))
    return generations, neural


def main():

    if 'andromeda' in sys.argv:
        simple_seed = np.random.randint(0, 2, 40000).reshape((200, 200))

        test_img_slice = plt.imread('/media/root/DB0/andromeda.jpg')
        test_img_slice = test_img_slice[500:900, 1000:1400, 0] / 3 + \
                         test_img_slice[500:900, 1000:1400, 1] / 3 + \
                         test_img_slice[500:900, 1000:1400, 2] / 3

        field = [[1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 1],
                 [1, 2, 0, 2, 1],
                 [1, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1]]

        sim, cells = simulate(50, test_img_slice, field)
        render(sim, 100, False)
        render(cells, 100, True)

        plt.imshow(test_img_slice, 'gray')
        plt.show()
        print "TEST IMAGE: "
        print test_img_slice.shape

    elif 'science' in sys.argv:
        g = plt.imread('/media/root/CoopersDB/SPACE.jpg')
        opt = int(input('Enter granularity for simulation[0-255]: '))
        granularity = np.arange(50,255)
        galaxy = (g[:, :, 0]/3 + g[:, :, 1]/3 + g[:, :, 2]/3)/granularity[opt]

        explorer = np.array([[1, 0, 0, 0, 1],
                            [0, 1, 1, 1, 0],
                            [1, 1, 1, 1, 1],
                            [0, 1, 1, 1, 0],
                            [1, 0, 0, 0, 1]])

        f0 = [[2,0,0,0,0,0,2],
              [0,1,1,1,1,1,0],
              [0,1,0,0,0,1,0],
              [2,1,0,1,0,1,2],
              [0,1,0,0,0,1,0],
              [0,1,1,1,1,1,0],
              [2,0,0,0,0,0,2]]

        f, ax = plt.subplots(1,2)
        ax[0].imshow(galaxy, 'inferno_r')
        ax[1].imshow(ndi.convolve(galaxy,explorer),'gray')
        plt.show()
        seed = ndi.convolve(galaxy,explorer)

        print "Analyzing Galaxy of shape "+str(seed.shape)
        if int(input('Enter 1 to continue:\n'))==1:
            dt0 = time.time()    # start the clock
            # run the simulation to eat away at empty space in the galaxy
            sim, cells = galactic(50, seed, f0)
            print str(time.time() - dt0) + "s"
            # Now Render the simulation, with step size and isColor args
            render(sim, 100,True)

        # sim, cells = simulate(10,seed,explorer)
        # dt1 = time.time()
        # render(cells,200,True)


if __name__ == '__main__':
    main()

