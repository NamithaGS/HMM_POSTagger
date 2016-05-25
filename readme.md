
#Hidden Markov Model Part of Speech Tagger

This is a Hidden Markov Model part-of-speech tagger for Catalan. The training data provided is tokenized and tagged. The test data is tokenized, the program will add the tags.

python hmmlearn.py /path/to/input
</br>
The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt.

python hmmdecode.py /path/to/input
</br>
The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.
