import os  
import random  
import time
import tweepy  #Twitter API
import google.generativeai as genai  #importGeminiAPI
from dotenv import load_dotenv  

#Load API keys from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY") 
API_SECRET = os.getenv("API_SECRET")  
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  
ACCESS_SECRET = os.getenv("ACCESS_SECRET")  
BEARER_TOKEN = os.getenv("BEARER_TOKEN") 
GEMINI_API_KEY = os.getenv("YOUR_GEMINI_API_KEY")  #GeminiAPI

#authenticateTweepy
client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY,
                        consumer_secret=API_SECRET, access_token=ACCESS_TOKEN,
                        access_token_secret=ACCESS_SECRET)

#configureGemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_roast(original_tweet):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Craft a savage yet humorous roast based on this tweet: '{original_tweet}' in less than 250 characters. Keep it witty but not overly offensive." #editAccordingly
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"Gemini API error: {e}") #ifNoResponseFromGemini
        return random.choice([
            "You're proof that even evolution takes a step back sometimes.",
            "You're like a cloud. When you disappear, it's a beautiful day.",
            "You bring everyone so much joy... when you leave the room.",
            "I'd agree with you but then we’d both be wrong.",
            "You're not stupid; you just have bad luck thinking."
        ])  #redundancy


def roast_mentions():
    mentions = client.get_users_mentions(id=client.get_me().data.id, tweet_fields=["conversation_id", "referenced_tweets"], max_results=5)  #fetchMentions
    if mentions.data:
        for mention in mentions.data:
            time.sleep(5)
            tweet_id = mention.id
            username = mention.author_id 
            original_tweet = mention.text.lower()  
            
            parent_text = ""
            if mention.referenced_tweets:
                for ref_tweet in mention.referenced_tweets:
                    if ref_tweet.type == "replied_to":
                        parent_tweet = client.get_tweet(ref_tweet.id, tweet_fields=["text"])
                        if parent_tweet.data:
                            parent_text = parent_tweet.data.text  
                        break
            
            roast = generate_roast(parent_text) #generateRoast
            reply_text = f"{roast}"  
            client.create_tweet(text=reply_text, in_reply_to_tweet_id=tweet_id)  #post
            print(f"Replied to @{username}: {roast}")

if __name__ == "__main__":
    roast_mentions()  #Call function to check mentions and reply



