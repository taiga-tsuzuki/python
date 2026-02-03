# 必要なライブラリをインポートします。
import os
import fitz  # PyMuPDFをインポートしてPDFファイルを操作します。
import openpyxl  # openpyxlをインポートしてExcelファイルを操作します。

# PDFファイルから情報を抽出する関数を定義します。
def extract_information_from_pdf(pdf_path, filename):
    """PDFファイルから特定のキーワードに続くテキストを抽出する"""
    # PDFファイルを開きます。
    doc = fitz.open(pdf_path)
    # 抽出する情報を格納する辞書を初期化します。
    extracted_data = {
        "ファイル名": filename.replace('.pdf', ''),  # ファイル名から.pdfを除去して格納します。
        "件名": "",
        "請求日": "",
        "請求金額": "",
        "お支払い期限": "",
        "振込先": ""
    }

    # PDFの各ページを順に処理します。
    for page in doc:
        # ページからテキストを抽出します。
        text = page.get_text()
        # 抽出したテキストを改行で分割します。
        lines = text.split('\n')
        # 分割した各行を順に処理します。
        for i, line in enumerate(lines):
            # 特定のキーワードに基づいて情報を抽出し、辞書に格納します。
            # 以下、特定の条件にマッチする行から情報を抽出しています。
            if 'ご請求金額' in line and i+1 < len(lines):
                extracted_data["請求金額"] = ''.join(filter(str.isdigit, lines[i+1].strip()))
            elif 'お支払い期限' in line and i+1 < len(lines):
                extracted_data["お支払い期限"] = lines[i+1].strip()
            elif '振込先' in line:
                transfer_info = lines[i+1].strip() if i+1 < len(lines) else ''
                transfer_info += ' ' + lines[i+2].strip() if i+2 < len(lines) else ''
                extracted_data["振込先"] = transfer_info
            elif '件名' in line and i+1 < len(lines):
                extracted_data["件名"] = lines[i+1].strip()
            elif '請求日' in line:
                extracted_data["請求日"] = lines[i+1].strip()
    # 抽出した情報を含む辞書を返します。
    return extracted_data

# 抽出した情報をExcelファイルに書き出す関数を定義します。
def write_information_to_excel(all_extracted_data, excel_path):
    """抽出した情報をExcelファイルに書き出す"""
    # 新しいワークブックを作成します。
    wb = openpyxl.Workbook()
    # アクティブなワークシートを取得します。
    ws = wb.active
    # ヘッダー行を追加します。
    ws.append(["ファイル名", "件名", "請求日", "請求金額", "お支払い期限", "振込先"])
    # 抽出した各データをExcelに追加します。
    for data in all_extracted_data:
        ws.append([
            data["ファイル名"],
            data["件名"],
            data["請求日"],
            data["請求金額"],
            data["お支払い期限"],
            data["振込先"]
        ])
    # ワークブックを指定したパスに保存します。
    wb.save(excel_path)

# 処理対象のPDFファイルが存在するディレクトリとExcelファイルのパスを設定します。
directory_path = '/Users/tsudzukitaiga/Desktop/python_lesson'
excel_path = '/Users/tsudzukitaiga/Desktop/python_lesson/サンプル出力先.xlsx'
# 抽出した情報を格納するリストを初期化します。
all_extracted_data = []

# 指定したディレクトリ内の全PDFファイルを処理します。
for filename in os.listdir(directory_path):
    if filename.endswith('.pdf'):
        # PDFファイルのフルパスを生成します。
        pdf_path = os.path.join(directory_path, filename)
        # PDFから情報を抽出します。
        extracted_data = extract_information_from_pdf(pdf_path, filename)
        # 抽出したデータをリストに追加します。
        all_extracted_data.append(extracted_data)

# 抽出した情報をExcelに書き出します。
write_information_to_excel(all_extracted_data, excel_path)

# 処理の完了を通知します。
print("情報の抽出とExcelへの書き出しが完了しました。")