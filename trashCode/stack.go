package main

import (
	"bufio"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/csv"
	"io"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

func certToCSV(cert *x509.Certificate, domain string) []string {
	var data []string
	data = append(data, domain[:len(domain)-4])
	var org string
	if len(cert.Issuer.Organization) > 0 {
		org = cert.Issuer.Organization[0]
	}
	data = append(data, org)
	if cert.PublicKey != nil {
		rsaPublicKey := cert.PublicKey.(*rsa.PublicKey)
		data = append(data, rsaPublicKey.N.String())
		data = append(data, strconv.Itoa(rsaPublicKey.E))
		data = append(data, strconv.Itoa(rsaPublicKey.Size()))
	}
	return data
}

func getCerts(d string) ([]*x509.Certificate, error) {
	out := []*x509.Certificate{}
	dialer := net.Dialer{}
	dialer.Timeout = 10 * time.Second
	conn, err := tls.DialWithDialer(&dialer, "tcp", d, &tls.Config{
		InsecureSkipVerify: true,
	})
	if err != nil {
		return out, err
	}
	defer conn.Close()
	for _, cert := range conn.ConnectionState().PeerCertificates {
		if v := cert.PublicKeyAlgorithm.String(); v != "RSA" {
			log.Printf("%q not using RSA algorithm but %q", d, cert.PublicKeyAlgorithm)
			continue
		}
		if len(cert.Issuer.Organization) < 1 {
			log.Printf("%q does not have organization", d)
			continue
		}
		out = append(out, cert)
	}
	return out, err
}

func analyze(dst chan []string, src chan string, errs chan error) {
	for domain := range src {
		certs, err := getCerts(domain)
		if err != nil {
			errs <- err
			continue
		}
		for _, cert := range certs {
			record := certToCSV(cert, domain)
			dst <- record
		}
	}
}

func readCSVFile(dst chan string, fp string) error {
	file, err := os.Create(fp)
	if err != nil {
		return err
	}
	defer file.Close()

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		if !strings.Contains(line, ":") {
			line = line + ":443"
		}
		dst <- line
	}
	return scanner.Err()
}

func readCSV(dst chan string, src io.Reader) error {
	scanner := bufio.NewScanner(src)
	for scanner.Scan() {
		line := scanner.Text()
		if !strings.Contains(line, ":") {
			line = line + ":443"
		}
		dst <- line
	}
	return scanner.Err()
}

func writeCSV(dst io.Writer, src chan []string, errs chan error) {
	w := csv.NewWriter(dst)
	for record := range src {
		if err := w.Write(record); err != nil {
			errs <- err
		}
		w.Flush()
	}
	if err := w.Error(); err != nil {
		errs <- err
	}
}
func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	var wg sync.WaitGroup
	errs := make(chan error)
	src := make(chan string)
	t1 := make(chan []string)
	f, err := os.Create("results.csv")
	check(err)

	// synchronize all routines to close errs once
	go func() {
		wg.Wait()
		close(errs)
	}()

	var wg2 sync.WaitGroup
	// analyze multiple domains in //
	for i := 0; i < 50; i++ {
		wg.Add(1)
		wg2.Add(1)
		go func() {
			defer wg.Done()
			defer wg2.Done()
			analyze(t1, src, errs)
		}()
	}

	// synchronize with analyze routines to close t1
	go func() {
		wg2.Wait()
		close(t1)
	}()

	// write the csv file
	wg.Add(1)
	go func() {
		defer wg.Done()
		writeCSV(f, t1, errs)
	}()

	// read the csv, fail if an error occurs reading the source
	wg.Add(1)
	go func() {
		defer wg.Done()
		err := readCSV(src, os.Stdin)
		if err != nil {
			log.Fatal(err)
		}
		close(src)
	}()

	// read and print errors, adjust exit code
	var exitCode int
	for err := range errs {
		log.Println(err)
		exitCode = 1
	}
	os.Exit(exitCode)
}
