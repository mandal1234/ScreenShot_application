import tkinter as tk
from PIL import Image, ImageTk
import mss
import os
from datetime import datetime
from pathlib import Path


#create screenshots folder

SAVE_DIR = Path.home() / "Screenshots"
SAVE_DIR.mkdir(exist_ok=True)


class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Tool")
        self.root.geometry("600x500")


        self.image_label = tk.Label(root, text="No Screenshot Yet")
        self.image_label.pack(pady=10)



        #buttons
        tk.Button(root, text="Capture Fullscreen (F1)", command=self.capture_fullscreen).pack(pady=5)
        tk.Button(root, text ="Capture Center (f2)", command=self.capture_center).pack(pady=5)
        tk.Button(root, text ="Open folder", command=self.open_folder).pack(pady=5)


        #status
        self.status = tk.Label(root, text="Ready", fg="green")
        self.status.pack(pady=10)

        #shortcuts
        root.bind("<F1>", lambda e: self.capture_fullscreen())
        root.bind("<F2>", lambda e: self.capture_center())

#Generate filename

    def get_filename(self):
        return SAVE_DIR / f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"



    #Fullscreen capture
    def capture_fullscreen(self):
        self.root.withdraw() #hide window

        with mss.mss() as sct:
            monitor = sct.monitors[0]
            screenshot = sct.grab(monitor)

            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

        self.root.deiconify() #show window again

        self.save_and_preview(img)


    #center region capture
    def capture_center(self):
        self.root.withdraw()

        with mss.mss() as sct:
            moniter = sct.monitors[0]

            width = moniter["width"]
            height = moniter["height"]

            region = {
                "left": int(width * 0.25),
                "top": int(height * 0.25),
                "width": int(width * 0.5),
                "height": int(height * 0.5)
            }

            screenshot = sct.grab(region)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

        self.root.deiconify()
        self.save_and_preview(img)


    # save + preview

    def save_and_preview(self, img):
        filepath = self.get_filename()
        img.save(filepath)

        #resize for preview

        preview = img.resize((400, 300))
        tk_img = ImageTk.PhotoImage(preview)

        self.image_label.config(image=tk_img, text="")
        self.image_label.image = tk_img

        self.status.config(text=f"Saved: {filepath}")


    #open folder


    def open_folder(self):
        os.startfile(SAVE_DIR)


#Run app

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()