# Imports

from PIL import Image, ImageDraw
import numpy as np
import cv2

# Write the required arguments


def plot_visualization(image, seg_store, outputs):

    # The function should plot the predicted segmentation maps and the bounding boxes on the images and save them.
    # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.

    # since there is only one image so find masks for only first image 
    pred_masks = seg_store[0][1]  # list of masks of the image
    # rolling the axis of image to bring it from (3,H,W) to (H,W,3)
    image = np.rollaxis(image, 0, 3)
    # Since we scaled the image between [0,1] so multiplying with 255 to regain the scalling
    original_image = image
    # iterating over predicted masks for particular image
    # if number of pred masks < 3 then taking all the masks else taking top 3 masks
    for index in range(min(3, len(pred_masks))):
        mask = pred_masks[index]
        # rolling the axis of masks to bring it from (3,H,W) to (H,W,3)
        mask = np.rollaxis(mask, 0, 3)
        # for coloring the masks
        rgb = [0, 0, 0]
        rgb[index] = 0.65
        # here we are using concept of inclusion-exclusion for coloring and making the masks transparent
        # we are substracting the part of image at the place of mask then adding the same part of image with lower intensity + more intesity of color
        image = image * (mask < 0.5).astype(int) + (mask >= 0.5).astype(int) * \
                tuple(rgb) + image * (mask > 0.5).astype(int)*0.35
    # converting the numpy array of image into PIL image
    PILimg = Image.fromarray(np.uint8((image*255)))
    img_path = f"{outputs}_Segmented.jpg"
    PILimg.save(img_path)
    # iterating over predicted boundry boxes for particular image
    # if number of pred bboxes < 3 then taking all the bboxes else taking top 3 bboxes
    PILimg = Image.fromarray(np.uint8((original_image*255)))
    for index in range(min(3, len(pred_masks))):
        # creating an instance of draw, for f=drawing boundry boxes and writing text
        draw = ImageDraw.Draw(PILimg)
        # creating variables for pred_class, pred_score, pred_boxes
        pred_class = seg_store[0][2][index]
        pred_score = seg_store[0][3][index]
        pred_boxes = seg_store[0][0]
        # storing top left and bottom right corners of the boundry boxes
        top_left, bottom_right = pred_boxes[index]
        x1, y1 = top_left
        x2, y2 = bottom_right
        # drawing boundry boxes with outline of blue color and width = 1
        draw.rectangle([x1, y1, x2, y2], outline='blue', width=3)
        # predicted score of the accuracy of the segmentor model for particular object
        pred_score = str(round(pred_score, 5))
        # creating f strings of the text which we want to print over the boundry boxes
        text = f"{pred_class} ({pred_score})"
        # here we are writing text on the image using opencv module we are using HERSHEY_DUPLEX font and 0.5 font size
        PILimg = Image.fromarray(cv2.putText(np.array(PILimg), text, tuple(map(
            int, [x1, y1-10])), cv2.FONT_HERSHEY_SIMPLEX, fontScale=.5, color=(0, 0, 0), lineType=cv2.LINE_AA))
    img_path = f"{outputs}_Bounding_boxed.jpg"
    PILimg.save(img_path)
