"""Build stealthsecurityar.com into ../public. Run: python3 src/build.py"""
import json, os, shutil, html
from datetime import date
from content import SITE, SERVICES, PRICING, PRICING_NOTES, ADDONS, ADDON_NOTES, INDUSTRIES, TOWNS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
FORM_ENDPOINT = os.environ.get("FORM_ENDPOINT", "")  # set when a lead endpoint exists
E = html.escape
PAGES = []  # paths for sitemap

ICONS = {
 "flame": '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.2 1-3.6 2.2-4.8.3 1.7 1.2 2.6 2.3 3C10.8 8.6 11 5.8 12 3z"/>',
 "shield": '<path d="M12 3l7 3v5.5c0 4.4-3 8.1-7 9.5-4-1.4-7-5.1-7-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
 "camera": '<rect x="3" y="7" width="13" height="10" rx="2"/><path d="M16 11l5-3v8l-5-3"/>',
 "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l8-8M16 7l2 2M14 9l2 2"/>',
 "server": '<rect x="4" y="4" width="16" height="7" rx="1.5"/><rect x="4" y="13" width="16" height="7" rx="1.5"/><path d="M8 7.5h.01M8 16.5h.01"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
}
def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

def nav():
    svc = "".join(f'<li><a href="/services/{s["slug"]}">{E(s["short"])}</a></li>' for s in SERVICES)
    ind = "".join(f'<li><a href="/industries/{i["slug"]}">{E(i["name"])}</a></li>' for i in INDUSTRIES)
    towns = "".join(f'<li><a href="/service-areas/{t["slug"]}">{E(t["name"])}</a></li>' for t in TOWNS)
    login = (f'<li><a href="{SITE["app_url"]}/">Employee login</a></li>'
             f'<li><a href="{SITE["app_url"]}/p/">Customer IT Help</a></li>'
             f'<li><a href="{SITE["app_url"]}/p/approve">Approve IT requests</a></li>')
    def dd(label, href, items):
        return (f'<li class="dd"><a href="{href}">{label}</a>'
                f'<button class="dd-t" aria-expanded="false" aria-label="Show {label} menu">'
                f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10l5 5 5-5"/></svg></button>'
                f'<ul class="dd-m">{items}</ul></li>')
    return f"""<header class="site-h">
<div class="topbar"><div class="wrap"><a href="tel:{SITE['phone_tel']}">{icon('phone')}{SITE['phone_display']}</a><a href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a><a class="tb-login" href="{SITE['app_url']}/">{icon('user')}Login</a></div></div>
<div class="wrap navrow">
<a class="brand" href="/" aria-label="Stealth Security home"><img class="mark" src="/assets/mark-light.png" alt="" width="34" height="42"><span class="word"><span class="w1">Stealth</span><span class="w2">Security</span></span></a>
<button class="menu-t" aria-expanded="false" aria-controls="mainnav">Menu</button>
<nav id="mainnav" aria-label="Main"><ul class="nav">
<li><a href="/">Home</a></li>
{dd('Services','/services',svc)}
<li><a href="/managed-it-pricing">IT Pricing</a></li>
{dd('Industries','/industries',ind)}
{dd('Service Areas','/service-areas',towns)}
<li><a href="/about">About</a></li>
{dd('Login', SITE['app_url'] + '/', login)}
<li><a class="btn btn-sm" href="/contact">Get a Quote</a></li>
</ul></nav></div></header>"""

