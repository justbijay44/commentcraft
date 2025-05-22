from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def category_comments(comment_text):
    comment_text = comment_text.lower()

    if '?' in comment_text:
        return 'question'
    
    if 'please make' in comment_text or 'video about' in comment_text or 'would love to see' in comment_text:
        return 'content_idea'
    
    if 'improve' in comment_text or 'better' in comment_text or 'should' in comment_text:
        return 'suggestion'
    
    return 'other'

def category_sentiment(comment_text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(comment_text)
    compound_score = scores['compound']
    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'