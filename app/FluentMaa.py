import os
import sys

from PySide6.QtCore import Qt, QTranslator
from PySide6.QtWidgets import QApplication

from app.common import windows_manager
from app.common.config import cfg
from app.view.main_window import MainWindow
from qfluentwidgets import FluentTranslator

if cfg.get(cfg.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
    app.setStyle("fusion")

locale = cfg.get(cfg.language).value
translator = FluentTranslator(locale)
galleryTranslator = QTranslator()
galleryTranslator.load(locale, "maa", ".", ":/i18n")

app.installTranslator(translator)
app.installTranslator(galleryTranslator)

w = MainWindow()
w.show()

windows_manager.main_window = w

app.exec()
