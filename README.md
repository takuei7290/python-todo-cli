# python-todo-cli

コマンドラインでタスクを管理するシンプルなToDoツールです。
Pythonの基礎、テスト、Git/GitHubのブランチ運用を学ぶために作成しました。

## 機能

- **追加 (add)**: タスクを新規登録する
- **一覧 (list)**: 全タスクを表示する(完了/未完了を表示して区別)
- **完了 (done)**: idを指定してタスクを完了状態にする(一覧からは消えない)
- **削除 (delete)**: idを指定してタスクを削除する

## 必要環境

- Python 3.12(動作確認済みバージョン)
- 本体は標準ライブラリのみで動作します(外部パッケージはテスト・開発用)

## セットアップ

```bash
git clone https://github.com/takuei7290/python-todo-cli.git
cd python-todo-cli

# 仮想環境を作成して有効化
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 開発用パッケージをインストール
pip install -r requirements.txt
```

## 使い方

```bash
# タスクを追加
python todo.py add 牛乳を買う
# => 追加しました

# 一覧を表示
python todo.py list
# => 1. 牛乳を買う [未完了]

# 完了にする
python todo.py done 1
# => 完了にしました

# 削除する
python todo.py delete 1
# => 削除しました

# ヘルプを表示
python todo.py --help
```

## データの保存形式

タスクは実行したディレクトリの `tasks.json` に保存され、プログラム終了後も保持されます。
各タスクは以下の項目を持ちます。

| 項目 | 内容 |
|---|---|
| `id` | 自動採番される番号 |
| `content` | タスクの内容 |
| `done` | 完了フラグ(初期値: `false`) |
| `created_at` | 作成日時 |

## テスト・開発

```bash
# テストを実行
pytest

# lint / フォーマットチェック
ruff check .
ruff format --check .
```

## 設計のポイント

- **argparseによるサブコマンド構成**: 引数不足や未知のコマンドのエラー処理・ヘルプ表示をargparseに任せ、自前の分岐を減らした
- **テストしやすい関数分割**: 各コマンドを関数に分け、保存先ファイル名を引数で差し替えられるようにして、本番の `tasks.json` を汚さずにテストできるようにした
- **パーサー構築の関数化**: `build_parser()` に切り出し、CLI引数の解釈もテストで検証している
- **壊れたデータへの対応**: `tasks.json` が壊れている・形式が違う場合も、クラッシュせずにメッセージを出して終了する
- **ブランチ運用**: 機能単位でブランチを切り、Pull Request経由でmainにマージしている
