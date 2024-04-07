ANALOGICAL_PROMPT_SYSTEM_MESSAGE = '\
Your task is to generate regular expression(regex). When presented with a problem,\
recall relevant problems as examples. Afterward, proceed to solve the initial problem.\
'

ANALOGICAL_PROMPT_Part1 = '\
# Initial Problem: \n\
What is the regular expression pattern that can be used to extract '

ANALOGICAL_PROMPT_Part2 = '\
 from the article?\n\n\
# Instructions:\n\
## Relevant Problems:\n\
Recall 5 examples of regular expression problems that are relevant to the initial problem.\
Your problems should be distinct from each other and from the initial\
problem (e.g., involving different numbers and names). For each problem:\n\
- After "Q: ", describe the problem\n\
- After "A: ", explain the solution and enclose the ultimate answer in \\boxed{}.\n\n\
## Solve the Initial Problem: \n\
Q: Copy and paste the initial problem here.\n\
A: Explain the solution and enclose the ultimate answer in \\boxed{} here.'

LEAST_TO_MOST_PROMPT_SYSTEM_MESSAGE = '\
Your task is to generate regular expression(regex). I will give you some relevant problems \
and solutions. Afterward, proceed to solve the initial problem.\n\
Pre knowledge:\n\
1. The word need use the \\b as the word boundary.\n\
2. The letter need to be respresented by [A-Za-z] instead of \\w.\
'
LEAST_TO_MOST_PROMPT = '\
## Relevant Problems:\n\
Q1: lines which do not contain the letter \'e\'.\n\
A1: Let\'s break down this problem: 1. lines which contain the letter \'e\'. 2. lines which do not contain the letter \'e\'.\n\
1. lines which contain the letter \'e\', the answer is: .*e.*\n\
2. lines which do not contain the letter \'e\', the answer is: ~(.*e.*)\n\
For initial problem Q1, the answer is: ~(.*e.*)\n\n\
Q2: lines that have at least 5 numbers.\n\
A2: Let\'s break down this problem: 1. lines that have numbers. 2. lines that have at least 5 numbers.\n\
1. lines that have numbers, the answer is: .*[0-9].*\n\
2. lines that have at least 5 numbers, the answer is: (.*[0-9].*){5,}\n\
For initial problem Q2, the answer is: (.*[0-9].*){5,}\n\n\
Q3: lines using words ending in \'er\'.\n\
A3: Let\'s break down this problem: 1. lines using words. 2. lines using words ending in \'er\'.\n\
1. lines using words, the answer is: .*\\b[A-Za-z]*\\b.*\n\
2. lines using words ending in \'er\', the answer is: .*\\b[A-Za-z]*er\\b.*\n\
For initial problem Q3, the answer is: .*\\b[A-Za-z]*er\\b.*\n\n\
Q4: lines which contain only lowercase letters.\n\
A4: Let\'s break down this problem: 1. what is the lowercase letter? 2. lines which contain only lowercase letters.\n\
1. what is the lowercase letter?, the answer is: [a-z]\n\
2. lines which contain only lowercase letters, the answer is: [a-z]*\n\
For initial problem Q4, the answer is: [a-z]*\n\n\
Q5: lines that contain the word \'dance\'.\n\
A5: Let\'s break down this problem: 1. what is the word? 2. lines that contain the word \'dance\'.\n\
1. what is the word?, the answer is: \\b[A-Za-z]\\b\n\
2. lines that contain the word \'dance\', the answer is: .*\\bdance\\b.*\n\
For initial problem Q5, the answer is: .*\\bdance\\b.*\n\n\
Q6: "lines using the word \'going\' followed by \'d\'.\n\
A6: Let\'s break down this problem: 1. lines using the word \'going\'. 2. lines using the word \'going\' followed by \'d\'.\n\
1. lines using the word \'going\', the answer is: .*\\bgoing\\b.*\n\
2. lines using the word \'going\' followed by \'d\'., the answer is: .*\\bgoing\\b.*d.*\n\
For initial problem Q6, the answer is: .*\\bgoing\\b.*d.\n\n\
## Solve the Initial Problem: \n\
'
# Let's break down this problem: 1. lines which contain the letter \'e\'. 2. lines which do not contain the letter \'e\'.
# print(NORMAL_PROMPT_FEW_SHOT)