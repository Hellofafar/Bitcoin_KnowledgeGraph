'use strict';

// // The Article Search API returns a max of 10 results at a time. Use "page" to paginate thru results

// Built by LucyBot. www.lucybot.com
var request = require('request');
var fs = require("fs");

var i = 0,
    maxSize = 100;

var test = function() {
    setTimeout(function() {
        request.get({
            url: "https://api.nytimes.com/svc/search/v2/articlesearch.json",
            qs: {
                'api-key': "b7b3fffa81764514844d7edeae70b79c",
                'q': "btc",  // Modify q to change the key word for query
                'fl': "web_url,headline,pub_date,word_count",
                'page': i
            },
        }, function(err, response, body) {
            var file = "DataCrawl/data/ytimes_btc.txt";
            body = body + '\n';

            fs.appendFile(file, body, function(err) {
                if (err) {
                    console.log(err);
                    throw err;
                }
                else {
                    console.log("Successfully get page:", i);
                }
            })
        });
        
        i++;
        if (i < maxSize) {
            test();
        }
    }, 1000);  // The Article Search API is rate limited to 1,000 calls per day, and 1 call per second.
}

test();

// var http = require('http');
// var fs = require('fs');

// var file = fs.createWriteStream("file.jpg");
// var request = http.get("http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg", function(response) {
//   response.pipe(file);
// });