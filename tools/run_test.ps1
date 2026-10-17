param([string]$Pck="", [string]$ExtraArgs="-8pautolobby -8pdebug", [int]$Wait=30)
# Launches the game from its folder with a test pck (retail pck untouched). Env: MP_GAME_DIR
$root = Split-Path $PSScriptRoot
if (-not $Pck) { $Pck = Join-Path $root "dist\test.pck" }
$gameDir = if ($env:MP_GAME_DIR) { $env:MP_GAME_DIR } else { "C:\games\videogames\Machine_Party" }
$env:PYTHONUTF8="1"; $env:PATH="$env:USERPROFILE\.local\bin;$env:PATH"
Get-Process "Machine Party" -ErrorAction SilentlyContinue | ForEach-Object { um win kill $_.Id | Out-Null }
Start-Sleep 2
New-Item -ItemType Directory -Force (Join-Path $root "shots") | Out-Null
$a = @('--main-pack',$Pck,'--windowed','--resolution','1920x1080','--log-file',(Join-Path $root "shots\godot.log"),'--') + ($ExtraArgs -split ' ')
Start-Process -FilePath (Join-Path $gameDir "Machine Party.exe") -WorkingDirectory $gameDir -ArgumentList $a | Out-Null
Start-Sleep $Wait
"started"
