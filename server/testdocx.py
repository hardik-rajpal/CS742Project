from docx import Document
doc = Document('test.docx')
paras = doc.paragraphs
print(len(paras))