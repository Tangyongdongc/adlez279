"""fetcher.py allows the user to fetch lyrics from numerous APIs and
save them as a text file in the /in directory.
"""
import os
import sys
from pathlib import Path


class Color:
    """Color definitions"""
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


print('fetcher.py fetches lyrics from various sources. '
      'Please choose which one you would like to use.')
print('If you experience any bugs, feel free to open an '
      'issue at https://github.com/adlez27/phonetic-songs')
print()
print(Color.BOLD + '1. MetroLyrics (tswift) - RECOMMENDED' + Color.END)
print('2. Genius')
print('3. AZLyrics.com (azapi)')
print('4. VocaDB')
print('5. UtaiteDB')
print('6. TouhouDB')
print('7. Piapro (currently not implemented)')
print('To close, type "q"')
option = input(': ')
print()

if option in ['2', '4', '5', '6', '7']:
    import requests

if option in ['2', '7']:
    from bs4 import BeautifulSoup

if not option == 'q':
    # MetroLyrics
    if option == '1':
        from tswift import Song
        print('You can either get the song with the song title and artist'
              'name, or you can search via lyrics.')
        print('Please choose which method you would like to use.')
        print('a. Artist Name + Song Title')
        print('b. Search by lyrics')
        ml_option = input(': ')

        if ml_option == 'a':
            artist_name = input('Type in the name of the artist: ')
            song_title = input('Type in the title of the song: ')

            lyrics = Song(title=song_title, artist=artist_name)

            filename = (artist_name + ' - ' + song_title + '.txt')

            if Path('in/').exists():
                basepath = Path('in/')
            else:
                os.mkdir('in')
                if Path('in/').exists():
                    basepath = Path('in/')

            with open(basepath/filename, 'w', encoding='utf-8') as export:
                export.write(lyrics.format())
                export.close()

            print('Downloaded: ' + artist_name + ' - ' + song_title)
        if ml_option == 'b':
            search_terms = input('Enter lyrics: ')

            lyrics = Song.find_song(search_terms)
            song_title = lyrics.title
            artist_name = lyrics.artist

            filename = (artist_name + ' - ' + song_title + '.txt')

            if Path('in/').exists():
                basepath = Path('in/')
            else:
                os.mkdir('in')
                if Path('in/').exists():
                    basepath = Path('in/')

            with open(basepath/filename, 'w', encoding='utf-8') as export:
                export.write(lyrics.format())
                export.close()

            print('Downloaded: ' + artist_name + ' - ' + song_title)

    # Genius
    if option == '2':
        def lyric_fetcher_genius(song_api_path):
            '''Lyric Fetching from Genius using API and HTML scraping'''
            song_url = base_url + song_api_path
            response = requests.get(song_url, headers=headers)
            json = response.json()
            song_path = json["response"]["song"]["path"]

            page_url = site_url + song_path
            page = requests.get(page_url)
            html = BeautifulSoup(page.text, 'html.parser')
            [h.extract() for h in html('script')]
            [h.extract() for h in html('[]')]
            lyrics_get = html.find(
                "div", class_="lyrics").get_text()
            return lyrics_get

        site_url = 'https://genius.com'
        base_url = 'https://api.genius.com'
        search_path = '/search'

        token = Path("./token.txt")
        if not token.exists():
            print('token.txt does not exist.')
            print('You don\'t have the token required to use Genius.')
            print('Visit the site below to get your own token, and follow'
                  'the instructions to get your own authorisation token.')
            print('https://docs.genius.com/#/getting-started-h1')
            print()
            sys.exit()

        with open('token.txt', 'r') as token:
            genius_token = token.read()
        token.close()
        headers = {'Authorization': 'Bearer ' + genius_token}

        print('You can get the lyrics by searching with the song title'
              ' and the artist name. You can also mass fetch based on '
              'the Billboard charts.')
        print('Please choose which method you would like to use.')
        print('a. Artist Name + Song Title')
        print('b. Chart Conversion')
        g_option = input(': ')

        if g_option == 'a':
            # Adapted: https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
            artist_name = input('Type in the name of the artist: ')
            song_title = input('Type in the title of the song: ')
            params = {'q': song_title}

            response = requests.get(base_url + search_path,
                                    params=params, headers=headers)
            json = response.json()
            song_info = None

            for hit in json['response']['hits']:
                if hit['result']['primary_artist']['name'] == artist_name:
                    song_info = hit
                    break
            if song_info:
                pass

            if __name__ == "__main__":
                search_url = base_url + "/search"
                data = {'q': song_title}
                response = requests.get(search_url, data=data, headers=headers)
                json = response.json()
                song_info = None
                for hit in json["response"]["hits"]:
                    if hit["result"]["primary_artist"]["name"] == artist_name:
                        song_info = hit
                        break
                if song_info:
                    song_api_path = song_info["result"]["api_path"]
                    lyrics = lyric_fetcher_genius(song_api_path)

            filename = (artist_name + ' - ' + song_title + '.txt')

            if Path('in/').exists():
                basepath = Path('in/')
            else:
                os.mkdir('in')
                if Path('in/').exists():
                    basepath = Path('in/')

            with open(basepath/filename, 'w', encoding='utf-8') as export:
                export.write(lyrics)
                export.close()

            print('Downloaded: ' + artist_name + ' - ' + song_title)
        if g_option == 'b':
            import csv

            chart_name = input('Type in the name of the chart: ')
            chart_path = ('charts/' + chart_name + '.csv')
            with open(chart_path) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=';')
                for row in readCSV:
                    artist_name = row[1]
                    song_title = row[0]
                    params = {'q': song_title}

                    response = requests.get(base_url + search_path,
                                            params=params, headers=headers)
                    json = response.json()
                    song_info = None

                    for hit in json['response']['hits']:
                        if hit['result']['primary_artist']['name'] == artist_name:
                            song_info = hit
                            break
                    if song_info:
                        pass

                    if __name__ == "__main__":
                        search_url = base_url + "/search"
                        data = {'q': song_title}
                        response = requests.get(
                            search_url, data=data, headers=headers)
                        json = response.json()
                        song_info = None
                        for hit in json["response"]["hits"]:
                            if hit["result"]["primary_artist"]["name"] == artist_name:
                                song_info = hit
                                break
                        if song_info:
                            song_api_path = song_info["result"]["api_path"]
                            lyrics = lyric_fetcher_genius(song_api_path)

                    filename = (artist_name + ' - ' + song_title + '.txt')

                    if Path('in/').exists():
                        basepath = Path('in/')
                    else:
                        os.mkdir('in')
                        if Path('in/').exists():
                            basepath = Path('in/')

                    with open(basepath/filename, 'w', encoding='utf-8') as export:
                        export.write(lyrics)
                        export.close()

                    print('Downloaded: ' + artist_name + ' - ' + song_title)

    # AZlyrics
    if option == '3':
        from azapi import AZlyrics

        print('Which search engine would you like to use for the retrevial of lyrics?')
        print('1. Google')
        print('2. DuckDuckGo')
        az_se = input(': ')
        print()

        while not az_se in ['1', '2']:
            print('Please specify the search engine.')
            print('Or type "q" to exit.')
            az_se = input(': ')
            print()
            if az_se == 'q':
                sys.exit()

        if az_se == '1':
            az_api = AZlyrics('google')

        if az_se == '2':
            az_api = AZlyrics('duckduckgo')

        print('You can either get the song with the song title and artist '
              'name, or you can search via lyrics.')
        print()
        print('If you don\'t remember the name of the artist, you can search by title only.')
        print('If you want to search by lyrics, put the lyrics in the title field')
        artist_name = input('Type in the name of the artist: ')
        song_title = input('Type in the title of the song: ')

        az_api.artist = artist_name
        az_api.title = song_title

        lyrics = az_api.getLyrics(save=False).strip()

        filename = (az_api.artist + ' - ' + az_api.title + '.txt')

        if Path('in/').exists():
            basepath = Path('in/')
        else:
            os.mkdir('in')
            if Path('in/').exists():
                basepath = Path('in/')

        with open(basepath/filename, 'w', encoding='utf-8') as export:
            export.write(lyrics)
            export.close()

        print('Downloaded: ' + artist_name + ' - ' + song_title)

    # VocaDB
    if option == '4':
        vdb_url = 'https://vocadb.net/api/'
        search_type = ['artists', 'songs']
        print('You can get the lyrics by searching with the song title'
              ' and artist name.')

        artist_name = input('Type in the name of the artist: ')
        song_title = input('Type in the title of the song: ')
        print()
        print('Specify whether the song is an "Original", "Remix", '
              '"Cover", or "Arrangement" to help filter results.')
        print('You can leave this field blank.')
        song_type = input(': ')
        print()

        artist_payloid = {'query': artist_name,
                          'namematchMode': 'Auto',
                          'preferAccurateMatches': 'true'}
        artist_search = requests.get(vdb_url + search_type[0],
                                     artist_payloid)

        artist_values = artist_search.json()
        artist_title = artist_values['items'][0]['name']
        print('Artist retrieved: ' + artist_title)
        artist_id = artist_values['items'][0]['id']

        song_payload = {'query': song_title, 'lang': 'English',
                        'songTypes': song_type, 'fields': 'Lyrics',
                        'artistId': artist_id,
                        'defaultNameLanguage': 'English'}
        song_search = requests.get(vdb_url + search_type[1],
                                   song_payload)

        song_values = song_search.json()
        song_name = song_values['items'][0]['name']
        print('Song retrieved: ' + song_name)
        lyrics_values = song_values['items'][0]['lyrics']
        lyrics = lyrics_values[0]['value']

        filename = (artist_title + ' - ' + song_name + '.txt')

        if Path('in/').exists():
            basepath = Path('in/')
        else:
            os.mkdir('in')
            if Path('in/').exists():
                basepath = Path('in/')

        with open(basepath/filename, 'w', encoding='utf-8') as export:
            export.write(lyrics)
            export.close()

        print('Downloaded: ' + artist_name + ' - ' + song_title)

    # UtaiteDB
    if option == '5':
        udb_url = 'https://utaitedb.net/api/'
        search_type = ['artists', 'songs']
        print('You can get the lyrics by searching with the song title'
              ' and artist name.')

        artist_name = input('Type in the name of the artist: ')
        song_title = input('Type in the title of the song: ')
        print()
        print('Specify whether the song is an "Original", "Remix", '
              '"Cover", or "Arrangement" to help filter results.')
        print('You can leave this field blank.')
        song_type = input(': ')
        print()

        artist_payloid = {'query': artist_name,
                          'namematchMode': 'Auto',
                          'preferAccurateMatches': 'true'}
        artist_search = requests.get(udb_url + search_type[0],
                                     artist_payloid)

        artist_values = artist_search.json()
        artist_title = artist_values['items'][0]['name']
        print('Artist retrieved: ' + artist_title)
        artist_id = artist_values['items'][0]['id']

        song_payload = {'query': song_title, 'lang': 'English',
                        'songTypes': song_type, 'fields': 'Lyrics',
                        'artistId': artist_id}
        song_search = requests.get(udb_url + search_type[1],
                                   song_payload)

        song_values = song_search.json()
        song_name = song_values['items'][0]['name']
        print('Song retrieved: ' + song_name)
        lyrics_values = song_values['items'][0]['lyrics']
        lyrics = lyrics_values[0]['value']

        filename = (artist_title + ' - ' + song_name + '.txt')

        if Path('in/').exists():
            basepath = Path('in/')
        else:
            os.mkdir('in')
            if Path('in/').exists():
                basepath = Path('in/')

        with open(basepath/filename, 'w', encoding='utf-8') as export:
            export.write(lyrics)
            export.close()

        print('Downloaded: ' + artist_name + ' - ' + song_title)

    # TouhouDB
    if option == '6':
        tdb_url = 'https://touhoudb.com/api/'
        search_type = ['artists', 'songs']
        print('You can get the lyrics by searching with the song title'
              ' and artist name.')

        artist_name = input('Type in the name of the artist: ')
        song_title = input('Type in the title of the song: ')
        print()
        print('Specify whether the song is an "Original", "Remix", '
              '"Cover", or "Arrangement" to help filter results.')
        print('You can leave this field blank.')
        song_type = input(': ')
        print()

        artist_payloid = {'query': artist_name,
                          'namematchMode': 'Auto',
                          'preferAccurateMatches': 'true'}
        artist_search = requests.get(tdb_url + search_type[0],
                                     artist_payloid)

        artist_values = artist_search.json()
        artist_title = artist_values['items'][0]['name']
        print('Artist retrieved: ' + artist_title)
        artist_id = artist_values['items'][0]['id']

        song_payload = {'query': song_title, 'lang': 'English',
                        'songTypes': song_type, 'fields': 'Lyrics',
                        'artistId': artist_id}
        song_search = requests.get(tdb_url + search_type[1],
                                   song_payload)

        song_values = song_search.json()
        song_name = song_values['items'][0]['name']
        print('Song retrieved: ' + song_name)
        lyrics_values = song_values['items'][0]['lyrics']
        lyrics = lyrics_values[0]['value']

        filename = (artist_title + ' - ' + song_name + '.txt')

        if Path('in/').exists():
            basepath = Path('in/')
        else:
            os.mkdir('in')
            if Path('in/').exists():
                basepath = Path('in/')

        with open(basepath/filename, 'w', encoding='utf-8') as export:
            export.write(lyrics)
            export.close()

        print('Downloaded: ' + artist_name + ' - ' + song_title)

    # Piapro
    if option == '7':
        print('This feature is not yet implemented, please try again later.')
sys.exit()
