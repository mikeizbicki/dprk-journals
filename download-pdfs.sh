#!/bin/sh

articles=$(grep -ho '/univ/ko/research/[a-zA-Z]*/[a-zA-Z0-9/]*[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]' -R webcache/www.ryongnamsan.edu.kp | sort | uniq)

num_articles=$(echo "$articles" | wc -l)
echo "num_articles=$num_articles"

for article in $articles; do
    url_html="http://www.ryongnamsan.edu.kp/$article"
    url_pdf="$(echo "$url_html" | cut -d'/' -f1-8)/paper/$(basename $article)"
    echo $(date -Ins) $url_pdf
    outdir=$(dirname "pdfs/$article")
    mkdir -p $outdir
    wget --tries=0 -c -a download.log -O "pdfs/$article" $url_pdf
done
