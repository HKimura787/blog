$VENV_PATH = $HOME + '\venv\dev311'

# if the virtual environment exists, exit
if (Test-Path $VENV_PATH) {
    Write-Host "Virtual environment already exists at $VENV_PATH"
    exit
}

# if return some error, retry to create a virtual environment
try {
    & $HOME\AppData\Local\Programs\Python\Python311\python.exe -m venv $VENV_PATH
}
catch {
    $PYTHON_VERSION = Python --version
    Write-Host "Virtual environment was created with $PYTHON_VERSION"
    Python -m venv $VENV_PATH
}

& $VENV_PATH\Scripts\python.exe -m pip install --upgrade pip
# & $VENV_PATH\Scripts\pip.exe install --upgrade pip
& $VENV_PATH\Scripts\pip.exe install -r requirements.txt