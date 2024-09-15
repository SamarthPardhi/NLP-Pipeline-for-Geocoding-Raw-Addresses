# NLP Pipeline for Geocoding Raw Addresses

Here is a portion of the code/project that has been made public. The complete code is hosted on the private Jupyter server of IISER Pune. In this project, we employ various machine learning methods for geocoding. We utilize state-of-the-art NLP tools, such as Spacy and Sentence Transformers, to standardize and extract features from the input addresses. We then use weak supervision and specialized supervised learning techniques to train models that accurately assign addresses to their respective wards.

## Files

1. `Addresses.csv`: The input file Addresses of residences in Pune city in raw format. [Gievn here as an example]
2. `localities_list.xlsx`: File containing the localities, Wards and Prabhags names as an additional information to classify the addresses. [Gievn here as an example]
3. `preprocess.py`: Preprocesses the address data
4. `SetFit on weak labelled data`: SetFit model trained on the weak labelled address data
5. `Skweak weak labelling`: Skweak model trained on the weak labelled address data
