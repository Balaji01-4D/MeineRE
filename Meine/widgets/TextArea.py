from textual.widgets import TextArea
from textual import work


class TextEditor(TextArea):

    def __init__(self, text = "", *, language = None, theme = "css", soft_wrap = True, tab_behavior = "focus", read_only = False, show_line_numbers = False, line_number_start = 1, max_checkpoints = 50, name = None, id = None, classes = None, disabled = False, tooltip = None):
        super().__init__(text, language=language, theme=theme, soft_wrap=soft_wrap, tab_behavior=tab_behavior, read_only=read_only, show_line_numbers=show_line_numbers, line_number_start=line_number_start, max_checkpoints=max_checkpoints, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip)
        self.filepath = None
            


    @work(exclusive=True)
    async def key_ctrl_s(self):
        with open(self.filepath,'w') as file:
            file.writelines(self.text)
        self.notify(f'{self.filepath.name} saved successfully')


