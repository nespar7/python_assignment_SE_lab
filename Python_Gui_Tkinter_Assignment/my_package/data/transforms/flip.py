import cv2 as cv

class FlipImage(object):

    # Storing the flip type with default being horizontal
    def __init__(self, flip_type='horizontal'):
        self.flip_type = flip_type
        
        
    def __call__(self, image):
        # Flipping the image
        if self.flip_type == 'horizontal':
            flipped_image = cv.flip(image, 1)
        else:
            flipped_image = cv.flip(image, 0)

        return flipped_image
       