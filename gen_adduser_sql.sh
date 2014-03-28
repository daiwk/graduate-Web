for i in $(seq 10); do
    let id=i+2
    echo "("$id",'test"$i"', '', '', '', 'pbkdf2_sha256"$"10000"$"r6jU3CNuHD1A"$"Wd/eTi5bM1OkOEktC0d5FgHTir1HnZdUuVgb1s9Y9gQ=', 1, 1, 0, '2014-02-09 16:02:47', '2014-02-04 00:00:00'),"
done
