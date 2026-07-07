"""
simple_shooting.py
ロータリーエンコーダーを使ったシューティングゲーム
対象: Raspberry Pi Pico + SSD1306 OLED (共立実験基板)

画面: SSD1306 物理128×64 を論理64×128 ポートレートとして使用
      座標変換 (90° CW 回転): 物理 px = 127-ly, py = lx
      上下が逆に見える場合は lpx() 内を oled.pixel(ly, 63-lx, col) に変更
"""

import machine
import ssd1306
import random
import utime

# ════════════════════════════════════════════════════════════
#  ハードウェア初期化
# ════════════════════════════════════════════════════════════
i2c  = machine.I2C(0,
                   sda=machine.Pin(8),
                   scl=machine.Pin(9),
                   freq=400_000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

enc_a = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
enc_b = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
sw    = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# ════════════════════════════════════════════════════════════
#  定数
# ════════════════════════════════════════════════════════════
LW             = 64     # 論理画面幅  (px)
LH             = 128    # 論理画面高  (px)

FIELD_TOP      = 10     # ゲームフィールド上端 Y
PLAYER_Y       = 120    # 自機 Y 固定位置（底辺）
PLAYER_INIT_X  = 28     # 自機初期 X（底辺中央）
PLAYER_STEP    = 2      # 1ステップあたりの移動量 (px)
PLAYER_MINX    = 4      # 自機左端クランプ
PLAYER_MAXX    = 59     # 自機右端クランプ

BULLET_SPEED   = 4      # 弾移動速度 (px/frame)
MAX_BULLETS    = 3      # 弾の同時最大数

ENEMY_SPEED    = 1      # 敵機移動速度 (px/frame)
MAX_ENEMIES    = 5      # 敵機の同時最大数
ENEMY_INTERVAL = 60     # 敵機出現間隔 (frame)
ENEMY_DEAD_Y   = 118    # 敵機がこの Y 以上に達するとゲームオーバー

ENC_STEPS      = 4      # 移動1ステップに必要なエンコーダーパルス数
                        # クリック感のあるエンコーダーは 4、ないものは 2
SW_DB_MS       = 50     # スイッチデバウンス (ms)
FRAME_MS       = 50     # フレーム周期 (ms) 約20fps

SCORE_KILL     = 10     # 敵撃墜スコア

# ════════════════════════════════════════════════════════════
#  座標変換
#  論理 (lx, ly)  64x128 ポートレート空間
#  ->  物理 (px, py) 128x64 ランドスケープ空間（90度 CW 回転）
#     物理 px = 127 - ly
#     物理 py = lx
# ════════════════════════════════════════════════════════════
def lpx(lx, ly, col=1):
    if 0 <= lx < LW and 0 <= ly < LH:
        oled.pixel(127 - ly, lx, col)

# ════════════════════════════════════════════════════════════
#  ミニフォント（5行 x 3列）
#  各行: 3ビット、bit2=左列 / bit1=中列 / bit0=右列
# ════════════════════════════════════════════════════════════
_FONT = {
    '0': [0b111, 0b101, 0b101, 0b101, 0b111],
    '1': [0b010, 0b110, 0b010, 0b010, 0b111],
    '2': [0b111, 0b001, 0b111, 0b100, 0b111],
    '3': [0b111, 0b001, 0b111, 0b001, 0b111],
    '4': [0b101, 0b101, 0b111, 0b001, 0b001],
    '5': [0b111, 0b100, 0b111, 0b001, 0b111],
    '6': [0b111, 0b100, 0b111, 0b101, 0b111],
    '7': [0b111, 0b001, 0b001, 0b001, 0b001],
    '8': [0b111, 0b101, 0b111, 0b101, 0b111],
    '9': [0b111, 0b101, 0b111, 0b001, 0b111],
    ':': [0b000, 0b010, 0b000, 0b010, 0b000],
    ' ': [0b000, 0b000, 0b000, 0b000, 0b000],
    'A': [0b111, 0b101, 0b111, 0b101, 0b101],
    'C': [0b111, 0b100, 0b100, 0b100, 0b111],
    'D': [0b110, 0b101, 0b101, 0b101, 0b110],
    'E': [0b111, 0b100, 0b111, 0b100, 0b111],
    'F': [0b111, 0b100, 0b111, 0b100, 0b100],
    'G': [0b111, 0b100, 0b101, 0b101, 0b111],
    'H': [0b101, 0b101, 0b111, 0b101, 0b101],
    'I': [0b111, 0b010, 0b010, 0b010, 0b111],
    'K': [0b101, 0b101, 0b110, 0b101, 0b101],
    'N': [0b101, 0b111, 0b101, 0b101, 0b101],
    'O': [0b111, 0b101, 0b101, 0b101, 0b111],
    'P': [0b110, 0b101, 0b110, 0b100, 0b100],
    'R': [0b110, 0b101, 0b110, 0b101, 0b101],
    'S': [0b111, 0b100, 0b111, 0b001, 0b111],
    'T': [0b111, 0b010, 0b010, 0b010, 0b010],
    'U': [0b101, 0b101, 0b101, 0b101, 0b111],
    'V': [0b101, 0b101, 0b101, 0b101, 0b010],
    'W': [0b101, 0b101, 0b101, 0b111, 0b010],
}

def draw_str(lx, ly, text, col=1):
    """論理座標 (lx, ly) を基点に文字列を描画。文字ピッチ 4px"""
    for i, ch in enumerate(text.upper()):
        pat = _FONT.get(ch)
        if pat is None:
            continue
        ox = lx + i * 4
        for row, bits in enumerate(pat):
            for bit in range(3):
                if bits & (0b100 >> bit):
                    lpx(ox + bit, ly + row, col)

# ════════════════════════════════════════════════════════════
#  図形描画（論理座標系）
# ════════════════════════════════════════════════════════════
def draw_player(cx, cy, col=1):
    # 自機：塗りつぶし上向き三角形
    # 頂点 (cx, cy-4)、底辺中央 (cx, cy)、底辺幅 9px
    for r in range(5):
        for dx in range(-r, r + 1):
            lpx(cx + dx, cy - 4 + r, col)


def draw_enemy(ex, ey, col=1):
    # 敵機：アウトライン菱形
    # 中心 (ex, ey)、幅 9px / 高さ 9px
    for r in range(9):
        half = r if r <= 4 else 8 - r
        if half == 0:
            lpx(ex, ey - 4 + r, col)
        else:
            lpx(ex - half, ey - 4 + r, col)
            lpx(ex + half, ey - 4 + r, col)


def draw_bullet(bx, by, col=1):
    # 弾：2x2 矩形
    lpx(bx,     by,     col)
    lpx(bx + 1, by,     col)
    lpx(bx,     by + 1, col)
    lpx(bx + 1, by + 1, col)


def draw_divider():
    # スコアエリアとフィールドの区切り線
    for x in range(LW):
        lpx(x, FIELD_TOP - 1, 1)

# ════════════════════════════════════════════════════════════
#  エンコーダー入力（ステートマシン方式）
#
#  状態 = (A<<1)|B の 2bit 値（0-3）
#  遷移テーブル: index = (前状態<<2)|現状態  値: +1(CW) / -1(CCW) / 0(無効)
#  チャタリングによる誤遷移は +1/-1 が交互に出て打ち消し合う
#  時間ベースのデバウンスは不要
#
#  回転方向が逆の場合: _ENC_TABLE の +1 と -1 を入れ替える
# ════════════════════════════════════════════════════════════
_ENC_TABLE = [0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0]
_enc_state = (enc_a.value() << 1) | enc_b.value()
_enc_cnt   = 0
_enc_dx    = 0

def _enc_irq(_pin):
    global _enc_state, _enc_cnt, _enc_dx
    new_state  = (enc_a.value() << 1) | enc_b.value()
    _enc_cnt  += _ENC_TABLE[(_enc_state << 2) | new_state]
    _enc_state = new_state
    if _enc_cnt >= ENC_STEPS:
        _enc_dx  += PLAYER_STEP
        _enc_cnt -= ENC_STEPS
    elif _enc_cnt <= -ENC_STEPS:
        _enc_dx  -= PLAYER_STEP
        _enc_cnt += ENC_STEPS

enc_a.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=_enc_irq)
enc_b.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=_enc_irq)

