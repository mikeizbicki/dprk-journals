#!/bin/sh

download_urls() {
    for cp in $(seq 0 $2); do
        wget -P webcache --recursive "$1?cp=$cp" --reject-regex '.'
    done
}

download_urls http://www.ryongnamsan.edu.kp/univ/ko/research/journals 350

#download_urls http://www.ryongnamsan.edu.kp/univ/ko/research/success 5
#download_urls http://www.ryongnamsan.edu.kp/univ/ko/research/articles 300
#download_urls http://www.ryongnamsan.edu.kp/univ/ko/research/literary 15
