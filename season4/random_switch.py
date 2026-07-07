from machine import Pin
import time, random

led  = Pin(10, Pin.OUT)
sw13 = Pin(13, Pin.IN, Pin.PULL_UP)

print("準備できたらEnterを押してください")
input()

time.sleep(random.uniform(2.0, 5.0))  # フェイク待機
led.value(1)
print("今だ！ スイッチを押せ！")

start = time.ticks_ms()
while sw13.value() == 1:
    pass
elapsed = time.ticks_diff(time.ticks_ms(), start)

led.value(0)
print(f"反応時間: {elapsed} ミリ秒")