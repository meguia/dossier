#!/usr/bin/env python3
"""Build an entirely static English/Spanish portfolio for GitHub Pages."""
from pathlib import Path
from html import escape
import json
import shutil
from text_links import institutional_text

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
DATA = json.loads((ROOT / 'content/portfolio.json').read_text())
E = escape

def paras(items):
    return ''.join(f'<p>{E(p)}</p>' for p in items)

def image(name, alt, prefix, cls='', eager=False):
    return f'<img src="{prefix}assets/images/{E(name)}" alt="{E(alt)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def channels():
    return '<div class="channels">'+''.join(f'<a href="{E(c["url"])}">{E(c["label"])} ↗</a>' for c in DATA['video_channels'])+'</div>'

def downloads(lang, prefix):
    t=DATA[lang]
    return f'<div class="actions"><a class="button" href="{prefix}downloads/Manuel-Eguia-Portfolio.pdf">{E(t["download"])} <span aria-hidden="true">↓</span></a><a class="text-link" href="{prefix}downloads/Manuel-Eguia-CV.pdf">{E(t["download_cv"])} <small>({E(t["labels"]["pdf_language"])})</small></a></div>'

def header(lang, prefix, project=None):
    t=DATA[lang]; home=prefix+('es/' if lang=='es' else '')
    current='works/'+project['id']+'/' if project else ''
    nav=''.join(f'<a href="{home}#{anchor}">{E(label)}</a>' for anchor,label in zip(['works','practice','cv','contact'],t['nav']))
    languages=''
    for language in ['en','es']:
        attr='aria-current="page"' if language==lang else ''
        lang_path='es/' if language=='es' else ''
        languages+=f'<a href="{prefix}{lang_path}{current}" lang="{language}" hreflang="{language}" {attr}>{language.upper()}</a>'
    return f'<a class="skip" href="#main">{E(t["labels"]["skip"])}</a><div class="wrap"><header class="site-header" id="top"><a class="brand" href="{home}">Manuel Eguía</a><nav class="nav" aria-label="Main">{nav}<span class="lang" aria-label="{E(t["labels"]["language"])}">{languages}</span></nav></header></div>'

def footer(lang):
    t=DATA[lang]
    return f'<footer class="contact-section" id="contact" aria-label="{E(t["contact_heading"])}"><div class="contact-grid"><div><p class="contact-name">{E(DATA["name"])}</p><p class="contact-location">{E(DATA["location"])}</p></div><address><a class="email" href="mailto:{DATA["email"]}">{DATA["email"]}</a>{channels()}</address></div></footer>'

def shell(lang,body,prefix,project=None):
    t=DATA[lang]; path=('es/' if lang=='es' else '')+('works/'+project['id']+'/' if project else '')
    title=(project[lang]['title']+' — ' if project else '')+'Manuel Eguía — '+t['title']
    desc=project[lang]['summary'] if project else t['intro']
    og=project['image'] if project else 'sonic-performance.jpg'
    alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{DATA["base_url"]}{("es/" if l=="es" else "")}{("works/"+project["id"]+"/" if project else "")}">' for l in ['en','es'])
    schema={'@context':'https://schema.org','@type':'Person','name':'Manuel Camilo Eguía','alternateName':'Manuel Eguía','url':DATA['base_url'],'jobTitle':t['role'],'sameAs':[c['url'] for c in DATA['video_channels']]}
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#f3f2ec"><link rel="canonical" href="{DATA["base_url"]}{path}">{alternates}<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{DATA["base_url"]}{path}"><meta property="og:image" content="{DATA["base_url"]}assets/images/{og}"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="{prefix}assets/site.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body>{header(lang,prefix,project)}{body}{footer(lang)}</body></html>'

def rows(items):
    html='<ul class="list">'
    for item in items:
        title=E(item['title']) if item.get('url') else institutional_text(item['title'])
        if item.get('url'): title=f'<a href="{E(item["url"])}">{title}</a>'
        html+=f'<li><span class="year">{E(item["year"])}</span><div><h4>{title}</h4>'
        if item.get('artist'): html+=f'<p>{E(item["artist"])}</p>'
        html+=f'<p>{E(item["detail"])}</p></div></li>'
    return html+'</ul>'

