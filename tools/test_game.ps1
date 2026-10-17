param([int]$Idx, [string]$Tag="g", [int[]]$Shots=@(25,40,55,75), [string]$Extra="-8pwander")
# Plays one minigame (Globals.MinigameIdentifier index) with 8 bots, screenshots at the given seconds.
# Needs `um` (https://github.com/rehan-remade/universal-modder) for window focus/screenshots.
$root = Split-Path $PSScriptRoot
$env:PYTHONUTF8="1"; $env:PATH="$env:USERPROFILE\.local\bin;$env:PATH"
& (Join-Path $PSScriptRoot "run_test.ps1") -ExtraArgs "-8pautolobby -8pdebug -8pauto $Extra -8pgame=$Idx" -Wait 32 | Out-Null
um win drive --proc "Machine Party" "focus" "key 0x77" | Out-Null
Start-Sleep 3
um win drive --proc "Machine Party" "key 0x78" | Out-Null
$t0 = Get-Date
foreach ($s in $Shots) {
  $wait = $s - ((Get-Date) - $t0).TotalSeconds
  if ($wait -gt 0) { Start-Sleep -Seconds $wait }
  um win shot --exe "Machine Party.exe" (Join-Path $root "shots\${Tag}${Idx}_t$s.png") --scale 0.5 | Out-Null
}
Select-String -Path (Join-Path $root "shots\godot.log") -Pattern "SCRIPT ERROR|Parse Error" -Context 0,2 | Select-Object -First 8 | ForEach-Object { $_.Line; $_.Context.PostContext }
