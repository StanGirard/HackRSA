
const mysql = require('mysql');
var fs = require('fs');

var read = 0
var errorNB = 0
// First you need to create a connection to the db host: 'database.cppynzdwfotc.eu-west-3.rds.amazonaws.com',
const con = mysql.createConnection({
    host: '167.172.165.158',
    user: 'admin',
    password: 'Stanley78!',
});


    con.connect((err) => {
        if (err) {
            console.log('Error connecting to Db');
            throw err;
            return;
        }
        console.log('Connection established');
    
        /*var sql = "CREATE TABLE IF NOT EXISTS `Certificates`.`certificate` (`id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `domain` VARCHAR(255) NULL, `certificate` VARCHAR(16000) NULL);";
        con.query(sql, function(err, result) {
            if (err) throw err;
            console.log("Table created");
        });*/
    });  