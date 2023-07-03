"""Test the Dialog class."""

from growtopia import Dialog, DialogElement


def test_dialog() -> None:
    """Hello Dialog"""

    hello = Dialog("test_dialog")

    hello.add_elements(
        DialogElement.textbox("Hello Player!"),
        DialogElement.checkbox("test_checkbox", "Do you want to play?", False),
        DialogElement.ending("test_dialog", "Back", "Enter"),
    )

    assert (
        hello.dialog
        == "add_textbox|Hello Player!|left|\nadd_checkbox|test_checkbox|Do you want to play?|0|\nend_dialog|test_dialog|Back|Enter"
    )


if __name__ == "__main__":
    test_dialog()