def research(lang):
    t=DATA[lang];items=''
    for p in DATA['publications']:
        title=E(p['title'])
        if p['url']: title=f'<a href="{p["url"]}">{title} ↗</a>'
        items+=f'<li><span class="year">{p["year"]}</span><div><div class="publication-title">{title}</div><div class="publication-meta">{E(p["authors"])}<br>{E(p["journal"])}</div></div><span class="publication-theme">{E(p[lang])}</span></li>'
    return f'<div class="research"><div class="research-head"><h3>{E(t["research_heading"])}</h3><p>{E(t["research_intro"])}</p></div><ol class="publications">{items}</ol></div>'

def homepage(lang):
    t=DATA[lang];prefix='../' if lang=='es' else '';l=t['labels']
    hero_title='Sound,<br>space &amp;<br><em>perception.</em>' if lang=='en' else 'Sonido,<br>espacio y<br><em>percepción.</em>'
    cards=''
    for p in DATA['projects']:
        q=p[lang]
        cards+=f'<a class="work-card" href="works/{p["id"]}/">{image(p["image"],q["alt"],prefix)}<div class="card-meta"><span>{p["number"]} / {E(q["medium"].split(" · ")[0])}</span><span>{p["year"]}</span></div><div class="card-title"><h3>{E(q["title"])}</h3><span class="arrow" aria-hidden="true">↗</span></div><div class="card-subtitle">{E(q["subtitle"])}</div><div class="card-credit">{E(p["credit"])}</div></a>'
    body=f'''<main id="main"><div class="wrap"><section class="hero"><div class="hero-top eyebrow"><span class="dot">{E(t['role'])}</span><span>{E(t['portfolio'])} / 2026</span></div><div class="hero-grid"><div><h1>{hero_title}</h1><p class="hero-text">{E(t['intro'])}</p>{downloads(lang,prefix)}</div><figure>{image('sonic-performer.jpg',DATA['projects'][0][lang]['alt'],prefix,'hero-image',True)}<figcaption class="caption"><span>01 / {E(DATA['projects'][0][lang]['title'])}</span><span>Manuel Eguía / Oscar Edelstein</span></figcaption></figure></div><div class="hero-bottom"><span class="eyebrow">Physics / Nonlinear dynamics / Neuroscience / Acoustics</span>{channels()}</div></section><section class="section" id="works"><div class="section-heading"><div><p class="eyebrow">01—04</p><h2>{E(t['work_heading'])}</h2></div><p>{E(t['work_intro'])}</p></div><div class="works-grid">{cards}</div></section></div><section class="statement-section section" id="practice"><div class="wrap statement-grid"><div><p class="eyebrow">{'Position & biography' if lang=='en' else 'Posición y biografía'}</p><h2>{E(t['statement_title'])}</h2><div class="portrait-row">{image('portrait.jpg','Manuel Eguía',prefix)}<p>{institutional_text(t['bio'])}</p></div></div><div class="statement-copy">{paras(t['statement'])}</div></div></section><div class="wrap"><section class="section practice-grid"><div><h2>{E(t['practice_heading'])}</h2>{paras(t['practice'])}<div class="current"><p class="eyebrow">{'Work in progress' if lang=='en' else 'Trabajo en proceso'}</p><h4>{E(t['current_heading'])}</h4><p>{E(t['current'])}</p></div></div><div><h3>{E(t['workshop_heading'])}</h3><p>{E(t['workshop_intro'])}</p>{rows(t['workshops'])}</div></section><section class="section collab-section"><div class="section-heading"><h3>{E(t['collab_heading'])}</h3><p>{E(t['collab_intro'])}</p></div>{rows(t['collaborations']).replace('class="list"','class="list collab-list"')}</section><section class="section cv-section" id="cv"><div class="section-heading"><h2>{E(t['cv_heading'])}</h2><div><p>{E(t['cv_intro'])}</p>{downloads(lang,prefix)}</div></div><div class="cv-columns"><div><h3>{E(l['positions'])}</h3>{rows(t['positions'])}<p class="programme">{E(t['programme'])}</p><h3>{E(l['education'])}</h3>{rows(t['education'])}</div><div><h3>{E(l['highlights'])}</h3>{rows(t['highlights'])}</div></div>{research(lang)}</section></div></main>'''
    if lang=='es': body=body.replace('Physics / Nonlinear dynamics / Neuroscience / Acoustics','Física / Dinámica no lineal / Neurociencias / Acústica')
    return shell(lang,body,prefix)

