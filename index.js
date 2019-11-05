var csv = require('csv-parser')
var fs = require('fs')
var data = []
const sslCertificate = require('get-ssl-certificate')
var error = 0;
var success = 0;
var encrypt = 0;
var inserted = 0;

const mysql = require('mysql');

// First you need to create a connection to the db
const con = mysql.createConnection({
    host: 'database.cppynzdwfotc.eu-west-3.rds.amazonaws.com',
    user: 'admin',
    password: 'Antoinestan78!',
});

con.connect((err) => {
    if (err) {
        console.log('Error connecting to Db');
        return;
    }
    console.log('Connection established');

    var sql = "CREATE TABLE IF NOT EXISTS `Certificates`.`certificate` (`id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `domain` VARCHAR(255) NULL, `certificate` VARCHAR(16000) NULL);";
    con.query(sql, function(err, result) {
        if (err) throw err;
        console.log("Table created");
    });
});

fs.createReadStream('top10milliondomains.csv')
    .pipe(csv())
    .on('data', async function(row) {

        await sslCertificate.get(row.Domain).then(async function(certificate) {
            var certi = JSON.stringify(certificate)
            var sql = "INSERT INTO Certificates.certificate (domain, certificate) VALUES (" + con.escape(row.Domain) + ", " + con.escape(certi) + ");";
            await con.query(sql, function(err, result) {

                if (err) throw err;
                inserted += 1
                console.log(inserted);

                if (certificate.issuer.O == "Let's Encrypt") {
                    encrypt += 1;
                }
                success += 1;
            });


        }).catch(function(erro) {
            //console.error(erro);
            error += 1;
        });

    })
    .on('end', function() {
        console.log('Data loaded')
    })
process.on('SIGINT', function() {
    console.log("Caught interrupt signal");
    console.log("Success: " + success)
    console.log("Error: ", error)
    console.log("Encrypt:", encrypt)
    process.exit();
});