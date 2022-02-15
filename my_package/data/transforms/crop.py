# Imports
from PIL import Image
import random


class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''

        # Write your code here
        self.new_height, self.new_width = shape
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        width, height = image.size
        if self.new_height > height or self.new_width > width:
            print("Can't crop, because crop size is more than original Image!")
            return image
        # Crop the center of the image
        if self.crop_type == 'center':
            left = (width - self.new_width)/2
            top = (height - self.new_height)/2
            right = (width + self.new_width)/2
            bottom = (height + self.new_height)/2

        else:
            left = random.randint(self.new_width/2, width-self.new_width/2)
            top = random.randint(self.new_height/2, height-self.new_height/2)
            right = left+self.new_width
            bottom = top+self.new_height

        # Crop the center of the image
        image = image.crop((left, top, right, bottom))

        return image
