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

# # matplotlib의 한글문제를 해결
font_name = font_manager.FontProperties(fname=r"C:/Windows/Fonts/malgun.ttf").get_name()

# # font_name
rc('font', family=font_name)

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart(data):
    labels = ['기쁨', '당황', '분노', '불안', '상처', '슬픔']
    num_labels = len(labels)

    data += data[:1]

    my_palette = plt.cm.get_cmap("Set2", len(labels))
    color = my_palette(5)

    angles = [n / float(num_labels) * 2 * pi for n in range(num_labels)]
    angles += angles[:1]

    plt.switch_backend('AGG')
    plt.rc('figure', figsize=(3, 3))
    ax = plt.subplot(1, 1, 1, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], labels, color='black', size=12)
    ax.tick_params(axis='x')

    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"], color="black", size=10)
    plt.ylim(0, 100)

    ax.plot(angles, data, color=color, linewidth=1, linestyle='solid')
    ax.fill(angles, data, color=color, alpha=0.5)

    # title = "감정 분석 결과 "
    # plt.title(title, fontsize=20, x=0.5, y=1.1)

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