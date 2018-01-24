# InvesMate
A unified investment manager with support for cryptocurrency exchanges and traditional stock market.

## Inspiration
There are lot of apps that target specific markets but there's none that allow you to easily manage investments across wide variety of traditional stock market like NYSE, NASDAQ and crypto exchanges like Coinbase, Binance etc.

## What it does
InvesMate allows you to view all your investments in one place, in addition to news feed curated based on your portfolio.

## How we built it
We hosted our application on Google App Engine which runs cron to fetch stock/crypto quotes and news from realtime APIs like IEX, Coinbase, Binance, Cryptocompare, Coindesk, Cointelegraph etc and push it to Firebase. InvesMate dashboard facilitates adding and fetching user's holding using Google Datastore. This dashboard also establishes connection with Firebase to get realtime updates on market values of quotes as well as updated news. It also calculates portfolio's overall and day gains/losses.

## Challenges we ran into
The challenging part was to listen changes/updates to only those quotes/news from Firebase which user has invested in rather than listening to all updates. It required kind of hacking to programmatically create independent listeners in javascript. 

## Accomplishments that we're proud of
Unified dashboard with odometer like portfolio values updating in realtime with relevant news feed.

## What we learned
We learned a lot about javascript and firebase

## What's next for InvesMate
Detailed graphs on historical data as well as trading predictions

## Play with InvesMate using Sample Account
Login: sample@invesmate.net  
Password: samplepassword

[![Demo](https://img.youtube.com/vi/vFtY6_3lOog/0.jpg)](https://www.youtube.com/watch?v=vFtY6_3lOog)
