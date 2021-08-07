from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout


# actual gui part
# init section
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Double Blink'))
layout.addWidget(QPushButton('triple blink'))

window.setLayout(layout)
window.show()

# label = QLabel('blink tracker app')
# label.show()
app.exec()
