    def update_end_pos(self, end_pos, intersection_point=None):
        if intersection_point:
            self.end_pos = intersection_point
            self.reflected = (
                True  # Set reflected to True when the light ray is reflected
            )
        else:
            self.end_pos = end_pos