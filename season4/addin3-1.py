def show_rank(avg):
    """平均反応時間からランクを決めて、LEDと文字で知らせる"""

    # ---- ランクを決める ----
    # count = 光らせるLEDの数（多いほど良い）
    if   avg < 250: rank, count = "SS", 3
    elif avg < 350: rank, count = "S",  3
    elif avg < 500: rank, count = "A",  2
    elif avg < 700: rank, count = "B",  1
    else:           rank, count = "C",  1

    print(f"  ランク: {rank}")
    all_off()
    time.sleep(1)     # 発表前のタメ

    # ---- SSだけ特別演出：全LEDが高速に光る ----
    if rank == "SS":
        for _ in range(10):
            for led in leds:
                led.value(1)
            time.sleep_ms(40)
            all_off()
            time.sleep_ms(40)

    # ---- ランクの数だけLEDを1つずつ点灯していく ----
    all_off()
    for i in range(count):
        leds[i].value(1)
        time.sleep_ms(400)     # 1つずつ増えていくのを見せる

    # ---- Cだけゆっくり点滅（もう少しがんばろう） ----
    if rank == "C":
        for _ in range(3):
            all_off()
            time.sleep_ms(400)
            leds[0].value(1)
            time.sleep_ms(400)