import random

quiz = [
    ("日本の首都は？", "東京", "地理"),
    ("日本一長い川は？", "信濃川", "地理"),
    ("日本一高い山は？", "富士山", "地理"),
    ("光合成をする器官は？", "葉緑体", "理科"),
    ("水の化学式は？", "H2O", "理科"),
    ("音の速さは約何m/sか？", "340", "理科"),
    ("地球の表面積の約何割が海か？", "7", "理科"),
    ("徳川幕府を開いたのは？", "徳川家康", "歴史"),
    ("日本で最初の元号は？", "大化", "歴史"),
    ("大政奉還が行われた年は？", "1867", "歴史"),
]

random.shuffle(quiz)  # リストをランダムに並び替え

scores = {}

for q, a, category in quiz:
    # カテゴリが初登場なら初期化
    if category not in scores:
        scores[category] = {"出題数": 0, "正解数": 0}

    scores[category]["出題数"] += 1

    print(q)
    ans = input("答えは？ ")
    if ans == a:
        print("正解！")
        scores[category]["正解数"] += 1
    else:
        print(f"残念… 正解は {a}")

# 集計
total = len(quiz)
correct = sum(v["正解数"] for v in scores.values())
rate = correct / total * 100

# 苦手カテゴリ：正解率が最も低いカテゴリ
weak = min(scores, key=lambda c: scores[c]["正解数"] / scores[c]["出題数"])

print("\n--- 結果 ---")
print(f"全体：{total}問中{correct}問正解（正解率 {rate:.0f}%）")
print()

print("カテゴリ別：")
for category, v in scores.items():
    r = v["正解数"] / v["出題数"] * 100
    print(f"  {category}：{v['出題数']}問中{v['正解数']}問正解（{r:.0f}%）")

print()
print(f"苦手なカテゴリ：{weak}")
print("\n辞書の中身：", scores)
