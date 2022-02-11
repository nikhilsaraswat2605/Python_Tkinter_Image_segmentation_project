# Imports

import re
from PIL import Image
import numpy as np
import json
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage


class Dataset(object):
    '''
        A class for the dataset that will return data items as per the given index
    '''

    def __init__(self, annotation_file, transforms=None):
        '''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''
        # parsing the .jsonl file
        with open(annotation_file) as f:
            # this was the small trick to parse the .jsonl file correctly
            self.data = json.loads('['+re.sub(r'\}\s\{', '},{', f.read())+']')

        self.transforms = transforms

    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.data)

    def __getitem__(self, idx):
        '''
            return the dataset element for the index: "idx"
            Arguments:
                idx: index of the data element.

            Returns: A dictionary with:
                image: image (in the form of a numpy array) (shape: (3, H, W))
                gt_png_ann: the segmentation annotation image (in the form of a numpy array) (shape: (1, H, W))
                gt_bboxes: N X 5 array where N is the number of bounding boxes, each 
                            consisting of [class, x1, y1, x2, y2]
                            x1 and x2 lie between 0 and width of the image,
                            y1 and y2 lie between 0 and height of the image.

            You need to do the following, 
            1. Extract the correct annotation using the idx provided.
            2. Read the image, png segmentation and convert it into a numpy array (wont be necessary
                with some libraries). The shape of the arrays would be (3, H, W) and (1, H, W), respectively.
            3. Scale the values in the arrays to be with [0, 1].
            4. Perform the desired transformations on the image.
            5. Return the dictionary of the transformed image and annotations as specified.
        '''
        # creating result  dictionary to return
        result = {}
        # image path
        ImagePath = 'data/'+self.data[idx]["img_fn"]
        # path of the segmented gray scale image
        gt_png_ann_path = 'data/'+self.data[idx]["png_ann_fn"]

        # opening images as PIL image
        Img = Image.open(ImagePath)
        gt_png_ann_Img = Image.open(gt_png_ann_path)

        # if transforms are not None, then iterate over all transformations class objects
        if not self.transforms == None:
            for transform_instance in self.transforms:
                Img = transform_instance.__call__(Img)

        # scaling the image between [0,1]
        image = np.array(Img)/255
        # rolling the axis of image to bring it from (H,W,3) to (3,H,W)
        image = np.rollaxis(image, 2, 0)
        # scaling the image between [0,1]
        gt_png_ann = np.array(gt_png_ann_Img)/255
        # rolling the axis of image to bring it from (H,W,3) to (3,H,W)
        gt_png_ann = np.rollaxis(
            gt_png_ann.reshape(*(gt_png_ann.shape), 1), 2, 0)

        result["image"] = image
        result["gt_png_ann"] = gt_png_ann
        result["gt_bboxes"] = []

        for item in self.data[idx]["bboxes"]:
            result["gt_bboxes"].append([item["category"]]+item["bbox"])
        result["gt_bboxes"] = np.array(result["gt_bboxes"])

        # returning the result dictionary
        return result
