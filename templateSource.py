class TemplateSource:

    def __init__(self, image):
        self.image = image
        self.grab_dimensions()

    def grab_dimensions(self):
        self.width, self.height = self.image.shape[::-1]