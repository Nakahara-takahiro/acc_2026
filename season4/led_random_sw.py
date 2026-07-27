# ========================================
# テーマ4 第3回 練習プログラム
# ランダム点灯チャレンジ【スイッチ判定つき】
#
# 第2回との違い：
#   ・スイッチ入力を受け付けるようになった
#   ・正解・不正解を判定するようになった
#   ・反応時間を計れるようになった
# ========================================

from machine import Pin
import time, random

# ---- ピンの設定 ----
leds  = [Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(12, Pin.OUT)]
sws   = [Pin(13, Pin.IN, Pin.PULL_UP),    # SW13 → 赤担当
         Pin(14, Pin.IN, Pin.PULL_UP),    # SW14 → 緑担当
         Pin(15, Pin.IN, Pin.PULL_UP)]    # SW15 → 青担当
names = ["赤", "緑", "青"]

# ---- 関数の定義 ----

def all_off():
    """全LEDを消灯する"""
    for led in leds:
        led.value(0)

def wait_for_switch():
    """
    どれかのスイッチが押されるまで待つ
    押されたスイッチの番号（0〜2）を返す
    タイムアウト（2秒）したら -1 を返す
    """
    # 計測開始
    start = time.ticks_ms()

    while True:
        # 2秒以上経ったらタイムアウト
        if time.ticks_diff(time.ticks_ms(), start) > 2000:
            return -1, 2000    # (押したスイッチ番号, 経過ms)

        # 3つのスイッチを順番にチェック
        for i, sw in enumerate(sws):
            if sw.value() == 0:    # 押された！
                elapsed = time.ticks_diff(time.ticks_ms(), start)
                return i, elapsed  # (押したスイッチ番号, 経過ms)

def countdown(sec):
    """カウントダウンを表示する"""
    for i in range(sec, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("スタート！\n")

# ---- ゲームの設定 ----
ROUNDS    = 10      # 問題数
MIN_WAIT  = 500     # 点灯までの最短待機時間（ms）
MAX_WAIT  = 2000    # 点灯までの最長待機時間（ms）
LIGHT_MS  = 800     # LEDの点灯時間（ms）

# ---- タイトル表示 ----
print("=" * 30)
print("  ランダム点灯チャレンジ")
print("  【スイッチ判定つき】")
print("=" * 30)
print("光ったLEDのスイッチを押せ！")
print("制限時間は 2秒 だよ\n")

countdown(3)

# ---- ラウンドループ ----
score    = 0    # 正解数
total_ms = 0    # 反応時間の合計（平均を出すため）

for round_num in range(1, ROUNDS + 1):

    all_off()

    # ランダムな待機時間
    wait_ms = random.randint(MIN_WAIT, MAX_WAIT)
    print(f"第{round_num}問： {wait_ms}ms 後に点灯...")
    time.sleep_ms(wait_ms)

    # ランダムにLEDを選んで点灯
    n = random.randint(0, 2)
    leds[n].value(1)
    print(f"  → {names[n]}が光った！　スイッチを押せ！")

    # スイッチ入力を待つ
    pressed, elapsed = wait_for_switch()

    # LEDを消す
    all_off()

    # 判定
    if pressed == -1:
        # タイムアウト
        print("  時間切れ！\n")

    elif pressed == n:
        # 正解
        score    += 1
        total_ms += elapsed
        print(f"  正解！　反応時間: {elapsed} ms\n")

    else:
        # 不正解
        print(f"  不正解…　{names[pressed]}を押した"
              f"（正解は{names[n]}）\n")

    time.sleep(0.3)    # 次の問題までの小休止

# ---- 結果表示 ----
print("=" * 30)
print(f"  結果： {score} / {ROUNDS} 問正解")

if score > 0:
    avg = total_ms // score    # 正解したときだけの平均
    print(f"  平均反応時間： {avg} ms")

print("=" * 30)