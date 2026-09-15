#!/usr/bin/env python3
"""Generate fixed-page HTML masters for PDF printing (not published)."""
from pathlib import Path
from html import escape as E
import json
import re
import argparse

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'working/print'
D=json.loads((ROOT/'content/portfolio.json').read_text())
T=D['en']
ASSETS=(ROOT/'assets').as_uri()+'/'

def img(name,cls='',alt=''):
    return f'<img src="{ASSETS}images/{name}" class="{cls}" alt="{E(alt)}">'

def paras(items): return ''.join(f'<p>{E(x)}</p>' for x in items)

def links(p):
    return '<div class="links">'+''.join(f'<a class="text-link" href="{E(x["url"])}">{E(x["en"])} ↗</a>' for x in p['links'])+'</div>'

def footer(n,title):
    return f'<footer class="page-footer"><span>Manuel Eguía / {E(title)}</span><span>{n:02d} / 12</span></footer>'

def page(n,title,body,cls=''):
    return f'<section class="page {cls}">{body}{footer(n,title)}</section>'

def head(p):
    q=p['en']
    return f'<header class="page-head"><p class="eyebrow">Selected work {p["number"]} / {p["year"]}</p><h2>{E(q["title"])}</h2><div class="subtitle">{E(q["subtitle"])}</div><div class="credits">{E(p["credit"])}</div></header>'

def facts(p):
    q=p['en']
    return '<div class="facts">'+''.join(f'<p><strong>{T["labels"][k]}</strong>{E(q[k])}</p>' for k in ['role','context'])+'</div>'

def work(n,p,cls=''):
    q=p['en']
    body=head(p)+f'<div class="work-grid"><figure>{img(p["image"],"main-photo",q["alt"])}<figcaption class="caption">{E(q["medium"])}</figcaption>{links(p)}</figure><div class="work-copy"><p class="summary">{E(q["summary"])}</p>{paras(q["body"])}{facts(p)}</div></div>'
    return page(n,q['title'],body,cls)

def rows(items):
    s=''
    for x in items:
        s+=f'<div class="print-row"><span class="year">{E(x["year"])}</span><div><h4>{E(x["title"])}</h4>'
        if x.get('artist'): s+=f'<p>{E(x["artist"])}</p>'
        s+=f'<p>{E(x["detail"])}</p></div></div>'
    return s

def publications():
    s='<ol class="research-list">'
    for p in D['publications']:
        s+=f'<li><span class="year">{p["year"]}</span><div><div class="pub-title"><a href="{p["url"]}">{E(p["title"])}</a></div><div class="pub-meta">{E(p["authors"])} · {E(p["journal"])}</div><div class="doi"><a href="{p["url"]}">{p["url"].replace("https://doi.org/", "doi: ")}</a></div></div></li>'
    return s+'</ol>'

def contact():
    return f'<div class="contact-block"><a class="email" href="mailto:{D["email"]}">{D["email"]}</a><p><a href="{D["base_url"]}">meguia.github.io/dossier</a><br><a href="https://vimeo.com/meguia">vimeo.com/meguia</a><br><a href="https://www.youtube.com/@manueleguia2915">youtube.com/@manueleguia2915</a></p></div>'

def cv_content():
    return f'<p class="eyebrow">Manuel Camilo Eguía / Buenos Aires, Argentina</p><h2>Selected CV</h2><p class="cv-intro">{E(T["cv_intro"])}</p><div class="cv-columns"><div><h3>Research &amp; teaching</h3>{rows(T["positions"])}<p class="programme">{E(T["programme"])}</p><h3>Education</h3>{rows(T["education"])}</div><div><h3>Exhibitions, residencies &amp; support</h3>{rows(T["highlights"])}</div></div>'

def document(body,title):
    return f'<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>{E(title)}</title><link rel="stylesheet" href="{ASSETS}print.css"></head><body>{body}</body></html>'

