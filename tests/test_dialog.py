from growtopia import Dialog

hello = Dialog()
hello.add_textbox("Hello Player!")
hello.add_checkbox("test_checkbox", "Do you want to play?", False)
hello.add_ending("test_dialog", "Back", "Enter")
print(hello) # add_textbox|Hello Player!|left|\nadd_checkbox|test_checkbox|Do you want to play?|0|\nend_dialog|test_dialog|Back|Enter|\n