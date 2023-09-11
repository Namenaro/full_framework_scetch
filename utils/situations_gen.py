from .ECG_utils import get_first_healthy_signal
from .extremum_finder import ExtremumFinder
from .draw_utils import draw_ECG, draw_vertical_line
from .html_logger import HtmlLogger

import matplotlib.pyplot as plt


class StartSituation:
    def __init__(self, signal, start_point):
        self.signal = signal
        self.start_point = start_point



class StartSituationsGen:
    def __init__(self, num_situations=15, is_test=False):
        self.signal = get_first_healthy_signal(is_test)
        self.num_situations = num_situations

        # получаем стартовые точки распознавания
        self.start_coords = self._get_coords_1st_points()
        self.current_i = -1

    def __iter__(self):
        return self

    def _get_coords_1st_points(self):
        coords = ExtremumFinder(self.signal).get_top_N_maxes(self.num_situations)
        return coords

    def __next__(self):
        self.current_i += 1
        if self.current_i < self.num_situations:
            new_situation = self._create_situation(self.start_coords[self.current_i])
            return new_situation
        raise StopIteration

    def _create_situation(self, start_point_general):
        left_pad = 25
        right_pad = 119 - 36

        situation_signal = self.signal[start_point_general - left_pad: start_point_general + right_pad]
        start_situation = StartSituation(situation_signal, start_point=left_pad)
        return start_situation


if __name__ == '__main__':
    log = HtmlLogger("situations_LOG")

    for situation in StartSituationsGen():
        fig, ax = plt.subplots()
        draw_ECG(ax, situation.signal)
        draw_vertical_line(ax, x=situation.start_point, y = max(situation.signal), label="start_point")
        log.add_fig(fig)