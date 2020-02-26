import dataCleaning
import statOnTweets
import getOldTweets
import liftToDissimilarityMatrix
import mds
import parseForSentiment
import sentiment
import createFinalExcelFile
import lift
import splitTweetsByLocation

if __name__ == "__main__":
    print("Let's go:")

    # Start the object that will be used to craft the successive queries through GetOldTweets

    searchCriteria = {
        "hashtags":[
            "#demdebate",
            "#democraticdebate"
        ]
    }

    # this dictionary needs to be created manually, I've run the frequency count script
    # iteratively to find the appropriate words to be replaced so that as many keywords with respect to any candidate
    # and issue is replaced appropriately

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

    # candidates is not used in the search query, but need to be listed for the creation of sentiment file and
    # calculation of lift between terms. Location is used so that lift and sentiment can later be compared by state
    # and adds to the query with the --near argument

    candidates = ['bernie','bloomberg']
    issues = ['economy','climate','immigration']
    states = ["Texas", "New York"]


    # adding both issues and location to the object that will craft the query. In this iteration, issues are not added
    # to the query as queries with the structure <hashtag> + <issue> --near <location> tend to give much smaller
    # tweet count (<200)

    searchCriteria["issues"] = issues
    searchCriteria["locations"] = states

    # creating a single array with issues and candidates that will be used as the input to the lift calculation file
    liftTopics = []
    for i in candidates:
        liftTopics.append(i)
    for i in issues:
        liftTopics.append(i)


    # name all the files that will be used throughout the pipeline.


    filePath = 'New York_all_tweets.csv'
    liftMatrixFile = "OutputFiles/Lift_Matrix.csv"
    liftValuesFile = "OutputFiles/Lift_Values.csv"
    replacementFile = "OutputFiles/replacementList.csv"
    dissimilarityMatrix = "OutputFiles/dissimilarity_matrix.xlsx"
    finalExcel = 'OutputFiles/excelFinalOutput.xlsx'
    numberOfNeighbours = 7


    # run successive queries through GetOldTweets that all get concatenated to a single csv file, with text and location
    # for each tweet. Note that the csv file created will not yet have the index column added by pandas when dropping
    # duplicates. If the pipeline is started by skipping the getTweets part, the file in filePath must be changed to
    # remove those header column so that word frequency count points to the right direction.

    # getOldTweets.getTweets(searchCriteria, 3500, filePath)


    # split tweets in two sets to do the location comparison, in a further fuller pipeline, this will be the branching
    # point to start a pipeline iteration for all tweets, then one for each state
    # splitTweetsByLocation.splitCSVByRegion(states,filePath)

    # use the pandas module to quickly remove duplicate tweets
    dataCleaning.removeDuplicates(filePath)

    # this script generates the csv file from the dictionary above. Important to note that at this point in the
    # pipeline, you need to manually run the statsOnTweets script (create the word_freq.csv document) and use the result
    # to create the replacement dictionary
    dataCleaning.createReplacementCSV(replacementDict, replacementFile)

    # actually makes the replacement from the generated files
    # to consolidate all terms pertaining to a candidate or issue
    dataCleaning.findAndReplace(filePath,replacementFile)

    # creates the word_freq and word_pair_freq docs if the replacement dictionary was already created for this dataset.
    statOnTweets.countAndClean(filePath)

    # calculates lift between each issues and candidate and outputs the matrix to a set of csv files
    lift.calculateLift(filePath,liftTopics,liftValuesFile,liftMatrixFile)

    # this script converts the liftMatrix file into a .xlsx file usable by the mds function
    liftToDissimilarityMatrix.convertMatrix(liftMatrixFile,dissimilarityMatrix)

    # creates the mds map
    mds.computeMDS(dissimilarityMatrix)

    # this iterate on each combination of candidates and issue to run the sentiment analysis
    for candidate in candidates:
        for issue in issues:
            # concatenates issue/candidate for the first output file
            outputfile = './SentimentFiles/'+candidate+issue+'.csv'

            # creates the csv file for sentiment analysis, using numberOfNeighbours as a parameter to try different
            # values with different datasets.
            parseForSentiment.calculateSentimentScore(filePath,candidate,issue,numberOfNeighbours,outputfile)

            # runs the actual sentiment analysis using nltk's vader, adding the word 'ie' to the stopwords dictionary,
            # as it appeared very frequently otherwise, seemingly without giving value
            sentiment.runSentimentAnalysis('./SentimentFiles/'+candidate+issue)

            # computes the average sentiment based on the number of tweets used to normalize the statistic.
            # a further point of research might examine the standard deviation of the same data set, to see how
            # polarizing a given pair of topics are.
            sentiment.computeAverage('./SentimentFiles/'+candidate+issue)

    # this concatenates the lift and sentiment analysis for each candidate/issue pair so that they can be examined
    # in a single table.
    createFinalExcelFile.createExcelSheet(candidates,issues,finalExcel,dissimilarityMatrix)


