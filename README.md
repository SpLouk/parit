David's Cool Cover Letter Writer is a program that takes a dictionary of keywords and sentences
and a job description ideally containing some of those key words and outputs a cover letter
that can be submitted to that company.

## How To Use

The letter writer reads input either from a command line argument or from an 'input.txt' file
in its directory. The program then scans the its dictionary for words that appear in the input,
and adds the corresponding sentence to the cover letter.

### Formatting the words.txt File

Each line in the words.txt file represents one entry in the sentence bank. The keyword should be at
the beginning of the line, and the corresponding sentence should follow after a '\' (backslash character).

Example line in words.txt

```
python\I am proficient at python.
```
