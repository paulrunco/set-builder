pyinstaller --clean --onefile --windowed ^
    --distpath="dist/" ^
    --icon="icon.ico" ^
    --name="Set Builder Utility" ^
    --add-data="icon.ico";. ^
    app.py