import tkinter as tk
from tkinter import ttk
import time, threading, requests, pathlib, os

from requests.models import Response

class bininfo:
    version: str = "1.0.0"

def update_self(lbl, prg):
    time.sleep(2)
    lbl['text'] = "Checking for an updated version of the updater..."
    time.sleep(1)
    r = requests.get("https://matthew5pl.net/cubey/api/updaterver.txt")
    lbl['text'] = "Latest version is: " + r.text
    time.sleep(1)
    lbl['text'] = "Current version is:" + bininfo.version
    time.sleep(2)
    if(bininfo.version == r.text):
        lbl['text'] = "No updates for the updater. Continuing..."
        time.sleep(1)
        lbl['text'] = "Downloading package..."
        link = "https://matthew5pl.net/cubey/cdn/cubey_linux_amd64_product.zip"
        file_name = str(os.path.join(pathlib.Path(__file__).parent.resolve(), "cubey.zip"))
        with open(file_name, "wb") as f:
            lbl['font'] = ("Arial", 10)
            lbl['text'] = "Saving to " + file_name + "..."
            resp = requests.get(link, stream=True)
            total_length = resp.headers.get('content-length')
            if total_length is None:
                f.write(resp.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in resp.iter_content(chunk_size=4096):
                    dl+=len(data)
                    f.write(data)
                    done = int(100 * dl / total_length)
                    prg['value'] = done
                    print(done)
                    if(done == 100):
                        lbl['text'] = "Done. You can now close this window."
    elif(bininfo.version != r.text):
        lbl['text'] = "Updating updater..."
        

winx, winy = 350,200

window = tk.Tk()
window.geometry("350x200")
window.title("Cubey's Adventures Lite Updater")
window.resizable(False, False)
window.grid()

title = tk.Label(
    text="Welcome! Ready to Download.",
    font=("Arial", 12),
)

prg = ttk.Progressbar(
    orient="horizontal",
    mode="determinate",
    length=winx/2
)

title.pack()
prg.pack()

dlthr = threading.Thread(target=update_self, kwargs={"lbl": title, "prg": prg})
dlthr.start()

window.mainloop()
