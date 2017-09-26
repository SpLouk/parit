# Parit

`Parit` is a program that takes a dictionary of keywords and sentences
and a job description ideally containing some of those key words and outputs a cover letter
that can be submitted to that company.

## How To Use

The letter writer reads input either from a command line argument or from file.
The program then scans the provided dictionary for words that appear in the input,
and adds the corresponding sentence to the cover letter.

## Formatting the sentences file

The sentences file is a JSON object with keys corresponding to the keywords that the program
should look for in the job posting, and values being either sentences or an array of sentences
from which the program will pick to put in the letter.

Example sentences file:

```
{
  "python": "I am proficient at python.",
  "scala": [
    "I have become comfortable programming in Scala during my last eight month co-op term at Foobar, where I used it every day.",
     "At Foobar, Scala was the primary language I coded in."
   ]
}
```

Example config file:

```
{
  "sender": "John Doe",
  "address": "123 Lorem Dr./Waterloo/Ontario/ABC 123"
}
```

Example credentials file:

```
{
  "username": "jdoe",
  "password": "jdoe123"
}
```
