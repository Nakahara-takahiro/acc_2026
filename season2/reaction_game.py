import machine
import neopixel
import time
import _thread
import sys

# ハードウェア設定
PIN_CONFIG = {
    "LED_PIN": 22,       # WS2812B接続GPIO番号
    "BUTTON_PIN": 15,    # タクトスイッチ接続GPIO番号
    "NUM_LEDS": 7,       # LEDの数
    "CENTER_LED": 3      # 中央のLED（0ベースで3 = 4番目）
}

# タイミング設定
TIMING = {
    "ANIMATION_DELAY": 0.05,  # LEDの点灯間隔（秒）
    "PAUSE_TIME": 2,          # 一時停止時間（秒）
    "BLINK_DELAY": 0.05,      # 点滅間隔（秒）
    "DEBOUNCE_TIME": 50       # チャタリング防止時間（ミリ秒）
}

# ゲーム設定
GAME_CONFIG = {
    "BLINK_COUNT": 5     # 点滅回数
}

# 色の定義
COLORS = {
    "RED": (50, 0, 0),    # 明るさを下げた赤
    "BLUE": (0, 0, 70),   # 明るさを下げた青
    "OFF": (0, 0, 0)      # 消灯
}


class LEDController:
    """LEDの制御を行うクラス"""
    
    def __init__(self, pin, num_leds, center_led):
        """LEDコントローラーの初期化"""
        self.np = neopixel.NeoPixel(machine.Pin(pin), num_leds)
        self.num_leds = num_leds
        self.center_led = center_led
        
    def clear(self):
        """すべてのLEDをオフにする"""
        for i in range(self.num_leds):
            self.np[i] = COLORS["OFF"]
        self.np.write()
        
    def set_initial_state(self):
        """初期状態に設定（中央は赤、他は消灯）"""
        for i in range(self.num_leds):
            self.np[i] = COLORS["RED"] if i == self.center_led else COLORS["OFF"]
        self.np.write()
        
    def update_led(self, pos):
        """指定位置のLEDを更新"""
        self.clear()
        color = COLORS["RED"] if pos == self.center_led else COLORS["BLUE"]
        self.np[pos] = color
        self.np.write()
        
    def blink(self, times, delay):
        """現在のLED状態を保存して点滅させる"""
        # 現在のLED状態を保存
        current_state = [self.np[i] for i in range(self.num_leds)]
        
        # 指定回数点滅
        for _ in range(times):
            # 消灯
            self.clear()
            time.sleep(delay)
            
            # 点灯（元の状態に戻す）
            for i in range(self.num_leds):
                self.np[i] = current_state[i]
            self.np.write()
            time.sleep(delay)


class ButtonHandler:
    """ボタン入力を処理するクラス"""
    
    def __init__(self, pin, debounce_time):
        """ボタンハンドラの初期化"""
        self.button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.debounce_time = debounce_time
        self.last_press_time = 0
        
    def is_pressed(self):
        """チャタリング防止付きのボタン押下検出"""
        if self.button.value() == 0:  # ボタンが押された（プルアップなので0）
            current_time = time.ticks_ms()
            
            # チャタリング防止
            if time.ticks_diff(current_time, self.last_press_time) > self.debounce_time:
                self.last_press_time = current_time
                return True
        return False


class ReflexGame:
    """反射神経ゲームの管理クラス"""
    
    def __init__(self):
        """ゲームの初期化"""
        self.led_controller = LEDController(
            PIN_CONFIG["LED_PIN"], 
            PIN_CONFIG["NUM_LEDS"], 
            PIN_CONFIG["CENTER_LED"]
        )
        self.button_handler = ButtonHandler(
            PIN_CONFIG["BUTTON_PIN"], 
            TIMING["DEBOUNCE_TIME"]
        )
        self.running = True
        self.paused = False
        
        # アニメーションの順序（0ベースインデックス）
        self.sequence = [3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 1, 2]
        
    def handle_button_press(self):
        """ボタン押下時の処理"""
        if self.button_handler.is_pressed() and not self.paused:
            self.paused = True
            time.sleep(TIMING["PAUSE_TIME"])
            self.led_controller.blink(GAME_CONFIG["BLINK_COUNT"], TIMING["BLINK_DELAY"])
            self.paused = False
            return True
        return False
    
    def run_animation(self):
        """LEDアニメーションを実行"""
        self.led_controller.set_initial_state()
        
        try:
            while self.running:
                for pos in self.sequence:
                    if not self.running:
                        break
                        
                    if self.paused:
                        # 一時停止中は待機
                        while self.paused and self.running:
                            time.sleep(0.1)
                        continue
                    
                    # LEDを更新
                    self.led_controller.update_led(pos)
                    
                    # 点灯間隔待機中にボタンチェック
                    start_time = time.ticks_ms()
                    while time.ticks_diff(time.ticks_ms(), start_time) < TIMING["ANIMATION_DELAY"] * 1000:
                        if self.handle_button_press() or not self.running or self.paused:
                            break
                        time.sleep(0.01)
                    
        except Exception as e:
            print(f"アニメーションエラー: {e}")
        finally:
            if not self.paused:
                self.led_controller.clear()
    
    def stop(self):
        """ゲームを停止"""
        self.running = False
        time.sleep(0.5)  # スレッドが終了するのを少し待つ
        self.led_controller.clear()

# メイン処理
def main():
    game = ReflexGame()
    
    # アニメーションを別スレッドで開始
    _thread.start_new_thread(game.run_animation, ())
    
    try:
        while True:
            # メインスレッドでも定期的にボタンチェック
            game.handle_button_press()
            time.sleep(0.1)
    except KeyboardInterrupt:
        game.stop()
        print("プログラムを終了します")


if __name__ == "__main__":
    main()