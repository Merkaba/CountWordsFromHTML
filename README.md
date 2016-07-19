# CountWordsFromHTML
Parses all the HTML files in the "Html" folder utilizing JSON and indexes terms, associating them with their document

hw3.py will take in the json repository path, parse all the html files included, and map words to their respective document while counting their frequency. Example of frequency distribution:

        >>> print(fdist1)
        <FreqDist with 19317 samples and 260819 outcomes>
        >>> fdist1.most_common(50)
        [(',', 18713), ('the', 13721), ('.', 6862), ('of', 6536), ('and', 6024),
        ('a', 4569), ('to', 4542), (';', 4072), ('in', 3916), ('that', 2982),
        ("'", 2684), ('-', 2552), ('his', 2459), ('it', 2209), ('I', 2124),
        ('s', 1739), ('is', 1695), ('he', 1661), ('with', 1659), ('was', 1632),
        ('as', 1620), ('"', 1478), ('all', 1462), ('for', 1414), ('this', 1280),
        ('!', 1269), ('at', 1231), ('by', 1137), ('but', 1113), ('not', 1103),
        ('--', 1070), ('him', 1058), ('from', 1052), ('be', 1030), ('on', 1005),
        ('so', 918), ('whale', 906), ('one', 889), ('you', 841), ('had', 767),
        ('have', 760), ('there', 715), ('But', 705), ('or', 697), ('were', 680),
        ('now', 646), ('which', 640), ('?', 637), ('me', 627), ('like', 624)]
        >>> fdist1['whale']
        906
