from machine import Pin
import time

# GPIO ピン設定
red   = Pin(10, Pin.OUT)
green = Pin(11, Pin.OUT)
blue  = Pin(12, Pin.OUT)

# 起動時に全消灯
red.off()
green.off()
blue.off()

# 赤 → 緑 → 青 を繰り返す
while True:
    # 赤 点灯
    red.on()
    green.off()
    blue.off()
    time.sleep(1)

    # 緑 点灯
    red.off()
    green.on()
    blue.off()
    time.sleep(1)

    # 青 点灯
    red.off()
    green.off()
    blue.on()
    time.sleep(1)
