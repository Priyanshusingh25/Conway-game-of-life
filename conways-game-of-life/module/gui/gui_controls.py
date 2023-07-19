import tkinter as tk
from tkinter import ttk


class GuiControls:
    select_options = {
        "20 x 20": (20, 20),
        "30 x 30": (30, 30),
        "40 x 40": (40, 40),
        "50 x 50": (50, 50),
    }

    def __init__(self, root, cell, rows, cols, controller) -> None:
        self.root = root
        self.cell = cell
        self.rows = rows
        self.cols = cols
        self.speed = 100
        self.controller = controller

    def set_and_position_controls(self):
        self.set_controls()
        self.position_controls()

    def set_controls(self):
        """ Set controls needed for the user interface """

        select_val = tk.StringVar()
        self.main = ttk.Frame(self.root)
        self.board_area = self.create_frame('ridge', 400, 300,)
        self.control_area = self.create_frame('ridge', 200, 300,)
        self.lbl_control_text = self.create_label(
            self.control_area, "Controls", 18)
        self.lbl_select = self.create_label(
            self.control_area, "Change dimension:")
        self.lbl_generation = self.create_label(
            self.control_area, "Generation")

        self.slider = self.create_slider()

        self.sel_size = self.create_combo(select_val)
        self.btn_start = self.create_button("Start", self.controller._on_start)
        self.btn_pause = self.create_button("Pause", self.controller._on_pause)
        self.btn_random = self.create_button(
            "Random", self.controller._on_random)
        self.btn_step = self.create_button("Step", self.controller._on_step)
        self.btn_clear = self.create_button("Clear", self.controller._on_clear)
        self.btn_exit = self.create_button("Exit", self.controller._on_exit)

        self.lbl_board_text = self.create_label(
            self.board_area, "Game Board", 18)
        self.board_canvas = self.create_canvas()

    def position_controls(self):
        """ Position the user controls (buttons, label) on the main frame """
        self.position_widget(
            self.main, 0, 0, stky=(tk.N, tk.S, tk.E, tk.W))

        self.position_widget(self.control_area, 0, 0, 2,
                             6, (tk.N, tk.S, tk.E, tk.W))
        self.position_widget(self.board_area, 2, 0, 4,
                             4, (tk.N, tk.S, tk.E, tk.W))

        self.position_widget(
            self.lbl_control_text, 0, 0, stky=(tk.N, tk.W))

        self.position_widget(
            self.lbl_board_text, 3, 0, stky=(tk.N, tk.W))
        self.position_widget(self.board_canvas, 3, 1, stky=(
            tk.N, tk.S, tk.E, tk.W), px=0, py=0)

        self.position_widget(self.lbl_select, 0, 3, stky=(
            tk.N, tk.W), px=(10, 0), py=(30, 0))
        self.position_widget(self.sel_size, 0, 4, stky=(tk.N, tk.W))

        self.position_widget(self.btn_start, 0, 5, stky=(tk.N, tk.W))
        self.position_widget(self.btn_pause, 0, 5, stky=(tk.N, tk.E))

        self.position_widget(self.btn_random, 0, 6, stky=(tk.N, tk.W))
        self.position_widget(self.btn_step, 0, 6, stky=(tk.N, tk.E))

        self.position_widget(self.slider, 0, 7, stky=(tk.W, tk.E))

        self.position_widget(
            self.lbl_generation, 0, 8, stky=(tk.N, tk.W))

        self.position_widget(self.btn_clear, 0, 9,
                             stky=(tk.N, tk.W, tk.S), py=(120, 0))
        self.position_widget(self.btn_exit, 0, 9, stky=(
            tk.N, tk.E, tk.S), py=(120, 0))

    def set_weight(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        # prevents left side widget from stretching
        self.main.columnconfigure(0, weight=0)
        self.main.columnconfigure(1, weight=0)
        self.main.columnconfigure(2, weight=0)
        # allow right side widget to stretch
        self.main.columnconfigure(3, weight=3)
        self.main.columnconfigure(4, weight=3)
        self.main.rowconfigure(1, weight=1)

    def create_button(self, text, action=None):
        """ Helper method to create a ttk Button"""
        return ttk.Button(self.control_area, text=text, command=action)

    def create_combo(self, selected):
        """ 
        Helper method to create a ttk Combo
        """
        combo = ttk.Combobox(self.control_area, textvariable=selected)
        combo['values'] = list(self.select_options.keys())
        combo.bind("<<ComboboxSelected>>", self._on_handle_combo_selected)
        return combo

    def _on_handle_combo_selected(self, event):
        key = self.sel_size.get()
        value = self.select_options[key]
        self.controller.set_dimensions(value)

    def create_label(self, parent, title, size=14):
        """Helper method to create a ttk Label"""
        return ttk.Label(parent, text=title, font=('Arial', size))

    def create_slider(self):
        slider = tk.Scale(self.control_area, from_=1, to=100,
                          orient=tk.HORIZONTAL, label='Speed', command=self.controller._on_change_speed)
        slider.set(self.speed)
        return slider

    def create_frame(self, relief, width, height):
        """ Helper method to create a ttk Frame """
        style = GuiControls.get_frame_style()
        style.configure('Frame.TFrame', background='gray')

        return ttk.Frame(self.main, borderwidth=5, relief=relief, width=width,
                         height=height, style='Frame.TFrame')

    def create_canvas(self):
        wd = self.cols * self.cell
        ht = self.rows * self.cell
        return tk.Canvas(self.board_area, width=wd, height=ht, background='white')

    def get_frame_style(color=None):
        """ Create style used by default for all Frames """
        style = ttk.Style()
        style.configure('TFrame', background='green')
        return style

    def position_widget(self, ctl, col, row, col_sp=None, row_sp=None, stky=None, px=10, py=10):
        ctl.grid(
            column=col, row=row, columnspan=col_sp,
            rowspan=row_sp, sticky=stky, padx=px, pady=py
        )

    def get_controls(self):
        controls = {}
        controls['main'] = self.main
        controls['board_area'] = self.board_area
        controls['control_area'] = self.control_area
        controls['lbl_control_text'] = self.lbl_control_text
        controls['lbl_select'] = self.lbl_select
        controls['lbl_generation'] = self.lbl_generation
        controls['slider'] = self.slider
        controls['sel_size'] = self.sel_size
        controls['btn_start'] = self.btn_start
        controls['btn_pause'] = self.btn_pause
        controls['btn_random'] = self.btn_random
        controls['btn_step'] = self.btn_step
        controls['btn_clear'] = self.btn_clear
        controls['btn_exit'] = self.btn_exit
        controls['lbl_board_text'] = self.lbl_board_text
        controls['board_canvas'] = self.board_canvas
        return controls
