# Parit
### Cover letter writing, automated

Parit is a program that takes a dictionary of keywords and sentences
and a job description ideally containing some of those key words and
outputs a cover letter that can be submitted to that company.

## Installation

Parit depends on [PyLatex](https://github.com/JelteF/PyLaTeX/), [PyYaml](https://github.com/yaml/pyyaml), and [lxml](https://github.com/lxml/lxml)
Follow the installation instructions for these packages on their pages.
Or, using [pip](https://github.com/pypa/pip):
```
sudo pip install pylatex pyyaml lxml
```

Install Parit:
```
git clone git@github.com:SpLouk/parit.git
cd parit
sudo make
parit --help
```

#### Run a quick demo:
```
parit -c demo/ -P demo/posting.yml
```

## Setup

In order to use Parit you must set up your `config.yml` and
`sentences.yml` files.  If you want to automatically pull job postings
from Waterloo Works, you must set up your `credentials.yml`
file.

Edit the files in `config/`, following the instructions given in each
of them. Then, run `sudo make` again or copy the files into
`~/.config/parit/` (or wherever you will keep your config files).

You are all set up!

## Use

Parit is designed to automatically pull job postings from the
University of Waterloo's Waterloo Works system. However, you can also
supply your own job postings, in the form of a YAML file.

### Waterloo Works

Once you have set up your config, sentences, and credentials files,
you can are ready to start generating cover letters from Waterloo
Works. There are two ways to do this.

The first is by supplying a posting ID:

```
parit -p POSTING_ID
```
Note: you may need to run Parit with 'sudo' if you have put read
protection on your credentials file.

The second way is to supply a search term:

```
parit -t SEARCH_TERM
```

Be aware that some search terms can return hundreds of results, and
Parit will go ahead and generate cover letters for all of them. It
might be best to run the search on Waterloo Works first, and make sure
that the results are what you expect.

### From File

You can supply a job posting formatted as a YAML file for Parit to
work with:

```
parit -P FILE_PATH
```

Your job posting should have similar fields as the [demo
posting](demo/posting.yml).
