'''
Presenter transmit data and control between models.py and view.py
'''

from .view import Application
from .models import Model
from typing import Protocol



class View(Protocol):
    def update_toc(self) -> None:
        ...
    def get_note(self) -> dict:
        '''
            return {'title': title, 'content': context}
        '''
        ...



class Presenter:
    def __init__(self, model, view: View):
        self.model = model()
        self.view = view(self)
        self.handle_update_toc()


    def handle_save_note(self, event=None) -> None:
        note = self.view.get_note() # get note title and content in widgets

        if note['title'] == '':
            self.view.error_empty_note_title()
            return None

        if self.view.current_working_note_toc_index == None: # if new, create
            self.model.db_note_create(note['title'], note['content'])
            toc_length = self.view.get_toc_length()
            self.view.current_working_note_toc_index = toc_length - 1 # set current working toc index to new note, to avoid recreate same note multiple times
        else: # if existed, update
            toc_index = self.view.current_working_note_toc_index
            note_id = self.view.mapping_toc_index_to_note_id[toc_index]
            self.model.db_note_update(note_id, note['title'], note['content'])
        
        self.handle_update_toc()
        self.view.btn_new_note['state'] = 'enable'

    def handle_delete_note(self, event=None) -> None:
        toc_index = self.view.get_delete_note_toc_index()
        note_id = self.view.mapping_toc_index_to_note_id[toc_index]
        print(note_id)
        self.model.db_note_delete([note_id])
        self.handle_update_toc()
        self.view.new_note()

    def handle_update_note(self, event=None) -> None:
        '''update existing note in database'''
        pass

    def handle_update_toc(self, event=None) -> None:
        note_list = self.model.db_note_get_all()
        self.view.update_toc(note_list)

    def handle_listbox_select(self, event=None) -> None:
        '''use mapping (view.listbox_toc.index -> note_id) to retrieve data from db'''
        selected = len(self.view.listbox_toc.curselection()) > 0 # if you deselect item, curselection will return empty tuple!
        if selected:
            toc_index = self.view.listbox_toc.curselection()[0]
            note_id = self.view.mapping_toc_index_to_note_id[toc_index]
            # print(f'toc_index: {toc_index} -> id: {note_id}')
            note = self.model.db_note_get_by_id(note_id)
            # print(note)
            self.view.update_note_frame(toc_index, title=note[3], content=note[4])
        self.handle_update_toc()
        self.view.btn_new_note['state'] = 'enable'

    def run(self) -> None:
        self.view.mainloop()