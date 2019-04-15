class Markdown:
    def __init__(self):
        self.body = []

    def h(self, header_level, text):
        self.body.append(''.join(['#' for _ in range(header_level)]) + ' {}'.format(text))

    def h1(self, text):
        self.body.append('# {}'.format(text))

    def h2(self, text):
        self.body.append('## {}'.format(text))

    def h3(self, text):
        self.body.append('### {}'.format(text))

    def h4(self, text):
        self.body.append('#### {}'.format(text))

    def quote(self, text):
        self.body.append('> {}'.format(text.replace('\n', '\n> ')))

    def build(self):
        return '\n\n'.join(self.body)
