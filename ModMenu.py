from ctypes import windll
import io
from pyperclip import copy
from tkinter import *
from urllib.request import urlopen
from PIL import Image, ImageTk
from json import load


class ModMenu:

    def __init__(self):
        self.mods = {}
        self.mods_images = {}

        self.Tk = Tk()

        self.GWL_EXSTYLE = -20
        self.WS_EX_APPWINDOW = 0x00040000
        self.WS_EX_TOOLWINDOW = 0x00000080

        self.Tk.overrideredirect(True)
        self.Tk.config(bg="gray13")
        self.Tk.resizable(width=False, height=False)
        self.Tk.title("ModMenu")

        try:
            self.Tk.iconbitmap("icon.ico")
        except:
            pass

        self.Tk.borderFrame = Frame(width=290, height=20, bg="gray20")
        self.Tk.borderFrame.pack_propagate(False)
        self.Tk.borderFrame.pack(side=TOP)

        self.Tk.helloText = Label(self.Tk.borderFrame, text="ModMenu",
                                  bg="gray20", fg="gray60")
        self.Tk.helloText.pack(side=LEFT)

        self.Tk.exit_button = Button(self.Tk.borderFrame, text="  X  ", command=self.exit,
                                     bd=0, bg="gray20", fg="gray60")
        self.Tk.exit_button.pack(side=RIGHT)
        self.Tk.exit_button.bind("<Enter>", self.on_enter_exit)
        self.Tk.exit_button.bind("<Leave>", self.on_leave_exit)

        self.Tk.borderFrame.bind("<Button-1>", self.start_move)
        self.Tk.borderFrame.bind("<ButtonRelease-1>", self.stop_move)
        self.Tk.borderFrame.bind("<B1-Motion>", self.moving)
        self.Tk.borderFrame.bind("<Map>", self.frame_mapped)

        # Moderators part
        self.Tk.after(10, self.mod_menu_panel())

        # Taskbar icon
        self.Tk.after(10, self.set_appwindow)

        # Start
        self.Tk.mainloop()

    def mod_menu_panel(self):
        mods = load(urlopen("https://api.vimeworld.ru/online/staff"))
        if self.mods != mods:
            try:
                self.Tk.rightFrame.destroy()
            except:
                pass

            if not mods:
                self.mods = mods
                self.mods_images = {}
                self.Tk.rightFrame = Frame(width=290, height=40, bg="gray15")
                self.Tk.rightFrame.pack_propagate(False)
                self.Tk.rightFrame.pack()
                self.Tk.rightFrame.text = Label(self.Tk.rightFrame, text="Никого нет в сети", bg="gray15", fg="#4879EA")
                self.Tk.rightFrame.text.configure(font=("TkDefaultFont", 14, "bold"))
                self.Tk.rightFrame.text.pack(side=TOP, pady=3, padx=3)

            else:
                self.mods = mods
                self.mods_images = {}

                self.Tk.rightFrame = Frame(width=290, bg="gray15")
                self.Tk.rightFrame.pack_propagate(False)
                self.Tk.rightFrame.pack()

                for mod in self.mods:
                    nick = mod.get("username")
                    if nick is not None:
                        self.Tk.modbox = Frame(self.Tk.rightFrame, width=290, height=60, bg="gray20")
                        self.Tk.modbox.pack_propagate(False)
                        self.Tk.modbox.pack(side=TOP, pady=5, padx=5)

                        image_byt = urlopen(f"https://skin.vimeworld.ru/head/{nick}/50.png").read()
                        image_b64 = Image.open(io.BytesIO(image_byt))
                        self.mods_images[nick] = ImageTk.PhotoImage(image_b64)
                        self.Tk.modbox.image = Label(self.Tk.modbox, image=self.mods_images.get(nick), bg="gray20")
                        self.Tk.modbox.image.pack(side=LEFT, pady=3, padx=3)
                        self.Tk.modbox.text = Label(self.Tk.modbox, text=nick, bg="gray20", fg="#4879EA")
                        self.Tk.modbox.text.configure(font=("TkDefaultFont", 14, "bold"))
                        self.Tk.modbox.text.pack(side=LEFT, pady=3, padx=3)

                        self.Tk.modbox.bind("<Button-1>", self.copy_on_click)
                        self.Tk.modbox.bind("<Enter>", self.on_enter)
                        self.Tk.modbox.bind("<Leave>", self.on_leave)
                        for child in self.Tk.modbox.winfo_children():
                            child.bind("<Button-1>", self.copy_on_click)
                            child.bind("<Enter>", self.on_enter)
                            child.bind("<Leave>", self.on_leave)

            self.Tk.rightFrame.config(height=round(70 * (len(self.Tk.rightFrame.winfo_children()))))

        self.Tk.after(5000, self.mod_menu_panel)

    # The part where you get the nickname of the moderator you click on.
    def copy_on_click(self, e):
        parent = e.widget._nametowidget(e.widget.winfo_parent())
        child = parent.winfo_children()[-1]
        if child.winfo_children():
            child = child.winfo_children()[-1]
        copy(child.cget("text"))
        child['foreground'] = "#15AD4B"

    # Make Icon in taskbar
    def set_appwindow(self):
        hwnd = windll.user32.GetParent(self.Tk.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, self.GWL_EXSTYLE, style)

        self.Tk.wm_withdraw()
        self.Tk.after(10, lambda: self.Tk.wm_deiconify())

    # Moving part
    def start_move(self, event):
        global x, y
        x = event.x
        y = event.y

    def stop_move(self, event):
        global x, y
        x = None
        y = None

    def moving(self, event):
        global x, y
        x_ = (event.x_root - x)
        y_ = (event.y_root - y)
        self.Tk.geometry("+%s+%s" % (x_, y_))

    def frame_mapped(self, e):
        self.Tk.update_idletasks()
        self.Tk.overrideredirect(True)
        self.Tk.state('normal')

    # Visual part
    def on_enter_exit(self, e):
        e.widget['background'] = 'red'
        e.widget['foreground'] = 'white'
        e.widget['activebackground'] = 'red'
        e.widget['activeforeground'] = 'white'

    def on_leave_exit(self, e):
        e.widget['background'] = 'gray20'
        e.widget['foreground'] = 'gray60'

    def on_enter(self, e):
        parent = e.widget._nametowidget(e.widget.winfo_parent())
        child = parent.winfo_children()[-1]
        child2 = parent.winfo_children()[0]
        if child.winfo_children():
            parent = child
            child2 = child.winfo_children()[0]
            child = child.winfo_children()[-1]
        parent['background'] = 'gray25'
        child['background'] = 'gray25'
        child2['background'] = 'gray25'

    def on_leave(self, e):
        parent = e.widget._nametowidget(e.widget.winfo_parent())
        child = parent.winfo_children()[-1]
        child2 = parent.winfo_children()[0]
        if child.winfo_children():
            parent = child
            child2 = child.winfo_children()[0]
            child = child.winfo_children()[-1]
        parent['background'] = 'gray20'
        child['background'] = 'gray20'
        child2['background'] = 'gray20'
        child['foreground'] = '#4879EA'

    # Exit part :)
    def exit(self):
        self.Tk.destroy()


def run():
    ModMenu()


if __name__ == '__main__':
    run()
