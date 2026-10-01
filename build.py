"""Render content/*.md into resume.html, cv.html and bio.html, then print resume.pdf.

Edit the Markdown in content/, then run:  python build.py
Needs: pip install markdown; Chromium (or Chrome) for the PDF step.
"""
import pathlib, shutil, subprocess, markdown

ROOT = pathlib.Path(__file__).parent
PAGES = [("resume", "Resume"), ("cv", "CV"), ("bio", "Bio")]

CSS = """
:root{--bg:#faf9f5;--ink:#1c1c1a;--muted:#5c5850;--rule:#e2ddd1;--acc:#2f5f7d}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161614;--ink:#ecebe6;--muted:#a9a396;--rule:#34332f;--acc:#8fb8d6}}
:root[data-theme="dark"]{--bg:#161614;--ink:#ecebe6;--muted:#a9a396;--rule:#34332f;--acc:#8fb8d6}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Georgia,ui-serif,serif}
main{max-width:760px;margin:0 auto;padding:32px 16px 80px}
nav{font:14px ui-sans-serif,system-ui,sans-serif;margin:0 0 2rem;display:flex;flex-wrap:wrap;gap:.4rem 1rem}
nav a{color:var(--acc);text-decoration:none}
nav a[aria-current]{color:var(--ink);font-weight:600}
h1{font-size:1.9rem;margin:0 0 .3rem;letter-spacing:-.01em}
h2{font:600 .8rem ui-sans-serif,system-ui,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:2.2rem 0 .7rem;border-bottom:1px solid var(--rule);padding-bottom:.35rem}
h3{font-size:1.02rem;margin:1.2rem 0 .3rem}
p{margin:.4rem 0}
ul{margin:.25rem 0 .5rem 1.2rem;padding:0}
li{margin:.18rem 0}
a{color:var(--acc)}
hr{border:0;border-top:1px solid var(--rule);margin:2rem 0}
footer{margin-top:3rem;color:var(--muted);font:13px ui-sans-serif,system-ui,sans-serif}
@media print{
 @page{size:letter;margin:.45in .5in}
 :root{--bg:#fff;--ink:#000;--muted:#333;--rule:#bbb;--acc:#000}
 body{font-size:10pt;line-height:1.32}
 h1{font-size:17pt;margin:0}
 h3{margin:.5rem 0 .1rem;font-size:10pt}
 li{margin:.05rem 0}
 p{margin:.15rem 0}
 main{max-width:none;padding:0}
 nav,footer{display:none}
 h2{margin:.7rem 0 .25rem;padding-bottom:.15rem}
 a{text-decoration:none}
}
"""

def nav(current):
    items = [("index.html", "Home")] + [(f"{s}.html", t) for s, t in PAGES] + [("resume.pdf", "Resume (PDF)")]
    cur = ' aria-current="page"'
    return "<nav>" + "".join(
        f'<a href="{h}"{cur if h == current + ".html" else ""}>{t}</a>' for h, t in items
    ) + "</nav>"

import re

def prep(md):
    # Python-Markdown needs a blank line before a list that follows a paragraph line.
    md = re.sub(r"(?m)^(?![ \t]*[-*] |[ \t]*$)(.+)\n(?=[-*] )", r"\1\n\n", md)
    # ...and 4-space indents for nested lists; the sources use 2.
    return re.sub(r"(?m)^((?:  )+)(?=[-*] )", lambda m: "    " * (len(m.group(1)) // 2), md)

for slug, title in PAGES:
    body = markdown.markdown(prep((ROOT / "content" / f"{slug}.md").read_text()), extensions=["extra", "sane_lists"])
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Adam W. Stauffer</title>
<style>{CSS}</style>
</head>
<body>
<main>
{nav(slug)}
{body}
<footer>© 2026 Adam W. Stauffer. All rights reserved.</footer>
</main>
</body>
</html>
"""
    (ROOT / f"{slug}.html").write_text(html)
    print("wrote", f"{slug}.html")

chrome = next((p for p in ["chromium", "chromium-browser", "google-chrome", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"] if shutil.which(p) or pathlib.Path(p).exists()), None)
if chrome:
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={ROOT / 'resume.pdf'}", (ROOT / "resume.html").resolve().as_uri()],
                   check=True, capture_output=True)
    print("wrote resume.pdf")
else:
    print("no Chromium found; resume.pdf not rebuilt")
