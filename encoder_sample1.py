from machine import Pin, PWM
from time import sleep_ms

# ピン設定
enc_a = Pin(17, Pin.IN, Pin.PULL_UP)
enc_b = Pin(16, Pin.IN, Pin.PULL_UP)
led   = PWM(Pin(12))
led.freq(1000)

# 状態
brightness = 32768  # 0〜65535
STEP = 4096         # 1ノッチあたりの変化量
last_a = enc_a.value()

while True:
    a = enc_a.value()
    if a != last_a:          # Aが変化したとき
        if enc_b.value() != a:
            brightness = min(65535, brightness + STEP)  # 時計回り→明るく
        else:
            brightness = max(0, brightness - STEP)      # 反時計回り→暗く
        led.duty_u16(brightness)
        last_a = a
    sleep_ms(1)