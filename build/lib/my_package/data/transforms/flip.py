# Imports
from PIL import Image


class FlipImage(object):
    '''
        Flips the image.
    '''

    def __init__(self, flip_type='horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''
        # Write your code here
        self.flip_type = flip_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        if self.flip_type == 'horizontal':
            # Do a flip of left and right (horizontal)
            hori_flippedImage = image.transpose(Image.FLIP_LEFT_RIGHT)
            return hori_flippedImage
        else:
            # Do a flip of top and bottom (verticle)
            Vert_flippedImage = image.transpose(Image.FLIP_TOP_BOTTOM)
            return Vert_flippedImage
