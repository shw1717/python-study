import flet as ft
import random

# 점수 계산 클래스
class BowlingGame:
    def __init__(self):
        self.rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def is_strike(self, index):
        return self.rolls[index] == 10
    
    def is_spare(self, index):
        return self.rolls[index] + self.rolls[index + 1] == 10
    
    def strike_score(self, index):
        return 10 + self.rolls[index + 1] + self.rolls[index + 2]
    
    def spare_score(self, index):
        return 10 + self.rolls[index + 2]
    
    def frame_score(self, index):
        return self.rolls[index] + self.rolls[index + 1]

    def score(self):
        scores = []
        score = 0
        index = 0

        for frame in range(10):
            if self.is_strike(index):
                score += self.strike_score(index)
                index += 1
            elif self.is_spare(index):
                score += self.spare_score(index)
                index += 2
            else:
                score += self.frame_score(index)
                index += 2

            scores.append(score)

        return scores

# Flet UI
def main(page: ft.Page):
    page.title = "볼링 게임"
    page.window_width = 500
    page.window_height = 700

    result_text = ft.Text("", size=14)

    def play_game(e):
        game = BowlingGame()

        # 게임 진행 (랜덤)
        for frame in range(1, 11):
            if frame < 10:
                first = random.randint(0, 10)
                game.roll(first)

                if first != 10:
                    second = random.randint(0, 10 - first)
                    game.roll(second)

            else:
                first = random.randint(0, 10)
                game.roll(first)

                second = random.randint(0, 10 if first == 10 else 10 - first)
                game.roll(second)

                if first == 10 or first + second == 10:
                    third = random.randint(0, 10)
                    game.roll(third)

        # 결과 출력 생성
        rolls = game.rolls
        scores = game.score()

        index = 0
        result = "볼링 점수판\n\n"

        for frame in range(1, 11):
            if rolls[index] == 10:
                frame_str = "[ X ]"
                index += 1

            elif rolls[index] + rolls[index+1] == 10:
                frame_str = f"[ {rolls[index]} | / ]"
                index += 2

            else:
                frame_str = f"[ {rolls[index]} | {rolls[index+1]} ]"
                index += 2

            result += f"{frame}프레임: {frame_str} → {scores[frame-1]}\n"

        result += f"\n최종 점수: {scores[-1]}"

        result_text.value = result
        page.update()

    # UI 구성
    page.add(
        ft.Column(
            [
                ft.Text("볼링 게임", size=24, weight="bold"),
                ft.ElevatedButton("게임 시작", on_click=play_game),
                result_text
            ],
            alignment="center"
        )
    )


# 실행
ft.app(target=main)