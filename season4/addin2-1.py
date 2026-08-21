def blink_all(times=2):
    """正解の演出：全LEDをパッパッと点滅"""
    for _ in range(times):
        for led in leds:
            led.value(1)
        time.sleep_ms(80)
        all_off()
        time.sleep_ms(80)

def blink_one(n, times=3):
    """不正解の演出：正解だったLEDを速く点滅して教える"""
    for _ in range(times):
        leds[n].value(1)
        time.sleep_ms(50)
        leds[n].value(0)
        time.sleep_ms(50)