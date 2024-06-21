

TEXT = {
    'uz': {
        'intro': 'Assalomu alaykum. Kompaniyamizga hush kelibsiz',
        'chose_lang': 'Iltimos tilni tanlang',
        'order': '🚛 Buyurtma qilish',
        'my_orders': '📥 Buyurtmalarim',
        'contact_operator': "📞 Operator bilan bog'lanish",
        'settings': "⚙️ Sozlamalar",
        'confirm': 'Tasdiqlash',
        'cancel': 'Bekor qilish',
    }
}


def get_text(text_code, language = 'uz'):
    lang_text = TEXT.get(language)
    text = lang_text.get(text_code)
    return text