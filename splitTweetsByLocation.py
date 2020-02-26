import csv

def splitCSVByRegion(regions,inputFile):
    for location in regions:
        outputFile = location+'_'+inputFile

        fullTweetsLocation = []

        with open(inputFile) as file:
            rows = csv.reader(file, delimiter=',')
            for row in rows:
                if row[1] == location:
                    fullTweetsLocation.append(row)
        file.close()

        with open(outputFile, mode='w') as tweetCollection:
            fieldnames = ['text', 'location']
            writer = csv.DictWriter(tweetCollection, fieldnames=fieldnames)
            writer.writeheader()

            for tweet in fullTweetsLocation:
                writer.writerow({'text': tweet[0], 'location':tweet[1]})



    return

if __name__ == "__main__":
    splitCSVByRegion(['Texas', 'New York'], 'all_tweets.csv')