#!/usr/bin/python3

import traceback
import glob
import os
import pprint
import json
import re
from pdfminer.high_level import extract_text


# see: https://stackoverflow.com/questions/34587346/python-check-if-a-string-contains-chinese-character
cjk_ranges = [
        ( 0xAC00,  0xD7A3),
        ( 0x4E00,  0x62FF),
        ( 0x6300,  0x77FF),
        ( 0x7800,  0x8CFF),
        ( 0x8D00,  0x9FCC),
        ( 0x3400,  0x4DB5),
        (0x20000, 0x215FF),
        (0x21600, 0x230FF),
        (0x23100, 0x245FF),
        (0x24600, 0x260FF),
        (0x26100, 0x275FF),
        (0x27600, 0x290FF),
        (0x29100, 0x2A6DF),
        (0x2A700, 0x2B734),
        (0x2B740, 0x2B81D),
        (0x2B820, 0x2CEAF),
        (0x2CEB0, 0x2EBEF),
        (0x2F800, 0x2FA1F)
    ]

def is_cjk(char):
    char = ord(char)
    for bottom, top in cjk_ranges:
        if char >= bottom and char <= top:
            return True
    return False


def has_cjk(line):
    '''
    >>> has_cjk('test')
    False
    >>> has_cjk('test발assd')
    True
    '''
    for c in line:
        if is_cjk(c):
            return True
    return False

def extract_lines(text):
    '''
    >>> extract_lines("""
    ... this is a 
    ... test
    ... 
    ... and another
    ... """)
    ['this is a test', 'and another']
    >>> print(extract_lines("""
    ... this is a 
    ... test
    ...    
    ... and another
    ... a
    ... a
    ... a
    ...
    ... b
    ... """))
    ['this is a test', 'and another a a a', 'b']
    '''
    lines = text.split('\n')
    newlines = []
    inpara = False
    for line in lines:
        line = line.strip()
        if inpara:
            if line == '':
                newlines.append(nextline)
                nextline = ''
                inpara = False
            else:
                nextline += ' ' + line
        else:
            if line != '':
                inpara = True
                nextline = line
    return newlines


if __name__=='__main__':

    # will store the metainfo for all the files
    with open('metainfo.jsonl', 'wt') as f:

        # get all pdf paths, removing subdirectories
        paths = glob.glob('pdfs/**', recursive=True)
        paths = [ path for path in paths if os.path.isfile(path) ]

        # These paths don't work
        bad_paths = ['pdfs/univ/ko/research/journals/13/2021/1/913eb3f7a1d5e28b3f30b2dda4f5569e']
        #paths = ['pdfs/univ/ko/research/journals/5/2015/8/8b4066554730ddfaa0266346bdc1b202']

        # process each pdf
        for path in paths[0:]:
            print("path=",path,flush=True)

            try:
                # process the text
                pdftext = extract_text(path)
                pdflines = extract_lines(pdftext)

                # extract header info
                info = {}
                info['path'] = path
                info['venue_korean'] = pdflines[0]
                info['subject_korean'] = pdflines[1]

                # sometimes the year and volume get merged onto a single line;
                # the parsing needs to be done differently whether this happens or not
                if '제' in pdflines[2]:
                    info['year_raw'] = pdflines[2].split('제')[0]
                    info['volume_raw'] = ' '.join(pdflines[2].split()[1:])
                    info['title_korean'] = pdflines[3]
                    info['authors_korean'] = pdflines[4]

                else:
                    info['year_raw'] = pdflines[2]
                    info['volume_raw'] = pdflines[3]
                    info['title_korean'] = pdflines[4]
                    info['authors_korean'] = pdflines[5]

                # get year
                m = re.search(r'\d{4}', info['year_raw'])
                info['year'] = int(m.group(0))

                # get volume
                m = re.search(r'\d+', info['volume_raw'])
                info['volume'] = int(m.group(0))
                m = re.search(r'\d+', info['volume_raw'][::-1])
                info['number'] = int(m.group(0)[::-1])

                # some pdfs contain an english title and abstract;
                # to extract this information, we put all of the lines of text at the bottom of the page that do not contain CJK characters in the bottomlines variable;
                # then if that variable is large enough,
                # we extract the appropriate lines
                bottomlines = []
                for line in reversed(pdflines):
                    if not has_cjk(line):
                        bottomlines.append(line)
                    else:
                        break
                bottomlines = list(reversed(bottomlines))

                if len(bottomlines)>2:
                    if bottomlines[0][0] == '－':
                        bottomlines = bottomlines[1:]
                    info['title_english'] = bottomlines[0]
                    info['authors_english'] = bottomlines[1]
                    info['abstract_english'] = ' '.join(bottomlines[2:-1])
                    info['keywords_english'] = bottomlines[-1]

                # made it to the end of the try block without an error,
                # so register success
                info['status'] = 'success'

            # record any errors
            except Exception as e:
                print(traceback.format_exc())
                info['status'] = 'failed: '+str(e)

            # print debug info
            if False:
                print("'\n'.join(pdflines)=",'\n'.join(pdflines))
                pprint.pprint(info)
                crash_me

            # append the info
            f.write(json.dumps(info)+'\n')
            f.flush()
