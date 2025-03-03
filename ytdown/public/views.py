from flask import render_template, Blueprint, request, jsonify, Response, abort, url_for
from flask_login import current_user
import youtube_dl, requests, json, uuid, os
from ytdown.models import Video, Resolutions, Faq
from datetime import datetime, timedelta
from ytdown import db

public = Blueprint('public',__name__)

def get_size(url):
    head = requests.head(url)
    if 'Content-Length' in head.headers:
        return convertFileSize(int(head.headers['Content-Length']))
    else:
        return 'unknown'

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

    duration = str(timedelta(seconds=int(meta['duration'])))
    thumbnail = meta['thumbnail']
    title = meta['title']

    video = Video(web_url=meta['webpage_url'], thumbnail=thumbnail, title=title,
        dw_date=datetime.today().strftime('%Y-%m-%d'), source='Youtube')
    db.session.add(video)
    db.session.commit()

    for m in meta['formats']:
        token = str(uuid.uuid4())
        if m['acodec'] != 'none' and m['vcodec'] != 'none':
            video_streams.append({
                'resolution': m['format_note'],
                'filesize': convertFileSize(m['filesize']),
                'ext': m['ext'],
                'token': token
            })
            resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
            db.session.add(resolution)
        elif m['acodec'] == 'none' and m['vcodec'] != 'none':
            video_without_sound.append({
                'resolution': m['format_note'],
                'filesize': convertFileSize(m['filesize']),
                'ext': m['ext'],
                'token': token
            })
            resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
            db.session.add(resolution)
        elif m['acodec'] != 'none' and m['vcodec'] == 'none':
            audio_streams.append({
                'resolution': 'audio',
                'filesize': convertFileSize(m['filesize']),
                'ext': m['ext'],
                'token': token
            })
            resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
            db.session.add(resolution)

    db.session.commit()
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

def twitter(meta):
    video_streams = []

    duration = str(timedelta(seconds=int(meta['duration'])))
    thumbnail = meta['thumbnail']
    title = meta['title']

    video = Video(web_url=meta['webpage_url'], thumbnail=thumbnail, title=title,
        dw_date=datetime.today().strftime('%Y-%m-%d'), source='Twitter')
    db.session.add(video)
    db.session.commit()

    for m in meta['formats']:
        token = str(uuid.uuid4())
        if m['protocol'] == 'https':
            video_streams.append({
                'resolution': str(m['height'])+'p',
                'filesize': get_size(m['url']),
                'ext': m['ext'],
                'token': token
            })
            resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
            db.session.add(resolution)

    db.session.commit()
    context = {
        'error': False,
        'duration': 'Duration ' + duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': sorted(video_streams, key=lambda d: int(d['resolution'].split('p')[0]), reverse=True)
    }
    return context

def izlesene(meta):
    video_streams = []

    duration = str(timedelta(seconds=int(meta['duration'])))
    thumbnail = meta['thumbnail']
    title = meta['title']

    video = Video(web_url=meta['webpage_url'], thumbnail=thumbnail, title=title,
        dw_date=datetime.today().strftime('%Y-%m-%d'), source='Izlesene')
    db.session.add(video)
    db.session.commit()

    for m in meta['formats']:
        token = str(uuid.uuid4())
        video_streams.append({
            'resolution': m['format_id'],
            'filesize': get_size(m['url']),
            'ext': m['ext'],
            'token': token
        })
        resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
        db.session.add(resolution)

    db.session.commit()
    context = {
        'error': False,
        'duration': 'Duration ' + duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': sorted(video_streams, key=lambda d: int(d['resolution'].split('p')[0]), reverse=True)
    }
    return context

def vimeo(meta):
    video_streams = []

    duration = str(timedelta(seconds=int(meta['duration'])))
    thumbnail = meta['thumbnail']
    title = meta['title']

    video = Video(web_url=meta['webpage_url'], thumbnail=thumbnail, title=title,
        dw_date=datetime.today().strftime('%Y-%m-%d'), source='Vimeo')
    db.session.add(video)
    db.session.commit()

    for m in meta['formats']:
        token = str(uuid.uuid4())
        if m['protocol'] == 'https':
            video_streams.append({
                'resolution': m['format_id'].split('-')[-1],
                'filesize': get_size(m['url']),
                'ext': m['ext'],
                'token': token
            })
            resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
            db.session.add(resolution)

    db.session.commit()
    context = {
        'error': False,
        'duration': 'Duration ' + duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': sorted(video_streams, key=lambda d: int(d['resolution'].split('p')[0]), reverse=True)
    }
    return context

