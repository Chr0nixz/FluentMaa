class Resource:
    def __init__(self):
        import app.common.compiled_resources  # type: ignore
        self.image = ':/images'
        self.qss = ':/qss'
        self.i18n = ':/i18n'

    def getImg(self, name):
        return self.image + '/' + name


resource = Resource()
