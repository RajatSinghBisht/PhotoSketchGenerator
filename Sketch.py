from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog

import cv2
import cam
import os


# select image from specific folder to make its sketch
def select_image():
    global panelA, panelB
    global path, pencil_sketch_image
    # path of selected image
    path = filedialog.askopenfilename()
    if len(path) > 0:
        # read image from provided path
        image = cv2.imread(path)

        # convert image to gray image
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # convert gray image to inverted gray image
        inverted_gray_image = cv2.bitwise_not(gray_image)

        # apply gaussian blur set kernel value according to image size
        blurred_image = cv2.GaussianBlur(inverted_gray_image, (77, 77), 0)

        # convert blurred image to inverted blurred image
        inverted_blurred_image = cv2.bitwise_not(blurred_image)

        # Performing bit-wise division between Gray image and Inverted blurred image
        pencil_sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

        image = cv2.resize(image, (600, 500))  # resize original  image to frame size

        sketch = pencil_sketch_image
        sketch = cv2.resize(sketch, (600, 500))  # resize sketch image to frame size

        # convert original image from BGR to RGB format for pil
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # convert opencv format image to Pillow format
        image = Image.fromarray(image)

        sketch = Image.fromarray(sketch)

        # convert pillow image format to ImageTk format
        image = ImageTk.PhotoImage(image)

        sketch = ImageTk.PhotoImage(sketch)

        if panelA is None or panelB is None:  # if panel to show image are not set
            panelA = Label(image=image)  # create panel A
            panelA.image = image  # show original image in panel A
            panelA.pack(side="left", padx=10, pady=10)  # set original image panel to left hand side

            panelB = Label(image=sketch)  # create panel B
            panelB.image = sketch  # show sketch image in panel B
            panelB.pack(side="right", padx=10, pady=10)  # set sketch image panel to left hand side

        # if panel are already set then set new images to these panels
        else:
            panelA.configure(image=image)
            panelB.configure(image=sketch)
            panelA.image = image
            panelB.image = sketch


# process the image by taking value from slider or manually entered
def process(k_size):
    if k_size % 2 == 0:  # if kernel size is even it will create error so convert even value to odd
        k_size += 1
    global panelA, panelB
    global pencil_sketch_image
    if path is not None and len(path) > 0:
        image = cv2.imread(path)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        inverted_gray_image = cv2.bitwise_not(gray_image)

        blurred_image = cv2.GaussianBlur(inverted_gray_image, (k_size, k_size), 0)

        inverted_blurred_image = cv2.bitwise_not(blurred_image)

        pencil_sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (600, 500))

        sketch = pencil_sketch_image
        sketch = cv2.resize(sketch, (600, 500))

        image = Image.fromarray(image)

        sketch = Image.fromarray(sketch)

        image = ImageTk.PhotoImage(image)

        sketch = ImageTk.PhotoImage(sketch)

        if panelA is None or panelB is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            panelB = Label(image=sketch)
            panelB.image = sketch
            panelB.pack(side="right", padx=10, pady=10)

        else:
            panelA.configure(image=image)
            panelB.configure(image=sketch)
            panelA.image = image
            panelB.image = sketch


# user can set contrast level with this slide function
def slide():
    print(horizontal.get())
    process(horizontal.get())


# save sketched Image .... user will select saving directory name
def save():
    file = filedialog.asksaveasfile(mode='wb', defaultextension=".png",
                                    filetypes=(("png files", "*,png"), ("all files", "*.*")))
    if file:
        abs_path = os.path.abspath(file.name)
        sk = Image.fromarray(pencil_sketch_image)
        sk.save(abs_path)


# user have to enter contrast level manually and press on Enter contrast level manually
def manual():
    val = e.get()
    process(int(val))
    e.delete(99, 'end')


# open camera and save sketch images
def sketch_cam():
    cam.sk_cam()


# close the tkinter application
def close():
    root.destroy()


root = Tk()
root.title('Sketch generator')  # title of tkinter application
root.iconbitmap('c:/Users/rajat/Desktop/CollegeProject/PhotoSketchGenerator/sktch.ico')  # icon for tkinter application
root['background'] = 'grey'  # set background of application to grey

horizontal = Scale(root, from_=0, to=200, orient=HORIZONTAL)  # create horizontal slider from value 0 to 200
horizontal.pack()

panelA = None
panelB = None
path = None
pencil_sketch_image = None

# button to select image
btn = Button(root, text="Select an image", command=select_image, fg="red")
btn.pack(side="bottom", fill="both", padx="10", pady="10")

# button to set contrast level using slider
my_contrast = Button(root, text="Contrast", command=slide, fg="green")
my_contrast.place(x=500, y=20)

# button to save image
save_btn = Button(root, text="Save", command=save, fg="blue")
save_btn.place(x=690, y=20)

# button to open camera and save sketch image
sketch_cam = Button(root, text="Open camera", command=sketch_cam)
sketch_cam.pack()

# button to exit from application
exit_btn = Button(root, text="Exit", command=close)
exit_btn.place(x=800, y=20)

# entry for contrast value ... to be entered by user
e = Entry(root, width=10, font=('Helvetica', 15))
e.insert(0, "99")
e.pack(padx=10, pady=10)

# button to process manually entered value for contrast
manual_entry = Button(root, text="Enter contrast level", command=manual)
manual_entry.pack(side="top")

root.mainloop()
