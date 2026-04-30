# Craftgnosis 公式ウェブサイト

株式会社Craftgnosis の公式HPソースコードです。

## ページ構成

| パス | 内容 |
|------|------|
| `/` | トップページ |
| `/about/` | 会社概要 |
| `/services/` | サービス |
| `/news/` | ニュース |
| `/seminar/` | フィジカルAI入門セミナー |
| `/contact/` | お問い合わせ |

## 技術構成

- 純粋なHTML / CSS / JavaScript（フレームワーク不使用）
- Google Fonts（Noto Serif JP / Noto Sans JP / DM Serif Display）
- 共通スタイル: `assets/css/common.css`
- 共通スクリプト: `assets/js/common.js`

## ローカルでの確認方法

ブラウザで `index.html` を直接開くか、簡易サーバーを起動してください。

```bash
# Python 3 の場合
python -m http.server 8000
```

## お問い合わせフォームの設定

`contact/index.html` の `<form action="...">` の URL を Formspree 等の実際のエンドポイントに変更してください。

## セミナー申込みフォームの設定

`seminar/index.html` の `https://forms.gle/XXXXXXXXXXXXXXXXXX` を実際の Google フォームの URL に変更してください。

---

© 2026 Craftgnosis, Inc.
