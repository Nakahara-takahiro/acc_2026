from machine import Pin
import time, random

# ピンの設定
leds = [Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(12, Pin.OUT)]
sws  = [Pin(13, Pin.IN, Pin.PULL_UP),
        Pin(14, Pin.IN, Pin.PULL_UP),
        Pin(15, Pin.IN, Pin.PULL_UP)]
names = ["赤", "緑", "青"]

# ランダムにLEDを1つ選んで点灯
time.sleep(random.uniform(1.0, 3.0))
n = random.randint(0, 2)
leds[n].value(1)
print(f"{names[n]}が光った！　対応するスイッチを押せ！")

# どのスイッチが押されたか待つ
pressed = -1
while pressed == -1:
    for i, sw in enumerate(sws):
        if sw.value() == 0:      # 押された
            pressed = i
            break

leds[n].value(0)

# 正解・不正解の判定
if pressed == n:
    print(f"正解！　{names[n]}のスイッチを押せた！")
else:
    print(f"不正解…　{names[pressed]}を押した（正解は{names[n]}）")