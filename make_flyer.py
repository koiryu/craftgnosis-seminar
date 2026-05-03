# -*- coding: utf-8 -*-
"""
Craftgnosis セミナーチラシ生成スクリプト (v2)
A4横 (841.89 x 595.28 pt)
"""

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from PIL import Image as PILImage
import os

# ── フォント登録 ──────────────────────────────────────────
pdfmetrics.registerFont(TTFont('YuGothR', 'C:/Windows/Fonts/YuGothL.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('YuGothM', 'C:/Windows/Fonts/YuGothM.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('YuGothB', 'C:/Windows/Fonts/YuGothB.ttc', subfontIndex=0))

# ── カラーパレット ─────────────────────────────────────────
STEEL      = HexColor('#3a4a5c')
STEEL_LT   = HexColor('#4e6278')
RUST       = HexColor('#b84c2b')
RUST_LT    = HexColor('#d9603a')
CREAM      = HexColor('#f5f2ec')
CREAM_DK   = HexColor('#e8e4da')
INK        = HexColor('#0f0e0c')
MUTED      = HexColor('#7a7367')
LINE       = HexColor('#d8d4cc')
WHITE      = white

# ── ページサイズ ───────────────────────────────────────────
W, H = landscape(A4)   # 841.89 x 595.28 pt
LEFT_W  = 265          # 左パネル幅
PAD     = 20           # 左右パディング

# ── パス ─────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT   = os.path.join(BASE_DIR, 'craftgnosis_seminar_flyer.pdf')
PHOTO    = os.path.join(BASE_DIR, 'assets', 'images', 'tsuji.jpg')


def draw_tag_border(c, x, y, text, font, size, text_color, border_color):
    """枠線タグ（返値：タグ幅）"""
    c.setFont(font, size)
    tw = c.stringWidth(text, font, size)
    px, py = 7, 3
    c.setStrokeColor(border_color)
    c.setLineWidth(0.7)
    c.setFillColor(HexColor('#00000000'))
    c.rect(x, y - py, tw + px * 2, size + py * 2, fill=0, stroke=1)
    c.setFillColor(text_color)
    c.drawString(x + px, y, text)
    return tw + px * 2


def draw_section_label(c, x, y, text, font='YuGothR', size=7):
    """セクションラベル（RUST色・右に線）"""
    c.setFont(font, size)
    c.setFillColor(RUST)
    c.drawString(x, y, text)
    tw = c.stringWidth(text, font, size)
    c.setStrokeColor(RUST)
    c.setLineWidth(0.5)
    c.line(x + tw + 6, y + size * 0.4, x + tw + 60, y + size * 0.4)


def wrap_draw(c, text, x, y, max_w, font, size, color, leading=None):
    """折り返しテキスト描画。最終行のY座標を返す"""
    if leading is None:
        leading = size * 1.65
    c.setFont(font, size)
    c.setFillColor(color)
    line = ''
    cur_y = y
    for ch in text:
        test = line + ch
        if c.stringWidth(test, font, size) > max_w:
            c.drawString(x, cur_y, line)
            cur_y -= leading
            line = ch
        else:
            line = test
    if line:
        c.drawString(x, cur_y, line)
    return cur_y - leading


def make_flyer():
    c = canvas.Canvas(OUTPUT, pagesize=landscape(A4))
    c.setTitle('Physical AI Seminar 2026 Flyer')

    # ══════════════════════════════════════════════════════
    # 左パネル（スチール背景）
    # ══════════════════════════════════════════════════════
    c.setFillColor(STEEL)
    c.rect(0, 0, LEFT_W, H, fill=1, stroke=0)

    # 上部ラスト線
    c.setFillColor(RUST)
    c.rect(0, H - 4, LEFT_W, 4, fill=1, stroke=0)

    # ロゴ
    logo_y = H - 30
    c.setFont('YuGothB', 10.5)
    c.setFillColor(WHITE)
    c.drawString(PAD, logo_y, 'Craft')
    lw = c.stringWidth('Craft', 'YuGothB', 10.5)
    c.setFillColor(RUST_LT)
    c.drawString(PAD + lw, logo_y, 'gnosis')

    # バッジ
    badge_y = H - 56
    draw_tag_border(c, PAD, badge_y, '招待制  ·  定員30名', 'YuGothR', 7.5,
                    RUST_LT, RUST)

    # アイキャッチ
    eye_y = badge_y - 18
    c.setFont('YuGothR', 6.5)
    c.setFillColor(HexColor('#ffffff55'))
    c.drawString(PAD, eye_y, 'PHYSICAL AI SEMINAR 2026')

    # メインタイトル
    t1_y = eye_y - 17
    c.setFont('YuGothB', 16)
    c.setFillColor(WHITE)
    c.drawString(PAD, t1_y, '製造業のための')
    c.setFont('YuGothB', 22)
    c.setFillColor(RUST_LT)
    t2_y = t1_y - 27
    c.drawString(PAD, t2_y, 'フィジカルAI')
    c.setFont('YuGothB', 16)
    c.setFillColor(WHITE)
    t3_y = t2_y - 24
    c.drawString(PAD, t3_y, '入門セミナー')

    # セパレータ
    sep_y = t3_y - 18
    c.setStrokeColor(HexColor('#ffffff22'))
    c.setLineWidth(0.5)
    c.line(PAD, sep_y, LEFT_W - PAD, sep_y)

    # ── 開催情報 ──
    # (key, value_lines)
    meta = [
        ('日  時', ['2026年6月18日（木）', '13:45 〜 17:00']),
        ('会  場', ['東京都内', '（申込確定後にご案内）']),
        ('定  員', ['30名（招待制・先着順）']),
        ('参加費', ['70,000円（税別）／名']),
    ]
    KEY_W  = 42
    VAL_X  = PAD + KEY_W + 6
    row_y  = sep_y - 14

    for key, val_lines in meta:
        c.setFont('YuGothR', 6.5)
        c.setFillColor(HexColor('#ffffff66'))
        c.drawString(PAD, row_y, key)
        c.setFont('YuGothM', 8)
        c.setFillColor(WHITE)
        for i, ln in enumerate(val_lines):
            c.drawString(VAL_X, row_y - i * 10, ln)
        row_y -= 10 * len(val_lines) + 13

    # インボイス・支払い注記
    note_y = row_y
    c.setFont('YuGothR', 6.5)
    c.setFillColor(HexColor('#ffffff55'))
    c.drawString(PAD, note_y,      '※ インボイス（適格請求書）非対応')
    c.drawString(PAD, note_y - 10, '※ お支払いは2026年6月末まで')
    note_y -= 24

    # ── 対象者 ──
    c.setFont('YuGothR', 6.5)
    c.setFillColor(RUST_LT)
    c.drawString(PAD, note_y, 'こんな方におすすめ')
    note_y -= 13

    targets = [
        '- 自動化技術を持つ製造業の技術者',
        '- AI導入を検討している設備・生産技術部門',
        '- SI・ロボットシステム構築に関わる方',
    ]
    for item in targets:
        c.setFont('YuGothR', 7)
        c.setFillColor(HexColor('#ffffffaa'))
        c.drawString(PAD, note_y, item)
        note_y -= 12

    # 主催（最下部固定）
    c.setFont('YuGothR', 6)
    c.setFillColor(HexColor('#ffffff44'))
    c.drawString(PAD, 13, '主催：株式会社Craftgnosis　craftgnosis.com')

    # ══════════════════════════════════════════════════════
    # 右パネル（クリーム背景）
    # ══════════════════════════════════════════════════════
    c.setFillColor(CREAM)
    c.rect(LEFT_W, 0, W - LEFT_W, H, fill=1, stroke=0)

    # 上部ラスト線（右）
    c.setFillColor(RUST)
    c.rect(LEFT_W, H - 4, W - LEFT_W, 4, fill=1, stroke=0)

    rp_x  = LEFT_W + PAD          # 右パネル開始X
    rp_w  = W - LEFT_W - PAD * 2  # 右パネル使用幅 ≈ 537pt

    # ── プログラムセクション ──
    draw_section_label(c, rp_x, H - 28, 'PROGRAM')
    c.setFont('YuGothB', 11)
    c.setFillColor(INK)
    c.drawString(rp_x, H - 44, '当日のプログラム')

    sessions = [
        ('13:45', '75分', 'Session 01',
         'フィジカルAIとは何か——基礎と最前線',
         'ロボット基盤モデルの仕組みと従来制御との本質的な違い。'
         'Sim-to-Real、エンドツーエンド制御など技術トレンドを概観。'),
        ('15:15', '75分', 'Session 02',
         '製造現場への適用事例と実装アプローチ',
         '国内外の先進導入事例を通じて、どの工程・ラインでフィジカル'
         'AIが有効か、実装の具体的アプローチを学ぶ。'),
        ('16:30', '30分', 'Session 03',
         '自社への取り込み方・個別相談 & Q&A',
         '参加企業の課題を踏まえたグループ討議と個別質疑。'
         '「自社ではどこから始めるか」を具体化するセッション。'),
    ]

    card_top  = H - 58     # カード上端Y
    card_h    = 135
    gap       = 8
    col_w     = (rp_w - gap * 2) / 3

    for idx, (time_s, dur, num, title, desc) in enumerate(sessions):
        cx = rp_x + idx * (col_w + gap)
        cy = card_top - card_h  # カード下端Y

        # カード背景（白）
        c.setFillColor(WHITE)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.4)
        c.roundRect(cx, cy, col_w, card_h, 3, fill=1, stroke=1)

        # 上部ラスト
        c.setFillColor(RUST)
        c.rect(cx, card_top - 3, col_w, 3, fill=1, stroke=0)

        # 時刻
        inner_x = cx + 10
        c.setFont('YuGothB', 15)
        c.setFillColor(RUST)
        c.drawString(inner_x, card_top - 20, time_s)
        tw = c.stringWidth(time_s, 'YuGothB', 15)
        c.setFont('YuGothR', 6.5)
        c.setFillColor(MUTED)
        c.drawString(inner_x + tw + 4, card_top - 15, dur)

        # セッション番号
        c.setFont('YuGothR', 6.5)
        c.setFillColor(MUTED)
        c.drawString(inner_x, card_top - 32, num)

        # タイトル（折り返し）
        wrap_draw(c, title, inner_x, card_top - 46,
                  col_w - 22, 'YuGothB', 8.5, INK, leading=13)

        # 説明（折り返し）
        wrap_draw(c, desc, inner_x, card_top - 76,
                  col_w - 22, 'YuGothR', 7, MUTED, leading=11)

    # ── 区切り線 ──
    div_y = card_top - card_h - 14
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(rp_x, div_y, rp_x + rp_w, div_y)

    # ══════════════════════════════════════════════════════
    # 下部：講師 + 概要ボックス
    # ══════════════════════════════════════════════════════
    bottom_y = div_y - 12   # 下部エリア開始Y
    SPK_W    = 255
    OVW_X    = rp_x + SPK_W + 16
    OVW_W    = rp_w - SPK_W - 16

    # ── 講師 ──
    draw_section_label(c, rp_x, bottom_y, 'SPEAKER')

    PHOTO_SZ = 56
    photo_y  = bottom_y - PHOTO_SZ - 10

    # 写真
    if os.path.exists(PHOTO):
        img = PILImage.open(PHOTO)
        iw, ih = img.size
        side  = min(iw, ih)
        left  = (iw - side) // 2
        crop  = img.crop((left, 0, left + side, side))
        tmp   = os.path.join(BASE_DIR, '_tmp_photo.jpg')
        crop.save(tmp, 'JPEG', quality=90)
        c.drawImage(tmp, rp_x, photo_y, PHOTO_SZ, PHOTO_SZ,
                    preserveAspectRatio=True, mask='auto')
    else:
        c.setFillColor(STEEL_LT)
        c.rect(rp_x, photo_y, PHOTO_SZ, PHOTO_SZ, fill=1, stroke=0)
        c.setFont('YuGothM', 18)
        c.setFillColor(WHITE)
        c.drawCentredString(rp_x + PHOTO_SZ / 2, photo_y + 16, '辻')

    # 名前・肩書き
    nx   = rp_x + PHOTO_SZ + 10
    ny   = bottom_y - 14
    c.setFont('YuGothB', 12)
    c.setFillColor(INK)
    c.drawString(nx, ny, '辻　俊明')

    c.setFont('YuGothM', 6.5)
    c.setFillColor(RUST)
    c.drawString(nx, ny - 14, '埼玉大学 工学部 電気電子物理工学科 准教授')
    c.setFillColor(MUTED)
    c.drawString(nx, ny - 25, '株式会社Craftgnosis 共同設立者・取締役')

    bio_texts = [
        '慶應義塾大学大学院にてロボット制御で博士号取得（2006年）。',
        '2012年より埼玉大学准教授。フィジカルAI・ロボット',
        '基盤モデルを専門とし、ムーンショット事業参画など',
        '産学連携プロジェクトを牽引。2026年4月Craftgnosis共同設立。',
    ]
    bio_y = ny - 38
    for ln in bio_texts:
        c.setFont('YuGothR', 6.5)
        c.setFillColor(MUTED)
        c.drawString(rp_x, bio_y, ln)
        bio_y -= 10

    # ── 概要ボックス ──
    box_top = bottom_y + 4
    box_bot = 13
    box_h   = box_top - box_bot

    c.setFillColor(CREAM_DK)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.4)
    c.roundRect(OVW_X, box_bot, OVW_W, box_h, 4, fill=1, stroke=1)

    draw_section_label(c, OVW_X + 10, box_top - 10, 'OVERVIEW')

    rows = [
        ('日  時', ['2026年6月18日（木）', '13:45〜17:00']),
        ('会  場', ['東京都内（申込確定後にご案内）']),
        ('定  員', ['30名（招待制・先着順）']),
        ('参加費', ['70,000円（税別）／名']),
        ('請求書', ['インボイス（適格請求書）非対応']),
        ('お支払', ['申込後に請求書発行', '2026年6月末までに振込']),
        ('主  催', ['株式会社Craftgnosis']),
    ]

    row_y2 = box_top - 24
    for key, val_lines in rows:
        c.setFont('YuGothR', 6.5)
        c.setFillColor(MUTED)
        c.drawString(OVW_X + 10, row_y2, key)
        c.setFont('YuGothM', 7)
        c.setFillColor(INK)
        for i, ln in enumerate(val_lines):
            c.drawString(OVW_X + 52, row_y2 - i * 9, ln)
        row_y2 -= 9 * len(val_lines) + 8
        # 細い区切り
        c.setStrokeColor(LINE)
        c.setLineWidth(0.3)
        c.line(OVW_X + 10, row_y2 + 6, OVW_X + OVW_W - 10, row_y2 + 6)

    # 申込ボタン
    if row_y2 > box_bot + 22:
        btn_y  = box_bot + 4
        btn_w  = OVW_W - 20
        c.setFillColor(RUST)
        c.roundRect(OVW_X + 10, btn_y, btn_w, 18, 3, fill=1, stroke=0)
        c.setFont('YuGothB', 7.5)
        c.setFillColor(WHITE)
        c.drawCentredString(OVW_X + 10 + btn_w / 2, btn_y + 5,
                            '参加申込み → forms.gle/sJkDNbPxFcvvKHtC7')

    c.save()

    # 一時ファイル削除
    tmp = os.path.join(BASE_DIR, '_tmp_photo.jpg')
    if os.path.exists(tmp):
        os.remove(tmp)

    print('OK: ' + OUTPUT)


if __name__ == '__main__':
    make_flyer()
