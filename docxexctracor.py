from docx import Document

def text_extracor_docx(file_path):
    docx_file = Document(file_path)
    docx_text = ''.join([p.text for p in docx_file.paragraphs])

    return docx_text 
  
  