

class InterpolationSegment:
    def __init__(self, coord1, val1, coord2, val2):
        self.coords = []
        self.vals = []

        if coord1 != coord2:

            self.left_coord= coord1
            self.left_val = val1

            self.right_coord = coord2
            self.right_val = val2

            if coord2 < coord1:
                self.left_coord = coord2
                self.left_val = val2

                self.right_coord = coord1
                self.right_val = val1
            self._calculate_interpolation()
        else:
            self.coords = [coord1]
            self.vals = [val1]

    def get_vals_from_left(self):
        return self.vals

    def get_indexes_from_left(self):
        return self.coords

    def _calculate_interpolation(self):
        self.coords = list(range(self.left_coord, self.right_coord + 1))
        step = (self.right_val - self.left_val) / (len(self.coords)-1)
        for i in range(len(self.coords) ):
            self.vals.append(self.left_val + i * step)