def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}">{E(s["short"])}</a></li>' for s in SERVICES)
    towns = "".join(f'<li><a href="/service-areas/{t["slug"]}">{E(t["name"])}</a></li>' for t in TOWNS)
    return f"""<footer class="site-f"><div class="wrap fgrid">
<div><p class="brand"><img class="mark" src="/assets/mark-light.png" alt="" width="30" height="37"><span class="word"><span class="w1">Stealth</span><span class="w2">Security</span></span></p><p>{E(SITE['tagline'])}</p><p class="lic-f">{icon('shield')}Licensed by the {SITE['license_by']}<br>{SITE['license_class']}<br>License {SITE['license_no']}</p>
<p><a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a><br><a href="mailto:{SITE['email']}">{SITE['email']}</a><br>{SITE['city']}, Arkansas</p>
<p><a href="{SITE['facebook']}" rel="noopener">Facebook</a></p></div>
<div><h2>Services</h2><ul>{svc}</ul></div>
<div><h2>Company</h2><ul><li><a href="{SITE['app_url']}/">Employee login</a></li><li><a href="{SITE['app_url']}/p/">Customer IT Help</a></li><li><a href="/about">About</a></li><li><a href="/managed-it-pricing">IT Pricing</a></li><li><a href="/industries">Industries</a></li><li><a href="/contact">Contact</a></li></ul></div>
<div><h2>Service Areas</h2><ul>{towns}</ul></div>
</div><div class="wrap legal">© {date.today().year} {E(SITE['legal'])}. All rights reserved.</div></footer>"""

def cta_band(text="Ready to protect your property?", sub=None):
    sub = sub or f"Call {SITE['phone_display']} or request a free quote."
    return f"""<section class="band"><div class="wrap band-in"><div><h2>{E(text)}</h2><p>{E(sub)}</p></div>
<div class="btns"><a class="btn" href="/contact">Request a Free Quote</a><a class="btn btn-ghost" href="tel:{SITE['phone_tel']}">{icon('phone')}{SITE['phone_display']}</a></div></div></section>"""

def license_strip():
    return (f'<section class="lic"><div class="wrap lic-in">{icon("shield","ico-lg")}<p><b>State licensed alarm systems company.</b> '
            f'Stealth Security is licensed by the {SITE["license_by"]} as a {SITE["license_class"]}, '
            f'license number <b>{SITE["license_no"]}</b>.</p></div></section>')

def crumbs(items):
    lis = "".join((f'<li><a href="{h}">{E(n)}</a></li>' if h else f'<li aria-current="page">{E(n)}</li>') for n, h in items)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": SITE['url'] + h} if h else {})}
        for i, (n, h) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>', ld

def hero(eyebrow, h1, lead, crumb_html="", buttons=True):
    b = (f'<div class="btns"><a class="btn" href="/contact">Request a Free Quote</a>'
         f'<a class="btn btn-ghost" href="tel:{SITE["phone_tel"]}">{icon("phone")}Call {SITE["phone_display"]}</a></div>') if buttons else ""
    return f"""<section class="hero"><div class="wrap">{crumb_html}<p class="eyebrow">{E(eyebrow)}</p><h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>{b}</div></section>"""

BUSINESS_LD = {
    "@context": "https://schema.org", "@type": ["LocalBusiness", "ProfessionalService"],
    "name": SITE["name"], "legalName": SITE["legal"], "url": SITE["url"] + "/",
    "telephone": SITE["phone_tel"], "email": SITE["email"],
    "address": {"@type": "PostalAddress", "addressLocality": SITE["city"], "addressRegion": SITE["region"], "addressCountry": "US"},
    "areaServed": [t["name"] + ", AR" if t["slug"] != "northwest-arkansas" else "Northwest Arkansas" for t in TOWNS],
    "sameAs": [SITE["facebook"]],
    "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
        "name": "Class E Alarm Systems Company License (Unrestricted) " + SITE["license_no"],
        "recognizedBy": {"@type": "GovernmentOrganization", "name": "Arkansas State Police"}},
    "description": "Security systems, commercial fire alarm, CCTV surveillance, access control and managed IT services in Arkansas.",
}

