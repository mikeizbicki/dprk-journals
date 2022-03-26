# DPRK-Journals

This is a collection of all of the PDFs published in journals by the Kim Il Sung University in the DPRK as of 25-03-2022.

The original source of this information is at the url <http://www.ryongnamsan.edu.kp/univ/ko/research/journals>,
but unfortunately the DPRK's website does not provide direct download links to the pdfs.
So I wrote some scripts that will download the raw pdfs.
All of the raw pdfs are in the `pdfs` folder in the same location that they are stored on the DPRK's server (which means they're organized by subject area and year).

The pdfs can be updated by running the two commands:
```
$ sh build-webcache.sh && sh download-pdfs.sh
```
The first command downloads the html files that store the links to the pdfs; the second command extracts those links and downloads the raw pdfs.
In total, it took me about 15 hours to download all of the pdfs.

A further command
```
$ python3 extract-info.py
```
will generate the `metainfo.jsonl` file that contains extracted metainfo about each of the files.
Unfortunately, the files do not store metainformation as-per the pdf standard, and so the information must be extracted directly from the text.
This is an error-prone process, especially since all of the pdfs have slightly different formatting from each other.
