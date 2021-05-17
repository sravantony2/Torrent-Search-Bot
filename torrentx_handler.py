# (c) @AbirHasan2005 & Hemanta Pokharel & The Anon Cat

import py1337x

torrent = py1337x.py1337x()


def queryMessageContent(torrentId):
    response = torrent.info(torrentId=torrentId)
    genre = '\n\n'+', '.join(response['genre']) if response['genre'] else None
    description = '\n'+response['description'] if genre and response['description'] else '\n\n'+response['description'] if response['description'] else None
    msg = f"/mirror {response['magnetLink']}"

    return msg
