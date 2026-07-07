from machine import Pin
import time

# 内部プルアップで入力設定
sw13 = Pin(13, Pin.IN, Pin.PULL_UP)
sw14 = Pin(14, Pin.IN, Pin.PULL_UP)
sw15 = Pin(15, Pin.IN, Pin.PULL_UP)

# 前回の状態を保持（チャタリング対策用）
prev13 = 1
prev14 = 1
prev15 = 1

while True:
    cur13 = sw13.value()
    cur14 = sw14.value()
    cur15 = sw15.value()

    # LOW（0）になった瞬間 = 押した瞬間だけ検出
    if cur13 == 0 and prev13 == 1:
        print("SW13 が押されました")

    if cur14 == 0 and prev14 == 1:
        print("SW14 が押されました")

    if cur15 == 0 and prev15 == 1:
        print("SW15 が押されました")

    prev13 = cur13
    prev14 = cur14
    prev15 = cur15

    time.sleep_ms(20)  # チャタリング対策（20ms）
