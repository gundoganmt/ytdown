from flask import render_template, Blueprint, request, jsonify, Response, abort
from flask_login import current_user
import youtube_dl, requests, timeit, datetime, json

public = Blueprint('public',__name__)

def get_size(url):
    #head = requests.head(url)
    return 255 #float(int(head.headers['Content-Length'])/1024/1024)

def convertFileSize(num):
    if not num:
        return 'unknown'
    kb = num/1024
    if kb < 1024:
        return "%.2fKb" % kb
    else:
        mb = kb/1024
        if mb < 1024:
            return "%.2fMb" % mb
        else:
            gb = mb/1024
            return "%.2fGb" % gb

def youtube(meta):
    video_streams = []
    video_without_sound = []
    audio_streams = []

    duration = str(datetime.timedelta(seconds=meta['duration']))
    thumbnail = meta['thumbnail']
    title = meta['title']
    for m in meta['formats']:
        if m['acodec'] != 'none' and m['vcodec'] != 'none':
            video_streams.append({
                'resolution': m['format_note'],
                'filesize': convertFileSize(m['filesize']),
                'ext': m['ext'],
                'video_url': m['url']
            })
        elif m['acodec'] == 'none' and m['vcodec'] != 'none':
            video_without_sound.append({
                'resolution': m['format_note'],
                'filesize': convertFileSize(m['filesize']),
                'ext': m['ext'],
                'video_url': m['url']
            })
        elif m['acodec'] != 'none' and m['vcodec'] == 'none':
            audio_streams.append({
                'resolution': 'audio',
                'filesize': convertFileSize(m['filesize']),
                'ext': m['ext'],
                'video_url': m['url']
            })

    context = {
        'error': False,
        'duration': 'Duration ' + duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': sorted(video_streams, key=lambda d: int(d['resolution'].split('p')[0]), reverse=True),
        'video_without_sound': sorted(video_without_sound, key=lambda d: int(d['resolution'].split('p')[0]), reverse=True),
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
        'duration': 'Duration ' + duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': sorted(video_streams, key=lambda d: int(d['resolution'].split('p')[0]), reverse=True)
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
