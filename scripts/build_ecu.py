"""Build the ECU tuning page from shared navigation and the existing enquiry form."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
home = (DIST / 'index.html').read_text()
header = re.search(r'<header>.*?</header>', home, re.S).group().replace('href="#"', 'href="/"')
header = re.sub(r'href="#([^\"]+)"', r'href="/#\1"', header)
header = header.replace('href="/ecu-remapping/"', 'href="/ecu-remapping/" aria-current="page"')
footer = re.search(r'<footer>.*?</footer>', home, re.S).group()
form = re.search(r'<form id="bloem-enquiry".*?</form>', home, re.S).group()
form = form.replace('aria-label="Vehicle enquiry"', 'aria-label="ECU tuning enquiry"')
faqs = [
    ('What is ECU tuning?', 'ECU tuning changes the software calibration that controls the engine. On a compatible vehicle, coordinated changes to torque request, air and fuel control can improve usable performance and response. The correct approach depends on the engine, ECU, transmission and hardware.'),
    ('Why invest in your own calibrated dynamometer?', 'It gives us a controlled, repeatable environment for development and comparison. We can evaluate the torque curve and power delivery while refining a calibration, instead of judging the result only by a peak number or how fast the vehicle feels.'),
    ('Will my vehicle need dyno testing?', 'The testing plan is agreed for the specific vehicle and the work required. Development, fault investigation and modified setups can have different requirements from a supported application using established development. Ask us what testing and reporting your quote includes.'),
    ('How much power or torque will I gain?', 'We confirm a realistic target once we know the exact vehicle and setup. Fuel, condition, ECU version and hardware all affect the outcome. Photographs show workshop applications; they are not promises of a particular power figure.'),
    ('Can you tune for towing and everyday driving?', 'Yes. Tell us how the vehicle is used so that the proposed calibration can focus on useful torque, progressive response and suitable delivery under load. Gearbox-related changes depend on the platform and available ECU or TCU support.'),
    ('Do I need an exhaust before a Stage 1 remap?', 'Many compatible, mechanically standard vehicles can use an appropriate Stage 1 calibration. Hardware requirements are assessed individually. If the vehicle is already modified, the software must be matched to that setup.'),
    ('What if my vehicle already has a fault or another tune?', 'Include any warning lights, symptoms, tuning boxes or existing software in your enquiry. Mechanical faults need proper assessment; a remap is not a repair for a boost leak, worn component or transmission problem.'),
    ('How do I book ECU tuning in Bloemfontein?', 'Complete the enquiry form with your vehicle details and typed location. Choose WhatsApp or email, review the prepared message and send it to Pieter. Compatibility, the proposed work and pricing are confirmed before booking.'),
]
faq_html = ''.join('<details><summary>' + escape(q) + '</summary><p>' + escape(a) + '</p></details>' for q, a in faqs)
main = (ROOT / 'content/ecu-page.html').read_text().replace('{{FAQ}}', faq_html).replace('{{FORM}}', form)
url = 'https://boostechbloem.com/ecu-remapping/'
title = 'ECU Tuning Bloemfontein | In-House Dyno Development | Boostech'
description = 'ECU tuning in Bloemfontein with in-house calibration development and our own calibrated dynamometer. Explore vehicle-specific remapping for bakkies, SUVs and cars.'
schema = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'Service', 'name': 'ECU tuning in Bloemfontein', 'url': url, 'description': description,
     'provider': {'@type': 'Organization', 'name': 'Boostech Bloemfontein', 'url': 'https://boostechbloem.com/'}, 'areaServed': ['Bloemfontein', 'Free State']},
    {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]},
]}
page = f'''<!doctype html><html lang="en-ZA"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#070c16"><title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="Boostech Bloemfontein"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{url}"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/ecu.css"><link rel="stylesheet" href="/enquiry.css?v=2"><script defer src="/enquiry.js?v=3"></script><script async src="https://www.googletagmanager.com/gtag/js?id=G-SJ8RNZBRSJ"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-SJ8RNZBRSJ');</script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body class="ecu-page"><a class="skip" href="#main">Skip to content</a>{header}<main id="main">{main}</main>{footer}</body></html>'''
(DIST / 'ecu-remapping').mkdir(exist_ok=True)
(DIST / 'ecu-remapping/index.html').write_text(page)
print('Built ECU tuning page with shared enquiry form and workshop photos.')
