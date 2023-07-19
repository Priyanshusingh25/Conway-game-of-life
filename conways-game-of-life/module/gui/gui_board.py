class GuiBoard:

    def __init__(self, root, rows, cols, cell, controller) -> None:
        self.rows = rows
        self.cols = cols
        self.controller = controller
        self.cell = cell
        self.root = root

    def setup_board(self):
        self.controller.setup()
