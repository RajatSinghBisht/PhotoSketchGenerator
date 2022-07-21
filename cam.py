import cv2
import os
from tkinter import filedialog
from PIL import Image


# open cam and process the video to sketch format
def sk_cam():
    def sketch(image):
        im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inverted_gray_image = cv2.bitwise_not(im_gray)
        blurred_image = cv2.GaussianBlur(inverted_gray_image, (91, 91), 0)
        inverted_blurred_image = cv2.bitwise_not(blurred_image)
        pencil_sketch_image = cv2.divide(im_gray, inverted_blurred_image, scale=256.0)
        return pencil_sketch_image

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame")
            break

        else:
            cv2.imshow('Original image', frame)  # cv2 window to show original image
            cv2.imshow('Sketcher', sketch(frame))  # cv2 window to show sketch image
            k = cv2.waitKey(1)

            # press Esc button to close the cam
            if k == 27:
                print("Closing cam")
                break

            # press space bar to save the image
            elif k == 32:
                file = filedialog.asksaveasfile(mode='wb', defaultextension=".png",
                                                filetypes=(("png files", "*,png"), ("all files", "*.*")))
                if file:
                    abs_path = os.path.abspath(file.name)
                    sk = Image.fromarray(sketch(frame))
                    sk.save(abs_path)

    cap.release()
    cv2.destroyAllWindows()
