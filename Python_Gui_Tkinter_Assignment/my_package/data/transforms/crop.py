import numpy as np

class CropImage(object):

    def __init__(self, shape, crop_type='center'):

        # Storing the shape and crop type
        self.shape = shape
        self.crop_type = crop_type

    # Finding the Starting and ending lines to crop the image to
    # and returning the cropped image 
    def __call__(self, image):

        height, width = image.shape[0:2]
        new_shape = self.shape
        new_height = new_shape[0]
        new_width = new_shape[1]
        start_row = int((height-new_height)/2)
        end_row = int((height+new_height)/2)
        start_col = int((width-new_width)/2)
        end_col = int((width+new_width)/2)


        if self.crop_type == 'center':
            cropped_image = image[start_row:end_row, start_col:end_col]
        else:
            random_height = np.random.randint(0, height-self.shape[0])
            random_width = np.random.randint(0, width-self.shape[1])
            cropped_image = image[random_height:random_height+self.shape[0], random_width:random_width+self.shape[1]]

        return cropped_image    
 