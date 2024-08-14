source ../../.venv/Scripts/activate
python -m nuitka --standalone --mingw64 \
--windows-console-mode=disable \
--output-dir=../../out \
--show-progress \
--enable-plugin=pyside6 \
../../app/FluentMaa.py