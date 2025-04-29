import os
import tweepy
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime
from google import genai

load_dotenv()

print("Twitter Key:", os.getenv('TWITTER_API_KEY'))  # Should show your actual key
print("Twitter Secret:", os.getenv('TWITTER_API_SECRET') is not None)  # Should be True


# def init_twitter():
#     # Get credentials with explicit checks
#     api_key = os.getenv('TWITTER_API_KEY')
#     api_secret = os.getenv('TWITTER_API_SECRET')
#     access_token = os.getenv('TWITTER_ACCESS_TOKEN')
#     access_secret = os.getenv('TWITTER_ACCESS_SECRET')

#     if not all([api_key, api_secret, access_token, access_secret]):
#         raise ValueError("Missing Twitter credentials in .env file")

#     return tweepy.API(tweepy.OAuth1UserHandler(
#         api_key,
#         api_secret,
#         access_token,
#         access_secret
#     ))

auth = tweepy.OAuth1UserHandler(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    callback="http://localhost:8000/callback"  # Must match registered URI
)

auth = tweepy.OAuth2UserHandler(
    client_id=os.getenv('TWITTER_CLIENT_ID'),
    redirect_uri="http://localhost/callback",  # Must match registered URI
    scope=["tweet.read", "tweet.write"],
    client_secret=os.getenv('TWITTER_CLIENT_SECRET')
)

def init_twitter():
    return tweepy.API(tweepy.OAuth1UserHandler(
        "CTZOzydmgKyP2bGALplF4O6Ry",
        "EweGPl6b8mYNuOgE7hSEPtLDw8mlDqJ3sSVv0z1UYxFapap5BU",
        "1670380152042426369-vHclIFEqBFBTu9DtAeyqBV1qYjxqmD",
        "a6Zi0rAqMKoKy1Xkyxg6gtTFD9FDJp6wPt4edDQMV0vrxtesr"
    ))
    

def generate_post(keywords):
    client = genai.Client(api_key="AIzaSyDY8Rn8cOeMIcRxikt20HetJp3DRPPAyNM")
    response = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17",
    contents=[f"I am a student Create a professional social media post about these topics: {keywords}. Include relevant hashtags. Keep it under 280 characters."]
    )
    return response.text

def post_to_twitter(api, content):
    try:
        api.update_status(content)
        print("Posted to Twitter successfully!")
    except tweepy.TweepyException as e:
        print(f"Twitter Error: {e}")

def daily_post():
    print(f"\nDaily Post Generator - {datetime.now().strftime('%Y-%m-%d')}")
    keywords = input("What did you work on today? (comma-separated keywords): ")
    
    post_content = generate_post(keywords)
    print("\nGenerated Post:\n" + post_content)
    
    confirm = input("\nPost this content? (y/n): ")
    if confirm.lower() == 'y':
        twitter_api = init_twitter()
        post_to_twitter(twitter_api, post_content)
    else:
        print("Posting cancelled.")

schedule.every().day.at("01:47").do(daily_post)

if __name__ == "__main__":
    
    daily_post()
    
    print("Social Media Scheduler Running...")
    while True:
        schedule.run_pending()
        time.sleep(60)