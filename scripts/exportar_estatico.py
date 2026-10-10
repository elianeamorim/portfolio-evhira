"""Gera a versão em arquivos prontos do portfólio, para colocar na public_html da Hostinger.

Uso (na raiz do projeto):  python scripts/exportar_estatico.py
Saída: dist/ (index.html, static/, .htaccess) e dist/portfolio-evhira.zip
O Flask continua sendo a fonte: mudou texto ou CSS, rode este script de novo.
"""
import shutil
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app import HEADERS_SEGURANCA, app  # noqa: E402

DIST = RAIZ / "dist"

HTACCESS_BASE = """# Gerado por scripts/exportar_estatico.py. Não editar à mão.
# O redirecionamento para HTTPS fica no painel da Hostinger (Forçar HTTPS), pois a CDN pode causar laço aqui.

<IfModule mod_headers.c>
@@CABECALHOS@@
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 30 days"
  ExpiresByType font/woff2 "access plus 365 days"
  ExpiresByType text/css "access plus 7 days"
</IfModule>
"""


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    resposta = app.test_client().get("/")
    assert resposta.status_code == 200, resposta.status_code
    (DIST / "index.html").write_bytes(resposta.data)
    shutil.copytree(RAIZ / "static", DIST / "static")

    cabecalhos = "\n".join(
        f'  Header always set {nome} "{valor}"' for nome, valor in HEADERS_SEGURANCA.items()
    )
    (DIST / ".htaccess").write_text(HTACCESS_BASE.replace("@@CABECALHOS@@", cabecalhos), encoding="utf-8")

    pacote = DIST / "portfolio-evhira.zip"
    with zipfile.ZipFile(pacote, "w", zipfile.ZIP_DEFLATED) as z:
        for arquivo in sorted(DIST.rglob("*")):
            if arquivo.is_file() and arquivo != pacote:
                z.write(arquivo, arquivo.relative_to(DIST).as_posix())
    print(f"ok: {pacote} ({pacote.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
