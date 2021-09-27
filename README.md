# model-card-generator
Command line tool to generate documentation in the form of a model card

Developed by [xD | U.S. Census Bureau](https://www.xd.gov/)

**What is a model card?**

A model card is a documentation tool to increase transparency and share information with a wider audience about a model’s intent, data, architecture, and performance. These brief documents are intended for a technical and non-technical audience to gain insight on a machine learning, AI, or automation model at any phase in development. 

The cards address bias in a user’s workflow by guiding them through a series of questions that illuminate steps frequently considered but not documented. The user is asked to describe topics such as: the use cases of the model, the structure of the data, and the evaluation tools used in development. 

**Why is this tool important?**

The model card generator aims to reduce bias in government machine learning workflows by exploring a model’s ability to perform across sensitive classes and by collecting this information in a readable format to a wider audience. Accessible documentation increases accountability and visibility of the models making decisions in government.

**How are model cards used?**

Once a model card has been created, there are several uses of the document. The cards generated in this tool are formatted to be added to a repository with the model. When accessed, a new user could reference this document for detailed information to guide their own use of the model. A model card could be shared with non-technical stakeholders for full transparency of performance and expectations.

## Installation

This package requires Python >= 3.2.

Clone the repo and install the package:
```
git clone git@github.com:XDgov/model-card-generator.git
```

Download markdown dependencies.
```
pip install markdown
```

## Features

* [`ModelCardGenerator.py`](model-card-generator/ModelCardGenerator.py): Main module that guides the user through model card creation.

## Usage

This command line tool creates a python shell in which the user is prompted to answer a series of questions regarding their model.

The script will generate a model card from the user's responses input through the command line or through a .txt document. To input answers through a .txt document. Begin the tool and answer the responses as prompted, selecting 'Text Document' as your input preference.
```
Usage: python ModelCardGenerator.py

  Generate a model card.

**Example usage:**

```

## Questions in Model Card

The questions included in this tool were developed by the team at xD with influence from the Google Model Card research paper and site. To suggest changes to the available questions, please [open an issue](https://github.com/XDgov/model-card-generator/issues).

* [Model Cards with Google](https://modelcards.withgoogle.com/about)
* [Google Model Card Research Paper](https://arxiv.org/abs/1810.03993)
