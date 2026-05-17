# VR AI Russian Girlfriend & Self-Regulating VTuber

このプロジェクトは、AIによる自律的な感情制御（Self-Regulation）と、高度なセキュリティ機能（プロンプトインジェクション対策、認証、出力フィルタリング）を備えたVR対応のVTuberシステムです。「ロシア人白人の彼女」という固有のペルソナ（アーニャ）を持っています。

## 特徴 (Features)

- **AI Core (LangChain/FastAPI):** 彼女としてのペルソナを維持しながら応答を生成。
- **Self-Regulation (自己制御システム):** 機嫌(mood)や親密度(intimacy)といった内部ステータスを管理し、AIの極端な暴走を防ぎます。
- **Security Layer (セキュリティ層):**
  - ユーザー認証: 指定されたマスター（Master）からのアクセスのみを許可します。
  - 入力サニタイズ: システムプロンプトの抽出やキャラクター崩壊を狙うプロンプトインジェクションを検知・ブロックします。
  - 出力フィルタリング: AIがメタ発言（「AIとして〜」など）をした場合、出力を安全なものに置き換えます。
- **WebXR Frontend (Three.js/VRM):** WebブラウザからVRヘッドセットで直接アクセス可能。AIの感情状態に応じて3Dモデル（VRM）の表情が自動的に変化します。

## 構成 (Architecture)

- `/backend/`
  - `app.py`: FastAPIによるAPIサーバーのメインスクリプト
  - `ai_core.py`: LLM（言語モデル）へのプロンプト生成と応答処理
  - `security.py`: セキュリティフィルタリング（入力/出力/認証）
  - `self_regulation.py`: 感情ステートマシン
  - `requirements.txt`: 必要なPythonパッケージ
- `/frontend/`
  - `index.html`: WebXRおよびThree.jsの表示用UI
  - `app.js`: 3Dモデル（VRM）の読み込み、API通信、アニメーション制御

## セットアップと起動 (Setup & Run)

### 1. バックエンドの起動

```bash
cd backend
pip install -r requirements.txt
python app.py
```
バックエンドは `http://localhost:8000` で起動します。

### 2. フロントエンドの起動

フロントエンドは静的なHTML/JSファイルです。VSCodeのLive ServerなどのローカルWebサーバーを使用して `/frontend/index.html` を開いてください。
（例: Python 3を使用する場合）

```bash
cd frontend
python -m http.server 3000
```
ブラウザで `http://localhost:3000` にアクセスします。

※ WebXR（VR）を使用する場合は、HTTPS接続環境、または localhost でMeta Questのブラウザ等からアクセスする必要があります。

## セキュリティの仕組みについて

本システムは、AIが常に「彼女」として振る舞うことを保証するため、`app.py`のエンドポイント内で以下の順序で処理を行っています。

1. **認証 (Authentication):** 送信元ユーザーIDを検証。
2. **入力検証 (Input Validation):** ブラックリストや正規表現を用いて悪意あるプロンプトを遮断。
3. **状態評価 (State Evaluation):** 入力に基づいて自己制御システムが現在の機嫌を更新。
4. **応答生成 (Generation):** 安全が確認された状態とプロンプトでAIが回答を生成。
5. **出力フィルタ (Output Filter):** 生成結果にメタ発言が含まれていないか最終確認。
6. **振る舞い決定 (Behavior Check):** 回答内容と現在の機嫌から、VR上のアバターに適用する表情（BlendShape）を決定。

これにより、自律的かつ安全なAIエージェントの運用を実現しています。