def main():
    global DEST
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'build/print')
    parser.add_argument('--proposal',type=Path,help='Optional local residency-proposal Markdown; never copied into the website.')
    args=parser.parse_args()
    DEST=args.output_dir
    DEST.mkdir(parents=True,exist_ok=True)
    p=D['projects'];pages=[]
    cover=f'<div class="cover-top"><span class="cover-name">Manuel Eguía</span><span>Selected works &amp; practice<br>2026</span></div><div class="cover-main"><div><h1>Sound,<br>space &amp;<br><em>perception.</em></h1><p class="role">Sound artist · Physicist · Researcher<br>Buenos Aires, Argentina</p><div class="small-links"><a href="https://vimeo.com/meguia">Vimeo ↗</a><a href="https://www.youtube.com/@manueleguia2915">YouTube ↗</a><a href="{D["base_url"]}">Website ↗</a></div></div><figure>{img("sonic-performer.jpg","cover-image",p[0]["en"]["alt"])}<figcaption class="caption">Sonic Crystal Room · Manuel Eguía / Oscar Edelstein</figcaption></figure></div>'
    pages.append(page(1,'Sound, space & perception',cover,'cover'))
    statement=f'<p class="eyebrow">Position / Biography</p><div class="statement-grid"><div><h2>{E(T["statement_title"])}</h2><div class="body">{paras(T["statement"])}</div></div><aside>{img("portrait.jpg","portrait","Manuel Eguía")}<div class="statement-bio">{E(T["bio"])}</div></aside></div>'
    pages.append(page(2,'Position & biography',statement))
    pages.append(work(3,p[0]))
    detail=f'<p class="eyebrow">Sonic Crystal Room / Acoustic architecture</p><div class="detail-grid">{img("sonic-columns.jpg","",p[0]["en"]["detail_alt"])}<div class="detail-text"><h2>{E(p[0]["en"]["detail_title"])}</h2>{paras(p[0]["en"]["detail"])}{img("sonic-red.jpg","detail-small","Sonic Crystal Room, rotating columns illuminated in red.")}<p class="caption">Mobile structures, changing acoustic perspectives.<br>Manuel Eguía / Oscar Edelstein</p></div></div>'
    pages.append(page(4,'Sonic Crystal Room',detail,'image-detail'))
    pages.append(work(5,p[1]))
    td=p[1]['en']
    labels=['01 / A familiar room','02 / Spatial transformation','03 / Returning from outside']
    sequence=''.join(f'<figure>{img(name,"",td["title"]+" — "+labels[i])}<figcaption>{labels[i]}</figcaption></figure>' for i,name in enumerate(p[1]['gallery']))
    transit=f'<p class="eyebrow">Transit / Site-specific virtual reality</p><h2>{E(td["detail_title"])}</h2><div class="two-columns"><div class="body">{paras(td["detail"])}</div><div><p class="large-summary">The same room.<br>A different sense of where we are.</p><p class="small muted">First episode: iM Konsthall, Moskosel, Sweden, 2023.<br>Manuel Eguía / Mauro Zannoli<br>Commission: Northern Sustainable Futures</p>{links(p[1])}</div></div><div class="transit-sequence">{sequence}</div>'
    pages.append(page(6,'Transit',transit,'transit-detail'))
    pages.append(work(7,p[2],'grapa-main'))
    gd=p[2]['en'];step_names=['01 / Immersive recording','02 / Acoustic survey','03 / Documentary']
    steps=''.join(f'<div class="process-step"><p class="eyebrow">{step_names[i]}</p><p>{E(txt)}</p></div>' for i,txt in enumerate(gd['detail']))
    grapa=f'<header class="page-head"><p class="eyebrow">Proyecto GRAPa / Fieldwork, April 2018</p><h2>{E(gd["detail_title"])}</h2></header><div class="process-grid"><div>{img("grapa-fieldwork.jpg","field-photo",gd["detail_alt"])}<div class="process-pair">{img("grapa-acoustics.jpg","","Acoustic measurement equipment in the natural amphitheatre.")}{img("grapa-coplera.jpg","","A coplera with her caja at Quebrada de las Conchas.")}</div><p class="caption">La Copla y el Anfiteatro de la Quebrada de las Conchas · Salta, Argentina<br>GRAPa, with Mariana Carrizo and local copleras and copleros.</p></div><div>{steps}<p class="small"><strong>Founder:</strong> Manuel Eguía<br>Team: Francisco Durante, Damián Payo, Mauro Zannoli and Manuel Eguía.</p></div></div>'
    pages.append(page(8,'Proyecto GRAPa',grapa,'grapa-process'))
    pages.append(work(9,p[3],'biocenosis'))
    practice=f'<p class="eyebrow">Laboratory / Education / Collaboration</p><h2>{E(T["practice_heading"])}</h2><div class="practice-cols"><div><div class="body">{paras(T["practice"])}</div><h3>{E(T["workshop_heading"])}</h3><p class="small">L.I.F.E. project, Performing Arts Forum, Saint-Erme, France. Initiated by Gabriel Catren.</p><div class="workshop-list">{rows(T["workshops"])}</div></div><div><h3 style="margin-top:0">Selected collaborations</h3><p class="small">Sound design and technological development in dialogue with the authors of these works.</p>{rows(T["collaborations"])}</div></div>'
    pages.append(page(10,'Research, teaching & collaboration',practice,'practice-page'))
    pages.append(page(11,'Selected CV',cv_content(),'cv-page'))
    last=f'<p class="eyebrow">Selected CV / Research</p><h2>{E(T["research_heading"])}</h2><div class="research-cols"><div class="body"><p>{E(T["research_intro"])}</p><h3>{E(T["current_heading"])}</h3><p>{E(T["current"])}</p>{contact()}<p class="doc-credit">Project photographs and stills supplied by Manuel Eguía. Authorship is credited on each project page. This selection draws on the artist’s dossiers and CV, with institutional records used to verify dates and credits.</p></div><div>{publications()}</div></div>'
    pages.append(page(12,'Research & contact',last,'research-page'))
    (DEST/'portfolio.html').write_text(document(''.join(pages),'Manuel Eguía — Portfolio'))
    cv1=page(1,'Selected CV',cv_content(),'cv-page').replace('01 / 12','01 / 02')
    cv2body=f'<p class="eyebrow">Manuel Camilo Eguía / Selected CV</p><div class="two-columns"><div><h3>Scientific publications</h3>{publications()}</div><div><h3>Selected artistic collaborations</h3>{rows(T["collaborations"])}{contact()}</div></div>'
    cv2=page(2,'Selected CV',cv2body,'cv-second').replace('02 / 12','02 / 02')
    (DEST/'cv.html').write_text(document(cv1+cv2,'Manuel Eguía — Selected CV'))
    if not args.proposal:
        print('Built 12-page portfolio and 2-page CV HTML masters.')
        return
    proposal=args.proposal.read_text()
    paragraphs=[x.strip() for x in proposal.split('\n\n') if x.strip()]
    clean=[]
    for x in paragraphs[2:]:
        x=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',x)
        x=x.replace('*Bending Pulses*','Bending Pulses').replace('“','“')
        clean.append(x)
    proposal_style=f'@font-face{{font-family:P;src:url("{ASSETS}fonts/LiberationSans-Regular.ttf")}}@page{{size:A4;margin:18mm 20mm}}*{{box-sizing:border-box}}body{{font-family:P,Arial,sans-serif;font-size:10.7pt;line-height:1.44;color:#202520;margin:0}}h1{{font-size:30pt;font-weight:400;letter-spacing:-.045em;margin:0 0 3mm}}.meta{{font-size:9pt;line-height:1.5;border-bottom:1px solid #adb4a7;padding-bottom:5mm;margin-bottom:6mm}}p{{margin:0 0 4mm}}footer{{font-size:8.4pt;border-top:1px solid #adb4a7;margin-top:6mm;padding-top:4mm}}a{{color:#85351f;text-decoration:none}}'
    proposal_html=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Bending Pulses — Manuel Eguía — Q-O2 2027</title><style>{proposal_style}</style></head><body><h1>Bending Pulses</h1><div class="meta">Q-O2 residency proposal, 2027<br>Manuel Eguía · Requested duration: four weeks · Accommodation not required<br>Portfolio: <a href="{D["base_url"]}">{D["base_url"]}</a></div>{paras(clean)}<footer>Manuel Eguía · <a href="mailto:{D["email"]}">{D["email"]}</a> · <a href="https://vimeo.com/meguia">Vimeo</a> · <a href="https://www.youtube.com/@manueleguia2915">YouTube</a></footer></body></html>'
    (DEST/'proposal.html').write_text(proposal_html)
    print('Built 12-page portfolio, 2-page CV and one-page proposal HTML masters.')

if __name__=='__main__': main()
