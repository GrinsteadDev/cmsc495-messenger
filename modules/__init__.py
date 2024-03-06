from sys import path
from os.path import dirname, realpath
from dotenv import load_dotenv

path.append(dirname(realpath(__file__)))
load_dotenv()