def page(path, title, desc, body, ld=None):
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, separators=(",", ":"))}</script>' for x in (ld or []))
    canon = SITE["url"] + (path if path != "/" else "/")
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:site_name" content="Stealth Security">
<meta name="theme-color" content="#16181c"><link rel="icon" href="/assets/favicon-48.png" type="image/png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><meta property="og:image" content="{SITE['url']}/assets/logo-dark.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=Jost:wght@500;700&family=Source+Sans+3:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">{lds}</head>
<body><a class="skip" href="#main">Skip to content</a>{nav()}<main id="main">{body}</main>{footer()}<script src="/assets/site.js" defer></script></body></html>"""
    d = os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(doc)
    PAGES.append(path)

def ul(items):
    return '<ul class="ticks">' + "".join(f"<li>{icon('check')}{E(x)}</li>" for x in items) + "</ul>"

def svc_cards(services):
    return '<div class="cards">' + "".join(
        f'<a class="card" href="/services/{s["slug"]}">{icon(s["icon"], "ico-lg")}<h3>{E(s["short"])}</h3><p>{E(s["card"])}</p><span class="more">Learn more →</span></a>'
        for s in services) + "</div>"

def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "src", "assets"), os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(ROOT, "src", "assets", "favicon-48.png"), os.path.join(OUT, "favicon.ico"))

    # Home
    towns = "".join(f'<a class="chip" href="/service-areas/{t["slug"]}">{icon("pin")}{E(t["name"])}</a>' for t in TOWNS)
    inds = "".join(f'<li><a href="/industries/{i["slug"]}">{E(i["name"])}</a></li>' for i in INDUSTRIES)
    body = hero("Arkansas security & technology",
                "Security, Fire Alarm, Surveillance & Managed IT for Arkansas",
                "Professionally installed security systems, commercial fire alarms, surveillance cameras, access control and managed IT services from one local company.") + license_strip() + f"""
<section class="sec"><div class="wrap"><p class="eyebrow">What we do</p><h2 class="h2">Our services</h2>{svc_cards(SERVICES)}</div></section>
<section class="sec alt"><div class="wrap split"><div><p class="eyebrow">Local advantage</p><h2 class="h2">Why Stealth Security</h2>
<p>Unlike national providers, Stealth Security delivers local service, support and accountability. Security, life safety and IT are handled under one roof, so one team knows your whole building.</p>
<a class="btn" href="/contact">Request a Free Quote</a></div>
{ul(["Arkansas based", f"Licensed by the Arkansas State Police (License {SITE['license_no']})", "Commercial and residential", "Local support", "Security, life safety and IT under one roof"])}</div></section>
<section class="sec"><div class="wrap split"><div><p class="eyebrow">Who we serve</p><h2 class="h2">Industries</h2><ul class="links">{inds}</ul></div>
<div><p class="eyebrow">Where we work</p><h2 class="h2">Service area</h2><div class="chips">{towns}</div></div></div></section>
{cta_band()}"""
    page("/", "Arkansas Security, Fire Alarm, Surveillance & Managed IT | Stealth Security",
         "Arkansas-based security systems, commercial fire alarm, CCTV surveillance, access control and managed IT services. Call 1-479-746-8298 for a free quote.",
         body, [BUSINESS_LD])

    # Services index + pages
    c, ld = crumbs([("Home", "/"), ("Services", None)])
    page("/services", "Security, Fire Alarm & IT Services | Stealth Security Arkansas",
         "Fire alarm, security systems, CCTV, access control and managed IT services from Stealth Security in Arkansas.",
         hero("Services", "Security, life safety and IT services", "Everything that protects your building and keeps your business running, from one local company.", c)
         + f'<section class="sec"><div class="wrap">{svc_cards(SERVICES)}</div></section>' + cta_band(), [ld])
    for s in SERVICES:
        c, ld = crumbs([("Home", "/"), ("Services", "/services"), (s["short"], None)])
        groups = "".join(f'<div class="group"><h3>{E(h)}</h3>{ul(items)}</div>' for h, items in s["groups"])
        brands = (f'<div class="brands"><h2 class="h3">Supported manufacturers and platforms</h2><p>' + " · ".join(E(b) for b in s["brands"]) + "</p></div>") if s["brands"] else ""
        f = s.get("feature")
        feat = (f'<section class="sec feat-sec"><div class="wrap split"><div><p class="eyebrow">{E(f["eyebrow"])}</p><h2 class="h2">{E(f["title"])}</h2>'
                f'<p class="lead-d">{E(f["lead"])}</p><a class="btn" href="/contact">{E(f["cta"])}</a></div>{ul(f["points"])}</div></section>') if f else ""
        prods = ""
        if s.get("products"):
            prods = ('<section class="sec"><div class="wrap"><p class="eyebrow">What we install</p><h2 class="h2">Products we work with</h2><div class="prods">'
                     + "".join(f'<article class="prod"><h3>{E(n)}</h3><p class="by">{E(by)}</p><p>{E(t)}</p></article>' for n, by, t in s["products"])
                     + '</div><p class="note">Product names are trademarks of their respective owners.</p></div></section>')
        others = [o for o in SERVICES if o["slug"] != s["slug"]]
        prose = "".join(f"<p>{E(p)}</p>" for p in s["body"])
        pricing_link = '<p><a class="btn btn-ghost-dark" href="/managed-it-pricing">See managed IT pricing</a></p>' if s["slug"] == "managed-it" else ""
        svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["title"], "serviceType": s["short"],
                  "provider": {"@type": "LocalBusiness", "name": SITE["name"], "telephone": SITE["phone_tel"], "url": SITE["url"] + "/"},
                  "areaServed": "Arkansas", "description": s["meta"]}
        body = hero(s["short"], s["title"], s["lead"], c) + f"""
