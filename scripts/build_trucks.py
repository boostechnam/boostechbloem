"""Build the Bloemfontein truck page using the shared header and enquiry form."""
from pathlib import Path
from html import escape
import re, json
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
home=(DIST/'index.html').read_text()
header=re.search(r'<header>.*?</header>',home,re.S).group().replace('href="#"','href="/"')
header=re.sub(r'href="#([^\"]+)"',r'href="/#\1"',header)
header=header.replace('href="/truck-eco-tuning/"','href="/truck-eco-tuning/" aria-current="page"')
footer=re.search(r'<footer>.*?</footer>',home,re.S).group()
form=re.search(r'<form id="bloem-enquiry".*?</form>',home,re.S).group()
form=form.replace('aria-label="Vehicle enquiry"','aria-label="Truck and fleet enquiry"').replace('All fields are required except additional details.','Complete your vehicle details and location. Fleet information and additional details are optional.')
form=re.sub(r'<select id="enquiry-service".*?</select>','<select id="enquiry-service" name="service"><option>Truck eco tuning</option><option>Fleet tuning assessment</option><option>Truck diagnostics and fault assessment</option></select>',form)
for a,b in [('e.g. Toyota','e.g. Volvo'),('e.g. Hilux','e.g. FH 520'),('e.g. 2.8 GD-6','Engine size or code'),('Your name</label>','Your name or company</label>')]:form=form.replace(a,b)
extra=''
for name,label,placeholder in [('fleetSize','Fleet size','e.g. 10 trucks'),('monthlyKm','Km per truck / month','e.g. 10,000 km'),('consumption','Current fuel use','e.g. 35 L/100 km'),('routes','Typical payload and routes','e.g. 34 tonnes, Bloemfontein to Durban')]:
 extra+=f'<div class="enquiry-field"><label for="enquiry-{name}">{label} <span>(optional)</span></label><input id="enquiry-{name}" name="{name}" data-enquiry-label="{label}" type="text" maxlength="240" placeholder="{placeholder}"></div>'
form=form.replace('<div class="enquiry-field enquiry-full"><label for="enquiry-notes">',extra+'<div class="enquiry-field enquiry-full"><label for="enquiry-notes">')
form=form.replace('Tell us about your goals, existing modifications or any warning lights.','Tell us your goals, fault codes, symptoms or existing modifications.')
faqs=[
('Can you assess my truck for tuning?','Send the make, model, year, engine, transmission and location. Compatibility and the scope of work are confirmed for the individual truck before booking.'),
('Is a fuel saving guaranteed?','No. Payload, route, driver behaviour, speed, tyres, weather and mechanical condition all affect fuel consumption. The calculator is a planning tool. Compare logged fuel records under similar operating conditions to measure the actual change.'),
('Does eco tuning mean reducing power?','The focus is usable torque in the engine’s working range and improved loaded drivability. The calibration is matched to the vehicle and its duty cycle, rather than simply reducing power or pursuing a maximum output figure.'),
('Can we begin with one truck?','Yes. A representative vehicle gives you a practical baseline for deciding on a wider fleet rollout. Include your fleet size and usual routes in the enquiry.'),
('What if the truck already has warning lights or smoke?','Include fault codes and symptoms when you contact us. Mechanical and diagnostic concerns should be assessed before tuning; additional fuel is not a remedy for an existing engine fault.'),
('How do I request a quote in Bloemfontein?','Complete the truck enquiry form with your vehicle details and typed location. Choose WhatsApp, Gmail in your browser or your configured email app, then review and send the prepared message to Pieter.')]
faq_html=''.join('<details><summary>'+escape(q)+'</summary><p>'+escape(a)+'</p></details>' for q,a in faqs)
main=(ROOT/'content/truck-page.html').read_text().replace('{{FORM}}',form).replace('{{FAQ}}',faq_html)
url='https://boostechbloem.com/truck-eco-tuning/'
title='Truck Tuning & Fleet Fuel Economy | Boostech Bloemfontein'
description='Truck ECU tuning and fleet economy assessments in Bloemfontein and the Free State. Explore usable torque, fuel savings and a calculator in rand.'
schema={'@context':'https://schema.org','@graph':[{'@type':'Service','name':'Truck eco tuning in Bloemfontein','url':url,'description':description,'provider':{'@type':'Organization','name':'Boostech Bloemfontein','url':'https://boostechbloem.com/'},'areaServed':['Bloemfontein','Free State'],'image':'https://boostechbloem.com/assets/trucks/scania-fleet.webp'},{'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]}]}
page=f'''<!doctype html><html lang="en-ZA"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#070c16"><title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://boostechbloem.com/assets/trucks/scania-fleet.webp"><meta property="og:image:alt" content="Scania fleet with side-tipper trailers"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/trucks.css"><link rel="stylesheet" href="/enquiry.css?v=2"><script defer src="/trucks.js"></script><script defer src="/enquiry.js?v=3"></script><script async src="https://www.googletagmanager.com/gtag/js?id=G-SJ8RNZBRSJ"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-SJ8RNZBRSJ');</script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body class="truck-page"><a class="skip" href="#main">Skip to content</a>{header}<main id="main">{main}</main>{footer}</body></html>'''
(DIST/'truck-eco-tuning').mkdir(exist_ok=True)
(DIST/'truck-eco-tuning/index.html').write_text(page)
print('Built truck eco tuning page with shared fleet enquiry and local photos.')
