import machine, neopixel, time
# 設定
PIN_NUM = 22      # GP22
LED_COUNT = 7
# 初期化
np = neopixel.NeoPixel(machine.Pin(PIN_NUM), LED_COUNT)
def test_loop():
    colors = [
        (255, 0, 0),   # 赤
        (0, 255, 0),   # 緑
        (0, 0, 255),   # 青
        (255, 255, 255) # 白
    ]
    
    for c in colors:
        for i in range(LED_COUNT):
            np[i] = c
        np.write()
        time.sleep(0.5)
    
    # 終了時に消灯
    for i in range(LED_COUNT): np[i] = (0,0,0)
    np.write()
    print("Test Completed!")
test_loop()