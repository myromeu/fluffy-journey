OTUServer
=====================


Веб-сервер частично реализующий протоĸол HTTP. Использует архитектуру основанную на потоков.

Пример запуска:
```
python3 httpd.py -w 6 -r web_root -H 192.168.0.1 -p 8080
```

Опции:
`-H` - хост на котором будет запущен сервер
`-p` - порт на котором будет запущен сервер

## Нагрузочное тестирование ##

```
$ ab -n 50000 -c 160 -r http://localhost:8080/   
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        little_0.01
Server Hostname:        localhost
Server Port:            8080

Document Path:          /
Document Length:        342 bytes

Concurrency Level:      160
Time taken for tests:   21.806 seconds
Complete requests:      50000
Failed requests:        0
Total transferred:      22000000 bytes
HTML transferred:       17100000 bytes
Requests per second:    2292.90 [#/sec] (mean)
Time per request:       69.781 [ms] (mean)
Time per request:       0.436 [ms] (mean, across all concurrent requests)
Transfer rate:          985.23 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3  64.0      0    3039
Processing:     3   66   7.8     66     900
Waiting:        3   66   7.8     66     900
Total:          7   70  65.4     66    3106

Percentage of the requests served within a certain time (ms)
  50%     66
  66%     67
  75%     68
  80%     68
  90%     69
  95%     70
  98%     71
  99%     74
 100%   3106 (longest request)
```
