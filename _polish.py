"""
Pasada de UX/coherencia narrativa:
1. Reordena secciones: Diagnóstico (Por canal, Hallazgos, Top, Temas) -> Acción (Decisiones, Formato, Recomendaciones)
2. Sidebar: agrega grupo ACCIÓN entre Diagnóstico y Datos
3. Quita numeracion (era inconsistente: solo algunas secciones tenian numero)
4. Agrega subtitulo descriptivo (.sec-desc) bajo cada .sec-lbl explicando que sirve la seccion
5. Tightens copy en panels donde hay redundancia
"""
import re
from pathlib import Path

p = Path(r'D:\codex005\index.html')
html = p.read_text(encoding='utf-8')

# ════════════════════════════════════════════════════════════
# 1. CSS: separar el border-bottom de sec-lbl en sec-desc
# ════════════════════════════════════════════════════════════
old_css = '''  .sec-lbl {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin-bottom: 4px;
  }'''
new_css = '''  .sec-lbl {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
  }
  .sec-desc {
    font-size: 13px;
    color: var(--text-2);
    line-height: 1.55;
    margin: 0 0 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
  }
  .sec-desc b { color: var(--text); font-weight: 600; }'''
assert old_css in html
html = html.replace(old_css, new_css)
print('1. CSS sec-lbl + sec-desc actualizado')

# ════════════════════════════════════════════════════════════
# 2. Cortar la seccion #hallazgos para reinsertarla luego
# ════════════════════════════════════════════════════════════
hallazgos_pattern = re.compile(
    r'      <!-- ═+ 3 · HALLAZGOS ═+ -->\n      <section id="hallazgos">.*?</section>\n\n',
    re.DOTALL
)
m = hallazgos_pattern.search(html)
assert m, 'no encontre la seccion hallazgos'
hallazgos_block = m.group(0)
html = hallazgos_pattern.sub('', html, count=1)
print('2. Seccion #hallazgos extraida')

# ════════════════════════════════════════════════════════════
# 3. Renombrar sec-lbl + agregar sec-desc en cada seccion
# ════════════════════════════════════════════════════════════
section_updates = [
    # (old_sec_lbl, new_sec_lbl, sec_desc)
    ('<div class="sec-lbl">1 · Diagnóstico por canal</div>',
     '<div class="sec-lbl">Diagnóstico por canal</div>',
     'Estado de cada canal al cierre del periodo. La caída es Instagram; el motor del crecimiento es TikTok.'),

    ('<div class="sec-lbl">2 · Top contenido del periodo</div>',
     '<div class="sec-lbl">Top contenido del periodo</div>',
     'Qué piezas funcionaron — filtra por <b>red social</b> y <b>mes</b> para encontrar patrones replicables.'),

    ('<div class="sec-lbl">Análisis por tema y hook</div>',
     '<div class="sec-lbl">Análisis por tema y hook</div>',
     'Qué temas concentran el alcance y qué ganchos disparan engagement, separados por red social.'),

    ('<div class="sec-lbl">Decisiones estratégicas</div>',
     '<div class="sec-lbl">Decisiones estratégicas</div>',
     'Qué hacer con cada post según dónde cae en la matriz <b>alcance × engagement</b>: repetir, ajustar gancho, ajustar mensaje, o detener.'),

    ('<div class="sec-lbl">Formato y anatomía del reel ganador</div>',
     '<div class="sec-lbl">Formato y anatomía del reel ganador</div>',
     'Template a replicar en cada nueva pieza: duración, franja horaria, apertura y estructura del top performer.'),

    ('<div class="sec-lbl">Recomendaciones de nuevos reels · qué grabar después</div>',
     '<div class="sec-lbl">Recomendaciones de nuevos reels</div>',
     '10 ideas concretas para producir esta semana — cada tarjeta cita el post que la sustenta.'),

    ('<div class="sec-lbl">3 · Hallazgos clave</div>',
     '<div class="sec-lbl">Hallazgos clave</div>',
     'Lo que el reporte revela en una mirada — leer antes de tomar decisiones tácticas.'),
]

for old_lbl, new_lbl, desc in section_updates:
    old_full = old_lbl
    new_full = new_lbl + f'\n        <div class="sec-desc">{desc}</div>'
    if old_full not in html and old_full not in hallazgos_block:
        print(f'  ! NO ENCONTRADO: {old_lbl[:60]}...')
        continue
    if old_full in html:
        html = html.replace(old_full, new_full)
    if old_full in hallazgos_block:
        hallazgos_block = hallazgos_block.replace(old_full, new_full)
