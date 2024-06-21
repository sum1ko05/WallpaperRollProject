import tkinter as tk
import subprocess
import config_manager as cfg
'''
version = "v. alpha 0.1.0"
wrp_title = "Wallpaper Roll Project " + version

#subprocess.Popen('python','change_wp_text.pyw').kill()

root.mainloop()
'''

modes = ['Autostart only',
         'Fixed interval (random)',
         'Fixed interval (linear)',
         'WIP',]

class Window:
    #transform:(width, height, xpos, ypos)
    def __init__(self, transform:tuple=(100, 100, 0, 0), title="SampleWindow", 
                 resizeable=(False, False), icon:str=None, data:dict={}):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f'{transform[0]}x{transform[1]}+{transform[2]}+{transform[3]}')
        self.root.resizable(resizeable[0], resizeable[1])
        if icon:
            self.root.iconbitmap(icon)
        self.data = data

        self.changing_var = tk.StringVar(value=self.data['Changing mode'])
        print(self.data['Themes'])

    def draw(self):
        frame_main = tk.Frame(master=self.root)
        frame_left = tk.Frame(master=frame_main)

        frame_change_mode = tk.LabelFrame(master=frame_left, text="Change mode")
        frame_fixed_settings = tk.LabelFrame(master=frame_left, text="Fixed settings")
        frame_change_mode.pack(side='top')
        frame_fixed_settings.pack(side='bottom')

        frame_right = tk.Frame(master=frame_main)

        frame_theme_explorer = tk.LabelFrame(master=frame_right, text='Theme explorer')
        frame_theme_settings = tk.LabelFrame(master=frame_right, text='Theme settings')
        frame_theme_explorer.pack(side='top')
        frame_theme_settings.pack(side='bottom')

        frame_left.pack(side='left', fill='y')
        frame_right.pack(side='right')

        frame_bottom = tk.Frame(master=self.root, height=14)

        frame_main.pack(side='top', fill='both')
        frame_bottom.pack(side='bottom', fill='both')


        modes_listbox = tk.Listbox(frame_change_mode)
        for option in modes:
            ratio = tk.Radiobutton(modes_listbox, text=option,
                                value=option, variable=self.changing_var, 
                                bg='white', command=self._update)
            ratio.pack(anchor='w')
        modes_listbox.yview_scroll(number=1, what='units')
        modes_listbox.pack()

        save_button = tk.Button(frame_bottom, width=20, height= 5, 
                                text="Save config", command=self._save)

        save_button.pack(side='right')

    def run(self):
        self.draw()
        self.root.mainloop()

    def _save(self):
        cfg.save_config(data)
        #print(self.data['Changing mode'])

    def _update(self):
        self.data['Changing mode'] = self.changing_var.get()
        

if __name__ == "__main__":
    version = "v. alpha 0.1.0"
    wrp_title = "Wallpaper Roll Project " + version

    data = cfg.load_config()

    win = Window(transform=(600,400,200,100),
                 title=wrp_title,
                 icon="sample_icon.ico",
                 data=data)
    win.run()