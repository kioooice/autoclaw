Set wps = CreateObject("Kwps.Application")
wps.Visible = False

htmlPath = "C:\Users\Administrator\Desktop\openclaw应用.html"
docxPath = "C:\Users\Administrator\Desktop\openclaw应用.docx"

Set doc = wps.Documents.Open(htmlPath)
doc.SaveAs2 docxPath, 16
doc.Close

wps.Quit

Set doc = Nothing
Set wps = Nothing

WScript.Echo "转换完成！"
