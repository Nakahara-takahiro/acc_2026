from machine import Pin, PWM
from neopixel import NeoPixel
from time import sleep_ms

# --- ピン設定 ---
enc_a = Pin(17, Pin.IN, Pin.PULL_UP)
enc_b = Pin(16, Pin.IN, Pin.PULL_UP)
sws   = [Pin(p, Pin.IN, Pin.PULL_UP) for p in (13, 14, 15)]  # R, G, B

np = NeoPixel(Pin(22), 1)  # WS2812B 1個

# --- 状態 ---
color    = [0, 0, 0]   # R, G, B 0〜255
bright   = 128         # 全体明るさ 0〜255
STEP     = 16          # 1ノッチあたりの変化量
last_a   = enc_a.value()
last_sw  = [1, 1, 1]

def get_selected():
    """押されているSWを返す。同時押し・未押しは -1"""
    pressed = [i for i in range(3) if sws[i].value() == 0]
    return pressed[0] if len(pressed) == 1 else -1

def apply():
    if get_selected() == -1:
        # 全体明るさモード：colorにbrightをスケーリングして反映
        r = color[0] * bright // 255
        g = color[1] * bright // 255
        b = color[2] * bright // 255
    else:
        r, g, b = color
    np[0] = (r, g, b)
    np.write()

while True:
    # --- スイッチ読み取り（立ち下がり検出） ---
    for i in range(3):
        v = sws[i].value()
        last_sw[i] = v

    # --- エンコーダー読み取り ---
    a = enc_a.value()
    if a != last_a:
        sel = get_selected()
        delta = STEP if enc_b.value() != a else -STEP

        if sel == -1:
            bright = max(0, min(255, bright + delta))
        else:
            color[sel] = max(0, min(255, color[sel] + delta))

        apply()
        last_a = a

    sleep_ms(1)