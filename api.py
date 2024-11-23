from statsbombpy import sb
import pandas as pd 
import matplotlib.pyplot as plt 
from mplsoccer import VerticalPitch , Pitch

"""
pip install statsbombpy
pip install pandas
pip install matplotlib
pip install mplsoccer
"""

"""
windows 
set SB_USERNAME=enzito
set SB_PASSWORD=enzito

linux 
export SB_USERNAME="enzito"
export SB_PASSWORD="enzito"

"""

print(sb.competitions())
