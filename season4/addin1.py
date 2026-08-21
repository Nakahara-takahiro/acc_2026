# 3つのスイッチを順番に調べる
        for i, sw in enumerate(sws):
            if sw.value() == 0:
                # ---- チャタリング防止 ----
                # ①まず反応時間を記録しておく（20msを含めないため）
                elapsed = time.ticks_diff(time.ticks_ms(), start)
                # ②20ミリ秒だけ待つ
                time.sleep_ms(20)
                # ③まだ押されていれば「本物の入力」
                if sw.value() == 0:
                    while sw.value() == 0:   # 指を離すまで待つ
                        pass
                    return i, elapsed
                # 20ms後に離れていた → ノイズなので無視して調べ直す