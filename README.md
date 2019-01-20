# gender
Guess the gender of the author of a short text. 

1. Corpora

1.1. `Corpus T` - a corpus of recent tweets.
1.1.1 Test access rights to Twitter's API via 'twirl'.
1.1.2 Select a library to consume the API.
'QTweetLib' requires Qt4, which I am reluctant to install.
'twitcurl' seems to work for a lot of people, but the included demo keeps returning:
`twitterClient:: twitCurl::accountVerifyCredGet web response:`
`{"errors":[{"code":89,"message":"Invalid or expired token."}]}`
Finally 'birdy' - "a super awesome Twitter API client for Python in just a little under 400 LOC." is selected.
1.1.3 For labling, obtain a table of common and unambiguous male and female names.
1.1.3.1 Downloaded 200 most common male/female names in the USA from `https://www.ssa.gov/OACT/babynames/decades/century.html`
With some scraping, a more comprehensive list of about 10 000 names can be compiled.
1.1.3.2 Remove any ambiguities and ensure the final lists are the same lenghth.

