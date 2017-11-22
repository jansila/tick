from tick.simulation import SimuLogReg, weights_sparse_gauss
from sklearn.model_selection import train_test_split
import numpy as np
from tick.inference import OnlineForestClassifier
from matplotlib.colors import ListedColormap

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.datasets import make_moons, make_classification, make_circles
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

from time import time


n_samples = 500
n_features = 2
seed = 123

np.set_printoptions(precision=2)

w0 = weights_sparse_gauss(n_features, nnz=2)
X, y = SimuLogReg(w0, -1., n_samples=n_samples, seed=seed).simulate()
y = (y + 1) / 2


def plot_decisions_regression(clfs, datasets, names):
    i = 1
    h = .02
    fig = plt.figure(figsize=(4 * (len(clfs) + 1), 4 * len(datasets)))
    # iterate over datasets
    for ds_cnt, ds in enumerate(datasets):
        X, y = ds
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=.4, random_state=42)

        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        # just plot the dataset first
        cm = plt.cm.RdBu
        ax = plt.subplot(len(datasets), len(clfs) + 1, i)
        if ds_cnt == 0:
            ax.set_title("Input data")
        ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=25, cmap=cm)
        # and testing points
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm, s=25,
                   alpha=0.6)
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())
        i += 1
        # iterate over classifiers
        for name, clf in zip(names, clfs):
            ax = plt.subplot(len(datasets), len(clfs) + 1, i)
            clf.fit(X_train, y_train)
            Z = clf.predict(np.array([xx.ravel(), yy.ravel()]).T)
            # Put the result into a color plot
            Z = Z.reshape(xx.shape)
            ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)
            # Plot also the training points
            ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm, s=15)
            # and testing points
            ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm,
                       s=15, alpha=0.6)
            ax.set_xlim(xx.min(), xx.max())
            ax.set_ylim(yy.min(), yy.max())
            ax.set_xticks(())
            ax.set_yticks(())
            if ds_cnt == 0:
                ax.set_title(name)
            i += 1

    plt.tight_layout()
    # plt.show()


def plot_decision_classification(classifiers, datasets, names):
    h = .02
    fig = plt.figure(figsize=(2 * (len(classifiers) + 1), 2 * len(datasets)))
    i = 1
    # iterate over datasets
    for ds_cnt, ds in enumerate(datasets):
        # preprocess dataset, split into training and test part
        X, y = ds
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=.4, random_state=42)
        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        # just plot the dataset first
        cm = plt.cm.RdBu
        cm_bright = ListedColormap(['#FF0000', '#0000FF'])
        ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
        if ds_cnt == 0:
            ax.set_title("Input data")
        # Plot the training points
        ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=10, cmap=cm)
        # and testing points
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm, s=10,
                   alpha=0.6)
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())
        i += 1
        # iterate over classifiers
        for name, clf in zip(names, classifiers):
            ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
            if hasattr(clf, 'clear'):
                clf.clear()
            clf.fit(X_train, y_train)
            Z = clf.predict_proba(np.array([xx.ravel(), yy.ravel()]).T)[:, 1]

            score = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
            # Put the result into a color plot
            Z = Z.reshape(xx.shape)
            ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)
            ax.set_xlim(xx.min(), xx.max())
            ax.set_ylim(yy.min(), yy.max())
            ax.set_xticks(())
            ax.set_yticks(())
            if ds_cnt == 0:
                ax.set_title(name)
            ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % score).lstrip('0'),
                    size=15, horizontalalignment='right')
            i += 1

    plt.tight_layout()
    # plt.show()


path = '/Users/stephane.gaiffas/Downloads/'

n_trees = 20

X, y = make_classification(n_samples=n_samples, n_features=2, n_redundant=0,
                           n_informative=2, random_state=1,
                           n_clusters_per_class=1)
rng = np.random.RandomState(2)
X += 2 * rng.uniform(size=X.shape)


# clf = OnlineForestClassifier(n_trees=n_trees, seed=123, step=1.)
# clf.fit(X, y)
# clf.print()

linearly_separable = (X, y)

datasets = [
    make_moons(n_samples=n_samples, noise=0.3, random_state=0),
    make_circles(n_samples=n_samples, noise=0.2, factor=0.5, random_state=1),
    linearly_separable
]

classifiers = [
    OnlineForestClassifier(n_trees=n_trees, seed=123, step=1.),
    ExtraTreesClassifier(n_estimators=n_trees),
    RandomForestClassifier(n_estimators=n_trees)
]

names = [
    "Online forest",
    "Extra trees",
    "Breiman RF"
]

plot_decision_classification(classifiers, datasets, names)

# plt.savefig('decisions.pdf')

plt.show()
