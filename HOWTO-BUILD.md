### 前提

1. https://www.python.org/downloads/ にある最新のPythonがインストールされていること。  
  インストール時、オプションの`Add python.exe to PATH`はオンにする。
1. OBS Studioがインストールされていること（起動は不要）。
2. `C:\Users\$env:username\workspace\mekakushi` を作業フォルダとする。  
   （変更する場合は適宜読み替えること）

## 開発開始時 (初回)

PowerShellターミナルを開き、以下を実行する。

```PowerShell
$ENV:http_proxy="http://proxy.yourcompany.co.jp:8080" ※必要な場合(適宜読み替え)
$ENV:https_proxy="http://proxy.yourcompany.co.jp:8080" ※必要な場合(適宜読み替え)
cd C:\Users\$env:username\workspace\mekakushi
python -m venv .venv
& .venv/Scripts/Activate.ps1
pip3 install -r requirements.txt
pip3 install pyinstaller
python -m pip install --upgrade pip
(コード修正)
python .\mekakushi.py --cam=0
※「q」で終了
deactivate
exit
```

## 開発継続時 (次回)

PowerShellターミナルを開き、以下を実行する。

```PowerShell
cd C:\Users\$env:username\workspace\mekakushi
& .venv/Scripts/Activate.ps1
(コード修正)
python .\mekakushi.py --cam=0
※「q」で終了
deactivate
exit
```

## EXEファイル作成時 (オプション)

PowerShellを開き、以下を実行する。  

```PowerShell
cd C:\Users\$env:username\workspace\mekakushi
& .venv/Scripts/Activate.ps1
pyinstaller .\mekakushi.spec --noconfirm
deactivate
exit
```

`dist`ディレクトリ配下にEXEファイル（mekakushi.exe）が生成される。
