if score > 0:
    avg = total_ms // score
    print(f"  平均反応時間: {avg} ms")
    show_rank(avg)              # ← LEDでランクを表示