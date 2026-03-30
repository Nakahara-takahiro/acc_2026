from machine import Pin, PWM
from time import sleep_ms

# --- ピン設定 ---
enc_a = Pin(17, Pin.IN, Pin.PULL_UP)
enc_b = Pin(16, Pin.IN, Pin.PULL_UP)

leds = [PWM(Pin(p)) for p in (10, 11, 12)]  # R, G, B
for led in leds:
    led.freq(1000)

sws = [Pin(p, Pin.IN, Pin.PULL_UP) for p in (13, 14, 15)]  # R, G, B 選択

# --- 状態 ---
brightness = [0, 0, 0]   # R, G, B それぞれ 0〜65535
STEP = 4096
selected = 0             # 現在選択中のチャンネル（0=R, 1=G, 2=B）
last_a  = enc_a.value()
last_sw = [1, 1, 1]      # プルアップなので初期値は1（開放）

def apply():
    for i, led in enumerate(leds):
        led.duty_u16(brightness[i])

while True:
    # --- スイッチ読み取り（押された瞬間だけ選択切替）---
    for i, sw in enumerate(sws):
        v = sw.value()
        if v == 0 and last_sw[i] == 1:   # 立ち下がり検出
            selected = i
        last_sw[i] = v

    # --- エンコーダー読み取り ---
    a = enc_a.value()
    if a != last_a:
        if enc_b.value() != a:
            brightness[selected] = min(65535, brightness[selected] + STEP)
        else:
            brightness[selected] = max(0, brightness[selected] - STEP)
        apply()
        last_a = a

    sleep_ms(1)