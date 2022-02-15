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
        return (
            # for 90 degree right rotation
            sample.rotate(270, Image.NEAREST, expand=1)
            if self.degrees == 270
            else sample.rotate(self.degrees)
        )
