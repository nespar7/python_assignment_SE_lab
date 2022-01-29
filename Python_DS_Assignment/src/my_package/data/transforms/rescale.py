import cv2 as cv

class RescaleImage(object):
    
    # Storing output size and resizing the image
    def __init__(self, scale):
        self.scale = scale

    def __call__(self, image):
        rescaled_image = cv.resize(image, None, fx=self.scale, fy=self.scale, interpolation=cv.INTER_LINEAR)
        return rescaled_image
