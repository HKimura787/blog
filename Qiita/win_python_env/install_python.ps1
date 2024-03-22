# Pythonインタプリンタのパスを取得する
$is_python = Get-Command python -ErrorAction SilentlyContinue

if ($is_python -eq $null) {
    echo "Python is not installed. Installing Python..."
    # すべてのユーザーにインストールしない、パスを追加する、テストを含めない
    ./python-3.11.0-amd64.exe /quiet InstallAllUsers=0 PrependPath=0 Include_test=0
    echo "Python has been installed."
}else{
    echo "Python is already installed."
}

# pythonのパス
$PYTHON_RELATIVE = '\AppData\Local\Programs\Python\Python311'
# 相対パスを絶対パスに変換する
$PYTHON_DIR = $HOME + $PYTHON_RELATIVE

# PythonのPathを通す
echo "Python path: $PYTHON_DIR"
Set-Item Env:Path $Env:Path";"$PYTHON_DIR
[Environment]::SetEnvironmentVariable("Path", $Env:Path, [System.EnvironmentVariableTarget]::Machine)

#  NumPyをインストールする
echo "Installing NumPy..."
# echo '$python_path'
python -m pip install numpy