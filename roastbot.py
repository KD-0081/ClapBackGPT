import os  # Standard library for environment variables
import random  # Used to select fallback roasts if API fails
import time
import tweepy  # Twitter API library (v2 OAuth only)
import google.generativeai as genai  # Google Gemini AI API
from dotenv import load_dotenv  # Library to load .env file


# Load API keys from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")  # Twitter API Key
API_SECRET = os.getenv("API_SECRET")  # Twitter API Secret
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Twitter Access Token
ACCESS_SECRET = os.getenv("ACCESS_SECRET")  # Twitter Access Secret
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # Twitter Bearer Token
GEMINI_API_KEY = os.getenv("YOUR_GEMINI_API_KEY")  # Gemini API Key

# Authenticate Twitter API using OAuth 2.0
client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY,
                        consumer_secret=API_SECRET, access_token=ACCESS_TOKEN,
                        access_token_secret=ACCESS_SECRET)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to generate a roast using Gemini API
def generate_roast(original_tweet):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Craft a savage yet humorous roast based on this tweet: '{original_tweet}' in less than 250 characters. Keep it witty but not overly offensive. Refuse to provide any comment on anything political or religious"
        response = model.generate_content(prompt)  # Generate text response from Gemini
        return response.text.strip()  # Return the clean response

    except Exception as e:
        print(f"Gemini API error: {e}")  # Print error if Gemini fails
        return random.choice([
            "You're proof that even evolution takes a step back sometimes.",
            "You're like a cloud. When you disappear, it's a beautiful day.",
            "You bring everyone so much joy... when you leave the room.",
            "I'd agree with you but then we’d both be wrong.",
            "You're not stupid; you just have bad luck thinking."
        ])  # Return a random predefined roast if API fails

# Function to fetch latest mentions and reply with a roast
def roast_mentions():
    mentions = client.get_users_mentions(id=client.get_me().data.id, tweet_fields=["conversation_id", "referenced_tweets"], max_results=5)  # Fetch latest mentions
    if mentions.data:
        for mention in mentions.data:
            time.sleep(5)  # Wait 5 seconds between requests
            tweet_id = mention.id  # Get tweet ID
            username = mention.author_id  # Get user ID who mentioned the bot
            original_tweet = mention.text.lower()  # Convert original tweet to lowercase
            
            # Get the original tweet being replied to
            parent_text = ""
            if mention.referenced_tweets:
                for ref_tweet in mention.referenced_tweets:
                    if ref_tweet.type == "replied_to":
                        parent_tweet = client.get_tweet(ref_tweet.id, tweet_fields=["text"])
                        if parent_tweet.data:
                            parent_text = parent_tweet.data.text  # Get original tweet's text
                        break
            
            roast = generate_roast(parent_text)  # Generate roast using actual tweet content
            reply_text = f"{roast}"  # Format reply tweet
            client.create_tweet(text=reply_text, in_reply_to_tweet_id=tweet_id)  # Post reply
            print(f"Replied to @{username}: {roast}")  # Print confirmation in console

# Main function to run the bot
if __name__ == "__main__":
    roast_mentions()  # Call function to check mentions and reply



