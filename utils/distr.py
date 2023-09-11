import random


class Distr:
    def __init__(self, sample):
        self.sample = sample

    def p_event_more_eq_than_val(self, val):
        num_elements_more_eq_than_val = 0
        for element in self.sample:
            if element >= val:
                num_elements_more_eq_than_val += 1
        return num_elements_more_eq_than_val/len(self.sample)

    def p_event_less_eq_than_val(self, val):
        num_elements_less_eq_than_val = 0
        for element in self.sample:
            if element <= val:
                num_elements_less_eq_than_val += 1
        return num_elements_less_eq_than_val/len(self.sample)

    def get_mean(self):
        return sum(self.sample)/len(self.sample)


    def get_random_subsample(self, len_subsample):
        subsample = random.sample(self.sample, len_subsample)
        #subsample = [random.choice(self.sample) for _ in range(len_subsample)]
        return subsample

    def get_main_sample(self):
        return self.sample

    def get_p_of_event(self, val1, val2):
        num_elements = 0
        if val1>val2:
            left = val2
            right = val1
        else:
            left = val1
            right = val2

        for element in self.sample:
            if element <= right and element >= left:
                num_elements += 1
        return num_elements/len(self.sample)

    def get_max_val(self):
        return max(self.sample)

    def get_min_val(self):
        return min(self.sample)

    def draw(self, ax):
        ax.hist(self.sample)


def get_distr_of_min_statistics(main_distr, len_subsample):
    statistics_sample = []

    NUM_EXPERIMENTS = 1120
    for _ in range(NUM_EXPERIMENTS):
        subsample = main_distr.get_random_subsample(len_subsample)
        statistics_sample.append(min(subsample))
    return Distr(statistics_sample)

def get_distr_of_max_statistics(main_distr, len_subsample):
    statistics_sample = []

    NUM_EXPERIMENTS = 1120
    for _ in range(NUM_EXPERIMENTS):
        subsample = main_distr.get_random_subsample(len_subsample)
        statistics_sample.append(max(subsample))
    return Distr(statistics_sample)


