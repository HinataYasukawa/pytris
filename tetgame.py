import tkinter as tk
from constants import BLOCK_SIZE, FIELD_WIDTH, FIELD_HEIGHT
from tetromino import TetrisBlock
from board import TetrisField, TetrisCanvas
from constants import FIELD_WIDTH, MOVE_LEFT, MOVE_RIGHT, MOVE_DOWN

class TetrisGame():
    def __init__(self, master):
        'テトリスのインスタンス作成'

        # ブロック管理リストを初期化
        self.field = TetrisField()

        # 落下ブロックをセット
        self.block = None

        # テトリス画面をセット
        self.canvas = TetrisCanvas(master, self.field)

        # テトリス画面アップデート
        self.canvas.update(self.field, self.block)

    def start(self, func):
        'テトリスを開始'

        # 終了時に呼び出す関数をセット
        self.end_func = func

        # ブロック管理リストを初期化
        self.field = TetrisField()

        # 落下ブロックを新規追加
        self.new_block()

    def new_block(self):
        'ブロックを新規追加'

        # 落下中のブロックインスタンスを作成
        self.block = TetrisBlock()

        if self.field.judge_game_over(self.block):
            self.end_func()
            print("GAMEOVER")

        # テトリス画面をアップデート
        self.canvas.update(self.field, self.block)

    def move_block(self, direction):
        'ブロックを移動'

        # 移動できる場合だけ移動する
        if self.field.judge_can_move(self.block, direction):

            # ブロックを移動
            self.block.move(direction)

            # 画面をアップデート
            self.canvas.update(self.field, self.block)

        else:
            # ブロックが下方向に移動できなかった場合
            if direction == MOVE_DOWN:
                # ブロックを固定する
                self.field.fix_block(self.block)
                self.field.delete_line()
                self.new_block()

class EventHandller():
    def __init__(self, master, game):
        self.master = master

        # 制御するゲーム
        self.game = game

        # イベントを定期的に発行するタイマー
        self.timer = None

        # ゲームスタートボタンを設置
        button = tk.Button(master, text='START', command=self.start_event)
        button.place(x=25 + BLOCK_SIZE * FIELD_WIDTH + 25, y=30)

    def start_event(self):
        'ゲームスタートボタンを押された時の処理'

        # テトリス開始
        self.game.start(self.end_event)
        self.running = True

        # タイマーセット
        self.timer_start()

        # キー操作入力受付開始
        self.master.bind("<Left>", self.left_key_event)
        self.master.bind("<Right>", self.right_key_event)
        self.master.bind("<Down>", self.down_key_event)

    def end_event(self):
        'ゲーム終了時の処理'
        self.running = False

        # イベント受付を停止
        self.timer_end()
        self.master.unbind("<Left>")
        self.master.unbind("<Right>")
        self.master.unbind("<Down>")

    def timer_end(self):
        'タイマーを終了'

        if self.timer is not None:
            self.master.after_cancel(self.timer)
            self.timer = None

    def timer_start(self):
        'タイマーを開始'

        if self.timer is not None:
            # タイマーを一旦キャンセル
            self.master.after_cancel(self.timer)

        # テトリス実行中の場合のみタイマー開始
        if self.running:
            # タイマーを開始
            self.timer = self.master.after(1000, self.timer_event)

    def left_key_event(self, event):
        '左キー入力受付時の処理'

        # ブロックを左に動かす
        self.game.move_block(MOVE_LEFT)

    def right_key_event(self, event):
        '右キー入力受付時の処理'

        # ブロックを右に動かす
        self.game.move_block(MOVE_RIGHT)

    def down_key_event(self, event):
        '下キー入力受付時の処理'

        # ブロックを下に動かす
        self.game.move_block(MOVE_DOWN)

        # 落下タイマーを再スタート
        self.timer_start()

    def timer_event(self):
        'タイマー満期になった時の処理'

        # 下キー入力受付時と同じ処理を実行
        self.down_key_event(None)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # アプリウィンドウの設定
        self.geometry("400x600")
        self.title("テトリス")

        # テトリス生成
        game = TetrisGame(self)

        # イベントハンドラー生成
        EventHandller(self, game)

if __name__ == "__main__":
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()