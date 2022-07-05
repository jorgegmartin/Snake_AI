import matplotlib.pyplot as plt
from IPython import display
import numpy as np

plt.ion()

def plot(scores, mean_scores, last_10scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.plot(last_10scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.text(len(last_10scores)-1, last_10scores[-1], str(last_10scores[-1]))
    plt.show(block=False)
    plt.pause(.1)