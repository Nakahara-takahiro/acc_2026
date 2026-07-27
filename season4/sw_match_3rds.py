from machine import Pin
import time, random

leds  = [Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(12, Pin.OUT)]
sws   = [Pin(13, Pin.IN, Pin.PULL_UP),
         Pin(14, Pin.IN, Pin.PULL_UP),
         Pin(15, Pin.IN, Pin.PULL_UP)]
names = ["赤", "緑", "青"]
score = 0

for q in range(1, 4):          # 3問
    for led in leds: led.value(0)
    time.sleep(random.uniform(1.0, 2.5))

    n = random.randint(0, 2)
    leds[n].value(1)
    print(f"第{q}問：{names[n]}が光った！")

    pressed = -1
    while pressed == -1:
        for i, sw in enumerate(sws):
            if sw.value() == 0:
                pressed = i
                break

    leds[n].value(0)

    if pressed == n:
        score += 1
        print("  → 正解！\n")
    else:
        print(f"  → 不正解（{names[pressed]}を押した）\n")
    time.sleep(0.5)

print(f"結果：{score} / 3 問正解")