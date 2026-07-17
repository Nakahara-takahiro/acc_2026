from machine import Pin
import time
import random

# ---- ピンの設定 ----
red   = Pin(10, Pin.OUT)
green = Pin(11, Pin.OUT)
blue  = Pin(12, Pin.OUT)

# リストにまとめると便利
leds  = [red, green, blue]
names = ["赤", "緑", "青"]

# ---- 関数の定義 ----

def all_off():
    """全LEDを消灯する"""
    for led in leds:
        led.value(0)

def light_up(n, duration_ms):
    """
    n番目のLEDをduration_msミリ秒だけ点灯する
    n=0: 赤  n=1: 緑  n=2: 青
    """
    all_off()
    leds[n].value(1)
    print(f"  {names[n]}LED 点灯（{duration_ms}ms）")
    time.sleep_ms(duration_ms)
    all_off()

def countdown(sec):
    """カウントダウンを表示する"""
    for i in range(sec, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("スタート！")

# ---- メインプログラム ----

print("=============================")
print("  ランダム点灯チャレンジ")
print("=============================")
print("LEDがランダムな順番・タイミングで光ります")
print()

# ゲームの設定
ROUNDS = 10          # 何回光らせるか
MIN_WAIT = 500       # 次の点灯まで最短何ms待つか
MAX_WAIT = 2000      # 次の点灯まで最長何ms待つか
MIN_LIGHT = 200      # 点灯時間の最短（ms）
MAX_LIGHT = 800      # 点灯時間の最長（ms）

# カウントダウン
countdown(3)
print()

# ---- ラウンドループ ----
for round_num in range(1, ROUNDS + 1):

    # ランダムな待機時間（次のLEDが光るまでのドキドキ時間）
    wait_ms = random.randint(MIN_WAIT, MAX_WAIT)
    print(f"第{round_num}回: {wait_ms}ms 後に点灯...")
    time.sleep_ms(wait_ms)

    # ランダムなLEDを選ぶ
    chosen = random.randint(0, 2)

    # ランダムな点灯時間
    light_ms = random.randint(MIN_LIGHT, MAX_LIGHT)

    # 点灯
    light_up(chosen, light_ms)

# ---- 終了 ----
print()
print("=============================")
print("  おわり！ お疲れさまでした")
print("=============================")
