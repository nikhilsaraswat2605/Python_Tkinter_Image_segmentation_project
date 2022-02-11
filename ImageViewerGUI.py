####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from my_package.model import InstanceSegmentationModel
from my_package.data import Dataset
from my_package.analysis import plot_visualization
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage


####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


# Define the function you want to call when the filebrowser button is clicked.


def fileClick(clicked, dataset, segmentor, img_path):

    ####### CODE REQUIRED (START) #######
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.
    name = filedialog.askopenfilename(filetypes=[(
        'Jpg Files', '*.jpg'), ('png Files', '*.png'), ('jpeg Files', '*.jpeg')])
    print(name)
    img_path["path"] = name
    # print(img_path)
    PILimage = Image.open(name)
    # scaling the image between [0,1]
    image = np.array(PILimage)/255
    # rolling the axis of image to bring it from (H,W,3) to (3,H,W)
    image = np.rollaxis(image, 2, 0)
    seg_store = []
    seg_store.append(segmentor(input=image))
    plot_visualization(image, seg_store, "output/")
    print("done!")
    msg.configure(font=("Arial Bold", 10),
                  text=f"""{img_path["path"]} - image is selected !""")
    msg.grid(row=1, columnspan=5)
    e.delete(0, 'end')
    e.insert(0, f"""{img_path["path"]} - image is selected !""")
    ####### CODE REQUIRED (END) #######

    # `process` function definition starts from here.
    # will process the output when clicked.


def process(clicked, img_path):

    ####### CODE REQUIRED (START) #######
    # Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
    # Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
    # Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.
    # print(img_path[0])
    global photo
    global photo2
    if img_path["path"] is None:
        msg.configure(font=("Arial Bold", 10),
                      text=f"No image is selected !")
        msg.grid(row=1, columnspan=5)
        return
    image = Image.open(img_path["path"])
    # image.show()
    resize = RescaleImage(500)
    image = resize(image=image)
    photo = ImageTk.PhotoImage(image)
    image_label = Label(root, image=photo)
    if clicked.get() == "Segmentation":
        # image.show()
        result_img_path = f"output/Seg.jpg"
        result_img = Image.open(result_img_path)
        result_img = resize(image=result_img)
        photo2 = ImageTk.PhotoImage(result_img)
        image_label2 = Label(root, image=photo2)
        image_label.grid(row=2, column=0)
        image_label2.grid(row=2, column=1)
    else:
        result_img_path = f"output/BB.jpg"
        result_img = Image.open(result_img_path)
        result_img = resize(image=result_img)
        photo2 = ImageTk.PhotoImage(result_img)
        image_label2 = Label(root, image=photo2)
        image_label.grid(row=2, column=0)
        image_label2.grid(row=2, column=1)
    ####### CODE REQUIRED (END) #######

    # `main` function definition starts from here.
if __name__ == '__main__':

    # CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    root = Tk()
    root.title("MY GUI")
    root.config(bg='#4A7A8C')
    root.geometry("800x40")
    # sb = Scrollbar(
    #     root,
    #     orient=HORIZONTAL
    # )

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
    global Msg
    msg = Label(root, text="")

    ####### CODE REQUIRED (START) #######
    # Declare the file browsing button

    img_path = {}
    img_path["path"] = None
    selectButton = Button(text='...', command=partial(
        fileClick, clicked, dataset, segmentor, img_path), padx=2, pady=2)
    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button 

    clicktypeDropDown = ttk.Combobox(
        root, width=27, values=options, textvariable=clicked, state="readonly")
    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    myButton = Button(root, text="Process",
                      command=partial(process, clicked, img_path), padx=2, pady=2)
    selectButton.grid(row=0, column=1)
    clicktypeDropDown.grid(row=0, column=2)
    myButton.grid(row=0, column=3)
    # sb.grid(row=5, columnspan=10, sticky=EW)
    # CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()

    ####### CODE REQUIRED (END) #######
