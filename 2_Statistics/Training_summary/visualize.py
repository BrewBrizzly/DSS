# Visualizing the training results

# Required modules
import numpy as np 
import matplotlib.pyplot as plt 

# Visualize
def visualize():

    # Read the numpy training array, Loss, Recall, Precision, Accuracy
    tr = np.load('/Users/stephannijdam/Desktop/Nw_models/New/100epochs/VGG16_training.npy')
    vd = np.load('/Users/stephannijdam/Desktop/Nw_models/New/100epochs/VGG16_validation.npy')

    # Seperate the results

    tr_l = []
    tr_r = []
    tr_p = []
    tr_a = []

    vd_l = []   
    vd_r = []
    vd_p = []
    vd_a = []

    for tr_i, vd_i in zip(tr, vd):

        tr_l.append(tr_i[0])
        tr_r.append(tr_i[1])
        tr_p.append(tr_i[2])
        tr_a.append(tr_i[3])

        vd_l.append(vd_i[0])
        vd_r.append(vd_i[1])
        vd_p.append(vd_i[2])
        vd_a.append(vd_i[3])

    # Creating an array to store both f1-scores 
    f1_train = []
    f1_val = []

    for pt, rt, pv, rv in zip(tr_p, tr_r, vd_p, vd_r):

        f1t = (2 * pt * rt) / (pt + rt)
        f1_train.append(f1t)

        f1v = (2 * pv * rv) / (pv + rv)
        f1_val.append(f1v)
        

    # Plot the training results
    x = np.arange(1, len(tr_l) + 1)

    # Creating the figure and axis
    fig, axs = plt.subplots(1, 1)

    # Adding the hist values to the axis 
    axs.plot(x, tr_l, label = 'Loss', linewidth = 1.0)
    axs.plot(x, f1_train, label = 'F1-score', linewidth = 1.0)
    axs.plot(x, tr_a, label = 'Accuracy', linewidth = 1.0)
    axs.legend()

    # Adding a limit and grid 
    # plt.xticks(x)
    axs.grid()
    plt.ylim([0, 1.1])

    # Setting the labels for the axis 
    axs.set_xlabel('epoch')
    axs.set_ylabel('Training values')
    # axs.legend()

    # Adding texts to the figure 
    plt.savefig('summary_training.png')
    plt.close()


    # Plotting validation results

    # Creating the figure and axis 
    fig, axs = plt.subplots(1, 1)

    # Adding the hist values to the axis 
    axs.plot(x, vd_l, label = 'Loss', linewidth = 1.0)
    axs.plot(x, f1_val, label = 'F1-score', linewidth = 1.0)
    axs.plot(x, vd_a, label = 'Accuracy', linewidth = 1.0)
    # axs.set_ylim([0, 1.1])
    axs.legend()

    # Adding a limit and grid

    # plt.xticks(x)
    axs.grid()

    # Setting the labels for the axis 
    axs.set_xlabel('epoch')
    axs.set_ylabel('Validation values')
    # axs.legend()

    # Adding texts to the figure 
    plt.savefig('summary_validation.png')
    plt.close()

visualize()


