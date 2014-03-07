# alfred-mtg

[Alfred 2](http://www.alfredapp.com/) workflow with tools for searching and browsing [magiccards.info](magiccards.info)


## Installation

[Download the workflow](http://chuck.mn/0j2n2c1G2u3c/download/mtg.alfredworkflow) and open the file with Alfred 2 to install.

To regenerate the Alfred Workflow from source:

    git archive --format=zip --output=~/mtg.alfredworkflow HEAD

## Usage

This workflow adds four commands to Alfred that interact with [magiccards.info](http://magiccards.info). As such, each query allows the same [syntax](http://magiccards.info/syntax.html) as on that site.

![Available commands](http://chuck.mn/image/2y3S3k412L1F/default.png)


### Search

	mtg search <query>

Opens magiccards.info in your default browser, with a swearch for `<query>`

**Example:** `mtg search t:sliver t:legend` will open up [this search page](http://magiccards.info/query?q=t%3Asliver%20t%3Alegend&v=scan&s=cname)


### Page

	mtg page <query>

Allows you to choose a card from the results of `<query>`, opening up its magiccards.info page in the default browser.

**Example:** `mtg page t:legend e:dgm` will return these results:

![Searching for legendary cards from Dragon's Maze](http://chuck.mn/image/2w1n0H0M0F2r/page.png)

Upon selecting "Teysa, Envoy of Ghosts", you will be brought to the page for [Teysa, Envoy of Ghosts](http://magiccards.info/dgm/en/108.html)


### Spoiler

	mtg spoiler <query>

Allows you to choose a card from the results of `<query>`, copying the spoiler text of the card to your clipboard.

**Example:** `mtg spoiler sorin` will return these results:

![Searching for cards with "Sorin" in the name](http://chuck.mn/image/2S0E3L3H0g2v/spoiler.png)

Upon selecting "Sorin, Lord of Innistead", the following text will be copied to your clipboard:

	Sorin, Lord of Innistrad (2WB)
	Planeswalker - Sorin
	+1: Put a 1/1 black Vampire creature token with lifelink onto the battlefield.
	-2: You get an emblem with "Creatures you control get +1/+0."
	-6: Destroy up to three target creatures and/or other planeswalkers. Return each card put into a graveyard this way to the battlefield under your control.
	Loyalty: 3
	http://magiccards.info/ddk/en/1.html


### Image

	mtg image <query>

Allows you to choose a card from the results of `<query>`, copying the URL to an image of the card to your clipboard. This is useful for pasting to IRC, Campfire, or other chat programs.

**Example:** `mtg image t:enchant squirrel` will return these results:

![Searching for enchantments with "squirrel" in the name](http://chuck.mn/image/220i143B3W35/image.png)

Upon selecting "Squirrel Mob", the following text will be copied to your clipboard:

	http://magiccards.info/scans/en/od/274.jpg


## Credits

- [magiccards.info](http://magiccards.info) for the awesome datas.
- [Daniel Shannon](http://daniel.sh/) for [alp](https://github.com/phyllisstein/alp).
- [Corey Csuhta](https://twitter.com/cjcsuhta) for brainstorming and brewing.


## License

[WTFPL](http://www.wtfpl.net/txt/copying/)
