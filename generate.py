import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "assets/fonts/DejaVuSans-Bold.ttf"
S = 1200
OUT = os.path.dirname(os.path.abspath(__file__))  # картинки ложатся рядом со скриптом

LOTS = [
    ("flagship", "TELEGRAM-БОТЫ\nПОД КЛЮЧ", "магазины · заявки · запись", (24, 30, 54), (58, 88, 180)),
    ("booking",  "БОТ ЗАПИСИ\nКЛИЕНТОВ",     "выбор даты · напоминания", (18, 40, 38), (28, 140, 118)),
    ("shop",     "БОТ-МАГАЗИН\nС ОПЛАТОЙ",   "каталог · корзина · СБП",  (44, 24, 20), (196, 96, 40)),
    ("miniapp",  "TELEGRAM\nMINI APP",       "приложение внутри Telegram", (30, 22, 48), (128, 74, 196)),
    ("ai",       "ИИ-КОНСУЛЬТАНТ\nВ TELEGRAM", "отвечает по вашим данным", (16, 34, 52), (36, 128, 190)),
]


def gradient(top, bottom):
    img = Image.new("RGB", (1, S))
    px = img.load()
    for y in range(S):
        t = y / (S - 1)
        px[0, y] = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom))
    return img.resize((S, S), Image.BICUBIC)


def fit(draw, text, size, max_w):
    while size > 20:
        f = ImageFont.truetype(FONT, size)
        if max(draw.textlength(line, f) for line in text.split("\n")) <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(FONT, size)


for name, title, sub, top, bottom in LOTS:
    img = gradient(top, bottom)
    d = ImageDraw.Draw(img, "RGBA")

    # мягкая засветка сверху, без резкого края
    glow = Image.new("L", (S, S), 0)
    ImageDraw.Draw(glow).ellipse((-200, -520, S + 200, 380), fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    img = Image.composite(Image.new("RGB", (S, S), (255, 255, 255)), img, glow)
    d = ImageDraw.Draw(img, "RGBA")

    # точечная сетка для фактуры
    for gx in range(90, S - 60, 46):
        for gy in range(90, S - 60, 46):
            d.ellipse((gx, gy, gx + 3, gy + 3), fill=(255, 255, 255, 20))

    accent = tuple(min(255, round(c * 1.5) + 40) for c in bottom)

    # рамка
    d.rounded_rectangle((36, 36, S - 36, S - 36), radius=44, outline=(255, 255, 255, 46), width=3)

    f_title = fit(d, title, 108, S - 240)
    f_sub = ImageFont.truetype(FONT, 42)
    f_foot = ImageFont.truetype(FONT, 36)

    lines = title.split("\n")
    lh = f_title.size + 26
    block_h = lh * len(lines)
    y = (S - block_h) // 2 - 70
    for line in lines:
        w = d.textlength(line, f_title)
        d.text(((S - w) / 2, y), line, font=f_title, fill=(255, 255, 255))
        y += lh

    # акцентная черта
    d.rounded_rectangle(((S - 180) / 2, y + 14, (S + 180) / 2, y + 24), radius=5, fill=accent)

    w = d.textlength(sub, f_sub)
    d.text(((S - w) / 2, y + 62), sub, font=f_sub, fill=(255, 255, 255, 216))

    foot = "Python  ·  aiogram 3  ·  исходный код"
    w = d.textlength(foot, f_foot)
    d.text(((S - w) / 2, S - 170), foot, font=f_foot, fill=(255, 255, 255, 170))

    img.save(f"{OUT}/{name}.jpg", quality=92)
    print(name, img.size)
