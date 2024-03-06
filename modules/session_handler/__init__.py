from sys import path
from os.path import dirname, realpath

path.append(dirname(realpath(__file__)))
path.append(f"{dirname(realpath(__file__))}/../")
