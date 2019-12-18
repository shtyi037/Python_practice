import os
import sys
import numpy as np


def jiecheng1(n):
    if n == 1:
        return n
    return n * jiecheng1(n - 1)


def jiecheng2(n):
    return (np.arange(n) + 1).prod()


def main(argc, argv, envp):
    a = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 3, 3, 3, 3, 3, 2, 1],
        [1, 2, 3, 4, 4, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 4, 4, 3, 2, 1],
        [1, 2, 3, 3, 3, 3, 3, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]])
    print(a, end='\n\n')
    b = a.clip(min=3)
    print(b, end='\n\n')
    c = a.clip(max=4)
    print(c, end='\n\n')
    d = a.clip(3, 4)
    print(d, end='\n\n')
    e = a.compress(a.ravel() > 3).reshape((3, 3))
    print(e, end='\n\n')
    f = np.arange(1, 6)
    g = f.prod()
    print(g)
    h = f.cumprod()
    print(h, end='\n\n')
    print(jiecheng1(5))
    print(jiecheng2(5))
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
