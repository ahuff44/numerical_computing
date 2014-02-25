import numpy as np
from matplotlib import pyplot as plt
from matplotlib import widgets as wg
from scipy.misc import comb
from numpy.random import rand

# Decasteljau's algorithm problem
def decasteljau(p,t):
    """ Evaluates a Bezier curve with control points 'p' at time 't'.
    The points in 'p' are assumed to be stored in its rows.
    'p' is assumed to be 2-dimensional."""
    n = p.shape[0]
    m = p.shape[1]
    q1 = p
    q2 = np.zeros((n, m))
    for i in xrange(n-1, 0, -1):
        q2 = np.zeros((i, m))
        for k in xrange(i):
            q2[k] = (1-t) * q1[k] + t * q1[k+1]
        q1 = q2
    return q2[0]

# used in interactive plot problem.
def decasteljau_animated(p, t, res=401):
    """ Produces a plot illustrating the Decasteljau algorithm
    at a given time 't'."""
    n = p.shape[0]
    plt.plot(p[:,0], p[:,1])
    plt.scatter(p[:,0], p[:,1])
    q1 = p
    q2 = np.zeros((n, 2))
    for i in xrange(n-1, 0, -1):
        q2 = np.zeros((i, 2))
        for k in xrange(i):
            q2[k] = (1-t) * q1[k] + t * q1[k+1]
        plt.plot(q2[:,0], q2[:,1])
        plt.scatter(q2[:,0], q2[:,1])
        q1 = q2
    # This line double-plots a point, but it will probably
    # be less costly to replot the last point than it
    # is to check on each iteration.
    plt.scatter(q2[:,0], q2[:,1], color='r', linewidth=3)
    t = np.linspace(0, 1, res)
    X = np.array([decasteljau(p,i) for i in t])
    plt.plot(X[:,0], X[:,1])
    pass

# interactive plot problem.
def decasteljau_interactive(n):
    """ Makes an interactive plot using a slider bar to show the
    Decasteljau algorithm at different times."""
    ax = plt.subplot(1, 1, 1)
    plt.subplots_adjust(bottom=0.25)
    plt.axis([-1, 1, -1, 1])
    axT = plt.axes([0.25, 0.1, 0.65, 0.03])
    sT = wg.Slider(axT, 't', 0, 1, valinit=0)
    pts = plt.ginput(n, timeout=240)
    plt.subplot(1, 1, 1)
    pts = np.array(pts)
    plt.cla()
    T0=0
    decasteljau_animated(pts, T0)
    plt.axis([-1, 1, -1, 1])
    plt.draw()
    def update(val):
        T = sT.val
        ax.cla()
        plt.subplot(1, 1, 1)
        decasteljau_animated(pts,T)
        plt.xlim((-1, 1))
        plt.ylim((-1,1))
        plt.draw()
    sT.on_changed(update)
    plt.show()

# Bernstein polynomial problem
def bernstein(i, n):
    """ Returns the 'i'th Bernstein polynomial of degree 'n'."""
    return comb(n, i, exact=True) * (np.poly1d([-1,1]))**(n-i) * (np.poly1d([1,0]))**i

# Coordinate function problem.
def bernstein_pt_aprox(X):
    """ Returns the 'x' and 'y' coordinate functions for a 2-dimensional
    Bezier curve with control points 'X'."""
    n = X.shape[0]
    xpoly = np.poly1d([0])
    ypoly = np.poly1d([0])
    for i in xrange(n):
        npoly = bernstein(i, n-1)
        xpoly += X[i,0] * npoly
        ypoly += X[i,1] * npoly
    return xpoly, ypoly

# plot demonstrating numerical instability in Bernstein polys.
def compare_plot(n, res=501):
    """ Produces a plot showing a Bezier curve evaluated via
    the Decasteljau algorithm and a Bezier curve evaluated using
    Bernstein polynomials. Control points are chosen randomly.
    Instability should be evident for moderately large values of 'n'."""
    X = rand(n, 2)
    t = np.linspace(0, 1, res)
    # This is slow.
    # It would be better to have a
    # decasteljau function that supported
    # arrays of time values.
    decasteljau_curve = np.array([decasteljau(X, ti) for ti in t])
    xpoly, ypoly = bernstein_pt_aprox(X)
    plt.plot(decasteljau_curve[:,0], decasteljau_curve[:,1], xpoly(t), ypoly(t))
    plt.show()

if __name__ == '__main__':
    decasteljau_interactive(5)
    compare_plot(4)
    compare_plot(30)
