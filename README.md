# Search Term Recommender
The [Search Term Recommender](https://search-term-recommender.readthedocs.io/en/latest/index.html) is an add-on for [Orange3](https://orangedatamining.com/), a data mining software which allows users to build data mining workflows by visual programming. This add-on supports researchers in finding search terms for a systematic literature research (SLR) by recommending search terms based on a set of input documents. 

The add-on consists of three widgets:
- [Import documents](https://search-term-recommender.readthedocs.io/en/latest/importer.html) 
- [Recommend search terms](https://search-term-recommender.readthedocs.io/en/latest/recommender.html)
- [Display search terms](https://search-term-recommender.readthedocs.io/en/latest/displayer.html)


## Installation
Create a conda environment like so:
```
conda create python=3.10 --platform osx-64 --name search-term-recommender
```

Install Orange3:
```
conda install orange3
```

Install [pke](https://github.com/boudinfl/pke/tree/master), an open source python-based toolkit for keyphrase extraction as specified in the README: 
```
pip install git+https://github.com/boudinfl/pke.git
```

Download the English language model for SpaCy:
```
python -m spacy download en_core_web_sm
```

Clone the repository:
```
git clone https://github.com/liaaneeee/Search-Term-Recommender.git
```

Pip install the add-on from the root directory:
```
pip install .
```



## Usage

## Example