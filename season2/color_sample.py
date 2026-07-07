# ★ R・G・B の数字を書き換えて、右上の「実行」ボタンを押そう！
# 0 = 消える　255 = 最大の明るさ

from machine import Pin
from neopixel import NeoPixel

np = NeoPixel(Pin(22), 7)

# ↓ここの数字を書き換えよう！
R = 255
G = 0
B = 0

# 全LEDを同じ色に光らせる
for i in range(7):
    np[i] = (R, G, B)
np.write()