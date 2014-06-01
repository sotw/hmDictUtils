'************************************************************
'* Modifying The System Path With New Entries *
'************************************************************
Dim ExistingPath, NewPath
Set argv = WScript.Arguments
myPath=argv(0)
Set oShell = WScript.CreateObject("WScript.Shell")
Set oEnv = oShell.Environment("SYSTEM")

'************************************************************
'* Add your Path Entry Here *
'************************************************************
ExistingPath = oEnv("PATH")
NewPath = ExistingPath & ";" & myPath
oEnv("PATH") = NewPath 'WRITE NEW PATH, INCLUDING OLD ONE