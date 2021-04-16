
class Window:
    def __init__(self, window):
        self.window = window
        self.main_row_count = 0
        for wgt in window.grid_slaves():
            wgt.grid_forget()

    @property
    def main_row(self):
        self.main_row_count += 1
        return self.main_row_count - 1
