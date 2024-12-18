import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import cv2
import webbrowser
import numpy as np


def convert_to_sketch(image_path, output_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 15)
    inverted_blurred = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blurred, scale=60.0)
    sharpened = cv2.addWeighted(sketch, 1.5, sketch, 0, -50)
    contrast = cv2.convertScaleAbs(sharpened, alpha=3, beta=0)
    cv2.imwrite(output_path, contrast)


def save_sketch_to_pdf(sketch_path, pdf_path):
    image = Image.open(sketch_path)
    image = image.convert("RGB") 
    image.save(pdf_path, "PDF")

def open_folder(path):
    folder = os.path.dirname(path)
    webbrowser.open(f"file:///C:/Users/DELL/PycharmProjects/beginnerPython/output/{folder}.pdf")

def process_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        return

    try:
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        sketch_path = os.path.join(output_folder, "sketch.jpg")
        pdf_path = os.path.join(output_folder, "output.pdf")

        convert_to_sketch(file_path, sketch_path)

        save_sketch_to_pdf(sketch_path, pdf_path)
        open_folder(pdf_path)

        messagebox.showinfo("Success", f"The image has been drawn successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


app = tk.Tk()
app.title("Photo to Sketch PDF Converter")

label = tk.Label(app, text="Upload a photo to convert to a sketch PDF")
label.pack(pady=10)

upload_button = tk.Button(app, text="Upload and Convert", command=process_image)
upload_button.pack(pady=20)

app.geometry("600x300")
app.mainloop()