import toml
from datetime import date

phon = toml.load("phonetic.toml")
blurb = open("site_data/blurb.html", encoding="utf-8").read()

def render_section(title, items):
    html = f"<h2>{title}</h2><ul>"
    for item in items:
        comp = item['component']
        used = ", ".join(item['used_in'])
        html += f"<li><strong>{comp}</strong>: {used}"
        if 'readings' in item:
            readings = ", ".join(item['readings'])
            html += f" (Readings: {readings})"
        if 'reason' in item:
            html += f" — <em>{item['reason']}</em>"
        html += "</li>\n"
    html += "</ul>"
    return html

html = "<!DOCTYPE html>\n"
html += "<html><head><link rel=\"stylesheet\" href=\"styles.css\"><meta charset='UTF-8'><title>Kanji Components</title></head><body>"
html += "<p>This site is a work in progress. Report any issues on <a href=\"https://github.com/j-ac/KanjiComponents/issues\">github</a>: </p>"
html += "<h1>Kanji - The Way They Were Meant To Be</h1>"
html += blurb
html += render_section("Useful Phonetic Components", phon.get("useful", []))
html += render_section("Non-Useful Phonetic Components", phon.get("non-useful", []))
html += "<p> The primary source for this site is The Complete Guide to Everyday Kanji by Yaeko Habein and Gerald Mathias. The distinction between \"useful\" and \"non-useful\" components is my own and not found in the text.</p>"
html += f"<footer><p><em>This site was last updated on {date.today().isoformat()}.</em></p></footer>"
html += "</body></html>"

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)