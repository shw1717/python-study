import flet as ft
import random

def main(page: ft.Page):
    page.title = "가위바위보 게임"
    page.window_width = 400
    page.window_height = 500

    user_score = 0
    com_score = 0

    result_text = ft.Text("게임을 시작하세요!", size=20)
    score_text = ft.Text("점수: 0 : 0", size=16)

    def play(user_choice):
        nonlocal user_score, com_score

        com_choice = random.randint(1, 3)

        choices = {1: "가위", 2: "바위", 3: "보"}

        if user_choice == com_choice:
            result = "무승부"
        elif (user_choice == 1 and com_choice == 3) or \
             (user_choice == 2 and com_choice == 1) or \
             (user_choice == 3 and com_choice == 2):
            result = "승리!"
            user_score += 1
        else:
            result = "패배!"
            com_score += 1

        result_text.value = f"나: {choices[user_choice]} / 컴퓨터: {choices[com_choice]}\n결과: {result}"
        score_text.value = f"점수: {user_score} : {com_score}"

        if user_score == 3:
            result_text.value += "\n 최종 승리!"
            reset()
        elif com_score == 3:
            result_text.value += "\n 컴퓨터 승리!"
            reset()

        page.update()

    def reset():
        nonlocal user_score, com_score
        user_score = 0
        com_score = 0

    page.add(
        ft.Column(
            [
                ft.Text("가위바위보 게임", size=30, weight="bold"),
                result_text,
                score_text,
                ft.Row(
                    [
                        ft.ElevatedButton("가위 ", on_click=lambda e: play(1)),
                        ft.ElevatedButton("바위 ", on_click=lambda e: play(2)),
                        ft.ElevatedButton("보 ", on_click=lambda e: play(3)),
                    ],
                    alignment="center"
                )
            ],
            alignment="center",
            horizontal_alignment="center"
        )
    )

ft.app(target=main)