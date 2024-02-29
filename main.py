import cv2
import pandas
print("Hi I am eshan")
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Slider Tree")

#add the image path here
img = cv2.imread('./spine.png', cv2.IMREAD_GRAYSCALE)
#Meeeenu

def threshold_image(*args):
    global tree

    min_threshold = int(min_slider.get())
    max_threshold = int(max_slider.get())


    min_text.delete(0, tk.END)
    min_text.insert(0, str(min_threshold))
    max_text.delete(0, tk.END)
    max_text.insert(0, str(max_threshold))

   
    ret, thresh_img = cv2.threshold(img, min_threshold, max_threshold, cv2.THRESH_BINARY)


    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    data = []
    for i, contour in enumerate(contours):
      
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        mask = np.zeros_like(img)
        cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)
        avg_pixel_value = cv2.mean(img, mask=mask)[0]

        data.append([i, area, perimeter, avg_pixel_value])

      
        cv2.drawContours(color_img, [contour], -1, (0, 255, 0), 1)

      
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.putText(color_img, str(i), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


    img_tk = ImageTk.PhotoImage(image=Image.fromarray(color_img))
    img_label.config(image=img_tk)
    img_label.image = img_tk

    # if tree:
    #     tree.destroy()

    
    tree = ttk.Treeview(root)
    tree["columns"] = ("area", "perimeter", "avg_pixel_value")
    tree.heading("#0", text="Contour")
    tree.heading("area", text="Area")
    tree.heading("perimeter", text="Perimeter")
    tree.heading("avg_pixel_value", text="Avg Pixel Value")
    for row in data:
        tree.insert("", tk.END, text=row[0], values=(row[1], row[2], row[3]))
    tree.grid(row=3, column=0, columnspan=2)


    


min_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Minimum Threshold", length=300, command=threshold_image)
min_slider.set(100)
min_slider.grid(row=0, column=0)

max_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Maximum Threshold", length=300, command=threshold_image)
max_slider.set(200)
max_slider.grid(row=1, column=0)


min_text = tk.Entry(root)
min_text.insert(0, str(min_slider.get()))
min_text.grid(row=0, column=1)

max_text = tk.Entry(root)
max_text.insert(0, str(max_slider.get()))
max_text.grid(row=1, column=1)


def update_slider(*args):
    try:
        min_slider.set(int(min_text.get()))
    except ValueError:
        pass

    try:
        max_slider.set(int(max_text.get()))
    except ValueError:
        pass

min_text.bind('<KeyRelease>', update_slider)
max_text.bind('<KeyRelease>', update_slider)


img_tk = ImageTk.PhotoImage(image=Image.fromarray(img))
img_label = tk.Label(root, image=img_tk)
img_label.grid(row=2, column=0, columnspan=2)

root.mainloop()
