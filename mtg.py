import os
import re
import sys
from urlparse import urlparse

import alp
from alp import Item

try:
    from PIL import Image
except ImportError:
    pil_installed = False
else:
    pil_installed = True
use_thumbs = os.environ.get('MTG_NO_THUMBNAILS', False) or pil_installed


action = sys.argv[1]
query = ' '.join(sys.argv[2:])


TITLES = {
    'image': 'MTG: Card Image',
    'page': 'MTG: Card Page',
    'spoiler': 'MTG: Card Spoiler',
}

NO_RESULTS = {
    'subtitle': 'No results found',
    'title': TITLES[action],
    'valid': False,
}

TOO_SHORT = {
    'subtitle': 'Minimum 4 characters',
    'title': TITLES[action],
    'valid': False,
}


class Card(object):
    def __init__(self, table):
        self.parse(table)

    def __repr__(self):
        return '<MTG Card: "%s">' % self.data['name']

    def sanitize(self, string):
        return string.replace(u'\u2014', '-').strip(' ')

    def parse(self, table):
        image, meta, printings = table('td')
        self.image_url = self.get_image_url(image)
        if use_thumbs:
            self.image_path = self.get_image_path()
            self.image_thumbnail = self.get_image_thumbnail()
        else:
            self.image_path = self.image_thumbnail = sys.executable
        self.cost = self.get_cost(meta)
        self.name = self.get_name(meta)
        self.text = self.get_text(meta)
        self.type, self.stats = self.get_type_line(meta)
        self.url = self.get_url(meta)

    def get_image_url(self, cell):
        return self.sanitize(cell('img')[0]['src'])

    def image_cache(self):
        cache = alp.cache('cards')
        if not os.path.exists(cache):
            os.makedirs(cache)
        return cache

    def get_image_path(self):
        cache = self.image_cache()
        filename = urlparse(self.image_url)[2][1:].replace('/', '_')
        destination = os.path.join(cache, filename)
        if not os.path.exists(destination):
            req = alp.Request(self.image_url)
            with open(destination, 'wb') as f:
                f.write(req.request.content)
        return destination

    def get_image_thumbnail(self):
        cache = self.image_cache()
        filename = 'thumb_%s' % os.path.basename(self.image_path)
        destination = os.path.join(cache, filename.replace('jpg', 'png'))
        if not os.path.exists(destination):
            full = Image.open(self.image_path)
            thumb = full.crop((56, 47, 256, 247))
            thumb.save(destination, 'PNG')
        return destination

    def get_cost(self, cell):
        try:
            cost = cell('p')[0].text.split(', \n')[1].split('(')[0]
        except IndexError:
            return None
        else:
            return self.sanitize(cost)

    def get_name(self, cell):
        return self.sanitize(cell.find('a').text)

    def get_text(self, cell):
        strings = cell.find('p', class_='ctext').find('b').stripped_strings
        return self.sanitize('\n'.join(strings))

    def get_type_line(self, cell):
        type_line = cell('p')[0].text.split(', \n')[0]
        card_type = stats = None
        if 'Creature' in type_line:
            stats = type_line.split(' ')[-1:][0]
            card_type = type_line.replace(stats, '')
        elif 'Planeswalker' in type_line:
            loyalty = re.search('(\(.*$)', type_line).groups()[0]
            stats = 'Loyalty: %s' % re.sub(r'[^\d.]+', '', loyalty)
            card_type = type_line.replace(loyalty, '')
        if card_type:
            return self.sanitize(card_type), self.sanitize(stats)
        return self.sanitize(type_line), None

    def get_url(self, cell):
        return 'http://magiccards.info' + self.sanitize(cell.find('a')['href'])

    def spoiler(self):
        def add(old, new, newline=True):
            if newline and old:
                old += '\n'
            old += new
            return old
        spoiler = add('', self.name)
        if self.cost:
            spoiler = add(spoiler, ' (%s)' % self.cost, newline=False)
        spoiler = add(spoiler, self.type)
        if self.text:
            spoiler = add(spoiler, self.text)
        if self.stats:
            spoiler = add(spoiler, self.stats)
        return add(spoiler, self.url)

    def title(self):
        return self.name

    def subtitle(self):
        if self.cost:
            return '%s (%s)' % (self.type, self.cost)
        return self.type

    def arg(self):
        if action == 'spoiler':
            return self.spoiler()
        elif action == 'image':
            return self.image_url
        else:
            return self.url

    def item(self):
        item = {
            'arg': self.arg(),
            'subtitle': self.subtitle(),
            'title': self.title(),
            'type': 'file',
            'uid': self.url,
            'valid': True
        }
        icon = self.image_thumbnail or self.image_path
        if icon:
            item['icon'] = icon
        return Item(**item)


class Search(object):
    url = 'http://magiccards.info/query'
    qs = {
        'q': 'l:en and not:funny and ',
        's': 'cname',
        'v': 'card',
    }

    def __init__(self, query):
        self.qs['q'] = self.qs['q'] + '(%s)' % query
        self._soup = self.do_soup()
        self.items = self.get_items()

    def __repr__(self):
        return '<MTG Card Search: "%s">' % self.qs['q']

    def do_soup(self):
        response = alp.Request(self.url, self.qs)
        return response.souper()

    def get_items(self):

        def is_card(tag):
            is_table = tag.name == 'table'
            is_card_table = tag.has_key('align') and tag['align'] == 'center'  # noqa
            has_card_data = len(tag('td')) == 3
            return is_table and is_card_table and has_card_data

        card_cells = self._soup(is_card)
        cards = [Card(cell) for cell in card_cells]
        return [card.item() for card in cards] if cards else []


if __name__ == '__main__':
    if len(query) > 3:
        search = Search(query)
        results = search.items
        alp.feedback(results) if results else alp.feedback([Item(**NO_RESULTS)])
    else:
        alp.feedback([Item(**TOO_SHORT)])