def projectpage(lang,p):
    t=DATA[lang];q=p[lang];prefix='../../../' if lang=='es' else '../../';l=t['labels']
    links=''.join(f'<a href="{E(a["url"])}">{E(a[lang])} ↗</a>' for a in p['links'])
    facts=''.join(f'<dt>{E(l[key])}</dt><dd>{E(q[key])}</dd>' for key in ['medium','role','context'])
    gallery=''
    if p['gallery']:
        gallery='<div class="gallery '+('three' if len(p['gallery'])==3 else '')+'">'+''.join(image(name, f'{q["title"]} — '+('project documentation' if lang=='en' else 'documentación del proyecto'),prefix) for name in p['gallery'])+'</div>'
    detail=''
    if p['id']!='biocenosis':
        detail=f'<section class="project-detail"><div class="detail-text"><h2>{E(q["detail_title"])}</h2><div>{paras(q["detail"])}</div></div>{image(p["detail_image"],q["detail_alt"],prefix,"detail-photo")}{gallery}</section>'
    nxt=DATA['projects'][(int(p['number']))%len(DATA['projects'])]
    home=prefix+('es/' if lang=='es' else '')
    body=f'''<main class="wrap" id="main"><section class="project-intro"><p class="eyebrow">{p['number']} / {p['year']} / {E(q['medium'])}</p><h1 class="project-title">{E(q['title'])}</h1><p class="project-subtitle">{E(q['subtitle'])}</p><p class="project-credit">{E(p['credit'])}</p></section><figure>{image(p['image'],q['alt'],prefix,'project-hero',True)}<figcaption class="caption"><span>{E(q['title'])} · {p['year']}</span><span>{E(p['credit'])}</span></figcaption></figure><section class="project-text"><div class="project-body"><p class="lead">{E(q['summary'])}</p>{paras(q['body'])}</div><aside><dl class="project-facts">{facts}</dl><div class="project-links">{links}</div></aside></section>{detail}<nav class="other-works" aria-label="{'Other works' if lang=='en' else 'Otras obras'}"><a href="{home}#works"><small>{E(t['work_heading'])}</small><strong>← {'All works' if lang=='en' else 'Todas las obras'}</strong></a><a href="../{nxt['id']}/"><small>{'Next work' if lang=='en' else 'Siguiente obra'}</small><strong>{E(nxt[lang]['title'])} →</strong></a></nav></main>'''
    return shell(lang,body,prefix,p)

def main():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    paths=[]
    for lang in ['en','es']:
        folder=OUT/('es' if lang=='es' else '')
        folder.mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(homepage(lang))
        paths.append(('es/' if lang=='es' else ''))
        for p in DATA['projects']:
            target=folder/'works'/p['id'];target.mkdir(parents=True,exist_ok=True)
            (target/'index.html').write_text(projectpage(lang,p))
            paths.append(('es/' if lang=='es' else '')+'works/'+p['id']+'/')
    (OUT/'.nojekyll').touch()
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+DATA['base_url']+'sitemap.xml\n')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+DATA['base_url']+p+'</loc></url>' for p in paths)+'</urlset>')
    print(f'Built {len(paths)} static pages in {OUT}')

if __name__=='__main__': main()
