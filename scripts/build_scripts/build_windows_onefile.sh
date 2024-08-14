source ../../.venv/Scripts/activate
python -m nuitka --standalone --onefile --mingw64 \
--windows-disable-console \
--output-dir=../../out/onefile \
--show-progress \
--enable-plugin=pyside6 \
../../app/FluentMaa.py