flask-sse
=========

A small module for sse in flask

There is a (hopefully) working test/demo in `example/`  
Just run `gunicorn -c gunsse.py app:app` from that directory, then browse to `http://localhost:8000`

There should be an alternating PING and PONGs, and a randomly-generated graph should scroll (like on the flot homepage).  
*The (blue) graphs don't look the same on different tabs*

Browse to `/graph` and a number will be show, and should be plotted in a different color on the graph, keep refreshing to plot more.  
This is an example of one thread/request having an effect on the stream, and thus other thread/requests.  
*The (yellow) graphs do look the same on different tabs*
