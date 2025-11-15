import feedparser
from strands import Agent, tool
from dotenv import load_dotenv

load_dotenv()

#ツールを定義
@tool
def get_aws_update(service_name: str) -> list:
    # AWS What's NewのRSSフィードURLをパース
    feed = feedparser.parse("https://aws.amazon.com/about-aws/whats-new/recent/feed/")
    result = []

    # フィードの各エントリをチェック
    for entry in feed.entries:
        print(f"entry:{entry.title}")
        if service_name.lower() in entry.title.lower():
            result.append({
                "published": entry.get("published", "N/A"),
                "summary": entry.get("summary", "")
            })

            # 最大3件まで取得
            if len(result) >= 3:
                break

    return result

# エージェントを作成
agent = Agent("us.anthropic.claude-3-7-sonnet-20250219-v1:0", tools=[get_aws_update])

# ユーザー入力を取得
service_name = input("アップデートを知りたいAWSサービス名を入力してください: ").strip()

# プロンプトを指定してエージェントを起動
prompt = f"AWSの{service_name}の最新アップデートを、日付付きで要約して。"
response = agent(prompt)

