import flet as ft

class Calculator:
    def __init__(self):
        self.expression = ""

    def add(self, value):
        self.expression += str(value)

    def clear(self):
        self.expression = ""

    def delete(self):
        self.expression = self.expression[:-1]

    def calculate(self):
        try:
            result = eval(self.expression)
            return result
        except:
            return "Error"

    def get_numbers(self):
        tokens = self.expression.replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").split()
        nums = []
        for t in tokens:
            try:
                nums.append(float(t))
            except:
                pass
        return nums

    def get_stats(self):
        nums = self.get_numbers()
        if not nums:
            return None
        return {
            "평균": sum(nums) / len(nums),
            "최대": max(nums),
            "최소": min(nums)
        }


def main(page: ft.Page):
    page.title = "계산기 게임"
    page.window_width = 350
    page.window_height = 550
    page.bgcolor = "#1e1e1e"

    calc = Calculator()

    display = ft.Text(value="", size=30, color="white")

    stats_text = ft.Text(value="", size=14, color="white")

    def update_display():
        display.value = calc.expression
        page.update()

    def button_click(e):
        calc.add(e.control.data)
        update_display()

    def clear_click(e):
        calc.clear()
        stats_text.value = ""
        update_display()

    def delete_click(e):
        calc.delete()
        update_display()

    def equal_click(e):
        result = calc.calculate()

        if result == "Error":
            display.value = "Error"
            stats_text.value = ""
        else:
            stats = calc.get_stats()
            display.value = str(result)

            if stats:
                stats_text.value = (
                    f"평균: {stats['평균']:.2f} | "
                    f"최대: {stats['최대']:.2f} | "
                    f"최소: {stats['최소']:.2f}"
                )

        page.update()

    def create_button(text, color="#333", data=None):
        return ft.ElevatedButton(
            text,
            data=data if data else text,
            width=70,
            height=60,
            bgcolor=color,
            color="white",
            on_click=button_click
        )

    page.add(
        ft.Column(
            [
                ft.Container(display, alignment=ft.Alignment(1, 0), padding=20),
                ft.Container(stats_text, alignment=ft.Alignment(1, 0), padding=10),

                ft.Row([create_button("7"), create_button("8"), create_button("9"), create_button("/", "#ff9500")]),
                ft.Row([create_button("4"), create_button("5"), create_button("6"), create_button("*", "#ff9500")]),
                ft.Row([create_button("1"), create_button("2"), create_button("3"), create_button("-", "#ff9500")]),
                ft.Row([create_button("0"), create_button("."), 
                        ft.ElevatedButton("⌫", on_click=delete_click, width=70, height=60),
                        create_button("+", "#ff9500")]),

                ft.Row([
                    ft.ElevatedButton("C", on_click=clear_click, width=150, height=60, bgcolor="red", color="white"),
                    ft.ElevatedButton("=", on_click=equal_click, width=150, height=60, bgcolor="#00c853", color="white"),
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)