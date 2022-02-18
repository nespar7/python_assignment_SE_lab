import cv2 as cv 

class BlurImage(object):

    def __init__(self, radius):
        self.radius = int(radius) # Storing the radius of blur 

    def __call__(self, image):
        gauss = cv.GaussianBlur(image, (self.radius, self.radius), 0) # Applying Gaussian blur on the image

        return gauss # returning the blurred image

        

