# Build Instructions  

The scripts build python project by Nuitka, please make sure that you have installed latest nuitka in venv  
Please build on Windows (other platforms haven't been tested)  
If you come to the exception like:  
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc1 in position xxx: invalid start byte  
Here is a temporary solution: (Nuitka's developer said it will be repaired next version)

- Open .venv\Lib\site-packages\nuitka\build\SconsCaching.py
- Find line: (line 282 in nuitka 2.4.5)

```
        for line in getFileContentByLine(ccache_logfile, encoding="utf8"):
```

- Delete ' , encoding="utf8" ', now it looks like:  

```
        for line in getFileContentByLine(ccache_logfile):
```

- Don't forget to save.

If you're using PyCharm or terminal, you can use commands below:  

```shell
./.venv/Scripts/activate
python -m nuitka --standalone --mingw64 --windows-console-mode=disable --output-dir=out --show-progress --enable-plugin=pyside6 app/FluentMaa.py
```

or run this if you want build onefile:

```shell
./.venv/Scripts/activate
python -m nuitka --standalone --onefile --mingw64 --windows-console-mode=disable --output-dir=out/onefile --show-progress --enable-plugin=pyside6 app/FluentMaa.py
```

(However, onefile is not recommended because it is prone to false alarms by antivirus software)
