"""Portfolio Évhira: página única, sem banco e sem login."""
import os
import secrets
from urllib.parse import quote

from flask import Flask, render_template

# Contato público da Évhira (CTA da página). Número com DDI e DDD, só dígitos.
WHATSAPP_NUMERO = "5511998917333"
WHATSAPP_MENSAGEM = "Olá, Eliane! Vi o portfólio da Évhira e quero conversar sobre o meu negócio."
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMERO}?text={quote(WHATSAPP_MENSAGEM)}"
EMAIL_CONTATO = "contato@evhira.com"

# Self-host em tudo: sem Google Fonts, sem CDN de ícone (ver CLAUDE.md).
CSP = (
    "default-src 'self'; "
    "img-src 'self' data: https:; "
    "style-src 'self' 'unsafe-inline'; "
    "font-src 'self'; "
    "script-src 'self'"
)

HEADERS_SEGURANCA = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Content-Security-Policy": CSP,
}


def create_app():
    app = Flask(__name__)
    # A página não usa sessão nem cookie; a chave existe só para a config nascer segura.
    # Vem do ambiente ou é sorteada a cada partida, nunca escrita no código.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    @app.context_processor
    def contato():
        return {"whatsapp_url": WHATSAPP_URL, "email_contato": EMAIL_CONTATO}

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    @app.after_request
    def seguranca(resp):
        for chave, valor in HEADERS_SEGURANCA.items():
            resp.headers[chave] = valor
        return resp

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
