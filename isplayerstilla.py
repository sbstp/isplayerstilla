import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TEMPLATE = """\
<!doctype html>
<html>
<meta charset="utf8">
<meta http-equiv="refresh" content="30">
<title>Is {player_name} still a member of the {original_team}?</title>
<body>
<center>
<h1>Is {player_name} still a member of the {original_team}?</h1>
<h1><a href="{player_url}" target="_blank">{answer}</a></h1>
</center>
<!-- https://github.com/sbstp/isplayerstilla -->
</body>
</html>
"""


def get_player_name(doc):
    title = doc.title.string
    pos = title.index("-")
    return title[:pos].strip()


def get_team_name(doc):
    h3 = doc.find("h3")
    a = h3.find("a")
    return "".join(a.strings).strip()


if len(sys.argv) != 3:
    print("isplayerstilla <url> <html file>")

output_path = Path(sys.argv[2])
original_team_path = output_path.with_suffix(".id")
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
player_name = get_player_name(doc)
team_name = get_team_name(doc)
# team_name = "Chicago Blackhawks" #  test purposes

if original_team is None:
    original_team_path.write_text(team_name)
    original_team = team_name


if original_team == team_name:
    answer = "Yes"
else:
    answer = "No, he's with the {team_name} now.".format(team_name=team_name)


output_path.write_text(
    TEMPLATE.format(
        player_name=player_name,
        original_team=original_team,
        answer=answer,
        player_url=player_url,
    )
)
