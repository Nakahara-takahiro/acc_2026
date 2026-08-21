if pressed == -1:
        print("  時間切れ！")
        blink_one(n)                       # 正解を光で教える
    elif pressed == n:
        score    += 1
        total_ms += ms
        print(f"  正解！ {ms}ms")
        blink_all()                        # おめでとう演出
    else:
        print(f"  不正解… {names[pressed]}を押した")
        blink_one(n)                       # 正解を光で教える