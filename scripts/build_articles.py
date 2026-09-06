"""Build the static Bloemfontein article hub and pages from content/articles.json."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
ORIGIN = 'https://boostechbloem.com'
ARTICLES = json.loads((ROOT / 'content/articles.json').read_text())
homepage = (DIST / 'index.html').read_text()
if 'href="/news-advice/"' not in homepage.split('</header>')[0]:
    homepage = homepage.replace('<a href="#questions">FAQs</a>', '<a href="#questions">FAQs</a><a href="/news-advice/">Articles</a>')
if 'href="/articles.css"' not in homepage:
    homepage = homepage.replace('</head>', '<link rel="stylesheet" href="/articles.css">\n</head>')
header = re.search(r'<header>.*?</header>', homepage, re.S).group()
header = header.replace('href="#"', 'href="/"')
header = re.sub(r'href="#([^\"]+)"', r'href="/#\1"', header)
footer = re.search(r'<footer>.*?</footer>', homepage, re.S).group()
if 'href="/news-advice/"' not in footer:
    footer = footer.replace('</footer>', '<a href="/news-advice/">Articles &amp; advice</a></footer>')
homepage = re.sub(r'<footer>.*?</footer>', lambda _: footer, homepage, flags=re.S)

def card(a):
    visual = ('<img src="' + escape(a['image'], quote=True) + '" alt="' + escape(a['image_alt'], quote=True) + '" loading="lazy" decoding="async">') if a['image'] else '<div class="article-card-type">AUDI · BMW · VW<br><strong>More than bakkies.</strong></div>'
    return f'<a class="article-card" href="/news-advice/{a["slug"]}/"><div class="article-card-image">{visual}</div><div class="article-card-copy"><p class="eyebrow">{escape(a["category"])}</p><h3>{escape(a["title"])}</h3><p>{escape(a["summary"])}</p><span class="article-card-read">Read article <span aria-hidden="true">↗</span></span></div></a>'

def layout(title, description, path, main, schema):
    return f'''<!doctype html>
<html lang="en-ZA"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#070c16">
<title>{escape(title)} | Boostech Bloemfontein</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{ORIGIN}{path}"><meta property="og:type" content="{'article' if path != '/news-advice/' else 'website'}"><meta property="og:site_name" content="Boostech Bloemfontein"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{ORIGIN}{path}">
<link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/articles.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-SJ8RNZBRSJ"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-SJ8RNZBRSJ');</script>
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script></head><body class="article-page"><a class="skip" href="#main">Skip to content</a>{header}<main id="main">{main}</main>{footer}</body></html>'''

hub_intro = '<section class="articles-intro"><p class="eyebrow">BOOSTECH BLOEMFONTEIN · ARTICLES &amp; ADVICE</p><h1>Know your vehicle.<br><em>Explore its potential.</em></h1><p>Vehicle guides, exhaust development and real-world stories from the Boostech network, with local advice for Bloemfontein and the Free State.</p></section>'
hub = hub_intro + '<section class="articles-hub" aria-label="All articles"><div class="article-card-grid">' + ''.join(card(a) for a in ARTICLES) + '</div></section>'
schema = {'@context':'https://schema.org','@type':'CollectionPage','name':'Articles & advice | Boostech Bloemfontein','url':ORIGIN+'/news-advice/','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':ORIGIN+'/news-advice/'+a['slug']+'/','name':a['title']} for i,a in enumerate(ARTICLES)]}}
(DIST/'news-advice').mkdir(exist_ok=True)
(DIST/'news-advice/index.html').write_text(layout('Articles & advice', 'Vehicle tuning guides, exhaust advice and Boostech network stories for Bloemfontein and the Free State.', '/news-advice/', hub, schema))

for a in ARTICLES:
    path = '/news-advice/'+a['slug']+'/'
    url = ORIGIN + path
    media = f'<figure class="article-hero-image"><img src="{escape(a["image"],quote=True)}" alt="{escape(a["image_alt"],quote=True)}" fetchpriority="high"></figure>' if a['image'] else '<div class="passenger-hero-panel"><span>Audi</span><span>BMW</span><span>Mercedes-Benz</span><span>Volkswagen</span><span>Petrol</span><span>Diesel</span></div>'
    hero = f'<section class="article-hero"><div><a class="article-back" href="/news-advice/">← All articles</a><p class="eyebrow">{escape(a["category"])}</p><h1>{escape(a["title"])}</h1><p class="article-intro">{escape(a["summary"])}</p><p class="article-byline">Boostech Bloemfontein · Knowledge from the Boostech network</p></div>{media}</section>'
    context = f'<p class="article-context">{escape(a["context"])}</p>' if a['context'] else ''
    share = f'<div class="article-share"><span>Share this article</span><a href="https://www.facebook.com/sharer/sharer.php?u={quote(url,safe="")}" target="_blank" rel="noopener noreferrer">Facebook</a><a href="https://wa.me/?text={quote(a["title"]+chr(10)+url,safe="")}" target="_blank" rel="noopener noreferrer">WhatsApp</a></div>'
    enquiry_url = '/?article=' + quote(a['title'], safe='') + '#contact'
    cta = f'<section class="article-local-contact"><p class="eyebrow">BLOEMFONTEIN · FREE STATE</p><h2>Let’s talk about your vehicle.</h2><p>Tell Pieter your vehicle’s year, make, model, engine, transmission and location. We’ll confirm compatibility, local availability and a quote for the work.</p><div class="article-contact-actions"><a class="button" href="{enquiry_url}">Enquire about your vehicle</a></div></section>'
    source = f'<p class="article-source">Adapted from <a href="{escape(a["source_url"],quote=True)}">the original Boostech article</a>. Vehicle photographs and development examples are shared from the Boostech network. Confirm the specification and suitability of your individual vehicle before booking.</p>'
    others = [x for x in ARTICLES if x['slug']!=a['slug']]
    related = sorted(others, key=lambda x: x['category'] != a['category'])[:3]
    more = '<section class="article-related"><h2>Keep exploring.</h2><div class="article-card-grid">'+''.join(card(x) for x in related)+'</div><a class="text-link" href="/news-advice/">View all articles →</a></section>'
    schema={'@context':'https://schema.org','@type':'Article','headline':a['title'],'description':a['summary'],'url':url,'mainEntityOfPage':url,'author':{'@type':'Organization','name':'Boostech Bloemfontein'},'publisher':{'@type':'Organization','name':'Boostech Bloemfontein','url':ORIGIN},'isBasedOn':a['source_url']}
    if a['image']:schema['image']=a['image']
    dest=DIST/path.strip('/')
    dest.mkdir(parents=True,exist_ok=True)
    dest.joinpath('index.html').write_text(layout(a['title'],a['summary'],path,'<article>'+hero+context+share+a['body']+cta+source+'</article>'+more,schema))

feature = '<!-- ARTICLES START --><section id="articles" class="home-articles"><div class="home-articles-heading"><div><p class="eyebrow">FROM THE BOOSTECH NETWORK</p><h2>Articles &amp; advice.</h2></div><a class="text-link" href="/news-advice/">Explore all '+str(len(ARTICLES))+' articles →</a></div><div class="article-card-grid">'+''.join(card(a) for a in ARTICLES[:3])+'</div></section><!-- ARTICLES END -->'
if '<!-- ARTICLES START -->' in homepage:
    homepage=re.sub(r'<!-- ARTICLES START -->.*?<!-- ARTICLES END -->',lambda _:feature,homepage,flags=re.S)
else:
    homepage=homepage.replace('<section id="contact"',feature+'\n<section id="contact"',1)
(DIST/'index.html').write_text(homepage.rstrip()+'\n')
urls=['/','/news-advice/']+['/news-advice/'+a['slug']+'/' for a in ARTICLES]
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+ORIGIN+u+'</loc></url>\n' for u in urls)+'</urlset>\n')
print(f'Built {len(ARTICLES)} articles, article hub, homepage feature and sitemap.')