<section class="sec"><div class="wrap narrow prose">{prose}{pricing_link}</div></section>
<section class="sec alt"><div class="wrap"><div class="groups">{groups}</div>{brands}</div></section>
{license_strip() if s["slug"] != "managed-it" else ""}
{feat}
{prods}
<section class="sec"><div class="wrap"><h2 class="h2">Other services</h2>{svc_cards(others)}</div></section>
{cta_band(s['cta'].capitalize() + ".")}"""
        page(f"/services/{s['slug']}", f"{s['title']} | Stealth Security Arkansas", s["meta"], body, [ld, svc_ld])

    # Pricing
    c, ld = crumbs([("Home", "/"), ("IT Pricing", None)])
    tiers = "".join(f"""<div class="tier{' feat' if p['featured'] else ''}">{'<p class="flag">Most popular</p>' if p['featured'] else ''}
<h2 class="h3">{E(p['name'])}</h2><p class="price">{E(p['price'])} <span>{E(p['unit'])}</span></p>
{f'<p class="intro">{E(p["intro"])}</p>' if p['intro'] else ''}{ul(p['items'])}
<p class="best"><b>Best for:</b> {E(p['best'])}</p><a class="btn{'' if p['featured'] else ' btn-ghost-dark'}" href="/contact">Get started</a></div>""" for p in PRICING)
    addons = "".join(f"""<div class="addon"><h3 class="h3">{E(a['group'])}</h3><p>{E(a['lead'])}</p>
<div class="ptable-wrap"><table class="ptable"><thead><tr><th scope="col">Service</th><th scope="col">Standard</th><th scope="col">Schools &amp; nonprofits</th></tr></thead><tbody>
{"".join(f'<tr><th scope="row">{E(r[0])}<span>{E(r[1])}</span></th><td>{E(r[2])}</td><td class="edu">{E(r[3])}</td></tr>' for r in a['rows'])}
</tbody></table></div></div>""" for a in ADDONS)
    page("/managed-it-pricing", "Managed IT Pricing | Stealth Security Arkansas",
         "Managed IT for Arkansas businesses from $55 per device per month, with Malwarebytes and offsite backup included. Help desk plans from $125 per user.",
         hero("Managed IT", "Managed IT pricing", "Predictable monthly support, priced per device.", c, buttons=False)
         + f'<section class="sec"><div class="wrap"><div class="tiers">{tiers}</div><ul class="pnotes">{"".join(f"<li>{icon('check')}{E(n)}</li>" for n in PRICING_NOTES)}</ul></div></section>'
         + f'<section class="sec alt" id="add-ons"><div class="wrap"><h2>Malwarebytes and offsite backup on their own</h2><p class="lead-sm">Already have IT staff? Add our endpoint protection or cloud backup without a full managed plan.</p><div class="addons">{addons}</div><ul class="pnotes">{"".join(f"<li>{icon('check')}{E(n)}</li>" for n in ADDON_NOTES)}</ul></div></section>'
         + cta_band("Schedule a free IT assessment."), [ld])

    # About
    c, ld = crumbs([("Home", "/"), ("About", None)])
    page("/about", "About Stealth Security | Arkansas Security & Managed IT",
         "Stealth Security is an Arkansas-based security and technology company in Clarksville serving businesses and homes across the state.",
         hero("About us", "About Stealth Security", "An Arkansas-based security and technology company providing protection for businesses and homes throughout the state.", c, buttons=False)
         + f"""<section class="sec"><div class="wrap split"><div class="prose"><p>We focus on reliable installation, responsive local support and long-term customer relationships.</p>
