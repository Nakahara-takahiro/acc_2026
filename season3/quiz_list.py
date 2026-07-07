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

scores = {}

for q, a, category in quiz:
    print(q)
    ans = input("答えは？ ")
    if ans == a:
        print("正解！")
        scores[category] = scores.get(category, 0) + 1
    else:
        print(f"残念… 正解は {a}")

print("\n--- カテゴリ別結果 ---")
for category, count in scores.items():
    print(f"{category}：{count}問正解")

print("\n辞書の中身：", scores)
