import os
from google import genai
from google.genai import types

# --- 設定エリア ---
# macOSの環境変数からAPIキーを読み込みます
API_KEY = os.environ.get('GEMINI_API_KEY')

def get_latest_news():
    # 1. キーがちゃんと設定されているかチェック
    if not API_KEY:
        print("【エラー】環境変数 'GEMINI_API_KEY' が見つかりません。")
        print("ターミナルで 'echo $GEMINI_API_KEY' を実行して表示されるか確認してください。")
        return

    # 2. Geminiを使うための準備（クライアント作成）
    client = genai.Client(api_key=API_KEY)

    # 3. 実行者にニュースのテーマを入力してもらう
    print("=== 世界のAI/ITニュース検索（Gemini版） ===")
    user_input = input("気になるキーワードを入力してください（例：最新のAI、半導体など）\n> ")

    # 4. Geminiへの「お願い（プロンプト）」を組み立てる
    prompt = f"""
    Google検索を使って、以下のキーワードに関する最新のニュースを3件探してください。
    キーワード: {user_input}

    各ニュースについて、以下の形式で日本語で出力してください。
    【見出し】（記事のタイトル）
    【内容】（2行程度で、何がすごいニュースなのかを中学生でもわかるように要約）
    【リンク】（ニュース記事のURL）
    """

    print(f"\n「{user_input}」の最新情報を世界中から探しています。少しお待ちください...\n")

    try:
        # 5. Geminiに「検索機能付き」で回答を生成してもらう
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                # Google検索を道具（ツール）として使う設定
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )

        # 6. 結果を画面（コマンドプロンプト/ターミナル）に表示
        print("=" * 60)
        if response.text:
            print(response.text)
        else:
            print("ニュースが見つかりませんでした。キーワードを変えて試してみてください。")
        print("=" * 60)

    except Exception as e:
        print(f"【実行エラー】トラブルが発生しました。\n内容: {e}")

# プログラムの開始地点
if __name__ == "__main__":
    get_latest_news()