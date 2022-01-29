import cv2 as cv

class RotateImage(object):

    # Storing the degee of rotation
    def __init__(self, degrees):
        self.degrees = degrees

    # Rotating the image about the centre
    def __call__(self, sample):

        height, width = sample.shape[0:2]
        rotation_mat = cv.getRotationMatrix2D((width/2, height/2), self.degrees, 1)
        rotated_image = cv.warpAffine(sample, rotation_mat, (width, height))

        return rotated_image
