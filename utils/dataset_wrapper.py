import json
from ECG_utils import raw_dataset_path, healthy
from draw_utils import draw_ECG, draw_vertical_line
from extremum_finder import ExtremumFinder
from html_logger import HtmlLogger

import matplotlib.pyplot as plt

class DataWrapper:
    def __init__(self):
        self._case_id_train = '1102625626'  # классически здоровый пациент
        self.half_len_cycle = 205
        self.data = json.load(open(raw_dataset_path, 'r'))

        self.train_signal_full = self._get_signal_by_case_id(self._case_id_train, lead_name='i')


    def get_train_cycle(self):
        return self.train_signal_full[0: 2*self.half_len_cycle+1]  # сердечный цикл для обучения по одному образцу: в центральной координате r-пик


    def get_true_situations(self, num_situations=None):
        full_healthy_signals = self._get_test_ECGS(num_cases=None)
        sitation_signals = []
        for full_signal  in full_healthy_signals:
            new_signals = self._get_situations_from_full_signal(full_signal, num_situations=4)
            sitation_signals = sitation_signals + new_signals
            if num_situations is not None:
                if len(sitation_signals) >=num_situations:
                    break

        coords = [self.half_len_cycle+1]* len(sitation_signals)
        return sitation_signals, coords

    def get_contrast_situations(self, num_situations=None):
        full_unhealthy_signals = self._get_contrast_ECGs(num_cases=None)
        sitation_signals = []
        for full_signal in full_unhealthy_signals:
            new_signals = self._get_situations_from_full_signal(full_signal, num_situations=4)
            sitation_signals = sitation_signals + new_signals
            if num_situations is not None:
                if len(sitation_signals) >= num_situations:
                    break

        coords = [self.half_len_cycle + 1] * len(sitation_signals)
        return sitation_signals, coords

    def get_corrupted_places_situations(self, num_situations=None):
        full_healthy_signals = self._get_test_ECGS(num_cases=None)
        sitation_signals = []
        for full_signal in full_healthy_signals:
            new_signals = self._get_situations_from_full_signal(full_signal, num_situations=56)
            sitation_signals = sitation_signals + new_signals[-4:]
            if num_situations is not None:
                if len(sitation_signals) >= num_situations:
                    break

        coords = [self.half_len_cycle + 1] * len(sitation_signals)
        return sitation_signals, coords


    #------------------------------------------------------------
    def _get_situations_from_full_signal(self, signal, num_situations):
        coords = ExtremumFinder(signal).get_top_N_maxes(num_situations)
        signals = []
        for coord in coords:
            LEFT = coord - self.half_len_cycle
            RIGHT = coord + self.half_len_cycle
            if LEFT < 0:
                continue
            if RIGHT >= len(signal) - 1:
                continue
            signals.append(signal[LEFT:RIGHT])
        return signals


    def _get_test_ECGS(self, num_cases=None):
        test_signals = []
        for case_id in self.data.keys():
            if case_id == self._case_id_train:
                continue
            diag = self.data[case_id]['StructuredDiagnosisDoc']
            if num_cases is not None:
                if len(test_signals) == num_cases:
                    break
            if healthy(diag):
                signal = self._get_signal_by_case_id(case_id, lead_name='i')
                test_signals.append(signal)

        return test_signals


    def _get_contrast_ECGs(self, num_cases):
        signals = []
        for case_id in self.data.keys():
            diag = self.data[case_id]['StructuredDiagnosisDoc']
            if num_cases is not None:
                if len(signals) == num_cases:
                    break
            if not healthy(diag):
                signal = self._get_signal_by_case_id(case_id, lead_name='i')
                signals.append(signal)

        return signals


    def _get_signal_by_case_id(self, case_id, lead_name):
        leads = self.data[case_id]['Leads']
        signal = leads[lead_name]['Signal']
        return signal


if __name__ == "__main__":
    dw = DataWrapper()
    signal = dw.get_train_cycle()
    fig, ax = plt.subplots()
    draw_ECG(ax, signal)
    plt.show()

    log = HtmlLogger("healthy_situations")
    signals, coords = dw.get_true_situations(num_situations=4)
    for i in range(len(signals)):
        signal  = signals[i]
        coord = coords[i]
        fig, ax = plt.subplots()
        draw_ECG(ax, signal)
        draw_vertical_line(ax, x=coord, y=max(signal))
        log.add_fig(fig)

    log = HtmlLogger("un_healthy_situations")
    signals, coords = dw.get_contrast_situations(num_situations=4)
    for i in range(len(signals)):
        signal = signals[i]
        coord = coords[i]
        fig, ax = plt.subplots()
        draw_ECG(ax, signal)
        draw_vertical_line(ax, x=coord, y=max(signal))
        log.add_fig(fig)

    log = HtmlLogger("corrupted_situations")
    signals, coords = dw.get_corrupted_places_situations(num_situations=4)
    for i in range(len(signals)):
        signal = signals[i]
        coord = coords[i]
        fig, ax = plt.subplots()
        draw_ECG(ax, signal)
        draw_vertical_line(ax, x=coord, y=max(signal))
        log.add_fig(fig)




