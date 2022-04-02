from ctypes import *


class Task(Structure):
    _fields_ = [
        ("id", c_int),
        ("pointX", c_float),
        ("pointY", c_float),
        ("pointZ", c_float),
        ("dirX", c_float),
        ("dirY", c_float),
        ("dirZ", c_float),
        ("x", c_int),
        ("y", c_int),
        ("r", c_float),
        ("g", c_float),
        ("b", c_float)
    ]