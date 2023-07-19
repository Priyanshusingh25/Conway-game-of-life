import random


class GuiController:
    """ 
        GuiController.

        This class is responsible for all the Game's logic.

        """

    def __init__(self, rows, cols, cell, root) -> None:
        self.controls = {}
        self.rows = rows
        self.cols = cols
        self.after_id = None
        self.cell = cell
        self.iteration = 0
        self.board = []
        self.root = root
        self.speed = 100

    def set_controls(self, controls):
        self.controls = controls

    def set_dimensions(self, dimension):
        self.rows = dimension[0]
        self.cols = dimension[1]
        self._on_stop()
        self._on_reset()

    def setup(self):
        self.board = self._create_board(self._get_zero_or_one)
        self._fill_board_with_cells()

    def _on_start(self):
        """ 
        Starts the Game.

        Parameters
        ----------
        self: GUI Object

        Return
        ------
        return: None.
        """

        self._on_update()

    def _create_board(self, func):
        """ Create the board without cells"""
        # create a temp array to hold the board
        board = []
        # iterate first the rows
        for row in range(self.rows):
            # append empty array to hold column values
            board.append([])
            for col in range(self.cols):
                board[row].append(func())
        return board

    def _on_update(self, is_single_step=None):
        temp_board = []
        for row in range(self.rows):
            temp_board.append([])
            for col in range(self.cols):
                temp_board[row].append(self._get_new_cell_state(row, col))

        # update the Game Board
        self.board = temp_board

        # clear the canvas
        self.controls['board_canvas'].delete('all')

        # fill the canvas with new board
        self._fill_board_with_cells()

        if is_single_step is None:
            # recursive call on update
            self.after_id = self.root.after(1000//self.speed, self._on_update)

        # update generation count
        self._on_update_generation()

    def _on_update_generation(self, count=None):
        if count == 0:
            self.iteration = 0
            self.controls['lbl_generation'].config(text='Generation: 0')
        else:
            self.iteration += 1
            self.controls['lbl_generation'].config(
                text=f'Generation: {self.iteration}')

    def _get_new_cell_state(self, row, col):
        number_of_neighbors = self._get_num_of_neighbors(row, col)

        # Rule -> Cell is alive
        if self._is_cell_alive(row, col):

            if number_of_neighbors < 2:
                # Cell dies of under population
                return 0
            elif number_of_neighbors == 2 or number_of_neighbors == 3:
                # Cell stays alive
                return 1
            elif number_of_neighbors > 3:
                # Cell dies of over population
                return 0

        # Cell is dead
        else:
            if number_of_neighbors == 3:
                # Cells becomes alive
                return 1
            else:
                # Cells stays dead
                return 0

    def _get_num_of_neighbors(self, row, col):
        # iterate the rows
        number_of_neighbors = 0
        for i_row in range(-1, 2):
            # iterate the columns
            for j_col in range(-1, 2):
                # if its the same cell
                if i_row == 0 and j_col == 0:
                    # skip the cell (we only need neighbors)
                    continue
                # calculate the neighbor row
                neighbor_row = row + i_row
                # calculate the neighbor col
                neighbor_col = col + j_col

                # check neighbor is out of bounds
                if neighbor_row < 0 or neighbor_row >= self.rows or neighbor_col < 0 or neighbor_col >= self.cols:
                    continue
                # increment neighbor
                number_of_neighbors += self.board[neighbor_row][neighbor_col]
        return number_of_neighbors

    def _is_cell_alive(self, row, col):
        return self.board[row][col] == 1

    def _fill_board_with_cells(self):
        """ Fill the board with alive or dead cells """
        # Iterate the rows
        for row in range(self.rows):
            # Iterate the columns
            for col in range(self.cols):
                x1 = col * self.cell
                y1 = row * self.cell
                x2 = x1 + self.cell
                y2 = y1 + self.cell

                props = (x1, y1, x2, y2, row, col)
                self._add_clickable_cell(props)

    def _add_clickable_cell(self, props):
        value = self.board[props[4]][props[5]]
        color = self._get_cell_color(value)
        self._add_shape_in_canvas(props, color)

    def _get_cell_color(self, value):
        return 'black' if value == 1 else 'white'

    def _on_cell_click_handler(self, props):
        value = self.board[props[4]][props[5]]
        new_value = 1 if value == 0 else 0

        color = self._get_cell_color(new_value)
        self.board[props[4]][props[5]] = new_value
        self._add_shape_in_canvas(props, color)

    def _add_shape_in_canvas(self, props, color):
        canvas = self.controls['board_canvas']
        rect = canvas.create_rectangle(
            props[0], props[1], props[2], props[3], fill=color, outline='black')
        canvas.tag_bind(rect, "<Button-1>",
                        lambda e: self._on_cell_click_handler(props))

    def _on_reset(self):
        self.board = self._create_board(self._get_zero_or_one)
        self.controls['board_canvas'].delete('all')
        self._fill_board_with_cells()
        self._on_update_generation(count=0)

    def _get_zero_or_one(self) -> int:
        return random.randint(0, 1)

    def _get_zero_only(self) -> int:
        return 0

    def _on_change_speed(self, speed):
        self.speed = int(speed)

    def _on_pause(self):
        self._on_stop()

    def _on_clear(self):
        self._on_stop()
        self.controls['board_canvas'].delete('all')
        self.board = self._create_board(self._get_zero_only)
        self._fill_board_with_cells()
        self._on_update_generation(count=0)

    def _on_stop(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)

    def _on_random(self):
        self._on_clear()
        self._on_reset()

    def _on_step(self):
        self._on_pause()
        self._on_update(is_single_step=True)

    def _on_exit(self):
        exit()
