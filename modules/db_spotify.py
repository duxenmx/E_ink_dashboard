from time import strftime
from time import gmtime
import tekore as tk
from PIL import Image
#import time
from modules import d_functions as d_f

import os
import requests

creddir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'credentials')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

file = os.path.join(creddir, 'tekore.cfg')
cover_path = os.path.join(picdir, 'cover.bmp')


def get_spot_info():
    conf = tk.config_from_file(file, return_refresh=True)
    token = tk.refresh_user_token(*conf[:2], conf[3])

    spotify = tk.Spotify(token)
    p = spotify.playback()

    with spotify.token_as(token):
        p = spotify.playback()
    x_limit = 24

    sp_data = []
    if p is not None:
        if p.is_playing is not False:
            if p.currently_playing_type == 'track':
                name = p.device.name
                sec_format = strftime("%M:%S", gmtime(p.item.duration_ms/1000))
                device = p.device.type
                title, title_2 = d_f.sep_strings(p.item.name, x_limit)
                if title_2 != ' ':

                    title_3, title_4 = d_f.sep_strings(title_2, x_limit)
                else:
                    title_3 = ' '
                    title_4 = ' '
                artists = p.item.artists
                artist = ''
                for x in range(len(artists)):
                    if artist == '':
                        artist = p.item.artists[x].name
                    else:
                        artist += ', ' + p.item.artists[x].name
                artist_fm, artist_fm2 = d_f.sep_strings(artist, x_limit)
                if artist_fm2 != ' ':

                    artist_fm3, artist_fm4 = d_f.sep_strings(artist_fm2, x_limit)
                else:
                    artist_fm3 = ' '
                    artist_fm4 = ' '

                album, album_2 = d_f.sep_strings(p.item.album.name, x_limit)
                if album_2 != ' ':

                    album_3, album_4 = d_f.sep_strings(album_2, x_limit)
                else:
                    album_3 = ' '
                    album_4 = ' '
                year = p.item.album.release_date[0:4]
                url = p.item.album.images[1].url
                img_data = requests.get(url).content
                duration = (p.item.duration_ms/1000)-(p.progress_ms/1000)

                with open(cover_path, 'wb') as handler:
                    handler.write(img_data)

                sp_data.append(str(p.currently_playing_type))
                sp_data.append(str(duration))
                sp_data.append('Active Reproduction on '+device + ' --> ' + name)
                sp_data.append('Song: ' + title)
                sp_data.append(title_3)
                sp_data.append(title_4)
                sp_data.append('By ' + artist_fm)
                sp_data.append(artist_fm3)
                sp_data.append(artist_fm4)
                sp_data.append('Album: '+album)
                sp_data.append(album_3)
                sp_data.append(album_4)
                sp_data.append('Year: [' + year + ']')
                sp_data.append('Duration = ' + str(sec_format) + ' min')

            elif p.currently_playing_type == 'ad':
                sp_data.append(str(p.currently_playing_type))
                sp_data.append('Playing Ads')

        else:
            sp_data.append('off')
            sp_data.append('Currently not playing')

    else:
        sp_data.append('off')
        sp_data.append('Currently not playing')

    return sp_data
    # print(sp_data)
    # time.sleep(10)


def draw_music_mod(tran_s_x, tran_s_y, spoti, color, draw, template):
    draw.text((tran_s_x, tran_s_y-40), 'SPOTIFY', font=d_f.font_size(30), fill=color)
    if spoti[0] == 'track':
        for x in range(2, len(spoti)):
            if spoti[x] != ' ':
                draw.text((tran_s_x, tran_s_y), spoti[x], font=d_f.font_size(18), fill=color)
                tran_s_y = tran_s_y + 20
        c_img = Image.open(cover_path)
        im_grey = c_img.convert('L')
        template.paste(im_grey.resize((180, 180)), (245, 75))
    elif spoti[0] == 'ad':
        draw.text((tran_s_x, tran_s_y), spoti[1], font=d_f.font_size(26), fill=color)
    elif spoti[0] == 'off':
        draw.text((tran_s_x, tran_s_y), spoti[1], font=d_f.font_size(26), fill=color)
