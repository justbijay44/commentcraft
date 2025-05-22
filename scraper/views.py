from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from django.conf import settings
from django.urls import reverse
from analysis.utils import category_comments, category_sentiment
from .models import Video, Comment

def dashboard(request):
    video_id = request.GET.get('video_id')
    comments = []
    video = None
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    if video_id:
        try:
            video = Video.objects.get(video_id=video_id)
            comments = Comment.objects.filter(video=video).order_by('-created_at')
            # Calculate sentiment counts
            positive_count = comments.filter(sentiment='positive').count()
            negative_count = comments.filter(sentiment='negative').count()
            neutral_count = comments.filter(sentiment='neutral').count()
        except Video.DoesNotExist:
            pass
    context = {
        'video_id': video_id,
        'video': video,
        'comments': comments,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count
    }
    return render(request, 'scraper/dashboard.html', context)


def fetch_comments(request):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    video_id = request.GET.get('video_id')
    if not video_id:
        return redirect('dashboard')
    
    #create or get video
    video, _ = Video.objects.get_or_create(
        video_id=video_id,
        defaults={'url': f'https://www.youtube.com/watch?v={video_id}'})

    try:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=20,
        ).execute()

        # Clear existing comments to avoid duplicates (optional, adjust as needed)
        Comment.objects.filter(video=video).delete()

        for item in response['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            category = category_comments(comment_text)
            sentiment = category_sentiment(comment_text)
            # Save to database with basic categorization
            Comment.objects.create(
                video=video,
                text=comment_text,
                category=category,
                sentiment=sentiment
            )
        return redirect(f"{reverse('dashboard')}?video_id={video_id}")
    except Exception as e:
        print(f"Error fetching comments: {e}")  # For debugging
        return redirect('dashboard')

