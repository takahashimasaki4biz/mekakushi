### 前提

OBS Studioがインストールされていること（起動は不要）。

## Pythonで実行する場合

PowerShellターミナルを開き、以下を実行する。

```PowerShell
cd C:\Users\$env:username\workspace\mekakushi
& .venv/Scripts/Activate.ps1
python .\mekakushi.py --cam=0
```

teamsやzoomを使用する。カメラには「OBS Virtual Camel」を選択する。

```PowerShell
※「q」で終了
deactivate
exit
```

## EXEファイルを実行する場合

mekakushi.exeをダブルクリックする（0番目のカメラが使用される）。
又はmekakushi.exeへのショートカットを作成し、引数として `--cam=1` 等を追加する。

teamsやzoomを使用する。カメラには「OBS Virtual Camel」を選択する。

「q」で終了
