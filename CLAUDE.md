# CLAUDE.md — Compositional Active Inference

本リポジトリは「応用圏論（discopy ベースの string diagram）」と「能動的推論（pyAgrum + jax/optax による変分自由エネルギー最適化）」を統合するプロジェクトである。Claude（および任意の AI コーディングアシスタント）が変更を提案・実行する際は、以下の開発ルールを必ず遵守すること。

## 1. エディタ前提：Cursor の Diff ビューに最適化された粒度で変更する

- 開発者は Cursor を使用しており、変更提案は常に **Diff ビューで一目で確認・採否できる粒度** で行うこと。
- 1 つの提案に「無関係な複数ファイルの大改修」を混ぜない。1 トピック ＝ 1 まとまりの diff。
- 既存行の whitespace 変更や import 並べ替えなどの**ノイズ diff** を新機能の diff に混入させない。

## 2. パッケージ管理とスクリプト実行は常に `uv`

- 依存追加: `uv add <pkg>`（バージョン制約は `pyproject.toml` 経由で管理）。
- 環境同期: `uv sync`。
- スクリプト実行: `uv run python ...` / `uv run pytest ...`。
- **`pip` および `conda` は本プロジェクトで一切使用してはならない**。`pip install`、`conda install`、`pip-tools`、`poetry` などの併用は禁止。仮想環境は `.venv/`（uv 管理）以外を作らない。

## 3. テストは `uv run pytest tests/`：圏論的モジュールの「合成可能性」を証明する

- 全テストは `tests/` 配下に配置し、コマンドは `uv run pytest tests/` で実行する。
- `src/categories/`、`src/lenses/`、`src/dynamics/`、`src/cosmology/` の各モジュールに対するテストは、単なる関数の入出力チェックを超えて、**圏論的な合成可能性**（例: `f ∘ g` の型整合、関手の `F(g ∘ f) == F(g) ∘ F(f)`、レンズの `put ∘ get` 則、モナド則等）を property-based に検証するアサーションを必ず含めること。
- 新規モジュールを追加した場合は、対応する合成則テストを同じ PR 内で追加する。

## 4. CI（GitHub Actions）green を完了条件にする

- 本リポジトリのソースオブトゥルースは GitHub Actions の CI 結果である。
- ローカルでの変更後は、**push する前に必ずローカルで `uv run pytest tests/` を実行して green を確認** すること。
- CI（`.github/workflows/ci.yml`）が赤になった場合、エラーログを読み、**自律的に原因を特定して修正コミットを追加し、CI を再実行して green を確認するまでがタスク完了**。「ローカルでは通った」「依存解決が不安定」等の理由で赤のまま完了報告してはならない。
- 隠れ依存・transitive 依存が原因の `ModuleNotFoundError` が出た場合、最初に見つかった 1 つを直しただけで完了とせず、**潜在する他の隠れ依存を追跡してまとめて解決する**（単一 CI 失敗を「最初の症状」と扱う方針）。

## 5. 機密情報・ローカル設定はコミットしない

- 以下は `.gitignore` で除外済みである。**意図的に強制 add してコミットしてはならない**。
  - `.env`（API キー、シークレット等）
  - `.claude/settings.local.json`（Claude Code のローカル設定）
  - `data/`（ローカル実験データ）
  - `.venv/`（uv 管理の仮想環境）
- 万一上記のいずれかをステージしてしまった場合は、`git rm --cached` で外し、コミット前に必ず差分を目視確認すること。`git add -A` / `git add .` は秘匿物巻き込みリスクがあるため、可能な限り具体的なパスを指定して add する。

---

上記 5 条のいずれかに反する変更は、**Cursor の Diff ビューで採否される前に Claude 側で自己却下** すること。
