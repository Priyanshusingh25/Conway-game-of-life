
from module.gui.gui_board import GuiBoard
from module.gui.gui_controller import GuiController
from module.gui.gui_controls import GuiControls


class GuiManager:
    """ Gui Manager class is responsible for creating,
        positioning, aligning and displaying of user interface elements
        like Frames, Labels, Buttons, Canvas etc.

        This ensures a clear separation of concern. """

    def __init__(self, root) -> None:
        # Defaults
        self._rows = 50
        self._cols = 50
        self._speed = 100
        self._cell = 10
        self._iteration = 0
        self._root = root

        self.controls = {}
        self.board = None
        self.controller = GuiController(
            self._rows, self._cols, self._cell, self._root)

    def setup(self):
        """ Setup user interface with the required controls """

        self.setup_controls()
        self.setup_board()

    def setup_controls(self):
        controls = GuiControls(self._root, self._cell,
                               self._rows, self._cols, self.controller)
        controls.set_and_position_controls()
        self.controls = controls.get_controls()
        self.controller.set_controls(self.controls)

    def setup_board(self):
        board = GuiBoard(self._root, self._rows, self._cols,
                         self._cell,  self.controller)
        board.setup_board()
        self.board = board
