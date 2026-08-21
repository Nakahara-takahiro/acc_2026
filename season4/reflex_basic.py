# ========================================
# テーマ4 第4回 反射神経ゲーム【基本版】
# 光ったLEDと同じ色のスイッチを押せ！
#
# GP10→赤LED  GP11→緑LED  GP12→青LED
# GP13→赤SW   GP14→緑SW   GP15→青SW
# ========================================

from machine import Pin
import time, random

# ---- ピンの設定 ----
leds  = [Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(12, Pin.OUT)]
sws   = [Pin(13, Pin.IN, Pin.PULL_UP),
         Pin(14, Pin.IN, Pin.PULL_UP),
         Pin(15, Pin.IN, Pin.PULL_UP)]
names = ["赤", "緑", "青"]

ROUNDS = 9        # 3レベル × 3問 = 9問

# ---- 関数 ----
def all_off():
    """全LEDを消灯する"""
    for led in leds:
        led.value(0)

def wait_for_switch(timeout):
    """スイッチが押されるまで待つ → (番号, 経過ms) を返す"""
    start = time.ticks_ms()
    while True:
        # 制限時間を過ぎたら -1 を返す
        if time.ticks_diff(time.ticks_ms(), start) > timeout:
            return -1, timeout
        # 3つのスイッチを順番に調べる
        for i, sw in enumerate(sws):
            if sw.value() == 0:
                # ★【追加①】チャタリング防止をここに入れる
                return i, time.ticks_diff(time.ticks_ms(), start)

# ---- ゲーム開始 ----
print("=" * 28)
print("  反射神経ゲーム スタート！")
print("  光ったLEDのスイッチを押せ！")
print("=" * 28)
time.sleep(1)

score    = 0      # 正解数
total_ms = 0      # 反応時間の合計

# ---- ラウンドループ ----
for r in range(1, ROUNDS + 1):
    all_off()

    # ---- レベルアップ：進むほど難しくなる ----
    if r <= 3:
        level, max_wait, timeout = 1, 2000, 2000    # やさしい
    elif r <= 6:
        level, max_wait, timeout = 2, 1500, 1200    # ふつう
    else:
        level, max_wait, timeout = 3, 1000,  800    # むずかしい

    print(f"第{r}問  レベル {'★' * level}{'☆' * (3 - level)}")

    # ランダムな時間だけ待ってから光らせる
    time.sleep_ms(random.randint(500, max_wait))

    n = random.randint(0, 2)          # 光らせるLEDを選ぶ
    leds[n].value(1)
    print(f"  → {names[n]}！")

    pressed, ms = wait_for_switch(timeout)
    all_off()

    # ---- 判定 ----
    if pressed == -1:
        print("  時間切れ！")
        # ★【追加②】不正解の演出をここに入れる
    elif pressed == n:
        score    += 1
        total_ms += ms
        print(f"  正解！ {ms}ms")
        # ★【追加②】正解の演出をここに入れる
    else:
        print(f"  不正解… {names[pressed]}を押した")
        # ★【追加②】不正解の演出をここに入れる

    time.sleep(0.3)

# ---- 結果表示 ----
print("=" * 28)
print(f"  結果: {score} / {ROUNDS} 問正解")
if score > 0:
    avg = total_ms // score
    print(f"  平均反応時間: {avg} ms")
    # ★【追加③】LEDでランクを表示する
print("=" * 28)