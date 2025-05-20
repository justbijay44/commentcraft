from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_id
    
class Comment(models.Model):
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    category = models.CharField(max_length=50, null=True, blank=True)
    sentiment = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.video.video_id}: {self.text[:20]}..."
