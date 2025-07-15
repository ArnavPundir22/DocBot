# typing_effect.py

from PyQt5.QtCore import QTimer

def type_text_effect(text_widget, full_text, interval=30):
    text_widget.clear()
    index = [0]

    def update_text():
        if index[0] < len(full_text):
            text_widget.insertPlainText(full_text[index[0]])
            index[0] += 1
        else:
            timer.stop()

    timer = QTimer()
    timer.timeout.connect(update_text)
    timer.start(interval)
