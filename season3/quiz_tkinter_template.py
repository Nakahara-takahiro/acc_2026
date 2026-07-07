import tkinter as tk
from tkinter import messagebox
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

shuffled_quiz = list(quiz)
random.shuffle(shuffled_quiz)

scores = {}

current_index = 0
current_choices = []

# 3択の選択肢を作る関数
def make_choices(correct_answer):
    all_answers = [q[1] for q in quiz]
    dummies = [ans for ans in all_answers if ans != correct_answer]
    selected_dummies = random.sample(dummies, 2)
    choices = [correct_answer] + selected_dummies
    random.shuffle(choices)
    return choices

# 問題を画面に表示する関数
def show_question():
    '''
    ここに入力する
    '''

# ボタンが押されたときに動く関数
def click_button(btn_num):
    global current_index
    
    selected_answer = current_choices[btn_num]
    q, a, category = shuffled_quiz[current_index]
    
    '''
    ここに入力する
    '''
    
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
    
    result_text = "--- カテゴリ別結果 ---\n"
    total_correct = 0
    
    for category, count in scores.items():
        result_text += f"{category}：{count}問正解\n"
        total_correct += count
        
    label_info.config(text="クイズ終了！")
    label_question.config(text=f"お疲れ様でした！\n合計正解数: {total_correct}問\n\n{result_text}")

# ーーー tkinterの画面作成 ーーー
root = tk.Tk()
root.title("3択クイズアプリ")
root.geometry("400x350")

'''
ここに入力する
'''
