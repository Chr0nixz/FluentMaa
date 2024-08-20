class Resource:
    def __init__(self):
        import app.common.compiled_resources  # type: ignore
        self.images = ':/images'
        self.qss = ':/qss'
        self.i18n = ':/i18n'
        self.gif = ':/images/gif'

    def getImg(self, name):
        return self.images + '/' + name

    def getGif(self, name):
        return self.gif + '/' + name


resource = Resource()
