import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TEMPLATE = """\
<!doctype html>
<html>
<title>Is {player_name} still a member of the {team_name}?</title>
<body>
<center>
<h1>Is {player_name} still a member of the {team_name}?</h1>
<h1><a href="{player_url}" target="_blank">{answer}</a></h1>
</center>
<!-- https://github.com/sbstp/isplayerstilla -->
</body>
</html>
"""


def get_team_url(doc):
    h3 = doc.find("h3")
    a = h3.find("a")
    return a.attrs["href"]


def get_player_name(doc):
    title = doc.title.string
    pos = title.index("-")
    return title[:pos].strip()


def get_team_name(doc):
    h3 = doc.find("h3")
    a = h3.find("a")
    return "".join(a.strings)


if len(sys.argv) != 3:
    print("isplayerstilla <url> <html file>")

output_path = Path(sys.argv[2])
original_team_path = output_path.with_suffix(".slug")
original_team = None
if original_team_path.exists():
    original_team = original_team_path.read_text().strip()

player_url = sys.argv[1]
resp = requests.get(
    player_url,
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    },
)

doc = BeautifulSoup(resp.text, "html.parser")
team_url = get_team_url(doc)
player_name = get_player_name(doc)
team_name = get_team_name(doc)

if original_team is None:
    original_team_path.write_text(team_url)
    answer = "Yes"
else:
    if original_team == team_url:
        answer = "Yes"
    else:
        answer = "No"


output_path.write_text(
    TEMPLATE.format(
        player_name=player_name,
        team_name=team_name,
        answer=answer,
        player_url=player_url,
    )
)
