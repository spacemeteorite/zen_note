from zen_note.models import Model
from zen_note.view import Application
from zen_note.presenter import Presenter 

my_presenter = Presenter(Model, Application)
my_presenter.run()