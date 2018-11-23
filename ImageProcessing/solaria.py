import numpy as np, matplotlib.pyplot as plt, matplotlib. animation as animation
import sys, os, time
import scipy.ndimage as ndi

cortana = [[0,1,1,1,0],
                       [1,2,2,2,1],
                       [1,2,1,2,1],
                       [1,2,2,2,1],
                       [0,1,1,1,0]]

def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data


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


def filter_preview(galaxy, seed):
    # Preview the filter to be used
    f, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(galaxy, 'inferno_r')
    ax[1].imshow(seed, 'gray')
    plt.show()


def menu_opts():
    print ":: AUTOMATATIZABLE FLAVORS ::"
    menu = {1:'galactic_exposure',2:'fractalize'}
    printout = ''
    for key in menu.keys():
        printout = '[ ' + str(key) + '] '+menu[key]
        print printout
    return menu[int(input('Enter a selection: '))]


def log_runtime(data):
    os.system('echo '+data+' >> runtimes.txt')


def fractalize(ngen, seed, conv):
    gen = 0
    generation = []
    neighbors = []
    medians = []
    while gen < ngen:
        generation.append(seed)
        world = ndi.convolve(seed,conv).flatten()
        step = seed.flatten()
        avg = world.mean()
        medians.append(avg)
        ii = 0
        for cell in world:
            if cell >= avg:
                step[ii] += 1
            else:
                step[ii] -= 1
            if cell % 2:
                step[ii] += 1
            ii += 1
        seed = step.reshape((seed.shape[0],seed.shape[1]))
        generation.append(seed)
        neighbors.append(world.reshape((seed.shape[0], seed.shape[1])))
        gen += 1
    return generation, neighbors


