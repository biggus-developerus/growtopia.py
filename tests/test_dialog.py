"""Test the Dialog class."""

from growtopia import Dialog


def test_dialog() -> None:
    """Hello Dialog"""

    hello = Dialog()

    hello.add_textbox("Hello Player!")
    hello.add_checkbox("test_checkbox", "Do you want to play?", False)
    hello.add_ending("test_dialog", "Back", "Enter")

    assert (
        hello.dialog
        == "add_textbox|Hello Player!|left|\nadd_checkbox|test_checkbox|Do you want to play?|0|\nend_dialog|test_dialog|Back|Enter|\n"
    )


if __name__ == "__main__":
    test_dialog()
