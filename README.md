# MWEAnnotation
A 15,722 word corpus comprehensively annotated for Multiword Expressions where each expression is tagged as Fixed, Semi-Fixed, or Flexible. Also contains some code used to process data and compute agreement as the corpus was being created.

# Corpus 
The corpus is prestented as XML files, with each file containing 20 texts. Each set of tokens identified as an MWE is listed along with the character span and classification of each. 

A .txt file is also included which contains all sentences in the corpus, each represented by a list of tuples made up of a token in the corpus and a corresponding tag. The tags are one of F, f, S, s, B, b, and O. F/f corresponds to fixed expressions, S/s corresponds to semi-flexible, B/b corresponds to flexible expressions and O represents a token that is not part of an MWE. Capital letters correspond to the first token in an MWE and lower case letters correspond to any other token in the MWE. 

For more details on the corpus and information on its creation, check out the final report. 