def main():
    if 'example' in sys.argv:
        simple_seed = np.random.randint(0, 2, 40000).reshape((200, 200))

        test_img_slice = plt.imread('/media/root/DB0/andromeda.jpg')
        test_img_slice = test_img_slice[1000:1400, 1000:1400, 0] / 3 + \
                         test_img_slice[1000:1400, 1000:1400, 1] / 3 + \
                         test_img_slice[1000:1400, 1000:1400, 2] / 3

        field = [[1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 1],
                 [1, 2, 0, 2, 1],
                 [1, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1]]

        sim, cells = simulate(20, test_img_slice, field)
        render(sim, 100, False)
        render(cells, 100, True)

        plt.imshow(test_img_slice, 'gray')
        plt.show()
        print "TEST IMAGE: "
        print test_img_slice.shape

    elif 'science' in sys.argv:
        explorer = np.array([[1, 0, 0, 0, 1],
                             [0, 1, 1, 1, 0],
                             [1, 1, 1, 1, 1],
                             [0, 1, 1, 1, 0],
                             [1, 0, 0, 0, 1]])

        f0 = [[2, 0, 0, 0, 0, 0, 2],
              [0, 1, 1, 1, 1, 1, 0],
              [0, 1, 0, 0, 0, 1, 0],
              [2, 1, 0, 1, 0, 1, 2],
              [0, 1, 0, 0, 0, 1, 0],
              [0, 1, 1, 1, 1, 1, 0],
              [2, 0, 0, 0, 0, 0, 2]]

        f1 = [[1,1,1,0,0,0,1,1,1],
              [1,3,1,0,0,0,1,3,1],
              [0,1,1,1,0,1,1,1,0],
              [0,0,0,1,1,1,0,0,0],
              [0,0,0,1,1,1,0,0,0],
              [0,0,0,1,1,1,0,0,0],
              [0,1,1,1,0,1,1,1,0],
              [1,3,1,0,0,0,1,3,1],
              [1,1,1,0,0,0,1,1,1]]

        g3 = plt.imread('/media/root/CoopersDB/Images/andromeda.jpg')
        g2 = plt.imread('/media/root/CoopersDB/Images/nebula.png')
        g1 = plt.imread('/media/root/CoopersDB/Images/SPACE.jpg')
        print "Please choose an image to run experiment with: "

        images = {1:'andromeda',2:'nebula',3:'space'}
        for image in images.keys():
            print "["+str(image)+" ] "+images[image]
        opt = images[int(input('Enter a selection: '))]

        if opt == 'andromeda':
            g = g3
        if opt == 'nebula':
            g = g2*259
        if opt == 'space':
            g = g1

        opt = int(input('Enter granularity for simulation[0-255]: '))
        granularity = np.arange(50,255)
        galaxy = (g[:, :, 0]/3 + g[:, :, 1]/3 + g[:, :, 2]/3)/granularity[opt]

        seed = ndi.convolve(galaxy, explorer)

        filter_preview(galaxy, seed)

        print "Analyzing Galaxy of shape "+str(seed.shape)

        selection = menu_opts()
        print "Simulation Started"
        dt0 = time.time()  # start the clock
        if selection == 'galactic_exposure':
            # run the simulation to eat away at empty space in the galaxy
            sim, cells = galactic(15, seed[500:1200,500:1200], f0)
            print str(time.time() - dt0) + "s"
            # Log Runtime for predicting wait time
            log_runtime(str(len(sim))+" frame [" + str(cells.pop(0).shape[0]) + "x" +
                        str(cells.pop(0).shape[0]) + "] in "+str(time.time()-dt0)+"s [GALACTIC]")
            # Now Render the simulation, with step size and isColor args
            render(sim, 100,True)
            render(cells,200,True)

            # Run the simulation
            sim, cell = galactic(10, galaxy, cortana)
            # or galactic(10, galaxy, f1)
            print str(time.time() - dt0) + "s"
            # Render the simulation
            render(sim, 100, True)
            render(cell, 100, True)
            # Log Runtime for predicting wait time
            log_runtime(str(galaxy.shape) + " // " + str(time.time() - dt0))
            # Log the runtime for predicting later on

        if selection == 'fractalize':
            z=0 # If you want to tweak the nebulizer at a tine grain level
            h=1 # This provides the generic parametrized version as neb[[]]
            k=2
            m=3
            n=4
            nebulizer = [[0,0,0,1,1,1,1,1,1,0,0,0],
                         [0,0,0,1,1,2,2,1,1,0,0,0],
                         [0,0,1,2,2,2,2,2,1,1,0,0],
                         [1,1,1,2,3,3,3,3,2,1,1,1],
                         [1,2,2,2,3,4,4,3,2,2,1,1],
                         [1,2,2,2,2,3,3,2,3,2,2,1],
                         [1,2,2,2,3,3,3,2,2,2,2,1],
                         [1,2,2,2,2,3,3,2,2,2,2,1],
                         [1,2,2,2,3,4,4,3,2,2,1,1],
                         [1,1,2,3,3,3,3,3,2,1,1,0],
                         [0,0,1,1,2,2,2,2,1,1,0,0],
                         [0,0,0,1,1,1,1,1,1,0,0,0]]

            neb = [[z,z,h,h,z,z],
                   [z,h,k,k,h,z],
                   [h,k,m,m,k,h],
                   [h,k,m,n,k,h],
                   [z,h,k,k,h,z],
                   [z,z,h,h,z,z]]

            """{DEBUG}"""
            plt.imshow(ndi.convolve(galaxy, nebulizer))
            plt.show()
            """{DEBUG}"""
            dt0 = time.time()

            sim, cells = fractalize(10, galaxy, neb)
            # Log the runtime for predicting later on
            log_runtime(str(len(sim)) + " frame [" + str(cells.pop(0).shape[0]) + "x" +
                        str(cells.pop(0).shape[0]) + "] in " + str(time.time() - dt0) + "s [FRACTALIZE]")

            render(sim, 200, True)
            render(cells,200,True)
        # sim, cells = simulate(10,seed,explorer)
        # dt1 = time.time()
        # render(cells,200,True)


if __name__ == '__main__':
    main()

