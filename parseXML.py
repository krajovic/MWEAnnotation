import os
import xml.etree.ElementTree as ET
import re

'''reads all annotated XML files in the input directory into a single text 
file representing all sentences in the ipnut files with each MWE tagged
with a its category. Eg, (_FLEXIBLE, _SEMI_FIXED, _FIXED). Each word in 
a given MWE is tagged, according to the classification of the MWE'''
def parse(docs):
    # write data to a file called 'mwe_data.txt'
     out_file = open("mwe_data.txt", 'w')
    # for all files in the directory
     for rt, dirs, files in os.walk(docs):
        for name in files:
            #print(os.path.join(rt,name))
            with open(os.path.join(rt,name), 'r') as f:
                #  variables to help ensure that adjacent MWEs do not get merged
                flexible = 1
                fixed = 1
                semi = 1
                # parse the xml
                tree = ET.parse(f)
                # root of xml tree
                root = tree.getroot()
                # the text is the first element in the root
                text = root[0].text
                # the tags are the second element
                tags = root[1]
                # tracks how much to adjust the string indices based on the length
                # of the tags that we've added so far
                tag_adjust = 0
                # list of all identified mwes
                tag_list = list(tags)
                # mwes sorted in the order that they appear in the text
                tag_list.sort(key=lambda x: int(x.attrib['spans'].split(',')[0].split('~')[0]), reverse=False)
                # regex to grab the id number
                id_num = re.compile('text-\d* reviews-\d{6}-\d{4}: ')
                # for each mwe
                for tag in tag_list:
                    # generate the tag
                    tag_name = '_' + tag.tag
                    # grab its span in the text
                    spans = tag.attrib['spans']
                    # if it's discontiguous, split into a list of spans
                    spans = spans.split(',')
                    # booleans tracking whether or not we just saw a certain kind of mwe
                    it_was_flexible = False
                    it_was_fixed = False
                    it_was_semi = False
                    # for all spans that this mwe covers
                    for span in spans:
                        # split the span into begin_index and end_index
                        span = span.split('~')
                        # adjust the end_index to account for added tags
                        end = int(span[1])+tag_adjust
                        # grab the text corresponding to the mwe from the original text
                        text_span = text[int(span[0])+tag_adjust:end]
                        # split the text span on whitespace to get each token
                        text_span = text_span.split()
                        # store the text at this point
                        old_text = text
                        # index at which to add the tag
                        add_at = int(span[0]) + tag_adjust
                        # for each word in the mwe
                        for word in text_span:
                            # if the tag is flexible, it can be discontiguous so we have to ensure it doesn't get split
                            # to make sure elements of flexible MWEs stay together, we will tag them with either
                            # _FLEXIBLE0 or _FLEXIBLE1, all words in the flexible MWE will have the same tag,
                            # and these tags will alternate for each flexible MWE identified.
                            if tag_name == '_FLEXIBLE':
                                # add the tag to the token
                                word = word + tag_name + str(flexible%2)
                                # track the fact that this was a flexible mwe
                                it_was_flexible = True
                            elif tag_name == '_SEMI_FIXED':
                                # add the tag to the token
                                word = word + tag_name + str(semi % 2)
                                # track the fact that this was a flexible mwe
                                it_was_semi = True
                            elif tag_name == '_FIXED':
                                # add the tag to the token
                                word = word + tag_name + str(fixed % 2)
                                # track the fact that this was a flexible mwe
                                it_was_fixed = True
                            # add the new token to the text
                            text = text[:add_at - 1] + ' ' + word + old_text[end:]
                            # update the tag adjust factor
                            tag_adjust += len(tag_name) + 1
                            # update the next point we will add a tag
                            add_at += len(word) + 1
                            # if it's not a flexible MWE, it will be contiguous, so it will never get split up
                            """else:
                                # add the tag to the token
                                word = word + tag_name
                                # add the new token to the text
                                text = text[:add_at-1] + ' ' + word + old_text[end:]
                                # update tag adjust factor
                                tag_adjust += len(tag_name)
                                # update the next point we will add a tag
                                add_at += len(word) + 1"""
                    # we just finished tagging a MWE of a certain type, so change the identifier
                    # that will be appended to the next one of that type that we see
                    if it_was_flexible:
                        flexible += 1
                        it_was_flexible = False
                    elif it_was_fixed:
                        fixed += 1
                        it_was_fixed = False
                    elif it_was_semi:
                        semi += 1
                        it_was_semi = False
                # for each line in the text
                for line in text.splitlines():
                    # grab the id number
                    id = re.search(id_num, line)
                    if id:
                       # the data from the line is everything except the id number
                        data = line[len(id.group()):]
                       # write the data to the file
                        out_file.write(data + '\n')


if __name__ == '__main__':
    pass
    #parse('raw_annotation')