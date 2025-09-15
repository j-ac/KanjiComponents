import toml
from datetime import date

phon = toml.load("phonetic.toml")
blurb = open("site_data/blurb.html", encoding="utf-8").read()
github_message = "<p>This site is a work in progress. Report any issues on <a href=\"https://github.com/j-ac/KanjiComponents/issues\">github</a>: </p>\n"

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

# Main page html
main_html = "<!DOCTYPE html>\n"
main_html += "<html><head><link rel=\"stylesheet\" href=\"styles.css\"><meta charset='UTF-8'><title>Kanji Components</title></head><body>"
main_html += github_message
main_html += "<h1>Kanji - The Way They Were Meant To Be</h1>"
main_html += blurb
main_html += render_section("Useful Phonetic Components", phon.get("useful", []))
main_html += "<p><a href=\"non_useful_phonetic.html\">View non-useful phonetic components</a></p>\n"
main_html += "<footer>"
main_html += "<p><em> The primary source for this site is The Complete Guide to Everyday Kanji by Yaeko Habein and Gerald Mathias. The distinction between \"useful\" and \"non-useful\" components is my own and not found in the text.</em></p>"
main_html += f"<p><em>This site was last updated on {date.today().isoformat()}.</em></p>"
main_html += "</footer>"
main_html += "</body></html>"

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(main_html)

# Non-useful phonetic page
phon_non_html = "<!DOCTYPE html>\n"
phon_non_html += "<p><a href=\"index.html\">Home</a></p>"
phon_non_html += "<html><head><link rel=\"stylesheet\" href=\"styles.css\"><meta charset='UTF-8'><title>Non-Useful Phonetic Kanji Components</title></head><body>\n"
phon_non_html += github_message
phon_non_html += "<p><b>I do not reccomend studying these kanji </b> as they are <b>not useful</b>. I keep them here for the sake of this site being complete, and because I cannot be certain I did not make any mistakes when I wrote it. Some may move to the main list if I find they were more useful than I gave them credit for.</p>\n"
phon_non_html += render_section("Non-Useful Phonetic Components\n", phon.get("non-useful", []))
phon_non_html += f"<footer><p><em>This site was last updated on {date.today().isoformat()}.</em></p></footer>"
phon_non_html += "</body></html>"

with open("docs/non_useful_phonetic.html", "w", encoding="utf-8") as f:
    f.write(phon_non_html)