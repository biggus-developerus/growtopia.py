__all__ = ("Dialog",)


class Dialog:
    def __init__(self):
        self.dialog = rf""

    def add_textbox(self, text: str):
        self.dialog += rf"add_textbox|{text}|left|\n"

    def add_smalltext(self, text: str):
        self.dialog += rf"add_smalltext|{text}|left|\n"

    def add_spacer_big(self):
        self.dialog += rf"add_spacer|big|\n"

    def add_spacer_small(self):
        self.dialog += rf"add_spacer|small|\n"

    def add_button_with_icon(self, name: str, text: str, itemid: int):
        self.dialog += rf"add_button_with_icon|{name}|{text}|staticBlueFrame|{itemid}|\n"
    
    def add_input_text(self, name: str, title: str, text: str, max_length: int):
        self.dialog += rf"add_text_input|{name}|{title}|{text}|{str(max_length)}|\n"

    def add_input_password(self, name:str, title: str, text: str, max_length: int):
        self.dialog += rf"add_text_input_password|{name}|{title}|{text}|{str(max_length)}|\n"

    def add_world_redirect(self, text: str, world_name: str):
        self.dialog += rf"add_url_button||{text}|NOFLAGS|OPENWORLD|{world_name}|\n"

    def add_item_picker(self, name: str, text: str, headertext: str):
        self.dialog += rf"add_item_picker|{name}|{text}|{headertext}|\n"

    def add_player_picker(self, name: str, text: str):
        self.dialog += rf"add_player_picker|{name}|{text}|\n"
    
    def add_label_with_icon_big(self, text: str, itemid: int):
        self.dialog += rf"add_label_with_icon|big|{text}|left|{str(itemid)}|\n"

    def add_label_with_icon_small(self, text: str, itemid: int):
        self.dialog += rf"add_label_with_icon|small|{text}|left|{str(itemid)}|\n"

    def add_checkbox(self, name: str, text: str, checked: bool):
        self.dialog += rf"add_checkbox|{name}|{text}|{int(checked)}|\n"

    def add_button(self, name: str, text: str):
        self.dialog += rf"add_button|{name}|{text}|noflags|0|0|\n"

    def add_ending(self, name: str, cancel: str, accept: str):
        self.dialog += rf"end_dialog|{name}|{cancel}|{accept}|\n"

    def allow_quick_exit(self):
        self.dialog += rf"add_quick_exit|\n"

    def add_achievement(self, title: str, text: str, iconid: int):
        self.dialog += rf"add_achieve|{title}|{text}|{iconid}|\n"

    def add_banner_image(self, filepath: str):
        self.dialog += rf"add_image_button|banner|{filepath}|noflags|||\n"

    def add_custom(self, raw: str):
        self.dialog += rf"{raw}"

    def __str__(self):
        return self.dialog
