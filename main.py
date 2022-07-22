import tkinter as tk
import subprocess
from threading import Thread
from tkinter import ttk, filedialog, messagebox,Menu,NORMAL,END



def click(event):
    url_box.configure(state=NORMAL)
    url_box.delete(0, END)
    url_box.unbind('<Button-1>', clicked)

def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

def paste():
    clipboard = root.clipboard_get()
    url_box.insert('end', clipboard)


def copy():
    inp = url_box.get()
    root.clipboard_clear()
    root.clipboard_append(inp)


def threading():
    t1 = Thread(target=get_video)
    t1.start()


def get_video():
    durl = url_box.get()
    if len(durl) == 0 or durl == "Enter Youtube URL:":
        tk.messagebox.showerror(title="Error", message="Enter Valid URL")
    if len(durl) > 1 and durl != "Enter Youtube URL:":
        dlocation = tk.filedialog.askdirectory(title='Select a Download location')
        if len(dlocation) == 0:
            tk.messagebox.showerror(title="Error", message="Select Save Location")
        elif len(dlocation) >= 1:
            progress_bar['value'] = 0
            p = subprocess.Popen(f'cmd /c bin\\yt-dlp.exe {durl} -P {dlocation} --ffmpeg-location bin\\ffmpeg.exe',
                                shell=True,
                                stdout=subprocess.PIPE)
            while True:
                progress_bar['value']+=10
                line = p.stdout.readline()
                value_label.configure(font=("Consolas",8), text=f'{line.decode().format(3, 5)}')
                if line == b'':
                    value_label.configure(foreground="#2fba2c",font="Consolas", text='Download Finished')
                    progress_bar['value'] = 100
                    break


icon_path = "Resources/logo.png"
root = tk.Tk()
root.title("Simple Youtube Downloader v1.0")
root.geometry('620x300')
root.configure(bg="#FFFFFF", borderwidth=0, highlightthickness=0)
root.iconphoto(False, tk.PhotoImage(file=icon_path))

type_label = tk.Label(root, bg="#FFFFFF", text="Simple Youtube Downloader", fg='#f95e61', bd=5,
                      font=('Consolas', 15))
type_label.pack(ipadx=20, ipady=25)

url_box = tk.Entry(root, bg="#FF0000", borderwidth=3, width=50)
url_box.insert(0, 'Enter Youtube URL:')
url_box.pack(pady=5)
clicked = url_box.bind('<Button-1>', click)

m = Menu(root, tearoff=0)
m.add_command(label="Copy", command=copy)
m.add_separator()
m.add_command(label="Paste", command=paste)

url_box.bind('<Button-3>', do_popup)

s = ttk.Style()
s.theme_use('alt')
s.configure("red.Horizontal.TProgressbar", background='#FF0000')

progress_bar = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=150,
    style='red.Horizontal.TProgressbar'
)
progress_bar.pack()

value_label = ttk.Label(root, background="#FFFFFF",text="")
value_label.pack()

button_image = tk.PhotoImage(file='Resources/logo.png')
download = tk.Button(root, image=button_image, borderwidth=0, highlightthickness=0, bg="#FAFAFA", text='Download',
                     command=threading)
download.pack(ipadx=1, ipady=1, pady=20, padx=250)

root.mainloop()
