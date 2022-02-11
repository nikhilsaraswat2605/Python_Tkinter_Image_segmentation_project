# Imports


class RescaleImage(object):
    '''
        Rescales the image to a given size.
    '''

    def __init__(self, output_size):
        '''
            Arguments:
            output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
        '''

        # Write your code here
        self.output_size = output_size

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''

        # Write your code here

        width, height = image.size
        if type(self.output_size) is int:
            if height > width:
                self.final_height = self.output_size
                self.final_width = int(width*(self.final_height/height))
            else:
                self.final_width = self.output_size
                self.final_height = int(height*(self.final_width/width))
        else:
            self.final_height, self.final_width = self.output_size

        resized_image = image.resize((self.final_height, self.final_width))
        return resized_image
