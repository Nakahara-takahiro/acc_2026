from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

# --- ピン設定 ---
enc_a = Pin(17, Pin.IN, Pin.PULL_UP)
enc_b = Pin(16, Pin.IN, Pin.PULL_UP)
sws   = [Pin(p, Pin.IN, Pin.PULL_UP) for p in (13, 14, 15)]  # R, G, B

np = NeoPixel(Pin(22), 7)  # WS2812B 7個

# --- 状態 ---
color  = [0, 0, 0]  # R, G, B 0〜255
bright = 128        # 全体明るさ 0〜255
STEP   = 16
last_a = enc_a.value()

def get_selected():
    """押されているSWを1つだけ返す。同時押し・未押しは -1"""
    pressed = [i for i in range(3) if sws[i].value() == 0]
    return pressed[0] if len(pressed) == 1 else -1

def apply():
    sel = get_selected()
    if sel == -1:
        # 未押し：brightでスケーリングして全灯
        r = color[0] * bright // 255
        g = color[1] * bright // 255
        b = color[2] * bright // 255
    else:
        r, g, b = color
    for i in range(7):
        np[i] = (r, g, b)
    np.write()

while True:
    sel   = get_selected()
    delta = 0

    # --- エンコーダー読み取り ---
    a = enc_a.value()
    if a != last_a:
        delta = STEP if enc_b.value() != a else -STEP
        last_a = a

    # --- 値の更新 ---
    if delta != 0:
        if sel == -1:
            # SW未押し → 全体明るさ変更
            bright = max(0, min(255, bright + delta))
        else:
            # SW押し中 → 対象チャンネルの色変更
            color[sel] = max(0, min(255, color[sel] + delta))
        apply()

    sleep_ms(1)