# ════════════════════════════════════════════════════════════
#  スイッチ入力
# ════════════════════════════════════════════════════════════
_sw_prev    = 1
_sw_last_ms = 0

def sw_pressed():
    global _sw_prev, _sw_last_ms
    val = sw.value()
    now = utime.ticks_ms()
    if val != _sw_prev and utime.ticks_diff(now, _sw_last_ms) >= SW_DB_MS:
        _sw_prev    = val
        _sw_last_ms = now
        return val == 0
    return False

# ════════════════════════════════════════════════════════════
#  ゲーム変数
# ════════════════════════════════════════════════════════════
STATE_PLAY = 0
STATE_OVER = 1

player_x = PLAYER_INIT_X
bullets  = []
enemies  = []
score    = 0
frame_n  = 0
state    = STATE_PLAY


def reset_game():
    global player_x, bullets, enemies, score, frame_n, state, _enc_dx, _enc_cnt
    player_x = PLAYER_INIT_X
    bullets  = []
    enemies  = []
    score    = 0
    frame_n  = 0
    state    = STATE_PLAY
    _enc_dx  = 0
    _enc_cnt = 0

# ════════════════════════════════════════════════════════════
#  描画
# ════════════════════════════════════════════════════════════
def render_game():
    oled.fill(0)
    draw_divider()
    draw_str(1, 1, "SC:" + str(score))
    draw_player(player_x, PLAYER_Y)
    for b in bullets:
        draw_bullet(b[0], b[1])
    for e in enemies:
        draw_enemy(e[0], e[1])
    oled.show()


