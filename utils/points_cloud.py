
class PointsCloud:
    def __init__(self, xs, ys, names):
        self.xs = xs
        self.ys = ys
        self.names = names

        self.ws = list([self.ys[i] + self.xs[i] for i in range(len(names))])

    def draw_on_01(self, ax):
        ax.scatter(self.xs, self.ys, alpha=0.5, s=7)
        for i, txt in enumerate(self.names):
            ax.annotate(txt, (self.xs[i], self.ys[i]),  fontsize=7)
        ax.set_xlim([-0.1, 1.1])
        ax.set_ylim([-0.1, 1.1])

    def get_top_n_indices(self, n):
        top_indixes = sorted(range(len(self.ws)), key=lambda i: self.ws[i], reverse=True)[:n]
        return top_indixes
