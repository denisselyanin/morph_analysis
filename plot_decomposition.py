import matplotlib.pyplot as plt
import numpy as np

from tagging import split_sentence

def plot_decomposition(sentence, replacements):
    plt.figure(figsize=(15, 5))
    plt.rc('font', size=5)

    tokens = split_sentence(sentence)

    token_coords = np.hstack((np.arange(len(tokens)) * 2,
                              np.zeros(len(tokens)))).reshape((2, -1)).T

    plt.scatter(*token_coords.T)
    plt.xticks(token_coords[:, 0], tokens, fontsize=12)

    for k, (bounds, token_name) in enumerate(replacements):
        xs = token_coords[[bounds[0], bounds[0], bounds[1], bounds[1]],
        0]
        ys = token_coords[[bounds[0], bounds[1]], 1].tolist()
        ys = ys[:1] + [max(ys) + 1] * 2 + ys[-1:]

        plt.plot(xs, ys)

        token_coords[bounds[0], 0] = (token_coords[bounds[0], 0] + token_coords[bounds[1], 0]) / 2
        token_coords[bounds[0], 1] = max(token_coords[bounds[0]:bounds[1] + 1, 1]) + 1
        token_coords = token_coords.tolist()
        token_coords = np.array(token_coords[:bounds[0] + 1] + token_coords[bounds[1] + 1:])

    plt.show()