<p>Most companies hire one vendor for fire alarms, another for cameras and a third for computers. Stealth Security handles security, life safety and IT under one roof, so there is one local team that knows your whole building and one number to call.</p>
<p>We are based in {SITE['city']}, Arkansas, and serve customers across the River Valley and beyond.</p></div>
<div><h2 class="h3">What we do</h2>{ul([s['short'] for s in SERVICES])}</div></div></section>""" + f"""
<section class="sec alt"><div class="wrap narrow"><p class="eyebrow">Licensing</p><h2 class="h2">State licensed</h2>
<p>Arkansas requires companies that sell, install and service alarm systems to be licensed by the Arkansas State Police under A.C.A. § 17-40-101 et seq. Stealth Security holds that license:</p>
<dl class="lic-dl"><dt>Licensed name</dt><dd>Stealth Security-Arkansas</dd><dt>License type</dt><dd>{SITE['license_class']}</dd><dt>License number</dt><dd>{SITE['license_no']}</dd><dt>Issued by</dt><dd>{SITE['license_by']}</dd></dl></div></section>""" + cta_band(), [ld, BUSINESS_LD])

    # Contact
    c, ld = crumbs([("Home", "/"), ("Contact", None)])
    opts = "".join(f"<option>{E(s['short'])}</option>" for s in SERVICES) + "<option>Multiple services</option>"
    page("/contact", "Contact Stealth Security | Request a Quote",
         "Request a free quote for security, fire alarm, camera, access control or managed IT services. Call 1-479-746-8298.",
         hero("Get in touch", "Request a quote", "Tell us about your building or project and we'll get back to you.", c, buttons=False)
         + f"""<section class="sec"><div class="wrap split contact">
<div><h2 class="h3">Contact information</h2><ul class="contact-list">
<li>{icon('phone')}<a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></li>
<li>{icon('mail')}<span class="sel">{SITE['email']}</span></li>
<li>{icon('pin')}{SITE['city']}, Arkansas</li></ul>
<h2 class="h3">Services we offer</h2>{ul([s['short'] for s in SERVICES])}</div>
<form id="quote" class="form" data-endpoint="{E(FORM_ENDPOINT)}" data-email="{SITE['email']}" novalidate>
<h2 class="h3">Request a quote</h2>
<label for="f-name">Name *</label><input id="f-name" name="name" autocomplete="name" required>
<label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required>
<label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel">
<label for="f-town">City or town</label><input id="f-town" name="town" autocomplete="address-level2">
<label for="f-svc">Service of interest</label><select id="f-svc" name="service"><option value="">Select a service…</option>{opts}</select>
<label for="f-msg">Message *</label><textarea id="f-msg" name="message" rows="5" required></textarea>
<input type="text" name="company_website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn" type="submit">Send message</button>
<p class="form-status" role="status" aria-live="polite"></p></form></div></section>""", [ld])

    # Industries
    c, ld = crumbs([("Home", "/"), ("Industries", None)])
    icards = '<div class="cards">' + "".join(f'<a class="card" href="/industries/{i["slug"]}"><h3>{E(i["name"])}</h3><p>{E(i["lead"])}</p><span class="more">Learn more →</span></a>' for i in INDUSTRIES) + "</div>"
    page("/industries", "Industries We Serve | Stealth Security Arkansas",
         "Security, fire alarm and IT solutions for Arkansas healthcare, schools, churches, retail, restaurants, warehouses, construction and offices.",
         hero("Industries", "Industries we serve", "Every kind of building has different risks. We design systems around how yours is used.", c, buttons=False)
         + f'<section class="sec"><div class="wrap">{icards}</div></section>' + cta_band(), [ld])
    for i in INDUSTRIES:
        c, ld = crumbs([("Home", "/"), ("Industries", "/industries"), (i["name"], None)])
        page(f"/industries/{i['slug']}", f"Security & IT for {i['name']} | Stealth Security Arkansas", i["meta"],
             hero("Industries", f"Security and IT for {i['name'].lower()}", i["lead"], c)
             + f'<section class="sec"><div class="wrap split"><div><h2 class="h3">What we typically set up</h2>{ul(i["needs"])}</div><div><h2 class="h3">Related services</h2>{svc_cards(SERVICES[:5])}</div></div></section>'
             + cta_band(), [ld])

    # Service areas
    c, ld = crumbs([("Home", "/"), ("Service Areas", None)])
    tcards = '<div class="cards">' + "".join(f'<a class="card" href="/service-areas/{t["slug"]}">{icon("pin","ico-lg")}<h3>{E(t["name"])}</h3><p>Serving {E(t["nearby"])}.</p><span class="more">Learn more →</span></a>' for t in TOWNS) + "</div>"
    page("/service-areas", "Service Areas | Stealth Security Arkansas",
         "Stealth Security serves Clarksville, Russellville, Ozark, Fort Smith and Northwest Arkansas.",
         hero("Service areas", "Where we work", f"Based in {SITE['city']}, serving the Arkansas River Valley and Northwest Arkansas.", c, buttons=False)
         + f'<section class="sec"><div class="wrap">{tcards}</div></section>' + cta_band(), [ld])
    for t in TOWNS:
        c, ld = crumbs([("Home", "/"), ("Service Areas", "/service-areas"), (t["name"], None)])
        prose = "".join(f"<p>{E(p)}</p>" for p in t["paras"])
        place = t["name"] + (", AR" if t["slug"] != "northwest-arkansas" else "")
        town_ld = dict(BUSINESS_LD, areaServed=place)
        body = hero("Service areas", f"Security, Fire Alarm & IT Services in {place}", f"Professional security, fire alarm, surveillance and managed IT services for businesses and homes in {t['area']}.", c) + f"""
