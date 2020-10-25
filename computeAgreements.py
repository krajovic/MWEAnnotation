import os
import xml.etree.ElementTree as ET

'''This script computes precision, recall, and f1-score between an annotator and the gold standard.'''

'''It outputs two values for each of these metrics, one corresponding to the precision, recall, and f1
for full, perfect MWE matches, and another corresponding to partial matches.'''

'''Full matches are only counted if the identified MWE has the exact same span as the MWE in the gold standard. 
Partial matches look at each word identified as part of an MWE. For example, if there exists a MWE comprised of 3 tokens
in the gold standard, and the annotator identifies two of these tokens as part of a MWE, but leave out the
third, these two tokens will count towards the annotator's score. Thereby the annotator is awarded partial
credit. Credit would not awarded, in a scenario like this, towards the full match agreement.'''


# the number of perfect matches between the annotator and the gold standard
full_shared = 0
# the number of MWEs identified by the annotator
an_full_count = 0
# the number of MWEs in the gold standard
gs_full_count = 0

# the number of partial matches between the annotator and the gold standard
partial_shared = 0
# the number of tokens identified as part of an MWE by the annotator
an_partial_count = 0
# the number of tokens that appear as part of an MWE in the gold standard
gs_partial_count = 0

# a collection of strings representing each MWE in the gold standard
gs_ftag_set = set()
# a collection of strings representing each MWE identified by the annotator
an_ftag_set = set()
# a collection of strings representing each word identified as part of a MWE in the gold standard
gs_tag_set = set()
# a collection of strings representing each word identified as part of a MWE by the annotator
an_tag_set = set()


'''reads in data from all files in two coordinated directories, one containing the gold standard
files and the other containing the files annotated by the given annotator.'''
def read_files(goldstandard, annotator):
    global full_shared, partial_shared, agreement_matrix, tag_to_index
    for rt, dirs, files in os.walk(annotator):
        for name in files:
        # open the annotator's file and the corresponding gold standard file
            with open(os.path.join(rt, name), 'r') as g, open(os.path.join(goldstandard, name[2:]), 'r') as a:
                # roots of the XML trees for each file
                g_root = ET.parse(g).getroot()
                a_root = ET.parse(a).getroot()
                # if the text are not the same, they can't be compared and there was an error
                # in the setup of the files, so raise an exception
                if not g_root[0].text == a_root[0].text:
                    raise ValueError('These texts are not the same and cannot be compared')
                # all tags in each file
                g_tags = list(g_root[1])
                a_tags = list(a_root[1])
                # the id helps to ensure that two MWEs with the same spans and same tokens in
                # different files cannot be confused. It serves as a unique identifier based on
                # the file name, which will be enough to differentiate MWEs with identical tokens
                # could never have the same span in a single file
                id = name[-6:-4]
                # count all MWEs in each file
                full_mwe(g_tags, a_tags, id)
                # count all words identified as part of a MWE in each file
                partial_mwe(g_tags, a_tags, id)
     # once all MWEs have been counted, count instances of overlap
    for tag in gs_ftag_set:
        if tag in an_ftag_set:
            # if the MWE in the gold standard was identified by the annotator, this is a match
            full_shared += 1
    # once all words have been counted, count instances of overlap
    for tag in gs_tag_set:
        if tag in an_tag_set:
            # if a word in the gold standard was identified by the annotator, this is a match
            partial_shared += 1


'''counts all MWEs found by the annotator, and all MWes in the gold standard and adds 
a string representation of each MWE to a set'''
def full_mwe(g_tags, a_tags, id):
    global gs_full_count, an_full_count, full_shared, gs_ftag_set, an_ftag_set
    # for all MWEs in the gold standard
    for tag in g_tags:
        # create a string representation of the MWE in the format:
            # <span>_<text>_id
        tag_string =  tag.attrib['spans'] + '_' + tag.attrib['text'] + '_' + id
        # add this representation to the set
        gs_ftag_set.add(tag_string)
        # increment the count by 1
        gs_full_count += 1
    # repeat this process for the annotator's files
    for tag in a_tags:
        tag_string = tag.attrib['spans'] + '_' + tag.attrib['text'] + '_' + id
        an_ftag_set.add(tag_string)
        an_full_count += 1


'''counts all tokens identifed as part of a MWE for both the annotator file
and the gold standard. Adds a string representation of each token to a set'''
def partial_mwe(g_tags, a_tags, id):
    global partial_shared
    # for each tag in the gold standard tags, count all words in the tag
    for tag in g_tags:
        split_and_count_words(tag, id, 'g')
    # for each tag in the annotator's tags, count all words in the tag
    for tag in a_tags:
        split_and_count_words(tag, id, 'a')


'''splits a tag into individual tokens and adds a unique string identifer of each 
token to the set of tokens identified.'''
def split_and_count_words(tag, id, key):
    global gs_tag_set, an_tag_set, gs_partial_count, an_partial_count
    # grab all spans, there will be 1 for contiguous MWEs, and more than 1 for discontiguous MWEs
    spans = tag.attrib['spans'].split(',')
    # if this is a contiguous MWE
    if len(spans) == 1:
        # grab the associated tokens
        text = tag.attrib['text'].split()
        # the index of where the MWE begins
        span_start = int(spans[0].split('~')[0])
        # for each token comprising the MWE
        for word in text:
            # unique identifier in form of: <span_start>_<token>_id
            tag_string = str(span_start) + '_' + word + '_' + id
            # if we are dealing with the gold standard add this to the gs set
            if key == 'g':
                gs_tag_set.add(tag_string)
                gs_partial_count += 1
            # if we are dealing with the annotator add this to the an set
            elif key == 'a':
                an_tag_set.add(tag_string)
                an_partial_count += 1
            # increment the span_start to the beginning of the next token
            span_start = span_start + len(word) + 1
    # if it's discontiguous
    else:
        # grab each chunk of text corresponding to each span
        text_chunks = tag.attrib['text'].split(' ... ')
        # for each chunk
        for i, text in enumerate(text_chunks):
            # split it into tokens
            text = text.split()
            # grab the corresponding span
            sub_span = spans[i]
            # note where the token starts
            span_start = int(sub_span.split('~')[0])
            # generate the unique identifier and add it to the appropriate set
            for word in text:
                tag_string = str(span_start) + '_' + word + '_' + id
                if key == 'g':
                    gs_tag_set.add(tag_string)
                    gs_partial_count += 1
                elif key == 'a':
                    an_tag_set.add(tag_string)
                    an_partial_count += 1
                span_start = span_start + len(word) + 1


'''Calculates prescision, recall, and f1-score for each of the two sets of counts. 
Prints out the results.'''
def eval():
    # calculations for Full Match
    print("Full MWE:")
    print('full shared: ' + str(full_shared))
    print('gs: ' + str(gs_full_count))
    recall = full_shared/gs_full_count
    precision = full_shared/an_full_count
    f1 = (2*precision*recall)/(precision+recall)
    print('  recall: ' + str(recall))
    print('  precision: ' + str(precision))
    print('  f1: ' + str(f1))
    # calculations for partial match
    print("Partial MWE:")
    r = partial_shared/gs_partial_count
    p = partial_shared/an_partial_count
    f = (2*p*r)/(p+r)
    print('  recall: ' + str(r))
    print('  precision: ' + str(p))
    print('  f1: ' + str(f))


if __name__ == '__main__':
    print()
    #read_files('gs', 'eli')
    #eval()
    #kappa()
    #read_files('gs', 'joe')
    #eval()
    #kappa()