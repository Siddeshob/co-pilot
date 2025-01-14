import PyPDF2
import pandas as pd
import json
import docx
import openpyxl

def read_file_content(filepath, file_ext):
    """
    Read and process different file types
    
    Args:
        filepath (str): Path to the file
        file_ext (str): File extension (e.g., '.pdf', '.txt')
        
    Returns:
        dict: Processed content and metadata
    """
    try:
        # PDF Processing
        if file_ext == '.pdf':
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                content = ""
                metadata = pdf_reader.metadata
                total_pages = len(pdf_reader.pages)
                
                for page in pdf_reader.pages:
                    content += page.extract_text()
                    
                return {
                    'content': content,
                    'metadata': metadata,
                    'pages': total_pages,
                    'type': 'pdf'
                }
        
        # Text File Processing
        elif file_ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                lines = len(content.splitlines())
                words = len(content.split())
                
                return {
                    'content': content,
                    'lines': lines,
                    'words': words,
                    'type': 'text'
                }
        
        # CSV Processing
        elif file_ext == '.csv':
            df = pd.read_csv(filepath)
            return {
                'content': df.to_dict(),
                'rows': len(df),
                'columns': list(df.columns),
                'type': 'csv'
            }
        
        # Excel Processing
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
            return {
                'content': df.to_dict(),
                'sheets': len(pd.ExcelFile(filepath).sheet_names),
                'rows': len(df),
                'columns': list(df.columns),
                'type': 'excel'
            }
        
        # JSON Processing
        elif file_ext == '.json':
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return {
                    'content': data,
                    'type': 'json'
                }
        
        else:
            return {
                'error': 'Unsupported file type',
                'type': file_ext
            }
            
    except Exception as e:
        return {
            'error': str(e),
            'type': 'error'
        }