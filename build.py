#!/usr/bin/env python3
"""Builds the Lowercase site (index, privacy, terms) from the markdown drafts in the app repo.
Usage: python3 build.py --email you@example.com --date "November 23, 2026"
"""
import argparse, html, re, pathlib
ap = argparse.ArgumentParser(); ap.add_argument("--email", required=True); ap.add_argument("--date", required=True)
a = ap.parse_args()
src = pathlib.Path("../BlankLauncher/legal")
css = """*{box-sizing:border-box}body{margin:0;background:#000;color:#f5f5f5;font:17px/1.6 -apple-system,system-ui,Helvetica,Arial,sans-serif}
main{max-width:640px;margin:0 auto;padding:48px 24px 80px}h1{font-size:34px;font-weight:500;line-height:1.15;margin:0 0 8px}
h2{font-size:21px;font-weight:500;margin:36px 0 6px}p,li{color:#c9c9c9}a{color:#f5f5f5}ul,ol{padding-left:22px}
nav{margin-bottom:40px;font-size:15px}nav a{margin-right:18px;color:#8c8c8c;text-decoration:none}small{color:#777}em{color:#8c8c8c}"""
def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    t = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1">\1</a>', t)
    return t
def md(text):
    out, lst = [], None
    for line in text.splitlines():
        if line.startswith("# "): out.append(f"<h1>{inline(line[2:])}</h1>"); continue
        if line.startswith("## "): out.append(f"<h2>{inline(line[3:])}</h2>"); continue
        m = re.match(r"(\d+)\. (.*)", line)
        if m:
            if lst != "ol": out.append("<ol>"); lst = "ol"
            out.append(f"<li>{inline(m.group(2))}</li>"); continue
        if lst: out.append(f"</{lst}>"); lst = None
        if line.strip(): out.append(f"<p>{inline(line)}</p>")
    if lst: out.append(f"</{lst}>")
    return "\n".join(out)
def page(title, body, root):
    nav = f'<nav><a href="{root}">lowercase</a><a href="{root}privacy/">privacy</a><a href="{root}terms/">terms</a></nav>'
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style></head><body><main>{nav}{body}</main></body></html>'
def doc(name):
    t = (src / name).read_text()
    t = re.sub(r"^\*Draft.*\*\n", "", t, flags=re.M)          # drop the draft banner
    return t.replace("[support email]", a.email).replace("[date]", a.date)
for name, folder, title in [("privacy-policy.md", "privacy", "Privacy Policy"), ("terms-of-use.md", "terms", "Terms of Use")]:
    p = pathlib.Path(folder); p.mkdir(exist_ok=True)
    (p / "index.html").write_text(page(f"Lowercase: {title}", md(doc(name)), "../"))
home = f"""<h1>lowercase</h1><p>a home screen made of words.<br>nothing else.</p>
<p>Lowercase turns your iPhone's apps into plain text: a quiet, full-screen launcher with themes, a keyboard and a notes widget.</p>
<h2>support</h2><p>Questions or problems: <a href="mailto:{a.email}">{a.email}</a></p>
<p><small>Austin Insurance Group LLC</small></p>"""
pathlib.Path("index.html").write_text(page("Lowercase", home, "./"))
print("built: index.html privacy/ terms/")
