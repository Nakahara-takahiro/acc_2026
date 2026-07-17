# ========================================
# どのLEDが光るかわからない！
# ランダムな待ち時間でランダムなLEDが光ります
# ========================================

# machine モジュールから Pin（ピン）を使えるようにする
# Pin = Raspberry Pi Pico のGPIOピンを操作する道具
from machine import Pin

# time モジュール：待ち時間を作るときに使う
import time

# random モジュール：ランダム（でたらめ）な数を作るときに使う
import random

# ---- ピンの設定 ----
# Pin(番号, Pin.OUT) で「このピンは出力（信号を出す）用」と宣言する
red   = Pin(10, Pin.OUT)   # GP10 → 赤LED
green = Pin(11, Pin.OUT)   # GP11 → 緑LED
blue  = Pin(12, Pin.OUT)   # GP12 → 青LED

# 3つのLEDをリスト（順番のある入れ物）にまとめる
# leds[0]=赤、leds[1]=緑、leds[2]=青
leds = [red, green, blue]

# 各LEDの名前もリストにまとめる（表示用）
names = ["赤", "緑", "青"]

# ---- メインの繰り返し ----
# while True: は「ずっと繰り返す」という意味
# 電源を切るまで止まらない
while True:

    # 【ステップ1】全部のLEDを消す
    # for文で leds の中身を1つずつ取り出して処理する
    for led in leds:
        led.value(0)    # value(0) = 消灯、value(1) = 点灯

    # 【ステップ2】ランダムな時間だけ待つ
    # random.uniform(a, b) は a以上b以下の小数をランダムに返す
    # 例：random.uniform(1.0, 3.0) → 1.3秒、2.7秒、1.0秒 など
    wait = random.uniform(1.0, 3.0)    # 1秒〜3秒のどこかで光る
    print(f"{wait:.1f}秒後に点灯します...")  # 小数点1桁で表示
    time.sleep(wait)                   # その秒数だけ待つ

    # 【ステップ3】ランダムにLEDを1つ選ぶ
    # random.choice(リスト) はリストの中からランダムに1つ選ぶ
    # ここでは leds の中から赤・緑・青のどれかが選ばれる
    chosen = random.choice(leds)

    # 選ばれたLEDが何番目か調べる（名前を表示するため）
    # leds.index(chosen) で chosen が何番目かわかる
    idx = leds.index(chosen)
    print(f"  → {names[idx]}LED が光った！")

    # 【ステップ4】選ばれたLEDを0.5秒だけ光らせる
    chosen.value(1)       # 点灯
    time.sleep(0.5)       # 0.5秒待つ
    chosen.value(0)       # 消灯

    # while True なのでステップ1に戻って繰り返す
