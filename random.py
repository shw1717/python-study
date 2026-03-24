import flet as ft
import random

def main(page: ft.Page):
    page.title = "업다운 게임"

    answer = random.randint(1, 100)
    result = ft.Text("1~100 사이 숫자를 맞춰보세요!", size=20)
    input_box = ft.TextField(label="숫자 입력", width=200)
    
    def check(e):
        nonlocal answer
        try:
            user = int(input_box.value)

            if user < answer:
                result.value = "UP"
            elif user > answer:
                result.value = "DOWN"
            else:
                result.value = "정답입니다!"
            
        except:
            result.value = "숫자를 입력하세요!"
        
        page.update()

    input_box.value = ""
    page.update()

    page.add(
        result,
        input_box,
        ft.ElevatedButton("확인", on_click=check)
    )

ft.app(target=main)