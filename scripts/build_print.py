#!/usr/bin/env python3
"""Generate fixed-page HTML masters for PDF printing (not published)."""
from pathlib import Path
from html import escape as E
import json
import re
import argparse
from text_links import institutional_text

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'working/print'
D=json.loads((ROOT/'content/portfolio.json').read_text())
T=D['en']
ASSETS=(ROOT/'assets').as_uri()+'/'

def img(name,cls='',alt=''):
    return f'<img src="{ASSETS}images/{name}" class="{cls}" alt="{E(alt)}">'

def paras(items, linked=False):
    format_text=institutional_text if linked else E
    return ''.join(f'<p>{format_text(x)}</p>' for x in items)

def links(p):
    return '<div class="links">'+''.join(f'<a class="text-link" href="{E(x["url"])}">{E(x["en"])} ↗</a>' for x in p['links'])+'</div>'

def footer(n,title,total=None):
    count=f'{total:02d}' if total is not None else '__PAGE_COUNT__'
    return f'<footer class="page-footer"><span>{E(D["name"])} / {E(title)}</span><span>{n:02d} / {count}</span></footer>'

def page(n,title,body,cls='',total=None):
    return f'<section class="page {cls}">{body}{footer(n,title,total)}</section>'

def head(p):
    q=p['en']
    return f'<header class="page-head"><p class="eyebrow">Selected work {p["number"]} / {p["year"]}</p><h2>{E(q["title"])}</h2><div class="subtitle">{E(q["subtitle"])}</div><div class="credits">{E(p["credit"])}</div></header>'

def facts(p):
    q=p['en']
    return '<div class="facts">'+''.join(f'<p><strong>{T["labels"][k]}</strong>{E(q[k])}</p>' for k in ['role','context'])+'</div>'

def work(n,p,cls=''):
    q=p['en']
    photo=img(p['image'],'main-photo',q['alt'])
    if p.get('hero_pair'):
        photo=f'<div class="print-photo-pair">{img(p["image"],"",q["alt"])}{img(p["hero_pair"],"",q["hero_pair_alt"])}</div>'
    if p.get('preview_link'):
        photo=f'<a href="{E(p["preview_link"])}">{photo}</a>'
    credit='<br>'+E(q['image_credit']) if q.get('image_credit') else ''
    body=head(p)+f'<div class="work-grid"><figure>{photo}<figcaption class="caption">{E(q["medium"])}{credit}</figcaption>{links(p)}</figure><div class="work-copy"><p class="summary">{E(q["summary"])}</p>{paras(q["body"])}{facts(p)}</div></div>'
    return page(n,q['title'],body,cls)

def rows(items):
    s=''
    for x in items:
        s+=f'<div class="print-row"><span class="year">{E(x["year"])}</span><div><h4>{institutional_text(x["title"])}</h4>'
        if x.get('artist'): s+=f'<p>{E(x["artist"])}</p>'
        s+=f'<p>{institutional_text(x["detail"])}</p></div></div>'
    return s

def publications():
    s='<ol class="research-list">'
    for p in D['publications']:
        s+=f'<li><span class="year">{p["year"]}</span><div><div class="pub-title"><a href="{p["url"]}">{E(p["title"])}</a></div><div class="pub-meta">{E(p["authors"])} · {E(p["journal"])}</div></div></li>'
    return s+'</ol>'

def contact():
    return f'<div class="contact-block"><a class="email" href="mailto:{D["email"]}">{D["email"]}</a><p><a href="{D["base_url"]}">meguia.github.io/dossier</a><br><a href="https://vimeo.com/meguia">vimeo.com/meguia</a><br><a href="https://www.youtube.com/@manueleguia2915">youtube.com/@manueleguia2915</a></p></div>'

def cv_content():
    return f'<p class="eyebrow">{E(D["name"])} / Buenos Aires, Argentina</p><h2>Selected CV</h2><p class="cv-intro">{E(T["cv_intro"])}</p><div class="cv-columns"><div><h3>Research &amp; teaching</h3>{rows(T["positions"])}<p class="programme">{E(T["programme"])}</p><h3>Education</h3>{rows(T["education"])}</div><div><h3>Exhibitions, residencies &amp; support</h3>{rows(T["highlights"])}</div></div>'

def document(body,title,total=None):
    if total is not None:
        body=body.replace('__PAGE_COUNT__',f'{total:02d}')
    return f'<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>{E(title)}</title><link rel="stylesheet" href="{ASSETS}print.css"></head><body>{body}</body></html>'

