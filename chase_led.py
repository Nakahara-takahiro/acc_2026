import machine, neopixel, time

# --- 準備設定 ---
PIN_NO = 22      
LED_KAZU = 7     
SPEED = 0.05     # 動くスピード (小さいほど速い)

np = neopixel.NeoPixel(machine.Pin(PIN_NO), LED_KAZU)

# 使いたい色のリスト (赤, 緑, 青, 黄, 紫)
IRO_LIST = [
    (255, 0, 0),   # 赤
    (0, 255, 0),   # 緑
    (0, 0, 255),   # 青
    (255, 255, 0), # 黄
    (255, 0, 255)  # 紫
]

print("スタート！ (Ctrl+C で止まるよ)")

try:
    while True: # ずっとくり返す
        # 1. 色のリストから ひとつずつ色を取り出す
        for iro in IRO_LIST:
            
            # 2. LEDを はしから順番に光らせる
            for i in range(LED_KAZU):
                np[i] = iro      
                np.write()       
                time.sleep(SPEED) 
                
                np[i] = (0, 0, 0) 

except KeyboardInterrupt:
    # プログラムを止めたときは、全部のLEDを消す
    for i in range(LED_KAZU):
        np[i] = (0, 0, 0)
    np.write()
    print("ストップしたよ")
