from django.shortcuts import render
from django.http import JsonResponse
from googleapiclient.discovery import build
from django.conf import settings

from .models import Video, Comment

def dashboard(request):
    comments = Comment.objects.all()
    return render(request, 'scraper/dashboard.html', {'comments': comments})

def category_comments(comment_text):
    if '?' in comment_text:
        return 'question'
    if 'please make' in comment_text.lower() or 'video about' in comment_text.lower():
        return 'content_idea'
    return 'suggestion'

def fetch_comments(request):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    video_id = request.GET.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'No video ID provided'}, status=400)
    
    #create or get video

    video, created = Video.objects.get_or_create(
        video_id=video_id,
        defaults={'url': f'https://www.youtube.com/watch?v={video_id}'})

    comments = []
    try:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=20,
        ).execute()
        for item in response['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment = Comment.objects.create(
                video=video,
                text=comment_text,
                category='uncategorized',  # Placeholder
                sentiment='unknown'       # Placeholder
            )

            comments.append(comment_text)
        return JsonResponse({'comments':comments})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

