''' mermaid
flowchart TD
    A([スタート]) --> B[ピンの設定\nGP10赤 GP11緑 GP12青]
    B --> C[["while True\n（ずっと繰り返す）"]]
    C --> D[全LEDを消灯]
    D --> E["待ち時間を決める\nrandom.uniform(1.0, 3.0)"]
    E --> F["その時間だけ待つ\ntime.sleep(wait)"]
    F --> G["光らせるLEDを選ぶ\nrandom.choice(leds)"]
    G --> H[選んだLEDを点灯]
    H --> I["0.5秒待つ\ntime.sleep(0.5)"]
    I --> C
'''