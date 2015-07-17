// nodejs imports
var fs = require('fs');
var Promise = require("promise");
// npm imports
var _ = require('lodash');
var express = require('express');

var app = express();
app.set('view engine', 'jade');
var fs = require('fs'),
    obj,
    currentTemp = '',
    requestedTemp = 70;



// Write the callback function
var handleFile = function () {
	return new Promise( function(fulfill, reject){
		fs.readFile('./temp_data.json', function(err, data){
		    if (err) {
		    	reject(err);
		    } else {
			    var self = this;
			    obj = JSON.parse(data);
			    currentTemp = obj.cur;
			    requestedTemp = obj.req;
			    fulfill(data);
			}
		});
	});
};

app.get('/', function (req, res, next) {
	handleFile().done(function(){
    	res.render('index', { title: 'BrewPI', ctemp: currentTemp, rtemp: requestedTemp});
    });
});
app.listen(8080, '$IP_ADDRESS$');