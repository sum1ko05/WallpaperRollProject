import tkinter as tk
import subprocess
import os
import config_manager as cfg

modes = ['Autostart only',
         'Fixed interval (random)',
         'Fixed interval (linear)',
         'Change theme at time (random)',
         'Change theme at time (linear)',]

def time_values() -> list:
    values = []
    for second in range(0, 86400):
        seconds = second % 60
        minutes = second // 60
        hours = minutes // 60
        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'
        values.append(f'{hours}:{minutes}:{seconds}')
    return values
def time_list_to_string(time:list) -> str:
    seconds = time[2]
    minutes = time[1]
    hours = time[0]
    if minutes < 10:
        minutes = f'0{minutes}'
    if seconds < 10:
        seconds = f'0{seconds}'
    #print(f'{hours}:{minutes}:{seconds}')
    return f'{hours}:{minutes}:{seconds}'

class Window:
    #transform:(width, height, xpos, ypos)
    def __init__(self, transform:tuple=(100, 100, 0, 0), title="SampleWindow", 
                 resizeable=(False, False), icon:str=None, minsize:tuple=(100, 100), 
                 data:dict={}):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f'{transform[0]}x{transform[1]}+{transform[2]}+{transform[3]}')
        self.root.resizable(resizeable[0], resizeable[1])
        self.root.minsize(minsize[0], minsize[1])
        if icon:
            self.root.iconbitmap(icon)
        self.data = data

        self.changing_var = tk.StringVar(value=self.data['Changing mode'])

    def draw(self):
        #Frame set
        frame_main = tk.Frame(master=self.root)
        frame_left = tk.Frame(master=frame_main)

        frame_change_mode = tk.LabelFrame(master=frame_left, text="Change mode")
        #frame_fixed_settings = tk.LabelFrame(master=frame_left, text="Fixed settings")
        frame_change_mode.pack(side='top')
        #frame_fixed_settings.pack(side='bottom')

        frame_right = tk.Frame(master=frame_main)

        frame_theme_explorer = tk.LabelFrame(master=frame_right, text='Theme explorer')
        frame_theme_settings = tk.LabelFrame(master=frame_right, text='Theme settings')
        frame_theme_explorer.pack(side='top')
        frame_theme_settings.pack(side='bottom')

        frame_left.pack(side='left', fill='both')
        frame_right.pack(side='right', fill='both')

        frame_bottom = tk.Frame(master=self.root, height=5)

        frame_main.pack(side='top', fill='both')
        frame_bottom.pack(side='bottom', fill='both')

        #Mode selector
        modes_listbox = tk.Listbox(frame_change_mode)
        for option in modes:
            ratio = tk.Radiobutton(modes_listbox, text=option,
                                value=option, variable=self.changing_var, 
                                bg='white', command=self._update)
            ratio.pack(anchor='w')
        modes_listbox.yview_scroll(number=1, what='units')
        modes_listbox.pack(fill='both')

        #Fixed entries
        fixed_theme_var = tk.StringVar(value=self.data['Fixed theme'])
        fixed_theme_entry = tk.Spinbox(frame_change_mode,
                                       command=lambda:self._update_fixed(what='theme',
                                                                         spin=fixed_theme_entry),
                                       values=list(self.data['Themes'].keys()),
                                       wrap=True,
                                       textvariable=fixed_theme_var)
        fixed_interval_var = tk.StringVar(value=time_list_to_string(self.data['Fixed interval']))
        fixed_interval_entry = tk.Spinbox(frame_change_mode,
                                          command=lambda:self._update_fixed(what='interval',
                                                                            spin=fixed_interval_entry),
                                          values=time_values(),
                                          textvariable=fixed_interval_var)
        fixed_interval_var.set(time_list_to_string(self.data['Fixed interval']))

        fixed_theme_entry.pack()
        fixed_interval_entry.pack()

        #Theme explorer
        theme_title_label = tk.Label(frame_theme_explorer, text='Theme title')
        theme_path_label = tk.Label(frame_theme_explorer, text='Theme path')
        theme_del_label = tk.Label(frame_theme_explorer, text='Delete')
        theme_add_label = tk.Label(frame_theme_explorer, text='Add')
        
        theme_listbox = tk.Listbox(frame_theme_explorer)
        theme_title_entry = tk.Entry(frame_theme_explorer)
        theme_path_entry = tk.Entry(frame_theme_explorer)
        theme_remove_button = tk.Button(frame_theme_explorer,
                                        text='🗑',
                                        command=lambda:self._del_theme(listbox=theme_listbox))
        theme_add_button = tk.Button(frame_theme_explorer,
                                     text='+',
                                     command=lambda:self._add_theme(title=theme_title_entry,
                                                                    path=theme_path_entry,
                                                                    listbox=theme_listbox))

        self._update_theme(listbox=theme_listbox)
        theme_title_label.grid(column=0, row=0, ipadx=8, ipady=1)
        theme_path_label.grid(column=1, row=0, ipadx=8, ipady=1)
        theme_del_label.grid(column=2, row=0, ipadx=4, ipady=1)
        theme_add_label.grid(column=3, row=0, ipadx=4, ipady=1)

        theme_title_entry.grid(column=0, row=1, ipadx=8, ipady=1)
        theme_path_entry.grid(column=1, row=1, ipadx=8, ipady=1)
        theme_remove_button.grid(column=2, row=1, ipadx=8, ipady=1)
        theme_add_button.grid(column=3, row=1, ipadx=8, ipady=1)
        theme_listbox.grid(column=0, columnspan=4, row=2, sticky='ew')

        #Theme settings
        setting_title_label = tk.Label(frame_theme_settings, text='Theme title')
        setting_time_label = tk.Label(frame_theme_settings, text='Set at time')
        setting_interval_label = tk.Label(frame_theme_settings, text='Interval')
        setting_del_label = tk.Label(frame_theme_settings, text='Delete')
        setting_add_label = tk.Label(frame_theme_settings, text='Add')

        setting_listbox = tk.Listbox(frame_theme_settings)
        setting_title_entry = tk.Spinbox(frame_theme_settings, width=10,
                                         values=list(self.data['Themes'].keys()))
        setting_time_entry = tk.Spinbox(frame_theme_settings, width=10,
                                        values=time_values())
        setting_interval_entry = tk.Spinbox(frame_theme_settings, width=10,
                                        values=time_values())
        setting_remove_button = tk.Button(frame_theme_settings,
                                        text='🗑',
                                        command=lambda:self._del_setting(listbox=setting_listbox))
        setting_add_button = tk.Button(frame_theme_settings,
                                     text='+',
                                     command=lambda:self._add_setting(title=setting_title_entry,
                                                                      time=setting_time_entry,
                                                                      interval=setting_interval_entry,
                                                                      listbox=setting_listbox))

        self._update_setting(listbox=setting_listbox)
        setting_title_label.grid(column=0, row=0, ipadx=8, ipady=1)
        setting_time_label.grid(column=1, row=0, ipadx=8, ipady=1)
        setting_interval_label.grid(column=2, row=0, ipadx=8, ipady=1)
        setting_del_label.grid(column=3, row=0, ipadx=4, ipady=1)
        setting_add_label.grid(column=4, row=0, ipadx=4, ipady=1)

        setting_title_entry.grid(column=0, row=1, ipadx=8, ipady=1)
        setting_time_entry.grid(column=1, row=1, ipadx=8, ipady=1)
        setting_interval_entry.grid(column=2, row=1, ipadx=8, ipady=1)
        setting_remove_button.grid(column=3, row=1, ipadx=8, ipady=1)
        setting_add_button.grid(column=4, row=1, ipadx=8, ipady=1)
        setting_listbox.grid(column=0, columnspan=5, row=2, sticky='ew')
        #Bottom buttons
        save_button = tk.Button(frame_bottom, width=20, height= 5, 
                                text="Save config", command=self._save)

        save_button.pack(side='right', ipady=1)

    def run(self):
        self.draw()
        self.root.mainloop()

    def _save(self):
        cfg.save_config(data)

    def _update(self):
        self.data['Changing mode'] = self.changing_var.get()

    def _update_fixed(self, what:str, spin:tk.Spinbox):
        if what == 'theme':
            self.data['Fixed theme'] = spin.get()
        if what == 'interval':
            self.data['Fixed interval'] = list(map(int, spin.get().split(':')))

    def _add_theme(self, title:tk.Entry, path:tk.Entry, listbox:tk.Listbox):
        if os.path.isdir(path.get()):
            self.data['Themes'].update({title.get(): path.get()})
            self._update_theme(listbox)

    def _del_theme(self, listbox:tk.Listbox):
        item = listbox.get(listbox.curselection()[0])
        dict_element = list(item.split(" | "))
        if dict_element[0] in self.data['Themes'].keys():
            self.data['Themes'].pop(dict_element[0])
            self._update_theme(listbox)

    def _update_theme(self, listbox:tk.Listbox):
        listbox.delete(first=0, last=listbox.size())
        for key in self.data['Themes']:
            listbox_mask = key + " | " + self.data['Themes'][key]
            listbox.insert(listbox.size(), listbox_mask)

    def _add_setting(self, title:tk.Spinbox, time:tk.Spinbox, interval:tk.Spinbox, listbox:tk.Listbox):
        time_list = list(map(int, time.get().split(':')))
        interval_list = list(map(int, interval.get().split(':')))
        self.data['Settings'].update({title.get(): [time_list, interval_list]})
        self._update_setting(listbox)

    def _del_setting(self, listbox:tk.Listbox):
        item = listbox.get(listbox.curselection()[0])
        dict_element = list(item.split(" | "))
        if dict_element[0] in self.data['Settings'].keys():
            self.data['Settings'].pop(dict_element[0])
            self._update_setting(listbox)

    def _update_setting(self, listbox:tk.Listbox):
        listbox.delete(first=0, last=listbox.size())
        for key in self.data['Settings']:
            listbox_mask = key + " | " + time_list_to_string(self.data['Settings'][key][0]) + " | " + time_list_to_string(self.data['Settings'][key][1])
            listbox.insert(listbox.size(), listbox_mask)
        
        

if __name__ == "__main__":
    version = "v. alpha 0.2.0"
    wrp_title = "Wallpaper Roll Project " + version

    data = cfg.load_config()

    win = Window(transform=(600,500,200,50),
                 title=wrp_title,
                 icon="sample_icon.ico",
                 data=data,
                 resizeable=(True, True),
                 minsize=(600, 500))
    win.run()