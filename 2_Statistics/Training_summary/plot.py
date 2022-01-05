# Creating a plot when a path to numpy array is given 

# Required modules
import matplotlib.pyplot as plt
import numpy as np  

def create_plot(path):
    y = np.load(path)
    x = np.arange(1, len(y) + 1)

    print(len(x))
    print(x)

    print(len(y))
    print(y)

    # Creating the figure and axis 
    fig, axs = plt.subplots(1, 1)

    # Adding the hist values to the axis 
    axs.plot(x, y, label = 'Loss', linewidth = 1.0)

    # Adding a limit and grid 
    # axs.set_xlim(1, len(x))
    # axs.set_ylim(min(y), max(y) + 0.1)
    plt.xticks(x)
    axs.grid()

    # Setting the labels for the axis 
    axs.set_xlabel('epoch')
    axs.set_ylabel('log loss')
    # axs.legend()

    # Adding texts to the figure 
    plt.savefig('summary.png')
    plt.close()

