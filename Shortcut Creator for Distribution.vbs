Option Explicit

Dim fso, shell, folderPath, launcherPath, iconPath, shortcutPath, shortcut

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

folderPath = fso.GetParentFolderName(WScript.ScriptFullName)
launcherPath = fso.BuildPath(folderPath, "Cer3erusI2PNG.bat")
iconPath = fso.BuildPath(folderPath, "cer3erus_i2png_icon.ico")
shortcutPath = fso.BuildPath(folderPath, "Cer3erusI2PNG.lnk")

If Not fso.FileExists(launcherPath) Then
    MsgBox "Required launcher was not found:" & vbCrLf & launcherPath, vbCritical, "Shortcut Creator for Distribution"
    WScript.Quit 1
End If

If Not fso.FileExists(iconPath) Then
    MsgBox "Required application icon was not found:" & vbCrLf & iconPath, vbCritical, "Shortcut Creator for Distribution"
    WScript.Quit 1
End If

Set shortcut = shell.CreateShortcut(shortcutPath)
shortcut.TargetPath = launcherPath
shortcut.Arguments = "%1"
shortcut.WorkingDirectory = folderPath
shortcut.IconLocation = iconPath & ",0"
shortcut.Description = "Cer3erusI2PNG - Drag and drop images here to convert them to PNG"
shortcut.Save

shell.Popup "Shortcut created for this folder:" & vbCrLf & folderPath & vbCrLf & vbCrLf & _
            "Copy Cer3erusI2PNG.lnk to your Desktop. If you move this folder, run this script again.", _
            7, "Shortcut Creator for Distribution", vbInformation
