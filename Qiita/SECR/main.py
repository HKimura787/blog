import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 個体数
num_individuals = 1

# 中心点の座標
center_x, center_y = 0, 0

# 移動範囲の半径
radius = 10

# 個体の初期位置
positions = [(random.uniform(-radius, radius), random.uniform(-radius, radius))]

# シミュレーションのステップ数
num_steps = 100

# グラフの設定
fig, ax = plt.subplots()
ax.set_xlim(-radius - 1, radius + 1)
ax.set_ylim(-radius - 1, radius + 1)
ax.set_aspect('equal')

# プロットオブジェクトの初期化
particle, = ax.plot([], [], 'bo', ms=6)
center_point, = ax.plot([], [], 'rx', ms=10)

# アニメーション関数
def animate(frame):
    # 個体の移動
    # ランダムな方向と距離を決める
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, 1.5)
    
    # 新しい位置を計算
    new_x = positions[0][0] + distance * math.cos(angle)
    new_y = positions[0][1] + distance * math.sin(angle)
    
    # 移動範囲を超えないようにする
    if ((new_x - center_x)**2 + (new_y - center_y)**2) > radius**2:
        return particle, center_point
    
    # 位置を更新
    positions[0] = (new_x, new_y)
    
    # プロットデータを更新
    particle.set_data(new_x, new_y)
    center_point.set_data(center_x, center_y)
    
    return particle, center_point

# アニメーションを作成
ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=50, blit=True)

plt.show()

