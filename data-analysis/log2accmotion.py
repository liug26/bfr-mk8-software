import argparse
import data_parser
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import integrate


# Usage example: python log2accmotion.py -i /Users/jasonliu/Downloads/0037.csv
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True, help="")
parser.add_argument('-t', '--title', required=False, default='Plot Title', help="")
parser.add_argument('-x', '--xaxis_title', required=False, default='Time (s)', help="")
parser.add_argument('-y', '--yaxis_title', required=False, default='Y Axis Title', help="")
parser.add_argument('-l', '--legend_title', required=False, default='Legend', help="")
parser.add_argument('--font_family', required=False, default='Courier New, monospace', help="")
parser.add_argument('--font_size', required=False, type=int, default=18, help="")
parser.add_argument('--font_color', required=False, default='RebeccaPurple', help="")

args = parser.parse_args()

G_ACC = 9.81


def main():
    data_parser.load(args.input)

    ax = data_parser.data['accx']
    ay = data_parser.data['accy']
    az = data_parser.data['accz']

    vx = integrate.cumtrapz(np.array(ax.y) * G_ACC, ax.x, initial=0)
    dx = integrate.cumtrapz(vx, ax.x, initial=0)
    vy = integrate.cumtrapz(np.array(ay.y) * G_ACC, ay.x, initial=0)
    dy = integrate.cumtrapz(vy, ay.x, initial=0)
    vz = integrate.cumtrapz(np.array(az.y) * G_ACC, az.x, initial=0)
    dz = integrate.cumtrapz(vz, az.x, initial=0)

    fig = go.Figure(go.Scatter3d(x=dx, y=dy, z=dz,
                                 mode="markers",
                                 marker=dict(color="red", size=10)
                                 ))
    fig.show()


if __name__ == '__main__':
    main()
