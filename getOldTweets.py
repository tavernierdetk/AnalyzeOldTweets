import GetOldTweets3
import csv


def getTweets(dictionary, numberOfTweets, outputFile):

    fullTweets = []
    for location in dictionary["locations"]:
        for hashtag in dictionary["hashtags"]:
            # for issue in dictionary["issues"]:
            searchTerms = GetOldTweets3.manager.TweetCriteria().setQuerySearch(hashtag).setMaxTweets(numberOfTweets)
            searchTerms = searchTerms.setNear(location)
            Tweets = GetOldTweets3.manager.TweetManager.getTweets(searchTerms)
            print(len(Tweets))
            for tweet in Tweets:
                fullTweets.append({
                    "text": tweet.text,
                    "location": location
                })

    with open(outputFile, mode='w') as tweetCollection:
        fieldnames = ['text', 'location']
        writer = csv.DictWriter(tweetCollection, fieldnames=fieldnames)
        writer.writeheader()

        for tweet in fullTweets:
            writer.writerow(tweet)
    return



if __name__ == "__main__":

    searchCriteria = {
        "hashtags":[
            "#demdebate",
            "#democraticdebate"
        ],
        "issues": [
            "immigration",
            "climate",
            "economy"
        ],
        "locations": [
            "texas",
            "new york"
        ]
    }

    getTweets(searchCriteria, 3000, "test_tweet.csv")

