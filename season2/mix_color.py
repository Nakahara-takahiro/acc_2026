# ★ 色A と 色B を混ぜると何色になる？
# STEP（混ぜる段階数）を増やすほどなめらかに変化する

from machine import Pin
from neopixel import NeoPixel
import time

np = NeoPixel(Pin(22), 7)  # GP22に7個のLEDを接続

# ↓ 混ぜる2色を書き換えよう！
COLOR_A = (255,   0,   0)   # 赤
COLOR_B = (  0,   0, 255)   # 青

STEP = 7   # 混ぜる段階数（LEDの数に合わせて7）

# 2色をLEDの位置で少しずつ混ぜて表示する
def blend(color_a, color_b, steps):
    for i in range(steps):
        # iが大きいほどcolor_bに近づく
        ratio = i / (steps - 1)   # 0.0 〜 1.0
        r = int(color_a[0] * (1 - ratio) + color_b[0] * ratio)
        g = int(color_a[1] * (1 - ratio) + color_b[1] * ratio)
        b = int(color_a[2] * (1 - ratio) + color_b[2] * ratio)
        np[i] = (r, g, b)
    np.write()

# 表示して止まる（書き換えるたびに実行）
blend(COLOR_A, COLOR_B, STEP)