<section class="sec"><div class="wrap split"><div class="prose">{prose}<p><b>Also serving:</b> {E(t['nearby'])}.</p></div>
<div><h2 class="h3">Services in {E(t['name'])}</h2>{ul(['Fire alarm installation and inspection', 'Security system installation', 'CCTV and surveillance cameras', 'Access control systems', 'Managed IT services', 'Local support and service'])}</div></div></section>
<section class="sec alt"><div class="wrap"><h2 class="h2">Our services</h2>{svc_cards(SERVICES)}</div></section>
{cta_band(f"Need security or IT help in {t['name']}?")}"""
        page(f"/service-areas/{t['slug']}", f"Security & Fire Alarm Services in {place} | Stealth Security", t["meta"], body, [ld, town_ld])

    # 404, robots, sitemap
    page("/404-page", "Page not found | Stealth Security", "Page not found.",
         hero("404", "Page not found", "That page moved or doesn't exist. Try the menu above, or call us.", "", True))
    shutil.move(os.path.join(OUT, "404-page", "index.html"), os.path.join(OUT, "404.html"))
    os.rmdir(os.path.join(OUT, "404-page")); PAGES.remove("/404-page")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    today = date.today().isoformat()
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in PAGES:
            f.write(f"<url><loc>{SITE['url']}{p if p != '/' else '/'}</loc><lastmod>{today}</lastmod></url>\n")
        f.write("</urlset>\n")
    base = os.environ.get("BASE_PATH", "").rstrip("/")
    if base:  # preview at a sub-path, e.g. GitHub Pages project URL
        for dp, _, fs in os.walk(OUT):
            for fn in fs:
                if fn.endswith(".html"):
                    fp = os.path.join(dp, fn); t = open(fp).read()
                    t = t.replace('href="/', f'href="{base}/').replace('src="/', f'src="{base}/')
                    t = t.replace(f'href="{base}//', 'href="//')
                    open(fp, "w").write(t)
    if os.environ.get("CUSTOM_DOMAIN"):
        open(os.path.join(OUT, "CNAME"), "w").write(os.environ["CUSTOM_DOMAIN"] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print(f"Built {len(PAGES)} pages into {OUT}")

if __name__ == "__main__":
    build()
