import random

# 점수 계산 클래스
class BowlingGame:
    def __init__(self):
        self.rolls = [] # 저장 리스트

    # 점수 기록
    def roll(self, pins):
        self.rolls.append(pins) # 쓰러뜨린 핀 개수 리스트에 추가

    # 스트라이크 확인
    def is_strike(self, index):
        return self.rolls[index] == 10 # 한 번에 10개 = 스트라이크
    
    # 스페어 확인
    def is_spare(self, index):
        return self.rolls[index] + self.rolls[index + 1] == 10 # 두 번 합쳐서 10 = 스페어
    
    # 스트라이크 점수 계산
    def strike_score(self, index):
        return 10 + self.rolls[index + 1] + self.rolls[index + 2] # 기본 10점 + 다음 2번 투구 점수
    
    # 스페어 점수 계산
    def spare_score(self, index):
        return 10 + self.rolls[index + 2] # 기본 10점 + 다음 1번 투구 점수
    
    # 일반 점수 계산
    def frame_score(self, index):
        return self.rolls[index] + self.rolls[index + 1] # 두 번 투구 점수 합

    # 전체 점수 계산
    def score(self):
        scores = [] # 프레임별 점수 저장 리스트
        score = 0 # 현재 총 점수
        index = 0 # 현재 투구 위치

        for frame in range(10): # 10프레임 반복
            if self.is_strike(index): # 스트라이크인 경우
                score += self.strike_score(index) # 점수 계산
                index += 1 # 스트라이크는 1칸 이동

            elif self.is_spare(index): # 스페어인 경우
                score += self.spare_score(index)
                index += 2 # 스페어는 2칸 이동

            else: # 일반 프레임
                score += self.frame_score(index)
                index += 2 # 일반은 2칸 이동

            scores.append(score) # 누적 점수 리스트에 저장

        return scores # 누적 점수 리스트에 반환
    
# 실행 코드

class RandomBowlingGame:
    def __init__(self):
        self.game = BowlingGame() # 객체 생성

    # 게임 진행
    def play(self):
        for frame in range(1, 11): # 1~10프레임 반복
            print(f"\n {frame}프레임")

            if frame < 10: # 1~9 프레임
                first = random.randint(0, 10) # 첫 번째 투구
                self.game.roll(first)
                print(f"첫 번째 투구: {first}")

                if first == 10: #스트라이크
                    print("스트라이크!")
                    continue
                
                second = random.randint(0, 10 - first) # 두 번째 투구 (남은 핀 수 만큼)
                self.game.roll(second)
                print(f"두 번째 투구: {second}")

                if first + second == 10:
                    print("스페어!")

            # 10번째 프레임
            else:
                first = random.randint(0, 10)
                self.game.roll(first)
                print(f"첫 번째 투구: {first}")

                second = random.randint(0, 10 if first == 10 else 10 - first) # 스트라이크면 다시 10 가능, 아니면 남은 핀
                self.game.roll(second)
                print(f"두 번째 투구: {second}")

                # 보너스 투구
                if first == 10 or first + second == 10:
                    third = random.randint(0, 10)
                    self.game.roll(third)
                    print(f"보너스 투구: {third}")

    # 결과 출력
    def show_result(self):
        rolls = self.game.rolls # 전체 투구 데이터
        scores = self.game.score() # 누적 점수 리스트
        index = 0 # 현재 투구 위치

        print("\n 볼링 점수판\n")

        for frame in range(1, 11): # 10프레임 출력
            if rolls[index] == 10: # 스트라이크
                frame_str = "[ X ]"
                index += 1

            elif rolls[index] + rolls[index+1] == 10: # 스페어
                frame_str = f"[ {rolls[index]} | / ]"
                index += 2

            else: # 일반
                frame_str = f"[ {rolls[index]} | {rolls[index+1]} ]"
                index += 2

            # 프레임별 누적 점수 출력
            print(f"{frame}프레임: {frame_str} → {scores[frame-1]}")

        # 최종 점수 출력
        print("\n 최종 점수:", scores[-1])
# 실행
if __name__ == "__main__":
    game = RandomBowlingGame() # 게임 객체 생성
    game.play() # 랜덤 게임 진행
    game.show_result() # 결과 출력