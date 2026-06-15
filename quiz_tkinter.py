import tkinter as tk
from tkinter import messagebox
import random  # ★quiz_random.pyの1行目と同じ

# ★quiz_random.pyの3〜14行目と同じクイズデータ
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

# リストをランダムに並び替え（★quiz_random.pyの16行目と同じ）
shuffled_quiz = list(quiz)
random.shuffle(shuffled_quiz)

# スコアを記録する辞書（★quiz_random.pyの18行目と同じ）
scores = {}

# 現在の問題の番号 (0からスタート)
current_index = 0
# 現在の画面に表示されている3つの選択肢
current_choices = []

# 3択の選択肢を作る関数
def make_choices(correct_answer):
    # すべての問題の「答え」を取り出してリストにする
    all_answers = [q[1] for q in quiz]
    # 正解以外の答え（ダミー候補）のリストを作る
    dummies = [ans for ans in all_answers if ans != correct_answer]
    # ダミー候補からランダムに2つ選ぶ
    selected_dummies = random.sample(dummies, 2)
    # 正解とダミーを合わせたリストを作る
    choices = [correct_answer] + selected_dummies
    # 選択肢をランダムに並べ替える
    random.shuffle(choices)
    return choices

# 問題を画面に表示する関数
def show_question():
    global current_choices
    
    # 現在の問題データを取得する（★quiz_random.pyの20行目のfor文と同じ変数）
    q, a, category = shuffled_quiz[current_index]
    
    # 画面のラベル（情報、問題文）を書き換える
    label_info.config(text=f"【{category}】 第 {current_index + 1} 問 / 全 {len(quiz)} 問")
    label_question.config(text=q)  # qを表示（★quiz_random.pyの21行目のprint(q)に対応）
    
    # 3択を生成する
    current_choices = make_choices(a)
    
    # ボタンの文字を更新する
    btn1.config(text=current_choices[0])
    btn2.config(text=current_choices[1])
    btn3.config(text=current_choices[2])

# ボタンが押されたときに動く関数
def click_button(btn_num):
    global current_index
    
    # 押されたボタンの回答と、現在の問題の正解・カテゴリを取得
    selected_answer = current_choices[btn_num]
    q, a, category = shuffled_quiz[current_index]
    
    # 正誤判定（★quiz_random.pyの23〜27行目と同じ判定とスコア記録ロジック）
    if selected_answer == a:
        messagebox.showinfo("結果", "正解！")
        scores[category] = scores.get(category, 0) + 1  # ★quiz_random.pyの25行目と同じ
    else:
        messagebox.showinfo("結果", f"残念… 正解は {a}")  # ★quiz_random.py of 27行目と同じ
        
    # 次の問題へ進む
    current_index += 1
    if current_index < len(quiz):
        show_question()
    else:
        show_result()

# 結果画面を表示する関数
def show_result():
    # 選択肢ボタンを画面から消す
    btn1.pack_forget()
    btn2.pack_forget()
    btn3.pack_forget()
    
    # 結果のテキストを作る（★quiz_random.pyの29行目に対応）
    result_text = "--- カテゴリ別結果 ---\n"
    total_correct = 0
    
    # カテゴリごとの正解数をループで取り出す（★quiz_random.pyの30〜31行目と同じループ）
    for category, count in scores.items():
        result_text += f"{category}：{count}問正解\n"
        total_correct += count
        
    # 画面表示を最終結果に更新する
    label_info.config(text="クイズ終了！")
    label_question.config(text=f"お疲れ様でした！\n合計正解数: {total_correct}問\n\n{result_text}")

# ーーー tkinterの画面作成 ーーー
root = tk.Tk()
root.title("3択クイズアプリ")
root.geometry("400x350")

# ラベルの作成と配置
label_info = tk.Label(root, text="", font=("MS Gothic", 12))
label_info.pack(pady=10)

label_question = tk.Label(root, text="", font=("MS Gothic", 14, "bold"), wraplength=350)
label_question.pack(pady=20)

# ボタンの作成と配置（押されたボタンの番号を click_button に渡す）
btn1 = tk.Button(root, text="", font=("MS Gothic", 12), width=30, command=lambda: click_button(0))
btn1.pack(pady=5)

btn2 = tk.Button(root, text="", font=("MS Gothic", 12), width=30, command=lambda: click_button(1))
btn2.pack(pady=5)

btn3 = tk.Button(root, text="", font=("MS Gothic", 12), width=30, command=lambda: click_button(2))
btn3.pack(pady=5)

# クイズを開始する
show_question()

# 画面を表示し続ける
root.mainloop()
