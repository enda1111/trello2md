import os
import dateutil.parser
import re
import pyperclip
import pytz
from argparse import ArgumentParser
from dotenv import load_dotenv
from os.path import join, dirname
from trelloc import TrelloBoard
from trelloc import Members
from markdown import Markdown


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def main(board_id, list_filter, verbose):
    trello = TrelloBoard(api_key(), token(), board_id)
    members = Members(api_key(), token())
    list_lists = trello.list_lists()

    md = Markdown()
    hl = 1

    for l in list_lists:
        if re.search(list_filter, l.name) is None:
            continue

        md.h(hl, l.name)

        cards = l.list_cards()
        for card in cards:
            card.fetch()
            card_members = ' '.join(
                map(lambda member_id: members.get_avatar_url(member_id), card.member_id)
            )

            md.h(
                hl + 1,
                '[:link:]({url}) {name} {members}'.format(url=card.url, name=card.name, members=card_members)
            )

            md.quote(card.description)
            comments = card.comments + card.attachments
            for comment in sorted(comments, key=lambda x: x['date'], reverse=True):
                md.quote('----')
                member_id = get_member_id(comment)
                avatar_url = members.get_avatar_url(member_id)
                md.quote('{avatar_url} {date}'.format(avatar_url=avatar_url, date=display_date(comment['date'])))

                if 'data' in comment and 'text' in comment['data']:
                    md.quote(comment['data']['text'])
                elif 'name' in comment and 'url' in comment:
                    md.quote('![{name}]({url})'.format(name=comment['name'], url=comment['url']))

    body_md = md.build()
    pyperclip.copy(body_md)
    if verbose is True:
        print(body_md)

    return ''


def get_member_id(comment):
    if 'memberCreator' in comment:
        return comment['memberCreator'].get('id', None)
    else:
        return comment.get('idMember', None)


def display_date(date_str):
    date = dateutil.parser.parse(date_str)
    date = date.astimezone(pytz.timezone('Asia/Tokyo')).replace(tzinfo=pytz.timezone('Asia/Tokyo'))
    return date.strftime('%Y/%m/%d (%a) %H:%M:%S')


def api_key():
    return os.environ['TRELLO_API_KEY']


def token():
    return os.environ['TRELLO_TOKEN']


def get_option():
    argument_parser = ArgumentParser()
    argument_parser.add_argument('-t', '--trello_id', type=str, default='', help='trello board ID')
    argument_parser.add_argument('-f', '--filter', type=str, default='.*', help='list filter')
    argument_parser.add_argument('-v', '--verbose', type=bool, default=False, help='print markdown')
    return argument_parser.parse_args()


if __name__ == '__main__':
    args = get_option()
    main(args.trello_id, args.filter, args.verbose)
