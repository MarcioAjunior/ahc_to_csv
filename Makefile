SCRIPT = ahc_to_csv.py

EXEC = ahc_to_csv.exe

build:
	pyinstaller --onefile $(SCRIPT)


all: build
