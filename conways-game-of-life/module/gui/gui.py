import tkinter as tk
from module.base.game import Game
from module.base.game_status import GameStatus

from module.gui.gui_manager import GuiManager


class GUI(Game):

    _manager = None
    _root = None

    def __init__(self, win_width=400, win_height=400) -> None:
        super().__init__(state=GameStatus.STARTING)

        self._root = tk.Tk()
        self._manager = GuiManager(self._root)

    # overriding
    def launch(self) -> None:
        self._root.resizable(False, False)
        self._root.title("Conway's Game of Life")
        self._manager.setup()
        self._root.mainloop()

    def save(self) -> None:
        pass

    def restore(self) -> None:
        pass

    def history(self) -> None:
        pass
