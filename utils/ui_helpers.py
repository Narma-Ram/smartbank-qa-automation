def click_element(element):
    element.click()

def fill_input(element, value):
    element.fill(value)

def handle_dialog(dialog, expected_message, accept=True):
    assert dialog.message == expected_message

    if accept:
        dialog.accept()
    else:
        dialog.dismiss()

def wait_for_element(element):
    element.wait_for()