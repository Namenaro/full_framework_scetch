import base64
import os.path
from io import BytesIO
import matplotlib.pyplot as plt

class HtmlLogger:
    def __init__(self, name, dir_path=None):
        self.name = name
        self.html = ''
        self.dir_path = dir_path

    def add_line_little(self):
        self.html += "<hr>"
        self.save()

    def add_line_big(self):
        self.html += "<hr style=\"height:10px;background:gray\">"
        self.save()

    def add_text(self, text):
        self.html += text + '<br>'
        self.save()

    def add_fig(self, fig):
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png', pad_inches=0.0, bbox_inches="tight")
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        self.html += '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '<br>'
        plt.close(fig)
        self.save()

    def save(self):
        filename = self.name + '.html'
        if self.dir_path is not None:
            filename = os.path.join(self.dir_path, filename)
        with open(filename, 'w') as f:
            f.write(self.html)
