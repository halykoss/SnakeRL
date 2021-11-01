from tkinter import Tk, Button, Canvas, Frame, BOTH
from game import Snake
import _thread
import numpy as np

from tensorflow import keras

field = Snake(12, 12)

class GameWindow(Frame):
    def __init__(self, game_field, w, h):
        self.game_field = game_field
        super().__init__()
        self.w = w
        self.h = h
        self.canvas = None
        self.start = False
        self.initUI()
        #self.bind("<Key>", self.startEvent)

    def keyEvent(self, keycode):
        self.game_field.next_move(keycode)
        self.canvas.forget()
        self.initUI()

    def initUI(self):
        self.master.title("Colours")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)

        tile_x = self.w / self.game_field.x
        tile_y = self.h / self.game_field.y

        for i in range(0, self.game_field.x):
            for j in range(0, self.game_field.y):
                color = "#6ec6ff"
                if self.game_field.matrix[i][j] == 255:
                    color = "#388e3c"
                if self.game_field.matrix[i][j] == 127:
                    color = "#ac0800"
                self.canvas.create_rectangle(tile_x * i, tile_y * j, tile_x * i + tile_x, tile_y * j + tile_y,
                                             outline=color, fill=color)

        if not self.game_field.end:
            self.canvas.create_text(50, 30, fill="black", font="Purisa",
                                    text="Score: {}".format(self.game_field.score))
        else:
            self.canvas.create_text(50, 30, fill="black", font="Purisa",
                                    text="Finito")

        self.canvas.pack(fill=BOTH, expand=1)
        self.bind('<Configure>', self.resize)

    def resize(self, event):
        self.w = event.width
        self.h = event.height
        print('width  = {}, height = {}'.format(self.w, self.h))
        self.canvas.forget()
        self.initUI()


root = Tk()
ex = GameWindow(field, 400, 400)

btn_arr = [
    Button(root, command=lambda: ex.keyEvent(37)),
    Button(root, command=lambda: ex.keyEvent(38)),
    Button(root, command=lambda: ex.keyEvent(39)),
    Button(root, command=lambda: ex.keyEvent(40))
]


def snake_movement(threadName, delay):
    width = field.generate_image().shape[0]
    height = field.generate_image().shape[1]
    next_state, _, _ = field.next_move(38)
    st_2 = [next_state]
    model = keras.models.load_model('snake_model.h5')
    while not field.end:
        st_1 = st_2
        st_2 = [field.generate_image().reshape(width, height)]
        st = np.vstack((st_1, st_2))
        res = np.argmax(model.predict(np.array([st, ]))[0])
        btn_arr[res].invoke()
    print("Usciti {}".format(field.score))


def main():
    # Create two threads as follows
    try:
        _thread.start_new_thread(snake_movement, ("Thread-1", 2,))
    except:
        print("Error: unable to start thread")
    root.geometry("400x400")
    root.mainloop()


if __name__ == '__main__':
    main()
