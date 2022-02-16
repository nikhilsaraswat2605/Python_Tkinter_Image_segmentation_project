####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from my_package.analysis import plot_visualization
from my_package.data import Dataset
from my_package.model import InstanceSegmentationModel
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage, rescale


####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
from os import path
import win32gui
import win32con
import numpy as np
from tkinter import CENTER, Label, Tk, Entry, StringVar, Button, LEFT, ttk, filedialog
from PIL import Image, ImageTk
from functools import partial
from warnings import filterwarnings

filterwarnings("ignore")
#nothing but just for hiding cmd
hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

# Define the function you want to call when the filebrowser button is clicked.


def fileClick(clicked, dataset, segmentor, img_path):
    ####### CODE REQUIRED (START) #######
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.
    filepath = filedialog.askopenfilename(filetypes=[(
        'Jpg Files', '*.jpg'), ('jpeg Files', '*.jpeg')], initialdir="data/imgs/")

    print(filepath)
    # try to open the path otherwise print an error message that no iage is selected
    try:
        PILimage = Image.open(filepath)
    except Exception as err:
        print("******************* ", err, " *******************")
        msg.configure(font=("Arial Bold", 15),
                      text='No image is selected !', bg="#FFEDDB")
        msg.place(x=80, y=25)
        return
    img_path["path"] = filepath
    my_data = dataset
    # scaling the image between [0,1]
    image = np.array(PILimage)/255
    # rolling the axis of image to bring it from (H,W,3) to (3,H,W)
    image = np.rollaxis(image, 2, 0)
    seg_store = [segmentor(input=image)]
    plot_visualization(image, seg_store, "output/")
    print("done!")
    msg.configure(font=("Arial Bold", 15),
                  text=f"""{path.basename(img_path["path"])} - image is selected !""", bg="#FFEDDB")
    msg.place(x=80, y=25)
    e.delete(0, 'end')
    e.insert(0, f"""{filepath} - image is selected !""")
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
    global result_img_photo
    # try to open the path otherwise print an error message that no iage is selected
    try:
        image = Image.open(img_path["path"])
    except Exception as err:
        print('******************* ', err, ' *******************')
        msg.configure(font=('Arial Bold', 15), text='No image is selected !')
        msg.place(x=80, y=25)
        return
    resize = RescaleImage(650)  # create an instance of the RescaleImage class
    image = resize(image=image)  # rescale the image
    width, height = image.size  # get width and height of the image

    photo = ImageTk.PhotoImage(image)
    image_label = Label(root, image=photo, bg="#FFEDDB")

    if clicked.get() == "Segmentation":  # segmention is clicked then get the segmentted image from the output folder and make lable of that image and place them in the root window
        result_img_path = 'output/_Segmented.jpg'
    else:  # segmention is clicked then get the segmentted image from the output folder and make lable of that image and place them in the root window
        result_img_path = 'output/_Bounding_boxed.jpg'

    result_img = Image.open(result_img_path)
    result_img = resize(image=result_img)
    result_img_photo = ImageTk.PhotoImage(result_img)
    result_img_label = Label(root, image=result_img_photo, bg="#FFEDDB")
    image_label.place(x=0, y=50)
    result_img_label.place(x=width+50, y=50)
    ####### CODE REQUIRED (END) #######

    # `main` function definition starts from here.
if __name__ == '__main__':
    # CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    global root  # declaring a global root window
    root = Tk()  # initializing the root window
    root.title("ImageViewerGUI - Nikhil Saraswat 20CS10039")  # title
    root.minsize(width=800, height=45)  # setting minimum size of root window
    root.configure(bg="#FFEDDB")
    root.state('zoomed')  # setting zoomed window state
    style = ttk.Style()
    style.theme_use('classic')
    style.configure("TCombobox", fieldbackground="#FFF5E1",
                    background="#FFF5E1")
    ####### CODE REQUIRED (END) #######

    # Setting up the segmentor model.
    annotation_file = './data/annotations.jsonl'  # path of annotation_file
    transforms = []  # transform list
    # Instantiate the segmentor model.
    segmentor = InstanceSegmentationModel()
    # Instantiate the dataset.
    dataset = Dataset(annotation_file, transforms=transforms)

    # Declare the options.
    options = ["Segmentation", "Bounding-box"]  # options for the dropdown
    clicked = StringVar()  # declaring a string variable of tkinter
    clicked.set(options[0])  # giving segmentation as a default option
    global e  # declaring a global entry variable
    # initializing e default width of 70
    e = Entry(root, width=70, bg="#FFF5E1")
    e.grid(row=0, column=0, columnspan=2, padx=5)
    global msg  # declaring a global variable for the message
    msg = Label(root, text="", justify=CENTER,
                bg="#FFEDDB")  # labeling the message
    global image_label  # declaring a global variable for image label
    # labeling the image label
    image_label = Label(root, image=None, bg="#FFEDDB")
    global result_img_label  # declaring a global variable for result image label
    # labeling result image label
    result_img_label = Label(root, image=None, bg="#FFEDDB")

    ####### CODE REQUIRED (START) #######
    img_path = {'path': None}  # creating a dictionary of path as None
    # Declare the file browsing button
    selectButton = Button(text='. . .', command=partial(
        fileClick, clicked, dataset, segmentor, img_path), padx=5, bg="#FFEDDB")
    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button
    clicktypeDropDown = ttk.Combobox(
        root, width=27, values=options, textvariable=clicked, state="readonly")
    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    myButton = Button(root, text="Process", command=partial(
        process, clicked, img_path), padx=2, bg="#FFEDDB")
    selectButton.grid(row=0, column=2, columnspan=2, padx=5)
    clicktypeDropDown.grid(row=0, column=4, columnspan=2, padx=5)
    myButton.grid(row=0, column=6, columnspan=2, padx=5)

    # CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()
    ####### CODE REQUIRED (END) #######
