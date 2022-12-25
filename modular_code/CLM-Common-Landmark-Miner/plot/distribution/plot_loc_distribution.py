import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


if __name__ == "__main__":
    results = pd.read_csv(os.path.join('..', 'data', 'detailed_result.csv'))
    results.fillna('', inplace = True)
    precision = np.zeros((6, 2), dtype = np.int)
    for index, result in results.iterrows():
        type_ = result['type']
        first = -1
        second = -1
        country = result['country']
        province = result['province']
        city = result['city']
        district = result['district']
        street = result['street']
        if street != '' and street != None:
            first = 5
        elif district != '' and district != None:
            first = 4
        elif city != '' and city != None:
            first = 3
        elif province != '' and province != None:
            first = 2
        elif country != '' and country != None:
            first = 1
        else:
            first = 0
        if type_ == 'lg' or type_ == 'pf':
            second = 0
        else:
            second = 1
        precision[first][second] += 1
    fig, ax = plt.subplots()
    size = 0.3
    labels = ['None', 'Country', 'Province', 'City', 'District', 'Street']
    inner_labels = []
    for i in range(6):
        label = labels[i] + ' (controllable): ' + str(precision[i][0])
        inner_labels.append(label)
        label = labels[i] + ' (uncontrollable): ' + str(precision[i][1])
        inner_labels.append(label)
    cmap = plt.get_cmap("tab20c")
    outer_colors = cmap((np.arange(6) * 4)[::-1])
    inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22])[::-1])
    
    ax.pie(precision.sum(axis=1), radius=1, colors=outer_colors, labels=labels,
       wedgeprops=dict(width=size, edgecolor='w'))
    ax.pie(precision.flatten(), radius=1-size, colors=inner_colors, labels=inner_labels,
       wedgeprops=dict(width=size, edgecolor='w'))
    ax.set(aspect="equal", title='Precision')
    plt.legend(loc='upper right')
    plt.savefig(os.path.join('..', 'data', 'precision.png'))
    # fig, ax = plt.subplots()

    # size = 0.3
    # vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

    # cmap = plt.get_cmap("tab20c")
    # outer_colors = cmap(np.arange(3)*4)
    # inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10]))

    # ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
    #     wedgeprops=dict(width=size, edgecolor='w'))

    # ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
    #     wedgeprops=dict(width=size, edgecolor='w'))

    # ax.set(aspect="equal", title='Pie plot with `ax.pie`')
    # plt.show()

