import os
import xml.etree.ElementTree as ET
from collections import defaultdict

# number of MWEs
mwe_count = 0
# number of words in all MWEs
word_count = 0

# number of flexible
flex_count = 0
# number of semi
semi_count = 0
# number of fixed
fix_count = 0

# word counts for each of these categories
num_words_fix = 0
num_words_flex = 0
num_words_semi = 0

# number of MWEs containing gaps
gaps = 0

# total words in corpus
total_words = 15722

'''generates counts to compute statistics on corpus'''
def read_files(goldstandard):
    global word_count, flex_count, semi_count, fix_count, number_of_words, num_words_fix, num_words_flex, num_words_semi, gaps, mwe_count
    for rt, dirs, files in os.walk(goldstandard):
        for name in files:
        # open the file in the gold standard
            with open(os.path.join(rt, name), 'r') as f:
                # roots of the XML trees for each file
                g_root = ET.parse(f).getroot()
                # all tags in this file
                g_tags = list(g_root[1])
                # for each tag in the file
                for tag in g_tags:
                    mwe_count += 1
                    # if it's flexible add to appropriate counts and count gap if it has one
                    if (tag.attrib['id'])[:2] == 'FL':
                        flex_count += 1
                        if '...' in tag.attrib['text']:
                            num = len(tag.attrib['text'].split()) - 1
                            gaps += 1
                        else:
                            num = len(tag.attrib['text'].split())
                        word_count += num
                        num_words_flex += num
                    # if it's fixed
                    elif (tag.attrib['id'])[:1] == 'F':
                        fix_count += 1
                        num = len(tag.attrib['text'].split())
                        word_count += num
                        num_words_fix += num
                    # if it's semi fixed
                    elif (tag.attrib['id'])[:1] == 'S':
                        semi_count += 1
                        num = len(tag.attrib['text'].split())
                        word_count += num
                        num_words_semi += num


def stats():
    global word_count, flex_count, semi_count, fix_count, number_of_words, num_words_fix, num_words_flex, num_words_semi, gaps, mwe_count
    print('words ' + str(word_count))
    print('flex words ' + str(num_words_flex))
    print('semi words ' + str(num_words_semi))
    print('fix words ' + str(num_words_fix))
    print('mwes ' + str(mwe_count))
    print('flex ' + str(flex_count))
    print('semi ' + str(semi_count))
    print('fix ' + str(fix_count))
    print('gaps ' + str(gaps))
    print('percent of words part of MWE ' + str(word_count/total_words))
    print('percent of MWEs flexible ' + str(flex_count/mwe_count))
    print('percent of MWEs fixed ' + str(fix_count/mwe_count))
    print('percent of MWEs semi ' + str(semi_count/mwe_count))
    print('percent gappy ' + str(gaps/flex_count))
    print('percent all gappy ' + str(gaps/mwe_count))
    print('percent of words part of fix ' + str(num_words_fix/total_words))
    print('percent of words part of semi ' + str(num_words_semi/total_words))
    print('percent of words part of flex ' + str(num_words_flex/total_words))
    print('avg words per mwe ' + str(word_count/mwe_count))
    print('avg words per flex ' + str(num_words_flex/flex_count))
    print('avg words per semi ' + str(num_words_semi/semi_count))
    print('avg words per fix ' + str(num_words_fix/fix_count))



if __name__ == '__main__':
    read_files('gs')
    stats()