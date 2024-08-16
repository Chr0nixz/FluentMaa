import os
import sys

from PySide6.QtCore import Qt, QTranslator
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.common.config import cfg
from app.view.main_window import MainWindow

if cfg.get(cfg.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
    app.setStyle("fusion")

locale = cfg.get(cfg.language).value
translator = FluentTranslator(locale)
maaTranslator = QTranslator()
maaTranslator.load(locale, "maa", ".", ":/i18n")

app.installTranslator(translator)
app.installTranslator(maaTranslator)

w = MainWindow()
w.show()

app.exec()
