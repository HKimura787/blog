import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import uniform, multivariate_normal

# 個体数
num_individuals = 1

# 中心点の座標
center_x, center_y = 0, 0

# 移動範囲の半径
radius = 10

# 目的分布の分散
target_variance = 5

# 提案分布の範囲
proposal_range = 2  # 提案分布の一様分布の範囲

# 個体の初期位置
positions = [(random.uniform(-radius, radius), random.uniform(-radius, radius))]

# シミュレーションのステップ数
num_steps = 2000

# グラフの設定
fig, ax = plt.subplots()
ax.set_xlim(-radius - 1, radius + 1)
ax.set_ylim(-radius - 1, radius + 1)
ax.set_aspect('equal')

# プロットオブジェクトの初期化
particle, = ax.plot([], [], 'bo', ms=6)
center_point, = ax.plot([], [], 'rx', ms=10)
trail, = ax.plot([], [], '-', lw=1, color='green', alpha=0.5)  # 軌跡を緑色に設定

# 軌跡のデータ
trail_data = []

# 2次元正規分布の確率密度関数
def normal_pdf(x, y, mean_x, mean_y, variance):
    return multivariate_normal.pdf([x, y], mean=[mean_x, mean_y], cov=[[variance, 0], [0, variance]])

# アニメーション関数
def animate(frame):
    # 現在の位置
    current_x, current_y = positions[0]
    
    # 提案分布から新しい位置を提案
    proposed_x = current_x + uniform.rvs(-proposal_range, 2 * proposal_range)
    proposed_y = current_y + uniform.rvs(-proposal_range, 2 * proposal_range)
    
    # 現在の位置と提案された位置の確率密度を計算
    current_pdf = normal_pdf(current_x, current_y, center_x, center_y, target_variance)
    proposed_pdf = normal_pdf(proposed_x, proposed_y, center_x, center_y, target_variance)
    
    # 受理率を計算
    acceptance_ratio = min(1, proposed_pdf / current_pdf)
    
    # 受理率に基づいて移動を決定
    if random.uniform(0, 1) < acceptance_ratio:
        positions[0] = (proposed_x, proposed_y)
    
    # 軌跡のデータを更新
    trail_data.append(positions[0])
    
    # プロットデータを更新
    particle.set_data(positions[0][0], positions[0][1])
    center_point.set_data(center_x, center_y)
    trail.set_data(*zip(*trail_data))  # 軌跡のデータを更新
    
    return particle, center_point, trail

# アニメーションを作成 
ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=50, blit=True,)
ani.save('mcmc.mp4', writer='ffmpeg', fps=30, dpi=100)
plt.show()