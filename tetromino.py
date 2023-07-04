import random
from constants import FIELD_WIDTH, MOVE_LEFT, MOVE_RIGHT, MOVE_DOWN

class TetrisSquare():
    def __init__(self, x=0, y=0, color="gray"):
        '１つの正方形を作成'
        self.x = x
        self.y = y
        self.color = color

    def set_cord(self, x, y):
        '正方形の座標を設定'
        self.x = x
        self.y = y

    def get_cord(self):
        '正方形の座標を取得'
        return int(self.x), int(self.y)

    def set_color(self, color):
        '正方形の色を設定'
        self.color = color

    def get_color(self):
        '正方形の色を取得'
        return self.color

    def get_moved_cord(self, direction):
        '移動後の正方形の座標を取得'

        # 移動前の正方形の座標を取得
        x, y = self.get_cord()

        # 移動方向を考慮して移動後の座標を計算
        if direction == MOVE_LEFT:
            return x - 1, y
        elif direction == MOVE_RIGHT:
            return x + 1, y
        elif direction == MOVE_DOWN:
            return x, y + 1
        else:
            return x, y

class TetrisBlock():
    def __init__(self):
        'テトリスのブロックを作成'

        # ブロックを構成する正方形のリスト
        self.squares = []

        # ブロックの形をランダムに決定
        block_type = random.randint(1, 4)

        # ブロックの形に応じて４つの正方形の座標と色を決定
        if block_type == 1:
            color = "red"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
                [FIELD_WIDTH / 2, 3],
            ]
            self.shape = [
                [1,0],
                [1,0],
                [1,0],
                [1,0]
            ]
        elif block_type == 2:
            color = "blue"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
            ]
            self.shape = [
                [1,1],
                [1,1]
            ]
        elif block_type == 3:
            color = "green"
            cords = [
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
            ]
            self.shape = [
                [1,1],
                [1,0],
                [1,0],
                [0,0]
            ]
        elif block_type == 4:
            color = "orange"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
                [FIELD_WIDTH / 2 - 1, 2],
            ]
            self.shape = [
                [1,1],
                [0,1],
                [0,1],
                [0,0]
            ]

        # 決定した色と座標の正方形を作成してリストに追加
        for cord in cords:
            self.squares.append(TetrisSquare(cord[0], cord[1], color))

    def get_squares(self):
        'ブロックを構成する正方形を取得'

        # return [square for square in self.squares]
        return self.squares

    def move(self, direction):
        'ブロックを移動'

        # ブロックを構成する正方形を移動
        for square in self.squares:
            x, y = square.get_moved_cord(direction)
            square.set_cord(x, y)

    def turn(self, block):
        'ブロックを回転'

        #ブロックの行列入れ替えて逆
        for square in self.squares:

            self.turnedShape = [list(reversed(col)) for col in zip(*block)]
            return self.turnedShape