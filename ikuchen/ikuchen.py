#!/usr/bin/env python3
"""
The IKuchen RCE Challenge.
Have the .py and eat it, too.
Just cat 🐈 the flag.
"""
import re, sys, signal, datetime
from subprocess import Popen, PIPE
from functools import partial
from socketserver import ForkingTCPServer, BaseRequestHandler

PORT = 5656


class RequestHandler(BaseRequestHandler):
    def handle(self):
        print(
            "{}: session for {} started".format(
                datetime.datetime.now(), self.client_address[0]
            )
        )
        fd = self.request.makefile("rwb", buffering=0)
        main(fd, fd, bytes=True)


def main(f_in=sys.stdin, f_out=sys.stdout, bytes=False):
    def enc(str):
        if bytes:
            return str.encode()
        return str

    def decode(b):
        if bytes:
            return b.decode()
        return b

    def alarm_handler(signum, frame):
        f_out.write(enc("\nOut[∞]: Good bye :)\n"))
        print("{}: Another timeout reached.".format(datetime.datetime.now()))
        sys.exit(15)

    if "debug" not in sys.argv:
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(15)

    f_out_no = f_out.fileno()

    r = r"p*[^%\x2D-\x3D\x40-\x50\x27\x5F-\x6D\x20\x76-\x7A]*,*"
    cat_food = partial(re.compile(r).sub, "")
    proc = Popen(
        ["python3", "-u", "-m", "IPython", "--HistoryManager.enabled=False"],
        stdin=PIPE,
        stdout=f_out_no,
        stderr=f_out_no,
    )
    si = proc.stdin
    f_out.write(
        enc(
            "Oh hi there, I didn't see you come in!\n"
            "  How do you do?\n"
            "  There must be a flag lying around somewhere on this blech.\n"
            "  If you could be so kind and help me find it.\n"
            "  How do 15 seconds of RCE in IPython sound?\n"
            "  Sadly the cat ate some of characters while I baked them. 🐈\n\n"
        )
    )
    while True:
        userinput = cat_food(decode(f_in.readline())).strip()
        if userinput.startswith("%"):
            f_out.write(
                enc(
                    (
                        "Out[?]: The cat 🐈 will eat lines starting with `%`.\n"
                        "        Oh and btw I found out it eats the following: `{}` \n\n"
                        "In [.]: ".format(r)
                    )
                )
            )
            f_out.flush()
        elif "%%" in userinput:
            f_out.write(
                enc(("Out[!]: The cat got this one. Seems to be yummy.\n\nIn [.]: "))
            )
        else:
            # forward "sanitized" input to IPython
            si.write("{}\n".format(userinput).encode())
            si.flush()


if __name__ == "__main__":
    print("Listening on port {}".format(PORT))
    ForkingTCPServer(("0.0.0.0", PORT), RequestHandler).serve_forever()
