# Imports
from PIL import Image


class RotateImage(object):
    '''
        Rotates the image about the centre of the image.
    '''

    def __init__(self, degrees):
        '''
            Arguments:
            degrees: rotation degree.
        '''

        # Write your code here
        self.degrees = degrees

    def __call__(self, sample):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here

        # for 90 degree right rotation
        if self.degrees == 270:
            rotated_image = sample.rotate(270, Image.NEAREST, expand=1)
            return rotated_image

        # general rotation in the left side
        else:
            rotated_image = sample.rotate(self.degrees)
            return rotated_image
