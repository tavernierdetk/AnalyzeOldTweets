import csv
import pandas as pd
from tempfile import NamedTemporaryFile
import shutil

def removeDuplicates(csvFilePath):

    df = pd.read_csv(csvFilePath)
    print(df.shape)
    df = df.drop_duplicates()
    print(df.shape)
    df.to_csv(csvFilePath)

def createReplacementCSV(dictionary, outputFile):
    with open(outputFile, mode='w') as tweetCollection:
        writer = csv.writer(tweetCollection, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for destTerm in dictionary:
            for originalTerm in dictionary[destTerm]:
                writer.writerow([destTerm,originalTerm])



def findAndReplace(filePath,replacementFile):

    tempfile = NamedTemporaryFile(delete=False, mode='w')

    with open(filePath, mode='r') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')
        for row in reader:

            with open(replacementFile) as csvfile:
                read = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row2 in read:
                        row[1] = row[1].lower().replace(row2[1].lower()," " + row2[0].lower() + " ")
            writer.writerow(row)

    shutil.move(tempfile.name, filePath)
    print ("Wrote to: " + filePath)



if __name__ == "__main__":

    replacementDict = {
        "bernie": [
            "bern",
            "bernard",
            "sanders",
            "berniesanders",
            "bernies"
        ],
        "bloomberg": [
            "mikebloomberg",
            "blooming",
            "mike",
            "michaelbloomberg",
            "vettingbloomberg",
            "bloomy",
            "bloomberg2020",
            "bloomberg‚Äôs",
            "bloombergisanoligarch",
            "bloombergistrump",
            "neverbloomberg",
            "maybebloomberg"
        ],
        "immigration": [
            "immigrant",
            "immigrants",
            "standupforimmigrants",
            "foreign"
        ],
        "climate": [
            "climatecrisis",
            "climatechange",
            "climateemergency",
            "endclimatesilence",
            "climatechangeisreal",
            "warming",
            "hospitals",
            "health",
            "energy"
        ],
        "economy": [
            "money",
            "hospitals",
            "taxes",
            "wealth",
            "socialist",
            "socialism",
            "billionaire",
            "billionaires"
        ]
    }
    # removeDuplicates('all_tweets.csv')
    createReplacementCSV(replacementDict)
    findAndReplace('all_tweets.csv', 'replacementList.csv')
