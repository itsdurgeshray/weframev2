#!/usr/bin/env python3
"""Builds the static pages from src/*.html by expanding <!--PARTIAL--> markers.
Run:  python3 build.py   (writes index.html, blog.html, sanity.html at the project root)
"""
import math, pathlib, re

ROOT = pathlib.Path(__file__).parent

# ---------- icons (Lucide-style, inline for Figma import) ----------
def ico(paths, sw=2, fill="none", vb="0 0 24 24", cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="{vb}" fill="{fill}" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')

I = {
  "ur": ico('<path d="M7 17 17 7M7 7h10v10"/>'),
  "r": ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
  "l": ico('<path d="M19 12H5M11 18l-6-6 6-6"/>'),
  "plus": ico('<path d="M12 5v14M5 12h14"/>'),
  "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>',
  "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2.5 2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3 6.1 20.6l1.3-6.6L2.5 9.4l6.6-.8z"/></svg>',
  "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="currentColor"/><path d="m7.5 12.5 3 3 6-6.5" fill="none" stroke="#010404" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  "verified": '<svg viewBox="0 0 24 24" aria-hidden="true" width="14" height="14"><path fill="#2E9AA0" d="M12 2l2.4 1.8 3-.2.9 2.9 2.5 1.7-1 2.8 1 2.8-2.5 1.7-.9 2.9-3-.2L12 22l-2.4-1.8-3 .2-.9-2.9-2.5-1.7 1-2.8-1-2.8 2.5-1.7.9-2.9 3 .2z"/><path d="m8.5 12 2.3 2.3 4.7-4.8" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  "linkedin": ico('<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M8 11v5M8 8v.01M12 16v-5M16 16v-3a2 2 0 0 0-4 0"/>', 1.8),
  "twitter": ico('<path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"/>', 1.8),
  "instagram": ico('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>', 1.8),
  "award": ico('<circle cx="12" cy="9" r="5"/><path d="m8.5 13.5-1.5 7 5-2.5 5 2.5-1.5-7"/>', 1.6),
}

TECH_MINI = ('<span class="icons"><i><img src="assets/svg/tile-icon-a.svg" alt=""></i>'
             '<i><img src="assets/svg/tile-icon-b.svg" alt=""></i><i><img src="assets/svg/tile-icon-next.svg" alt=""></i></span>')
CASE_P = ("Rebuilt the booking funnel on a headless stack paired with an organic content system. "
          "Rebuilt the booking funnel on a headless stack paired with an organic content system."
          "Rebuilt the booking funnel on a headless stack paired with an organic content system.")

# ---------- partials ----------
def case_card(img, video=False, chips=("travel", "A Series"), backed=False, short=False):
    shot = f'<img src="assets/img/{img}" alt="" loading="lazy" width="1200" height="800">'
    if video:
        shot += f'<span class="play"><span class="play-badge">{I["play"]}</span></span>'
    chip_html = "".join(f'<span class="chip xs">{c}</span>' for c in chips)
    if backed:
        chip_html = (f'<span class="chip xs">{chips[0]}</span>'
                     '<span class="chip xs backed">backed by <img src="assets/img/logo-yc.png" alt="Y Combinator" width="10" height="10"></span>')
    p = "Rebuilt the booking funnel on a headless stack paired with an organic content system." if short else CASE_P
    return f'''<article class="case glass rv">
          <div class="shot">{shot}</div>
          <div class="meta">
            <div class="row"><h3 class="h5">Unimig</h3><div class="chips">{chip_html}</div></div>
            <p>{p}</p>
            <div class="tiles">
              <div class="tile">{TECH_MINI}<span>tech stack</span></div>
              <div class="tile"><b>Health-Tech</b><span>industry</span></div>
              <div class="tile"><b>E-Commerce</b><span>project type</span></div>
            </div>
          </div>
          <a class="btn btn-line btn-sm" href="#">Read Full Case Study</a>
        </article>'''

def cases_home():
    return "\n        ".join([
        case_card("yt-top6.jpg", video=True, backed=True),
        case_card("shot-certify.jpg"), case_card("shot-luma.jpg"),
        case_card("shot-luma.jpg"), case_card("shot-unimig.jpg"), case_card("shot-certify.jpg")])

def cases_three():
    return "\n        ".join([case_card("shot-unimig.jpg", short=True), case_card("shot-certify.jpg", short=True), case_card("shot-luma.jpg", short=True)])

Q1 = ("In just six months, Ehroo helped us generate 300+ qualified meetings and significantly grow our visibility across AI search platforms. "
      "Working with their team has been one of the best growth decisions we've made. In just six months, Ehroo helped us generate 300+ qualified "
      "meetings and significantly grow our visibility across AI search platforms.")
Q2 = "Bishen and his team shared valuable insights regarding their vast experience with Directus. They are very capable"
Q3 = ("I highly recommend Bishen for any Builder.io and Next.js projects. Their work on our project was exceptional, delivering a high-quality, "
      "performant website that exceeded our expectations. They demonstrated excellent technical skills, clear communication, and a strong work "
      "ethic throughout the process. The developer's expertise in integrating Builder.io with Next.js resulted in a user-friendly, scalable "
      "solution that perfectly met our needs. Their proactive approach and ability to meet deadlines make them a valuable asset to any team. "
      "If you're looking for a skilled and reliable developer for your web projects, look no further!")
Q4 = ("Overall, the team demonstrated great attention to detail, excellent communication, and a commitment to delivering high-quality results "
      "on time. I look forward to working with them again on future projects.")

def review(qid, quote, chips, video=False, wide=False):
    stars = "".join([I["star"]] * 5)
    vid = (f'<div class="vid"><img src="assets/img/verdict-video.jpg" alt="Client video testimonial" loading="lazy" width="540" height="960">'
           f'<span class="play"><span class="play-badge aqua">{I["play"]}</span></span></div>') if video else ""
    ch = "".join(f'<span class="chip light">{c}</span>' for c in chips)
    body = quote if not video else f"{quote}<br><br>{quote}"
    long = len(body) > 260
    more = f'<button class="more" type="button" data-more="{qid}">Read more</button>' if long else ""
    return f'''<article class="review glass{'' if video else ' no-vid'}{' wide' if wide else ''}">
        {vid}
        <div class="body-col">
          <div class="brand"><span class="who"><img src="assets/img/logo-luma.png" alt="" width="32" height="32">Luma Travel</span><span class="chips">{ch}</span></div>
          <blockquote id="{qid}" class="clamp{' long' if long else ''}">{body}</blockquote>
          {more}
          <div class="person"><img src="assets/img/avatar-carl.jpg" alt="" width="32" height="32" loading="lazy"><div><b>Carl-Johan Larsson {I["verified"]}</b><span>Senior Partnership Manager, Velmie</span></div><span class="stars" aria-label="5 out of 5">{stars}</span></div>
          <div class="rv-svc"><span class="chip light">Headless Development</span><span class="chip light">SEO</span><span class="chip light">CRO</span></div>
        </div>
      </article>'''

def reviews(prefix="r"):
    cards = [review(f"{prefix}1", Q1, ["Series A", "Travel"], video=True, wide=True),
             review(f"{prefix}2", Q2, ["$165M Funding", "Travel"]),
             review(f"{prefix}3", Q3, ["$165M Funding", "Travel"]),
             review(f"{prefix}4", Q4, ["Series A", "Travel"])]
    return f'''<div class="rev-rail rail fade-x" data-rail>
      {''.join(cards)}
    </div>
    <div class="wrap"><div class="dots mobile-only" data-dots></div></div>'''

LOGOS = [("ll-2-90", "Bentley"), ("ll-3-124", "OnePlus"), ("ll-4-74", "Dubai"), ("ll-1-152", "Keeway"), ("ll-6-136", "Insta360")]
def logo_track(alt=True):
    one = "".join(f'<img src="assets/svg/{f}.svg" alt="{a if alt else ""}" height="30">' for f, a in LOGOS)
    two = "".join(f'<img src="assets/svg/{f}.svg" alt="" height="30">' for f, a in LOGOS)
    return f'<div class="marquee-track">{one}{two}</div>'

def ent():
    return f'''<div class="glass ent">
      <span class="ent-bg" aria-hidden="true"></span>
      <div class="copy">
        <span class="eyebrow sm">Enterprise ready</span>
        <h2 class="h3">Trusted By Investor-Backed And Enterprise Teams.</h2>
        <p>From seed-stage startups to Series C platforms, our clients are backed by investors who expect execution, not excuses.</p>
        <div class="btns"><a class="btn btn-aqua btn-sm" href="#contact">Book a Meeting</a><a class="btn btn-line btn-sm" href="#cases">Read Success Stories</a></div>
      </div>
      <div class="logos" aria-label="Clients">
        <div class="marquee">{logo_track()}</div>
        <div class="marquee rev">{logo_track(False)}</div>
      </div>
    </div>'''

LUCIDE = {
  "code": '<path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>',
  "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
  "users": '<path d="M18 21a8 8 0 0 0-16 0"/><circle cx="10" cy="8" r="5"/><path d="M22 20c0-3.37-2-6.5-4-8a5 5 0 0 0-.45-8.3"/>',
  "zap": '<path d="M15.914 4a1.5 1.5 0 00-2.474-1.561l-9 9A1.5 1.5 0 005.5 14h4.002a.5.5 0 01.471.666L8.086 20a1.5 1.5 0 002.475 1.56l9-9A1.5 1.5 0 0018.5 10h-3.997a.5.5 0 01-.472-.667z"/>',
  "headset": '<path d="M3 11h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5Zm0 0a9 9 0 1 1 18 0m0 0v5a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3Z"/><path d="M21 16v2a4 4 0 0 1-4 4h-5"/>',
  "clip": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
}
CMP = [("code", "Sanity-Certified Engineers", "Yes", "Sometimes", "Rarely"),
       ("box", "Dedicated Content Architecture", "Yes", "Rarely", "Sometimes"),
       ("users", "Design & Engineering - One Team", "Yes", "No", "Sometimes"),
       ("zap", "Typical Timelines", "4 to 8 weeks", "8 to 16 weeks", "12 to 24 weeks"),
       ("headset", "Post-Launch Support SLA", "Included", "No", "Add-On Cost"),
       ("clip", "Editor Training Included", "Yes", "Rarely", "Sometimes")]
CHECK = ('<svg class="ck" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="10" fill="#6BF1FF"/>'
         '<path d="m6 10.2 2.7 2.7L14 7.6" fill="none" stroke="#020B0C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def lu(k):
    return ('<svg class="fi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{LUCIDE[k]}</svg>')

def compare():
    logo = '<img src="assets/svg/table-logo.svg" alt="Weframetech" width="146" height="24">'
    esc = lambda t: t.replace("&", "&amp;")
    rows = "".join(
        f'<tr><th scope="row"><span>{lu(i)}{esc(f)}</span></th>'
        f'<td class="us"><span class="v">{CHECK}{u}</span></td><td><span class="v">{fr}</span></td><td><span class="v">{ag}</span></td></tr>'
        for i, f, u, fr, ag in CMP)
    items = "".join(
        f'<li><span class="lbl">{lu(i)}{esc(f)}</span><div class="cells">'
        f'<div class="c us"><span class="sr-only">Weframetech: </span><span class="v">{CHECK}{u}</span></div>'
        f'<div class="c"><span class="sr-only">Freelancer: </span><span class="v">{fr}</span></div>'
        f'<div class="c"><span class="sr-only">Traditional Agency: </span><span class="v">{ag}</span></div></div></li>'
        for i, f, u, fr, ag in CMP)
    head = ('<div class="section-head rv"><div class="stack"><span class="eyebrow">Why weframetech</span>'
            '<h2 class="h2">Compared To Freelancer Or<br class="hide-m"> Traditional Agency.</h2>'
            '<p class="body">Sanity work fails most often on the content model, not the front end. Here\'s where that actually gets built right.</p></div></div>')
    table = (f'<table class="cmp-t"><thead><tr><th scope="col">Features</th><th scope="col" class="us">{logo}</th>'
             f'<th scope="col">Freelancer</th><th scope="col">Traditional Agency</th></tr></thead><tbody>{rows}</tbody></table>')
    mob = (f'<div class="cmp-m"><div class="cmp-m-head" aria-hidden="true"><div>{logo}</div><div>Freelancer</div>'
           f'<div>Traditional Agency</div></div><ul>{items}</ul></div>')
    return f'{head}\n    <div class="compare rv">{table}{mob}</div>'

def founders():
    vids = [("438s3acHWK8", "yt-top6.jpg", "My Top 6 Fav headless tools"), ("vAJsOLVA5tM", "yt-vs.jpg", "Headless CMS comparison"),
            ("438s3acHWK8", "yt-top6.jpg", "My Top 6 Fav headless tools")]
    items = "".join(
        f'<a class="yt rv" href="https://www.youtube.com/watch?v={v}" data-yt="{v}" aria-label="Play video: {t}" target="_blank" rel="noopener">'
        f'<img src="assets/img/{img}" alt="" loading="lazy" width="960" height="540"><span class="yt-play"><img src="assets/svg/youtube.svg" alt="" width="64" height="64"></span></a>'
        for v, img, t in vids)
    return f'''<div class="section-head rv"><div class="stack"><span class="eyebrow">From Our Founders</span><h2 class="h2">Headless, AI, SEO, &amp; Product<br class="hide-m"> Engineering.</h2></div>
      <div class="rail-ctrl hide-m"><button class="rail-btn" data-prev aria-label="Previous">{I["l"]}</button><button class="rail-btn" data-next aria-label="Next">{I["r"]}</button></div></div>
    <div class="yt-rail rail" data-rail>{items}</div>
    <div class="dots mobile-only" data-dots></div>'''

STEPS = ["Discovery", "Strategy", "UX/UI Design", "Engineering", "Growth", "Launch"]
def gantt():
    out = []
    for i, s in enumerate(STEPS):
        out.append(f'''<div class="g-row" role="listitem" style="--i:{i}">
        <span class="g-lbl">{s}</span>
        <div class="g-track"><div class="g-bar"><span class="g-wk">Week 3-4</span><b>Execute and compound</b><span class="g-ico">{I["award"]}</span></div></div>
      </div>''')
    return "\n      ".join(out)

def faq():
    a = ("Choosing the right Sanity CMS agency can have a significant impact on your website's performance, content management experience, "
         "and long-term scalability. Whether you're building a marketing website, ecommerce storefront, enterprise platform, or a headless "
         "digital experience, partnering with an experienced Sanity CMS agency ensures your content infrastructure is flexible, future-proof, and easy to manage.")
    items = "".join(
        f'<details class="rv"{" open" if i == 0 else ""}><summary>Looking for the Best Sanity CMS Agency in Bangalore?<i>{I["plus"]}</i></summary><div class="ans">{a}</div></details>'
        for i in range(5))
    return f'<h2 class="h3-md rv" style="margin-bottom:var(--sec-head)">Frequently Asked Questions</h2><div class="faq">{items}</div>'

def footer():
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="top">
      <div class="brand-col">
        <img src="assets/svg/wft-mark.svg" alt="Weframe Tech" width="60" height="60">
        <p><span>Interested working together ?</span> trying out our platform or contact us.</p>
        <div class="social"><a href="#" aria-label="LinkedIn">{I["linkedin"]}</a><a href="#" aria-label="Twitter">{I["twitter"]}</a><a href="#" aria-label="Instagram">{I["instagram"]}</a></div>
      </div>
      <div class="cols">
        <div><h5>Services</h5><ul><li><a href="#">Headless Ecom</a></li><li><a href="#">UI/UX Designing</a></li><li><a href="#">CTO as a Service</a></li><li><a href="#">Jamstack Development</a></li><li><a href="#">MVP &amp; POC Development</a></li><li><a href="#">Custom Software Development</a></li></ul></div>
        <div><h5>About</h5><ul><li><a href="blog.html">Blogs</a></li><li><a href="#">About us</a></li><li><a href="#">Case Studies</a></li><li><a href="#">Get Instant Quotation</a></li></ul></div>
        <div><h5>Help</h5><ul><li><a href="#">Careers</a></li><li><a href="#">Contact Us</a></li><li><a href="#">Book a Call</a></li></ul></div>
      </div>
    </div>
    <div class="word" aria-hidden="true">Weframetech</div>
    <div class="bottom"><span>@2026 All Right Reserved</span><span class="pw"><img src="assets/svg/powered-by-directus.svg" alt="Powered by directus" width="180" height="18"></span></div>
  </div>
</footer>'''


def nav(cta="Get Instant Quote", here=""):
    ur = I["ur"]
    links = [("Services", "index.html#services"), ("Case Studies", "index.html#cases"), ("Blogs", "blog.html"), ("About Us", "index.html#team"), ("Contact", "index.html#contact")]
    top = "".join(f'<a href="{h}"{" aria-current=\"page\"" if t == here else ""}>{t}</a>' for t, h in links)
    sheet = "".join(f'<a href="{h}">{t} {ur}</a>' for t, h in links)
    return f'''<header class="nav">
  <div class="wrap">
    <a class="nav-logo" href="index.html" aria-label="Weframe Tech home"><img src="assets/img/logo-weframetech.png" alt="weframetech" width="162" height="30"></a>
    <nav class="nav-menu" aria-label="Primary">{top}</nav>
    <div class="nav-cta">
      <a class="btn btn-aqua" href="index.html#contact">{cta}</a>
      <button class="menu-btn" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="sheet" role="dialog" aria-label="Menu">
  <nav>{sheet}</nav>
  <div class="sheet-foot">
    <a class="btn btn-aqua btn-block" href="index.html#contact">Book a Call</a>
    <a class="btn btn-white btn-block" href="sanity.html#pricing">Our Pricing</a>
    <p>#1 Directus Partner</p>
  </div>
</div>'''


def wave():
    import random
    rnd = random.Random(7)
    hs = [max(18, min(100, int(40 + 55 * abs(math.sin(i * .55)) * rnd.uniform(.5, 1.1)))) for i in range(64)]
    return "".join(f'<i style="--h:{h};--d:{i}"></i>' for i, h in enumerate(hs))


def portfolio():
    items = [("shot-unimig.jpg", "logo-unimig.png", "Unimig"), ("shot-certify.jpg", "logo-certify.png", "CertifyOS"),
             ("shot-luma.jpg", "logo-luma.png", "Luma Travel"), ("shot-unimig.jpg", "logo-unimig.png", "Unimig")]
    return "".join(f'''<a class="pf glass rv" href="index.html#cases"><span class="pf-shot"><img src="assets/img/{s}" alt="{n} website" loading="lazy" width="1200" height="800"></span>
        <span class="pf-foot"><span class="br"><img src="assets/img/{l}" alt="" width="28" height="28"><b>{n}</b></span><span class="chip xs">travel</span></span></a>''' for s, l, n in items)

def clients():
    items = [("logo-certify.png", "CertifyOS", "Public", "pub"), ("logo-luma.png", "Luma Travel", "Public", "pub"), ("logo-unimig.png", "Unimig", "private/nda", "nda")]
    return "".join(f'''<article class="client glass rv">
        <div class="cl-head"><span class="br"><img src="assets/img/{l}" alt="" width="28" height="28"><b>{n}</b></span><span class="status {c}"><i></i>{st}</span></div>
        <div class="tiles">
          <div class="tile">{TECH_MINI}<span>tech stack</span></div>
          <div class="tile"><b>Health-Tech</b><span>industry</span></div>
          <div class="tile"><b>A-Series</b><span>funding</span></div>
        </div>
        <a class="btn btn-line btn-sm btn-block" href="#">Read Full Case Study</a>
      </article>''' for l, n, st, c in items)

def logotrack():
    seq = [("ll-1-152", "Keeway"), ("ll-2-90", "Bentley"), ("ll-3-124", "OnePlus"), ("ll-4-74", "Dubai"), ("ll-1-152", "Keeway"), ("ll-6-136", "Insta360"), ("ll-2-90", "Bentley")]
    a = "".join(f'<img src="assets/svg/{f}.svg" alt="{n}" height="28">' for f, n in seq)
    b = "".join(f'<img src="assets/svg/{f}.svg" alt="" height="28">' for f, n in seq)
    return f'<div class="marquee-track">{a}{b}</div>'

# ---------- tech wheel ----------
CATS = ["Frontend", "Backend", "Design", "Headless CMS", "Marketing", "Data & DevOps", "CMS", "SEO", "Composable Commerce"]
def wheel():
    import json
    raw = (ROOT / "assets/js/wheel-data.js").read_text()
    data = json.loads(raw[raw.index("=") + 1:].strip().rstrip(";"))
    cats, icons = data["cats"], data["icons"]
    C, R, r, n, gap, rl = 382, 382, 317, len(cats), 0.8, 349.5
    def pt(rad, ang):
        a = math.radians(ang)
        return C + rad * math.cos(a), C + rad * math.sin(a)
    groups = []
    for i, c in enumerate(cats):
        mid = -90 + i * 360 / n
        a0, a1 = mid - 180 / n + gap, mid + 180 / n - gap
        x0, y0 = pt(R, a0); x1, y1 = pt(R, a1); x2, y2 = pt(r, a1); x3, y3 = pt(r, a0)
        d = f"M {x0:.2f} {y0:.2f} A {R} {R} 0 0 1 {x1:.2f} {y1:.2f} L {x2:.2f} {y2:.2f} A {r} {r} 0 0 0 {x3:.2f} {y3:.2f} Z"
        sx, sy = pt(rl, mid - 180 / n); ex, ey = pt(rl, mid + 180 / n)
        arc = f"M {sx:.2f} {sy:.2f} A {rl} {rl} 0 0 1 {ex:.2f} {ey:.2f}"
        name = c["n"].replace("&", "&amp;")
        pressed = "true" if i == 0 else "false"
        groups.append(f'<g class="seg-g" role="button" tabindex="0" aria-label="{name}" aria-pressed="{pressed}" data-i="{i}">'
                      f'<path class="seg" d="{d}"/><path id="wl{i}" d="{arc}" fill="none"/>'
                      f'<text class="lbl" dominant-baseline="central"><textPath href="#wl{i}" startOffset="50%" text-anchor="middle">{name}</textPath></text></g>')
    first = cats[0]
    lis = "".join(f'<li>{icons[t]}<span class="sr-only">{t}</span></li>' for t in first["items"])
    defs = ('<svg class="wf-defs" width="0" height="0" aria-hidden="true"><defs><linearGradient id="wfGrad" x1="0.5" y1="0" x2="0.5" y2="1.13">'
            '<stop offset="0" stop-color="#AAF7FF"/><stop offset="1" stop-color="#004A52"/></linearGradient></defs></svg>')
    svg = (f'<svg class="wheel" viewBox="0 0 764 764" role="group" aria-label="Tech stack categories">'
           f'<g class="ring" data-ring style="transform:rotate(0deg)">{"".join(groups)}</g></svg>')
    badge = f'<div class="w-badge" aria-hidden="true"><span class="w-bi" data-w-badge>{first["badge"]}</span></div>'
    core = (f'<div class="w-core"><span class="eyebrow">Tech stack</span><div class="w-swap" data-w-swap>'
            f'<h3 class="w-title" data-w-title>{first["n"]}</h3>'
            f'<ul class="w-icons" data-w-icons aria-label="{first["n"]} technologies" style="grid-template-columns:repeat({len(first["items"])},max-content)">{lis}</ul>'
            f'</div></div>')
    return "\n      ".join([defs, svg, badge, core])

PARTIALS = {
    "CASES": cases_home, "CASES3": cases_three, "REVIEWS": reviews, "ENT": ent, "COMPARE": compare,
    "FOUNDERS": founders, "GANTT": gantt, "FAQ": faq, "FOOTER": footer, "WHEEL": wheel,
    "NAV": lambda: nav(), "PORTFOLIO": portfolio, "CLIENTS": clients, "LOGOTRACK": logotrack, "WAVE": wave, "NAVBLOG": lambda: nav(here="Blogs"), "NAVMEET": lambda: nav("Book a Meeting", "Services"),
}

def build():
    for src in sorted(p for p in (ROOT / "src").glob("*.html") if not p.name.startswith("_")):
        html = src.read_text()
        html = re.sub(r"<!--([A-Z0-9]+)-->", lambda m: PARTIALS[m.group(1)]() if m.group(1) in PARTIALS else m.group(0), html)
        bad = [c for c in ("—", "–") if c in html]
        (ROOT / src.name).write_text(html)
        print(f"built {src.name} ({len(html)//1024} KB){'  WARNING dashes: ' + str(bad) if bad else ''}")

if __name__ == "__main__":
    build()
