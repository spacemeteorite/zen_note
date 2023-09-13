'''view provides all attributes and methods related to user interface, but
view itself don't control or change any thing, it needs to transmit event 
to presenter.py, and wait for it to call method in view.py and model.py'''

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Protocol



class Presenter(Protocol):
    def handle_save_note(self, event: tk.Event):
        '''save note to database'''
        ...
    def handle_delete_note(self, event: tk.Event):
        '''delete note from database'''
        ...
    def handle_update_toc(self, event: tk.Event):
        '''update toc listbox'''
        ...


class Application(tk.Tk):
    def __init__(self, presenter: Presenter):
        super().__init__()

        # variables
        self.variables = {
            'title': tk.StringVar(),
            'content': tk.StringVar(),
        }
        self.mapping_toc_index_to_note_id = dict()
        self.current_working_note_toc_index = None # tracking current working note to update it in database.

        # window init configuration
        self.title('Zen Note')

        # widgets creation
        self.frame_toc = ttk.Frame(self, relief='ridge', borderwidth=5)
        self.listbox_toc = tk.Listbox(self.frame_toc)
        self.menu_toc = tk.Menu(self.listbox_toc, tearoff=False)
        self.menu_toc.add_command(label='delete note', command=presenter.handle_delete_note)

        self.frame_note = ttk.Frame(self, relief='ridge', borderwidth=5)
        self.entry_title = ttk.Entry(self.frame_note, textvariable=self.variables['title'])
        self.text_content = tk.Text(self.frame_note)
        self.frame_note_frame_btn = ttk.Frame(self.frame_note, relief='solid', borderwidth=3)
        self.btn_save = ttk.Button(self.frame_note_frame_btn, text='save')
        self.btn_new_note = ttk.Button(self.frame_note_frame_btn, text='new note', command=self.new_note)

        # widgets row and column configuration
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self.frame_toc.columnconfigure(0, weight=1)
        self.frame_toc.rowconfigure(0, weight=1)

        self.frame_note.columnconfigure(0, weight=1)
        self.frame_note.rowconfigure(1, weight=1)

        # widgets grid layout
        self.frame_toc.grid(row=0, column=0, sticky='wens')
        self.listbox_toc.grid(row=0, column=0, sticky='wens')

        self.frame_note.grid(row=0, column=1, sticky='wens')
        self.entry_title.grid(row=0, column=0, sticky='we', pady=10)
        self.text_content.grid(row=1, column=0, sticky='wens')
        self.frame_note_frame_btn.grid(row=2, column=0, sticky='we')
        self.btn_save.grid(row=0, column=0, sticky='w')
        self.btn_new_note.grid(row=0, column=1, sticky=' e')

        # bind event to handler
        self.btn_save.bind('<ButtonRelease-1>', presenter.handle_save_note)
        self.listbox_toc.bind('<<ListboxSelect>>', presenter.handle_listbox_select)
        self.listbox_toc.bind("<Button-3>", self.toc_popup)



    # attribute getters
    def get_toc_length(self):
        toc_length = len(self.listbox_toc.get(0, tk.END))
        return toc_length


    def get_note(self):
        '''get current content in note frame'''
        title = self.variables['title'].get()
        content = self.text_content.get('1.0', tk.END)
        return {'title':title, 'content':content}


    def get_delete_note_toc_index(self):
        '''delete note by index of selected item in toc listbox'''
        print('trying to delete note')
        toc_index = int(self.current_working_note_toc_index)
        self.current_working_note_toc_index = None
        return toc_index


    # ui updaters
    def new_note(self) -> None:
        '''clear note frame for creating new note'''
        self.current_working_note_toc_index = None
        self.variables['title'].set('new note')
        self.text_content.delete('1.0', tk.END)
        self.btn_new_note['state'] = 'disabled'
    

    def update_note_frame(self, toc_index:int, title:str, content:str) -> None:
        '''update note frame to current working note'''
        self.current_working_note_toc_index = toc_index
        print('current_working', self.current_working_note_toc_index)
        print('note_index', toc_index, 'note_id', self.mapping_toc_index_to_note_id[toc_index])
        self.variables['title'].set(title)
        self.text_content.delete('1.0', tk.END)
        self.text_content.insert('1.0', content)
    

    def update_toc(self, note_list: list[tuple]):
        '''
        1. provide a list of row(which is tuple) in database
        and update the listbox
        [(id, creation_time, last_update_time, title, content),(...),...]
        2. append a mapping listbox_index -> note_id for retrieve note in database
        '''
        self.listbox_toc.delete(0, tk.END)
        listbox_index = 0
        for note in note_list:
            self.listbox_toc.insert(tk.END, f"{note[3]}   {note[2]}")
            self.mapping_toc_index_to_note_id[listbox_index] = note[0]
            listbox_index += 1
        self.update()


    # Popups
    def toc_popup(self, event):
        if self.current_working_note_toc_index is not None:
            print(event.x_root, event.y_root)
            self.menu_toc.tk_popup(event.x_root, event.y_root)


    def error_empty_note_title(self):
        messagebox.showinfo('No title', 'Note title can not be empty!')


    def run(self):
        self.mainloop()



if __name__ == '__main__':
    app = Application()
    app.run()