import tkinter as tk

from constants import FIELD_WIDTH, FIELD_HEIGHT, BLOCK_SIZE
from tetromino import TetrisSquare

class TetrisField():
    def __init__(self):
        self.width = FIELD_WIDTH
        self.height = FIELD_HEIGHT

        # フィールドを初期化
        self.squares = []
        for y in range(self.height):
            for x in range(self.width):
                # フィールドを正方形インスタンスのリストとして管理
                self.squares.append(TetrisSquare(x, y, "gray"))

    def get_width(self):
        'フィールドの正方形の数（横方向）を取得'

        return self.width

    def get_height(self):
        'フィールドの正方形の数（縦方向）を取得'

        return self.height

    def get_squares(self):
        'フィールドを構成する正方形のリストを取得'

        return self.squares

    def get_square(self, x, y):
        '指定した座標の正方形を取得'

        return self.squares[y * self.width + x]

    def judge_game_over(self, block):
        'ゲームオーバーかどうかを判断'

        # フィールド上で既に埋まっている座標の集合作成
        no_empty_cord = set(square.get_cord() for square
                            in self.get_squares() if square.get_color() != "gray")

        # ブロックがある座標の集合作成
        block_cord = set(square.get_cord() for square
                            in block.get_squares())

        # ブロックの座標の集合と
        # フィールドの既に埋まっている座標の集合の積集合を作成
        collision_set = no_empty_cord & block_cord

        # 積集合が空であればゲームオーバーではない
        if len(collision_set) == 0:
            ret = False
        else:
            ret = True

        return ret

    def judge_can_move(self, block, direction):
        '指定した方向にブロックを移動できるかを判断'

        # フィールド上で既に埋まっている座標の集合作成
        no_empty_cord = set(square.get_cord() for square
                            in self.get_squares() if square.get_color() != "gray")

        # 移動後のブロックがある座標の集合作成
        move_block_cord = set(square.get_moved_cord(direction) for square
                            in block.get_squares())

        # フィールドからはみ出すかどうかを判断
        for x, y in move_block_cord:

            # はみ出す場合は移動できない
            if x < 0 or x >= self.width or \
                    y < 0 or y >= self.height:
                return False

        # 移動後のブロックの座標の集合と
        # フィールドの既に埋まっている座標の集合の積集合を作成
        collision_set = no_empty_cord & move_block_cord

        # 積集合が空なら移動可能
        if len(collision_set) == 0:
            ret = True
        else:
            ret = False

        return ret

    def fix_block(self, block):
        'ブロックを固定してフィールドに追加'

        for square in block.get_squares():
            # ブロックに含まれる正方形の座標と色を取得
            x, y = square.get_cord()
            color = square.get_color()

            # その座標と色をフィールドに反映
            field_square = self.get_square(x, y)
            field_square.set_color(color)

    def delete_line(self):
        '行の削除を行う'

        # 全行に対して削除可能かどうかを調べていく
        for y in range(self.height):
            for x in range(self.width):
                # 行内に１つでも空があると消せない
                square = self.get_square(x, y)
                if(square.get_color() == "gray"):
                    # 次の行へ
                    break
            else:
                # break されなかった場合はその行は空きがない
                # この行を削除し、この行の上側にある行を１行下に移動
                for down_y in range(y, 0, -1):
                    for x in range(self.width):
                        src_square = self.get_square(x, down_y - 1)
                        dst_square = self.get_square(x, down_y)
                        dst_square.set_color(src_square.get_color())
                # 一番上の行は必ず全て空きになる
                for x in range(self.width):
                    square = self.get_square(x, 0)
                    square.set_color("gray")


class TetrisCanvas(tk.Canvas):
    def __init__(self, master, field):
        'テトリスを描画するキャンバスを作成'

        canvas_width = field.get_width() * BLOCK_SIZE
        canvas_height = field.get_height() * BLOCK_SIZE

        # tk.Canvasクラスのinit
        super().__init__(master, width=canvas_width, height=canvas_height, bg="white")

        # キャンバスを画面上に設置
        self.place(x=25, y=25)

        # 10x20個の正方形を描画することでテトリス画面を作成
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white", width=1,
                    fill=square.get_color()
                )

        # 一つ前に描画したフィールドを設定
        self.before_field = field

    def update(self, field, block):
        'テトリス画面をアップデート'

        # 描画用のフィールド（フィールド＋ブロック）を作成
        new_field = TetrisField()
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                color = square.get_color()

                new_square = new_field.get_square(x, y)
                new_square.set_color(color)

        # フィールドにブロックの正方形情報を合成
        if block is not None:
            block_squares = block.get_squares()
            for block_square in block_squares:
                # ブロックの正方形の座標と色を取得
                x, y = block_square.get_cord()
                color = block_square.get_color()

                # 取得した座標のフィールド上の正方形の色を更新
                new_field_square = new_field.get_square(x, y)
                new_field_square.set_color(color)

        # 描画用のフィールドを用いてキャンバスに描画
        for y in range(field.get_height()):
            for x in range(field.get_width()):

                # (x,y)座標のフィールドの色を取得
                new_square = new_field.get_square(x, y)
                new_color = new_square.get_color()

                # (x,y)座標が前回描画時から変化ない場合は描画しない
                before_square = self.before_field.get_square(x, y)
                before_color = before_square.get_color()
                if(new_color == before_color):
                    continue

                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                # フィールドの各位置の色で長方形描画
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white", width=1, fill=new_color
                )

        # 前回描画したフィールドの情報を更新
        self.before_field = new_field