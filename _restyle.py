"""Alineacion estetica con la Calculadora de inversion de Lima Retail:
- Sidebar pasa de fondo navy a claro
- Top banner full-width con marca + nombre del tablero (separador vertical)
- Ajustes de bordes/spacing/colores en sidebar
"""
import re
from pathlib import Path

p = Path(r'D:\codex005\index.html')
html = p.read_text(encoding='utf-8')

# ════════════════════════════════════════════════════════════
# 1. CSS :root — sidebar tokens light
# ════════════════════════════════════════════════════════════
old_root = '''    --sidebar-bg:    #0F172A;
    --sidebar-text:  #CBD5E1;
    --sidebar-muted: #475569;'''
new_root = '''    --sidebar-bg:    #FFFFFF;
    --sidebar-text:  #475569;
    --sidebar-muted: #94A3B8;'''
assert old_root in html, '!! root vars no encontrados'
html = html.replace(old_root, new_root)
print('1. CSS :root sidebar tokens updated')

# ════════════════════════════════════════════════════════════
# 2. CSS .sidebar block + sub-rules (light variant)
# ════════════════════════════════════════════════════════════
old_sb = '''  .sidebar {
    width: 240px;
    background: var(--sidebar-bg);
    color: var(--sidebar-text);
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 0;
    max-height: 100vh;
    overflow-y: auto;
  }
  .s-brand {
    padding: 20px 20px 18px;
    border-bottom: 1px solid rgba(255,255,255,.06);
    margin-bottom: 10px;
  }
  .s-title { font-size: 15px; font-weight: 600; color: #fff; letter-spacing: -.01em; }
  .s-sub   { font-size: 12px; color: #64748B; margin-top: 2px; }
  .s-group-lbl {
    font-size: 10px; text-transform: uppercase; color: var(--sidebar-muted);
    letter-spacing: .08em; padding: 10px 22px 6px; font-weight: 600;
  }
  .s-item {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 14px; margin: 0 8px;
    border-radius: var(--r-sm);
    color: var(--sidebar-text);
    font-size: 13px; cursor: pointer;
    text-decoration: none;
    transition: background .15s;
  }
  .s-item:hover  { background: rgba(255,255,255,.04); color: #fff; text-decoration: none; }
  .s-item.active { background: rgba(37,99,235,.14); color: #60A5FA; }
  .s-div { border: none; border-top: 1px solid rgba(255,255,255,.06); margin: 6px 12px; }
  .s-footer {
    padding: 14px 20px; font-size: 11px; color: #334155;
    border-top: 1px solid rgba(255,255,255,.06); margin-top: auto;
  }'''

new_sb = '''  .sidebar {
    width: 240px;
    background: var(--sidebar-bg);
    color: var(--sidebar-text);
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 49px;
    max-height: calc(100vh - 49px);
    overflow-y: auto;
    border-right: 1px solid var(--border);
  }
  .s-group-lbl {
    font-size: 10px; text-transform: uppercase; color: var(--muted);
    letter-spacing: .08em; padding: 18px 22px 8px; font-weight: 600;
  }
  .s-group-lbl:first-of-type { padding-top: 22px; }
  .s-item {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 14px; margin: 0 8px;
    border-radius: var(--r-sm);
    color: var(--text-2);
    font-size: 13px; cursor: pointer;
    text-decoration: none;
    transition: background .15s, color .15s;
  }
  .s-item:hover  { background: #F1F5F9; color: var(--text); text-decoration: none; }
  .s-item.active { background: var(--brand-soft); color: var(--brand-text); font-weight: 500; }
  .s-div { border: none; border-top: 1px solid var(--border); margin: 8px 14px; }
  .s-footer {
    padding: 14px 22px; font-size: 11px; color: var(--muted);
    border-top: 1px solid var(--border); margin-top: auto;
  }'''
assert old_sb in html, '!! .sidebar block no encontrado'
html = html.replace(old_sb, new_sb)
print('2. .sidebar styles convertidos a tema claro')

# ════════════════════════════════════════════════════════════
# 3. Agregar CSS para .app-banner
# ════════════════════════════════════════════════════════════
banner_css = '''  /* ═══ Top banner (estilo Calculadora Lima Retail) ═══ */
  .app-banner {
    background: #fff;
    padding: 14px 28px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 16px;
    position: sticky;
    top: 0;
    z-index: 20;
  }
  .app-banner-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -.01em;
  }
  .app-banner-sep {
    width: 1px;
    height: 18px;
    background: var(--border);
  }
  .app-banner-sub {
    font-size: 14px;
    color: var(--text-2);
    font-weight: 500;
  }

'''
# Insertar antes del comment de Filter bar
old_anchor = '  /* ═══ Filter bar (rango de fechas) ═══ */'
assert old_anchor in html
html = html.replace(old_anchor, banner_css + old_anchor)
print('3. CSS de .app-banner agregado')

# ════════════════════════════════════════════════════════════
# 4. HTML: agregar banner antes del shell + remover s-brand del sidebar
# ════════════════════════════════════════════════════════════
old_body_open = '''<body>

<!-- ═══════════════════════════════════════════════════════════════════
     Bloque de DATOS · poblado manualmente desde el PDF de Metricool.'''

new_body_open = '''<body>

<div class="app-banner">
  <div class="app-banner-title">Lima Retail</div>
  <div class="app-banner-sep"></div>
  <div class="app-banner-sub">Plan de Contenidos · Q2 2026</div>
</div>

<!-- ═══════════════════════════════════════════════════════════════════
     Bloque de DATOS · poblado manualmente desde el PDF de Metricool.'''
assert old_body_open in html, '!! anchor body open no encontrado'
html = html.replace(old_body_open, new_body_open)
print('4a. Banner HTML agregado al body')

# Remover el bloque s-brand del sidebar (la marca ahora vive en el banner)
old_brand = '''    <div class="s-brand">
      <div class="s-title">Lima Retail</div>
      <div class="s-sub">Plan de Contenidos · Q2 2026</div>
    </div>

    '''
new_brand = '    '
assert old_brand in html, '!! s-brand no encontrado'
html = html.replace(old_brand, new_brand)
print('4b. s-brand removido del sidebar')

# Limpiar el "margin-top:14px" del segundo s-group-lbl ya que agregamos padding-top general
old_acc = '<div class="s-group-lbl" style="margin-top:14px">Acción</div>'
new_acc = '<div class="s-group-lbl">Acción</div>'
if old_acc in html:
    html = html.replace(old_acc, new_acc)
    print('4c. margin-top inline removido del grupo Accion')

p.write_text(html, encoding='utf-8')
print(f'\nOK · {p.stat().st_size:,} bytes')