def vlive(meta):
    video_streams = []

    duration = str(timedelta(seconds=int(meta['duration'])))
    thumbnail = meta['thumbnail']
    title = meta['title']

    video = Video(web_url=meta['webpage_url'], thumbnail=thumbnail, title=title,
        dw_date=datetime.today().strftime('%Y-%m-%d'), source='Vlive')
    db.session.add(video)
    db.session.commit()

    for m in meta['formats']:
        token = str(uuid.uuid4())
        if m['ext'] == 'mp4':
            video_streams.append({
                'resolution': m['format_id'].split('_')[-1].replace('P', 'p'),
                'filesize': convertFileSize(m['filesize']),
                'ext': m['ext'],
                'token': token
            })
            resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
            db.session.add(resolution)

    db.session.commit()
    context = {
        'error': False,
        'duration': 'Duration ' + duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': sorted(video_streams, key=lambda d: int(d['resolution'].split('P')[0]), reverse=True)
    }
    return context

def instagram(meta):
    unique_filename = str(uuid.uuid4())+'.jpg'
    UPLOAD_IMG_FOLDER = os.path.join(os.getcwd(), 'ytdown/static/images')

    img_data = requests.get(meta['thumbnail']).content
    with open(os.path.join(UPLOAD_IMG_FOLDER, unique_filename), 'wb+') as handler:
        handler.write(img_data)

    video_streams = []
    duration = str(timedelta(seconds=int(meta['duration'])))
    thumbnail = url_for('static', filename='images/'+unique_filename)
    title = meta['title']

    video = Video(web_url=meta['webpage_url'], thumbnail=thumbnail, title=title,
        dw_date=datetime.today().strftime('%Y-%m-%d'), source='Instagram')
    db.session.add(video)
    db.session.commit()

    for m in meta['formats']:
        token = str(uuid.uuid4())
        if m['ext'] == 'mp4':
            video_streams.append({
                'resolution': m['format'].split(' - ')[-1],
                'filesize': get_size(m['url']),
                'ext': m['ext'],
                'token': token
            })
            resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
            db.session.add(resolution)

    db.session.commit()
    context = {
        'error': False,
        'duration': 'Duration ' + duration,
        'thumbnail': thumbnail,
        'title': title,
        'video_streams': video_streams
    }
    return context

def soundcloud(meta):
    audio_streams = []

    duration = str(timedelta(seconds=int(meta['duration'])))
    thumbnail = meta['thumbnail']
    title = meta['title']

    video = Video(web_url=meta['webpage_url'], thumbnail=thumbnail, title=title,
        dw_date=datetime.today().strftime('%Y-%m-%d'), source='SoundCloud')
    db.session.add(video)
    db.session.commit()

    for m in meta['formats']:
        token = str(uuid.uuid4())
        if m['protocol'] == 'http':
            audio_streams.append({
                'resolution': 'Audio',
                'filesize': get_size(m['url']),
                'ext': m['ext'],
                'token': token
            })
            resolution = Resolutions(download_url=m['url'], ext=m['ext'], token=token, vid_id=video.id)
            db.session.add(resolution)

    db.session.commit()
    context = {
        'error': False,
        'duration': 'Duration ' + duration,
        'thumbnail': thumbnail,
        'title': title,
        'audio_streams': audio_streams
    }
    return context

@public.route('/')
def index():
    downloader_list = ['youtube', 'twitter', 'instagram', 'vlive', 'vimeo', 'soundcloud', 'izlesene']
    dw = request.args.get('downloader', type=str)
    if not dw in downloader_list and dw:
        abort(404), 404
    all_faq = Faq.query.all()
    return render_template('public/index.html', dw=dw, all_faq=all_faq)

@public.route('/extractor', methods=['POST'])
def extractor():
    if request.method == 'POST':
        url = request.form['inputValue']
        ydl_opts = {
            'quiet': True,
            'geo_bypass': True,
            'skip_download': True,
            'cookies': 'cookies.txt',
            'verbose': True
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(url, download=False)
        except:
            abort(404), 404

        if meta['extractor'] == 'youtube':
            return youtube(meta)
        elif meta['extractor'] == 'Izlesene':
            return izlesene(meta)
        elif meta['extractor'] == 'vimeo':
            return vimeo(meta)
        elif meta['extractor'] == 'vlive':
            return vlive(meta)
        elif meta['extractor'] == 'Instagram':
            return instagram(meta)
        elif meta['extractor'] == 'twitter':
            return twitter(meta)
        elif meta['extractor'] == 'soundcloud':
            return soundcloud(meta)

@public.route('/download')
def download():
    token = request.args.get('token', type=str)
    res = Resolutions.query.filter_by(token=token).first_or_404()

    filename = str(res.res.title) + "." + str(res.ext)

    r = requests.get(res.download_url, stream=True)
    if 'Content-Length' in r.headers:
        headers = {
            'Content-Disposition': 'attachment; ' 'filename='+filename,
            'Content-Length': int(r.headers['Content-Length'])
        }
    else:
        headers = {
            'Content-Disposition': 'attachment; ' 'filename='+filename,
        }
    return Response(r, headers=headers)
