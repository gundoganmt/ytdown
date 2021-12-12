from flask import render_template, Blueprint, request, jsonify, Response, abort
from flask_login import current_user
import youtube_dl, requests, timeit, datetime, json

public = Blueprint('public',__name__)

def get_size(url):
    head = requests.head(url)
    return float(int(head.headers['Content-Length'])/1024/1024)

def youtube(meta):
    video_streams = []
    video_without_sound = []
    audio_streams = []

    duration = str(datetime.timedelta(seconds=meta['duration']))
    thumbnail = meta['thumbnail']
    title = meta['title']
    for m in meta['formats']:
        if meta['acodec'] != 'none' and meta['vcodec'] != 'none':
            if not m['filesize']:
                filesize = get_size(m['url'])
            video_streams.append({
                'resolution': m['format_note'],
                'filesize': m['filesize'],
                'ext': m['ext'],
                'video_url': m['url']
            })
        elif meta['acodec'] == 'none' and meta['vcodec'] != 'none':
            if not m['filesize']:
                filesize = get_size(m['url'])
            video_without_sound.append({
                'resolution': m['format_note'],
                'filesize': m['filesize'],
                'ext': m['ext'],
                'video_url': m['url']
            })
        elif meta['acodec'] != 'none' and meta['vcodec'] == 'none':
            if not m['filesize']:
                filesize = get_size(m['url'])
            audio_streams.append({
                'resolution': 'audio',
                'filesize': m['filesize'],
                'ext': m['ext'],
                'video_url': m['url']
            })

    context = {
        'error': False,
        'duration': duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': video_streams,
        'video_without_sound': video_without_sound,
        'audio_streams': audio_streams
    }
    return context

def izlesene(meta):
    video_streams = []

    duration = str(datetime.timedelta(seconds=meta['duration']))
    thumbnail = meta['thumbnail']
    title = meta['title']
    for m in meta['formats']:
        video_streams.append({
            'resolution': m['format_id'],
            'filesize': 255, #get_size(m['url']),
            'ext': m['ext'],
            'video_url': m['url']
        })

    context = {
        'error': False,
        'duration': duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': video_streams,
    }
    return context

@public.route('/')
def index():
    return render_template('public/index.html')

@public.route('/extractor', methods=['POST'])
def extractor():
    if request.method == 'POST':
        # url = request.form['inputValue']
        # print(url)
        # ydl_opts = {}
        # try:
        #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #         meta = ydl.extract_info(url, download=False)
        #     return jsonify(meta)
        # except:
        #     pass

        with open('C:/Users/Mehmet/Desktop/ytdown/izlesene.json') as f:
            meta = json.load(f)

        if meta['extractor'] == 'youtube':
            return youtube(meta)
        elif meta['extractor'] == 'Izlesene':
            return izlesene(meta)

@public.route('/download')
def download():
    r = requests.get("", stream=True)
    headers = {
        'Content-Disposition': 'attachment; ' 'filename=trial.mp4',
        'Content-Length': r.headers['Content-Length']
    }
    return Response(r, headers=headers)
