import fitz
import openpyxl

doc = fitz.open('/Users/tsudzukitaiga/Desktop/python_lesson/サンプル請求書.pdf')

page = doc[0]

text = page.get_text()

# print(text)

words = ['hellow','world']

text = ' '.join(words)

print(text)

wb = openpyxl.Workbook()
ws = wb.active

ws.append(['名前','年齢','都市'])
ws.append(['大河',29,'東京'])

excel_path = 'example.xlsx'
wb.save(excel_path)