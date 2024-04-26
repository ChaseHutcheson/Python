class Settings:
    def __init__(
        self,
        screen_size: tuple[int, int],
        screen_color: tuple[int, int, int],
        snap_radius: int,
    ):
        self.screen_size = screen_size
        self.screen_color = screen_color
        self.snap_radius = snap_radius

    @staticmethod
    def get_colors():
        colors = {
            "Black": (0, 0, 0),
            "White": (255, 255, 255),
            "Red": (255, 0, 0),
            "Green": (0, 255, 0),
            "Blue": (0, 0, 255),
            "Yellow": (255, 255, 0),
            "Orange": (255, 165, 0),
            "Gray": (128, 128, 128),
            "Brown": (165, 42, 42),
            "Purple": (128, 0, 128),
        }
        return colors
