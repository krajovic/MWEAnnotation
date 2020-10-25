import os
import numpy as np
import xml.etree.ElementTree as ET

'''This script calculates Cohen's Kappa on two input sets of annotation'''

# a mapping from tag to index in the agreement matrix
tag_to_index = {'F':0, 'S':1, 'B':2}
# matrix representing agreement on classification of identified MWEs
agreement_matrix = np.zeros((3,3),dtype=int)

# the set of MWEs identified by annotator1
ann1_tags = set()
# the set of MWEs identified by annotator2
ann2_tags = set()

'''Reads in and stores all MWEs identified by each annotator in the corresponding directories'''
def read_files(ann1, ann2):
    global ann1_tags, ann2_tags, agreement_matrix
    for rt, dirs, files in os.walk(ann1):
        for name in files:
        # with both files corresponding to a given text open,
            with open(os.path.join(rt, name), 'r') as a1, open(os.path.join(ann2, str(2) + name[1:]), 'r') as a2:
                # the roots of the XML trees for each file
                a1_root = ET.parse(a1).getroot()
                a2_root = ET.parse(a2).getroot()
                # if they are not the same text there has been a mistake in file naming
                if not a1_root[0].text == a2_root[0].text:
                    raise ValueError('These texts are not the same and cannot be compared')
                # tags in each file
                a1_tags = list(a1_root[1])
                a2_tags = list(a2_root[1])
                # unique identifier for this file
                id = name[-6:-4]
                # add the tags to the tag sets
                get_tags(a1_tags, a2_tags, id)
    # for every MWE identified by both annotators, add a count to the appropriate place
    # in the matrix to represent it.
    for tag in ann1_tags:
        # MWE of annotator1 without the classification tag
        trim = tag[2:]
        for tag2 in ann2_tags:
            # MWE of annotator2 without the classification tag
            trim2 = tag2[2:]
            # if they are equal, this is a match
            if trim == trim2:
                # add one to the agreement matrix in the location according to the classification tags.
                agreement_matrix[tag_to_index[tag[:1]]][tag_to_index[tag2[:1]]] += 1


'''Adds all tags to the tag_set along with their classification.'''
def get_tags(a1_tags, a2_tags, id):
    global ann1_tags, ann2_tags
    # for all of annotator1's tags
    for tag in a1_tags:
        # create a tag according to the classification of the MWE
        if tag.tag == 'FLEXIBLE':
            t = 'B'
        elif tag.tag == 'SEMI_FIXED':
            t = 'S'
        else:
            t = 'F'
        # the unique identifier is <classification_tag>_<span>_<text>_id
        tag_string = t + '_' + tag.attrib['spans'] + '_' + tag.attrib['text'] + '_' + id
        # add the unique identifier to the tag set
        ann1_tags.add(tag_string)
    # repeat this process for annotator2
    for tag in a2_tags:
        if tag.tag == 'FLEXIBLE':
            t = 'B'
        elif tag.tag == 'SEMI_FIXED':
            t = 'S'
        else:
            t = 'F'
        tag_string = t + '_' + tag.attrib['spans'] + '_' + tag.attrib['text'] + '_' + id
        ann2_tags.add(tag_string)


'''Calculates Cohen's Kappa and prints it.'''
def kappa():
    global agreement_matrix
    # calculate observed agreement
    observed = agreement_matrix.diagonal().sum()/agreement_matrix.sum()
    # calculate expected agreement
    expected = 0
    for i in range(0, len(agreement_matrix[0])):
        j = abs(len(agreement_matrix[0])-i-1)
        num = agreement_matrix[i].sum() * agreement_matrix[:,i].sum()
        expected += (num/agreement_matrix.sum())
    expected = expected/agreement_matrix.sum()
    # calculate Kappa
    kappa = (observed-expected)/(1-expected)
    print('Kappa: ' + str(kappa))


if __name__ == '__main__':
    print()
    #read_files('a1', 'a2')
    #print(agreement_matrix)
    #kappa()