print('3. sec-lbl renombrados + sec-desc agregadas')

# ════════════════════════════════════════════════════════════
# 4. Reinsertar #hallazgos despues de #por-canal
# ════════════════════════════════════════════════════════════
# Tambien limpiar el numero "3" del comentario HTML
hallazgos_block = hallazgos_block.replace(
    '<!-- ═══════ 3 · HALLAZGOS ═══════ -->',
    '<!-- ═══════ HALLAZGOS ═══════ -->'
)
# Buscar el final de la seccion #por-canal para insertar despues
# La seccion #por-canal termina con </section> y luego viene un comentario
por_canal_end = re.compile(
    r'(      <section id="por-canal">.*?</section>\n\n)',
    re.DOTALL
)
m = por_canal_end.search(html)
assert m, 'no encontre el final de por-canal'
html = html[:m.end()] + hallazgos_block + html[m.end():]
print('4. #hallazgos reinsertado despues de #por-canal')

# ════════════════════════════════════════════════════════════
# 5. Limpiar numeros "1 · " y "2 · " de comentarios HTML
# ════════════════════════════════════════════════════════════
html = html.replace('<!-- ═══════ 1 · POR CANAL ═══════ -->', '<!-- ═══════ POR CANAL ═══════ -->')
html = html.replace('<!-- ═══════ 2 · TOP CONTENIDO ═══════ -->', '<!-- ═══════ TOP CONTENIDO ═══════ -->')
print('5. Numeros removidos de comentarios HTML')

# ════════════════════════════════════════════════════════════
# 6. Sidebar: reordenar y agregar grupo ACCIÓN
# ════════════════════════════════════════════════════════════
old_sb = '''    <div class="s-group-lbl">Diagnóstico</div>
    <a href="#por-canal"         class="s-item">Por canal · IG vs TikTok</a>
    <a href="#top"               class="s-item">Top contenido</a>
    <a href="#temas-ganchos"     class="s-item">Temas y ganchos</a>
    <a href="#decisiones"        class="s-item">Decisiones estratégicas</a>
    <a href="#formato"           class="s-item">Formato del reel</a>
    <a href="#recomendaciones"   class="s-item">Recomendaciones</a>
    <a href="#hallazgos"         class="s-item">Hallazgos clave</a>'''
new_sb = '''    <div class="s-group-lbl">Diagnóstico</div>
    <a href="#por-canal"         class="s-item">Por canal · IG vs TikTok</a>
    <a href="#hallazgos"         class="s-item">Hallazgos clave</a>
    <a href="#top"               class="s-item">Top contenido</a>
    <a href="#temas-ganchos"     class="s-item">Temas y ganchos</a>

    <div class="s-group-lbl" style="margin-top:14px">Acción</div>
    <a href="#decisiones"        class="s-item">Decisiones estratégicas</a>
    <a href="#formato"           class="s-item">Formato del reel</a>
    <a href="#recomendaciones"   class="s-item">Recomendaciones</a>'''
assert old_sb in html
html = html.replace(old_sb, new_sb)
print('6. Sidebar reorganizado: Diagnostico + Accion + Datos')

# ════════════════════════════════════════════════════════════
# 7. Tightening de copy en panel-sub (ya un poco redundante con sec-desc)
# ════════════════════════════════════════════════════════════
tightenings = [
    # Top contenido — el sec-desc ya cubre el filtro, simplificar el sub del panel
    ('<div class="panel-sub">El patrón ganador: hook con dolor + emoji · 15-20s · Meta/Google Ads</div>',
     '<div class="panel-sub">El patrón ganador: emoji + pregunta-dolor · 15-20s · Meta/Google Ads</div>'),

    # Decisiones — el sec-desc ya explica los cuadrantes
    ('<div class="panel-title">Qué hacer con cada tipo de contenido</div>\n              <div class="panel-sub">Clasificación por cuadrante (alcance × engagement) sobre la mediana del periodo</div>',
     '<div class="panel-title">Clasificación por cuadrante</div>\n              <div class="panel-sub">Cada post evaluado contra la mediana del periodo · top 6 visibles por cuadrante</div>'),
]
for old, new in tightenings:
    if old in html:
        html = html.replace(old, new)
    else:
        print(f'  ! tightening no encontrado: {old[:60]}...')
print('7. Copy de panels tightened')

p.write_text(html, encoding='utf-8')
print(f'\nOK · {p.stat().st_size:,} bytes')
