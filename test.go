package main

import (
    "fmt"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)

func dbConn() (db *sql.DB) {
    dbDriver := "mysql"
    dbUser := "admin"
    dbPass := "Stanley78!"
    dbName := "tcp(139.59.179.77:3306)/Certificates"
    db, err := sql.Open(dbDriver, dbUser+":"+dbPass+"@"+dbName)
    if err != nil {
        panic(err.Error())
	}
    return db
}

func main() {
    fmt.Println("Go MySQL Tutorial")

    // Open up our database connection.
    // I've set up a database on my local machine using phpmyadmin.
    // The database is called testDb
	db := dbConn()
	selDB, err := db.Query("SELECT count(*) FROM cert")
	fmt.Println("%s",selDB)
	if err != nil {
        panic(err.Error())
    }
    // defer the close till after the main function has finished
    // executing
    defer db.Close()

}