def main():
    global DEST
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'build/print')
    parser.add_argument('--proposal',type=Path,help='Optional local residency-proposal Markdown; never copied into the website.')
    args=parser.parse_args()
    DEST=args.output_dir
    DEST.mkdir(parents=True,exist_ok=True)
    projects={p['id']:p for p in D['projects']};pages=[]
    sonic=projects['sonic-crystal-room'];transit_project=projects['transit'];grapa_project=projects['grapa'];biocenosis=projects['biocenosis']
    wind=projects['wind-chimes'];iris=projects['iris']
    contents_items=''.join(f'<li><p class="work-index">{p["number"]} / {p["year"]}</p><a href="{D["base_url"]}works/{p["id"]}/">{E(p["en"]["title"])} ↗</a><p class="work-description">{E(p["en"]["subtitle"])}</p></li>' for p in D['projects'])
    contents=f'<p class="eyebrow">{E(D["name"])} / Portfolio</p><p class="contents-intro">{E(T["intro"])}</p><div class="contents-links"><a href="{D["base_url"]}">Website ↗</a><a href="{D["base_url"]}downloads/Manuel-Eguia-CV.pdf">Selected CV ↗</a></div><h2>{E(T["work_heading"])}</h2><ol class="work-contents">{contents_items}</ol>'
    pages.append(page(len(pages)+1,'Selected works',contents,'contents-page'))
    statement=f'<div class="about-print-grid"><figure>{img("portrait.jpg","about-print-portrait",D["name"])}</figure><div class="about-print-copy"><p class="eyebrow">{E(T["about_heading"])}</p><h2>{E(T["statement_title"])}</h2><div class="body">{paras(T["statement"],linked=True)}</div></div></div>'
    pages.append(work(len(pages)+1,sonic))
    detail=f'<p class="eyebrow">Sonic Crystal Room / Acoustic architecture</p><div class="detail-grid">{img("sonic-columns.jpg","",sonic["en"]["detail_alt"])}<div class="detail-text"><h2>{E(sonic["en"]["detail_title"])}</h2>{paras(sonic["en"]["detail"])}{img("sonic-red.jpg","detail-small","Sonic Crystal Room, rotating columns illuminated in red.")}<p class="caption">Mobile structures, changing acoustic perspectives.<br>{E(D["name"])} / Oscar Edelstein</p></div></div>'
    pages.append(page(len(pages)+1,'Sonic Crystal Room',detail,'image-detail'))
    pages.append(work(len(pages)+1,wind,'wind-main'))
    wd=wind['en']
    wind_detail=f'<p class="eyebrow">The Wind Chimes / Collective construction and performance</p><div class="detail-grid"><figure>{img(wind["detail_image"],"wind-portrait",wd["detail_alt"])}<figcaption class="caption">{E(wd["image_credit"])}</figcaption></figure><div class="detail-text"><h2>{E(wd["detail_title"])}</h2>{paras(wd["detail"])}{links(wind)}</div></div>'
    pages.append(page(len(pages)+1,'The Wind Chimes',wind_detail,'image-detail wind-detail'))
    pages.append(work(len(pages)+1,iris,'iris-page'))
    pages.append(work(len(pages)+1,transit_project))
    td=transit_project['en']
    labels=['01 / A familiar room','02 / Spatial transformation','03 / Returning from outside']
    sequence=''.join(f'<figure>{img(name,"",td["title"]+" — "+labels[i])}<figcaption>{labels[i]}</figcaption></figure>' for i,name in enumerate(transit_project['gallery']))
    transit=f'<p class="eyebrow">Transit / Site-specific virtual reality</p><h2>{E(td["detail_title"])}</h2><div class="two-columns"><div class="body">{paras(td["detail"])}</div><div><p class="large-summary">A virtual journey that begins<br>and ends in the same room.</p><p class="small muted">First episode: iM Konsthall, Moskosel, Sweden, 2023.<br>{E(D["name"])} / Mauro Zannoli<br>Commission: Northern Sustainable Futures</p>{links(transit_project)}</div></div><div class="transit-sequence">{sequence}</div>'
    pages.append(page(len(pages)+1,'Transit',transit,'transit-detail'))
    pages.append(work(len(pages)+1,grapa_project,'grapa-main'))
    gd=grapa_project['en'];step_names=['01 / Immersive recording','02 / Acoustic survey','03 / Documentary']
    steps=''.join(f'<div class="process-step"><p class="eyebrow">{step_names[i]}</p><p>{E(txt)}</p></div>' for i,txt in enumerate(gd['detail']))
    grapa=f'<header class="page-head"><p class="eyebrow">Proyecto GRAPa / Fieldwork, April 2018</p><h2>{E(gd["detail_title"])}</h2></header><div class="process-grid"><div>{img("grapa-fieldwork.jpg","field-photo",gd["detail_alt"])}<div class="process-pair">{img("grapa-acoustics.jpg","","Acoustic measurement equipment in the natural amphitheatre.")}{img("grapa-coplera.jpg","","A coplera with her caja at Quebrada de las Conchas.")}</div><p class="caption">La Copla y el Anfiteatro de la Quebrada de las Conchas · Salta, Argentina<br>GRAPa, with Mariana Carrizo and local copleras and copleros.</p></div><div>{steps}<p class="small"><strong>Founder:</strong> {E(D["name"])}<br>Team: Francisco Durante, Damián Payo, Mauro Zannoli and {E(D["name"])}.</p></div></div>'
    pages.append(page(len(pages)+1,'Proyecto GRAPa',grapa,'grapa-process'))
    pages.append(work(len(pages)+1,biocenosis,'biocenosis'))
    pages.append(page(len(pages)+1,T['about_heading'],statement,'about-page'))
    practice=f'<p class="eyebrow">Laboratory / Education / Collaboration</p><h2>{E(T["practice_heading"])}</h2><div class="practice-cols"><div><div class="body">{paras(T["practice"],linked=True)}<h3>{E(T["current_heading"])}</h3><p>{E(T["current"])}</p><p>{E(T["collab_intro"])}</p></div></div><div><h3 class="collaboration-heading">{E(T["collab_heading"])}</h3>{rows(T["collaborations"])}</div></div>'
    pages.append(page(len(pages)+1,T['practice_heading'],practice,'practice-page'))
    workshops=f'<p class="eyebrow">International workshops / Saint-Erme, France</p><h2>{E(T["workshop_heading"])}</h2><div class="workshops-print-grid"><div class="body"><p>{E(T["workshop_intro"])}</p></div><div class="workshop-list">{rows(T["workshops"])}</div></div>'
    pages.append(page(len(pages)+1,T['workshop_heading'],workshops,'workshops-page'))
    pages.append(page(len(pages)+1,'Selected CV',cv_content(),'cv-page'))
    last=f'<p class="eyebrow">Selected CV / Research</p><h2>{E(T["research_heading"])}</h2><div class="research-cols"><div class="body"><p>{E(T["research_intro"])}</p>{contact()}<p class="doc-credit">Work and image credits appear on the relevant project pages.</p></div><div>{publications()}</div></div>'
    pages.append(page(len(pages)+1,'Research & contact',last,'research-page'))
    (DEST/'portfolio.html').write_text(document(''.join(pages),D['name']+' — Portfolio',len(pages)))
    cv1=page(1,'Selected CV',cv_content(),'cv-page',total=2)
    cv2body=f'<p class="eyebrow">{E(D["name"])} / Selected CV</p><div class="two-columns"><div><h3>Scientific publications</h3>{publications()}</div><div><h3>{E(T["collab_heading"])}</h3>{rows(T["collaborations"])}{contact()}</div></div>'
    cv2=page(2,'Selected CV',cv2body,'cv-second',total=2)
    (DEST/'cv.html').write_text(document(cv1+cv2,D['name']+' — Selected CV'))
    if not args.proposal:
        print(f'Built {len(pages)}-page portfolio and 2-page CV HTML masters.')
        return
    proposal=args.proposal.read_text()
    paragraphs=[x.strip() for x in proposal.split('\n\n') if x.strip()]
    clean=[]
    for x in paragraphs[2:]:
        x=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',x)
        x=x.replace('*Bending Pulses*','Bending Pulses').replace('“','“')
        clean.append(x)
    proposal_style=f'@font-face{{font-family:P;src:url("{ASSETS}fonts/LiberationSans-Regular.ttf")}}@page{{size:A4;margin:18mm 20mm}}*{{box-sizing:border-box}}body{{font-family:P,Arial,sans-serif;font-size:10.7pt;line-height:1.44;color:#202520;margin:0}}h1{{font-size:30pt;font-weight:400;letter-spacing:-.045em;margin:0 0 3mm}}.meta{{font-size:9pt;line-height:1.5;border-bottom:1px solid #adb4a7;padding-bottom:5mm;margin-bottom:6mm}}p{{margin:0 0 4mm}}footer{{font-size:8.4pt;border-top:1px solid #adb4a7;margin-top:6mm;padding-top:4mm}}a{{color:#85351f;text-decoration:none}}'
    proposal_html=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Bending Pulses — {E(D["name"])} — Q-O2 2027</title><style>{proposal_style}</style></head><body><h1>Bending Pulses</h1><div class="meta">Q-O2 residency proposal, 2027<br>{E(D["name"])} · Requested duration: four weeks · Accommodation not required<br>Portfolio: <a href="{D["base_url"]}">{D["base_url"]}</a></div>{paras(clean)}<footer>{E(D["name"])} · <a href="mailto:{D["email"]}">{D["email"]}</a> · <a href="https://vimeo.com/meguia">Vimeo</a> · <a href="https://www.youtube.com/@manueleguia2915">YouTube</a></footer></body></html>'
    (DEST/'proposal.html').write_text(proposal_html)
    print(f'Built {len(pages)}-page portfolio, 2-page CV and one-page proposal HTML masters.')

if __name__=='__main__': main()
