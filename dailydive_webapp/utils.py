import base64
import uuid
from .models import *
from io import BytesIO
from matplotlib import pyplot as plt
from math import pi
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import matplotlib.colors as mcolors
from matplotlib import font_manager, rc # rc == run configure(configuration file) # 한글 폰트 세팅
import seaborn as sns
import numpy as np

# # matplotlib의 한글문제를 해결

# old_path = r"C:/Windows/Fonts/malgun.ttf"
path = 'dailydive_webapp/static/dailydive_webapp/font/NanumGothic.ttf'
font_name = font_manager.FontProperties(fname=path).get_name()
# # font_name
rc('font', family=font_name)

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', facecolor='#141033')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(data):
    labels = ['Sleep', 'Exercise', 'Rest', 'Diet', 'SNS']
    num_labels = len(labels)

    data += data[:1]

    color = "purple"

    angles = [n / float(num_labels) * 2 * pi for n in range(num_labels)]
    angles += angles[:1]

    plt.switch_backend('AGG')
    plt.rc('figure', figsize=(5, 5))

    ax = plt.subplot(1, 1, 1, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    ax.patch.set_facecolor('#141033')
    plt.xticks(angles[:-1], labels, color='white', size=12)
    ax.tick_params(axis='x')

    ax.set_rlabel_position(0)
    plt.yticks([5, 10, 15, 20], ["5", "10", "15", "20"], color="white", size=10)
    plt.ylim(0, 25)

    ax.plot(angles, data, color=color, linewidth=1, linestyle='solid')
    ax.fill(angles, data, color=color, alpha=0.5)

    for g in ax.yaxis.get_gridlines():  ## grid line
        g.get_path()._interpolation_steps = len(labels)

    spine = Spine(axes=ax,
                  spine_type='circle',
                  path=Path.unit_regular_polygon(len(labels)))

    ## Axes의 중심과 반지름을 맞춰준다.
    spine.set_transform(Affine2D().scale(.5).translate(.5, .5) + ax.transAxes)

    ax.spines = {'polar': spine}

    chart = get_graph()

    return chart


def get_bar_chart(data):
    labels = ['Joy', 'Fear', 'Anger', 'Anxiety', 'Hurt', 'Sadness']

    color = ['#E46729', '#FDA521', '#E14374', '#1D82B1', '#54187B', '#9C0E6B']

    plt.rcParams['axes.facecolor'] = '#141033'
    plt.rcParams['axes.edgecolor'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
  
    sorted_data, sorted_labels = zip(*sorted(zip(data, labels), reverse=False))
    plt.figure(figsize=(5, 5))
    plt.barh(sorted_labels, sorted_data, color=color, height=0.5)
    plt.xticks(ticks=[])


    chart = get_graph()

    return chart