def render_gameover():
    oled.fill(0)
    draw_str(12, 20, "GAME")
    draw_str(12, 30, "OVER")
    draw_str(1,  50, "SC:" + str(score))
    draw_str(8,  72, "PUSH")
    draw_str(4,  84, "SW TO")
    draw_str(4,  96, "START")
    oled.show()

# ════════════════════════════════════════════════════════════
#  メインループ
# ════════════════════════════════════════════════════════════
reset_game()
render_game()

while True:
    t0      = utime.ticks_ms()
    pressed = sw_pressed()

    if state == STATE_OVER:
        if pressed:
            reset_game()
            render_game()
        utime.sleep_ms(max(0, FRAME_MS - utime.ticks_diff(utime.ticks_ms(), t0)))
        continue

    # 入力
    irq_s   = machine.disable_irq()
    dx      = _enc_dx
    _enc_dx = 0
    machine.enable_irq(irq_s)

    player_x = max(PLAYER_MINX, min(PLAYER_MAXX, player_x + dx))

    if pressed and len(bullets) < MAX_BULLETS:
        bullets.append([player_x, PLAYER_Y - 6])

    # 更新
    new_bullets = []
    for b in bullets:
        ny = b[1] - BULLET_SPEED
        if ny >= 0:
            new_bullets.append([b[0], ny])
    bullets = new_bullets

    for e in enemies:
        e[1] += ENEMY_SPEED

    frame_n += 1
    if frame_n % ENEMY_INTERVAL == 0 and len(enemies) < MAX_ENEMIES:
        enemies.append([random.randint(4, 59), FIELD_TOP + 4])

    # 衝突判定
    hit_bullets  = set()
    live_enemies = []
    for e in enemies:
        ex, ey = e[0], e[1]
        killed = False
        for i, b in enumerate(bullets):
            if i in hit_bullets:
                continue
            bx, by = b[0], b[1]
            if bx <= ex + 4 and bx + 1 >= ex - 4 and by <= ey + 4 and by + 1 >= ey - 4:
                hit_bullets.add(i)
                score += SCORE_KILL
                killed = True
                break
        if not killed:
            live_enemies.append(e)
    bullets = [b for i, b in enumerate(bullets) if i not in hit_bullets]
    enemies = live_enemies

    # ゲームオーバー判定
    if any(e[1] >= ENEMY_DEAD_Y for e in enemies):
        state = STATE_OVER
        render_gameover()
        utime.sleep_ms(max(0, FRAME_MS - utime.ticks_diff(utime.ticks_ms(), t0)))
        continue

    # 描画
    render_game()

    elapsed = utime.ticks_diff(utime.ticks_ms(), t0)
    utime.sleep_ms(max(0, FRAME_MS - elapsed))
