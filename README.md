# SSLCertificates

The first step is to gather millions of SSL certificates. I found two solutions that i can share, you either download it from a website or you

Download [Top10MillionWebsites](https://www.domcop.com/files/top/top10milliondomains.csv.zip) or Crawl the data from [CommonCrawl](https://commoncrawl.org/the-data/get-started/) which is 60TB of Crawled Websites. With a powerfull enough computer you could parse websites name and get millions of websites.

## Get the certificates

### Javascript Hell
Requesting millions of certificates isn't an easy task. As a javascript developper I never encountered such a task. It needs to be fast and efficient. I got to experience my first memory leak in Nodejs, out of memory. I also experienced low request per second (40 per seconds).

You can check index.js in the trashCode folder if you want to see the implementation on JS.

### Let's Go Python 

I decided to move to python3 to avoid many of the headaches that I got with Nodejs. The results were not as expected (60-70) per seconds. No memory issues this time !

You can check test.py if you want to see the implementation in Python.

### Go for the win

Python was not good enough, Goland seemed like a good fit. Never used before but seemed like a good choice.

The program can be found in src/main.go

```bash
cat domainnames | go run main.go
```

You need to have one domain per line
#### V2 of main.go

> The V2 of main.go allows you to skip the next steps.

## Process the certificates

We need to decode and parse the certificates to find the information that we need. In my case the issuer, n and e

### Javascript Hell Again

I might not have learned the lesson the first time but i tried again with JS. This time I had to read 4.5M files. 

You can find my programs in filewalker.js, read.js and readfile.js

### Python for the win

I then decided to move on and use python.
The script decodes the certificates files from a folder and insert the corresponding values in a database.

## Batch GCD 

Now it is time to hack !

I created a python notebook MultiplyCerts to see the basic implementation and complexity of a Batch GCD implementation.

I found out that the complexity of the basic implementation of Batch GCD is X^2

You can find the results in MultiplyCerts.htlm

### Batch GCD Implementation

> Working on a C++ implementation with GMP for arbitrary long number.
For 20M certificates with end up with numbers that have 4*10^10 digits.

If you want to know more, please send me an email to girard.stanislas@gmail.com








