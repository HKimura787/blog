# Pythonインタプリンタのパスを取得する
$is_python = Get-Command python -ErrorAction SilentlyContinue

if ($is_python -eq $null) {
    echo "Python is not installed. Installing Python..."
    # すべてのユーザーにインストールしない、パスを追加する、テストを含めない
    ./python-3.11.0-amd64.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    echo "Python has been installed."
}else{
    echo "Python is already installed."
}

# pythonのパス
$PYTHON = '\AppData\Local\Programs\Python\Python311\python.exe'

# 現在のディレクトリを表示する
echo "Current directory: $PWD"

#  NumPyをインストールする
echo "Installing NumPy..."
# echo '$python_path'
& $HOME$PYTHON