class Entry:
    def __init__(self, w, k):
        self.w = w
        self.k = k

    def _other_w_better(self, other_w):
        return self.w < other_w  # больше лучше

    def _other_k_better(self, other_k):
        return self.k < other_k  # больше лучше

    def _other_w_worse(self, other_w):
        if self.w == other_w:
            return False
        return not self._other_w_better(other_w)

    def _other_k_worse(self, other_k):
        if self.k == other_k:
            return False
        return not self._other_k_better(other_k)

    def other_strictly_worse(self, entry):
        w_ok = False
        if self._other_w_worse(entry.w) :
            w_ok = True

        k_ok = False
        if self._other_k_worse(entry.k):
            k_ok = True
        return w_ok and k_ok

    def other_better(self, entry):
        # каждая компонента лучше или равна
        w_ok = False
        if self._other_w_better(entry.w) or self.w == entry.w:
            w_ok = True

        k_ok = False
        if self._other_k_better(entry.k) or self.k == entry.k:
            k_ok = True

        return w_ok and k_ok

    def is_compromise_with(self, entry):
        if self._other_w_better(entry.w) and self._other_k_worse(entry.k):
            return True
        if self._other_k_better(entry.k) and self._other_w_worse(entry.w):
            return True
        return False

class Pareto2d:
    def __init__(self):
        self.pareto_entries_indexed = {}

    def _add_entry(self, entry, index):
        is_in_pareto = True
        for i in list(self.pareto_entries_indexed.keys()):
            existing_entry = self.pareto_entries_indexed[i]
            if entry.other_better(existing_entry):
                is_in_pareto = False # если она не является строго лучше хотя бы одной, то она точно не в парето
                break

        if is_in_pareto:
            # она точно должна быть добавлена, а некоторые, возможно, удалены
            for i in list(self.pareto_entries_indexed.keys()):
                existing_entry = self.pareto_entries_indexed[i]
                if not entry.is_compromise_with(existing_entry):
                    del self.pareto_entries_indexed[i]
            self.pareto_entries_indexed[index]= entry



    def process_ws_ks(self, ws_list, ks_list):
        entries_list_to_process = list([Entry(w=ws_list[i], k=ks_list[i]) for i in range(len(ws_list))])
        for i in range(len(entries_list_to_process)):
            entry = entries_list_to_process[i]
            self._add_entry(entry, index=i)
        pareto_indexes = list(self.pareto_entries_indexed.keys())
        return pareto_indexes


class Slayter2d:
    def __init__(self):
        self.pareto_entries_indexed = {}

    def _add_entry(self, entry, index):
        is_in_slayter = True
        for i in list(self.pareto_entries_indexed.keys()):
            existing_entry = self.pareto_entries_indexed[i]
            if existing_entry.other_strictly_worse(entry):
                is_in_slayter = False # если нашлась точка, что наша хуже по всем параметрам, то не слейтер
                break

        if is_in_slayter:
            # она точно должна быть добавлена, а некоторые, возможно, удалены
            for i in list(self.pareto_entries_indexed.keys()):
                existing_entry = self.pareto_entries_indexed[i]
                if entry.other_strictly_worse(existing_entry):
                    del self.pareto_entries_indexed[i]

            self.pareto_entries_indexed[index]= entry



    def process_ws_ks(self, ws_list, ks_list):
        entries_list_to_process = list([Entry(w=ws_list[i], k=ks_list[i]) for i in range(len(ws_list))])
        for i in range(len(entries_list_to_process)):
            entry = entries_list_to_process[i]
            self._add_entry(entry, index=i)
        pareto_indexes = list(self.pareto_entries_indexed.keys())
        return pareto_indexes



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    #random.seed = 4

    mu, sigma = 0, 0.1  # mean and standard deviation
    sample_len = 100
    ws = [0,1, -1, 0,   1,  0.5] #np.random.normal(mu, sigma, sample_len)  #
    ks = [1,0, -1, 0.5, -1, 1] #np.random.normal(mu, sigma+8, sample_len)  # [1,0, -1, 0.5]

    pareter = Slayter2d()
    indexes = pareter.process_ws_ks(ws, ks)

    plt.scatter(ws, ks, c="red", alpha=0.5)
    for i in indexes:
        w = ws[i]
        k = ks[i]
        plt.scatter(w, k, c='green')

    plt.show()
