####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from my_package.analysis import plot_visualization
from my_package.data import Dataset
from my_package.model import InstanceSegmentationModel
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage, rescale


####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
from os import path
import numpy as np
from tkinter import Label, Tk, Entry, StringVar, Button, LEFT, ttk, filedialog
from PIL import Image, ImageTk
from functools import partial
from warnings import filterwarnings


filterwarnings("ignore")
# Define the function you want to call when the filebrowser button is clicked.


def fileClick(clicked, dataset, segmentor, img_path):
    ####### CODE REQUIRED (START) #######
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.
    filepath = filedialog.askopenfilename(filetypes=[(
        'Jpg Files', '*.jpg'), ('png Files', '*.png'), ('jpeg Files', '*.jpeg')], initialdir="data/imgs/")

    print(filepath)
    # try to open the path otherwise print an error message that no iage is selected
    try:
        PILimage = Image.open(filepath)
    except Exception as err:
        print("******************* ", err, " *******************")
        msg.configure(font=("Arial Bold", 10),
                      text=f"No image is selected !")
        msg.place(x=80, y=25)
        return
    img_path["path"] = filepath
    my_data = dataset
    # scaling the image between [0,1]
    image = np.array(PILimage)/255
    # rolling the axis of image to bring it from (H,W,3) to (3,H,W)
    image = np.rollaxis(image, 2, 0)
    seg_store = []
    seg_store.append(segmentor(input=image))
    plot_visualization(image, seg_store, "output/")
    print("done!")
    msg.configure(font=("Arial Bold", 10),
                  text=f"""{path.basename(img_path["path"])} - image is selected !""")
    msg.place(x=80, y=25)
    e.delete(0, 'end')
    e.insert(0, f"""{img_path["path"]} - image is selected !""")
    process(clicked=clicked, img_path=img_path)
    ####### CODE REQUIRED (END) #######

    # `process` function definition starts from here.
    # will process the output when clicked.


def process(clicked, img_path):

    ####### CODE REQUIRED (START) #######
    # Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
    # Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
    # Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.

    global photo
    global photo2
    # if no image is selected then print an error message that no iage is selected
    if img_path["path"] is None:
        msg.configure(font=("Arial Bold", 10),
                      text=f"No image is selected !")
        msg.place(x=80, y=25)
        return
    # try to open the path otherwise print an error message that no iage is selected
    try:
        image = Image.open(img_path["path"])
    except Exception as err:
        print("******************* ", err, " *******************")
        msg.configure(font=("Arial Bold", 10),
                      text=f"No image is selected !")
        msg.place(x=80, y=25)
        return
    resize = RescaleImage(600)  # create an instance of the RescaleImage class
    image = resize(image=image)  # rescale the image
    width, height = image.size  # get width and height of the image

    photo = ImageTk.PhotoImage(image)
    image_label = Label(root, image=photo)

    if clicked.get() == "Segmentation":  # segmention is clicked then get the segmentted image from the output folder and make lable of that image and place them in the root window
        result_img_path = f"output/_Segmented.jpg"
        result_img = Image.open(result_img_path)
        result_img = resize(image=result_img)
        photo2 = ImageTk.PhotoImage(result_img)
        result_img_label = Label(root, image=photo2)
        image_label.place(x=50, y=50)
        result_img_label.place(x=width+150, y=50)
    else:  # segmention is clicked then get the segmentted image from the output folder and make lable of that image and place them in the root window
        result_img_path = f"output/_Bounding_boxed.jpg"
        result_img = Image.open(result_img_path)
        result_img = resize(image=result_img)
        photo2 = ImageTk.PhotoImage(result_img)
        result_img_label = Label(root, image=photo2)
        image_label.place(x=50, y=50)
        result_img_label.place(x=width+150, y=50)
       ####### CODE REQUIRED (END) #######

    # `main` function definition starts from here.
if __name__ == '__main__':
    # CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    global root
    root = Tk()
    root.title("ImageViewerGUI - Nikhil Saraswat 20CS10039")
    root.geometry("800x45")
    ####### CODE REQUIRED (END) #######

    # Setting up the segmentor model.
    annotation_file = './data/annotations.jsonl'
    transforms = []

    # Instantiate the segmentor model.
    segmentor = InstanceSegmentationModel()
    # Instantiate the dataset.
    dataset = Dataset(annotation_file, transforms=transforms)

    # Declare the options.
    options = ["Segmentation", "Bounding-box"]
    clicked = StringVar()
    clicked.set(options[0])
    global e
    e = Entry(root, width=70)
    e.grid(row=0, column=0)
    global msg
    msg = Label(root, text="", justify=LEFT)
    global image_label
    image_label = Label(root, image=None)
    global image_label2
    result_img_label = Label(root, image=None)

    ####### CODE REQUIRED (START) #######
    # Declare the file browsing button
    img_path = {}
    img_path["path"] = None
    selectButton = Button(text='...', command=partial(
        fileClick, clicked, dataset, segmentor, img_path), padx=5)
    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button
    clicktypeDropDown = ttk.Combobox(
        root, width=27, values=options, textvariable=clicked, state="readonly")
    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    myButton = Button(root, text="Process",
                      command=partial(process, clicked, img_path), padx=2)
    selectButton.grid(row=0, column=1)
    clicktypeDropDown.grid(row=0, column=2)
    myButton.grid(row=0, column=3)

    # CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()
    ####### CODE REQUIRED (END) #######
