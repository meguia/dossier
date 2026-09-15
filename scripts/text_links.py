"""Inline institutional links shared by the website and print editions."""
from html import escape


def institutional_text(text):
    html = escape(text)
    for label, url in (
        ('Universidad Nacional de Quilmes', 'https://www.unq.edu.ar/'),
        ('LAPSo', 'https://lapso.org/'),
    ):
        html = html.replace(label, f'<a class="institution-link" href="{url}">{label}</a>')
    return html
