VanDev meetup: [A little competition](http://www.meetup.com/VanDev/events/93217772/)
=====================================

The Challenge: Monkey see, monkey do.


Human beings are very good at mimicry.

Given a transform like:
abc -> abd

and another input like:
bcd -> ?

a human being can mimic that actions of the original transform.

For example, they might say:

given: abc -> abd

it is logical that: bcd -> bce

because: "increment the last position in the sequence"

it is logical that: bcd -> bcd

because: "replace the last position with the letter d"

The challenge is given an example transform from one sequence of letters to another sequence of letters produce logical suggestions of how that transform applies to another sequence of letters.

Examples:

abc -> abd, wer -> ?

abbc -> abc, asdd -> ?

ert -> ettq, zqa -> ?

abc -> mjjkkk, mpq -> ?

abc -> abbddd, xyz -> ?

Output as many logical applications of the mapping as possible and for each include the reasons behind the mapping. Optionally attempt to rank the outputs by a metric of your own devising.

Inputs and outputs will be restricted to the 26 lowercase letters.

Proposed Solution
=================
I took a hint from [Statistical Phrase Based Translation](http://www.isi.edu/~marcu/papers/phrases-hlt2003.pdf). I consider string to left hand side of the rule as source language and to right hand side as target. 
But normally in case of statistical phrase based translation system, we have a big parallel corpus from where we generate phrase translation table with appropriate translation probablities learnt from the training dataset.

In my case, I used the rule and the "untranslated" source string to produce the required phrase table. One assumption I made while implementing the algorithm is that the two source string would be of same length. However, 
if we can align the two strings somehow, the algorithm can be modified easily.

e.g  if a b c -> a b d  then   x y c ->  ?  

for generating phrase table, I will take all possible uni-gram, bi-gram, tri-gram from left hand side and will try to map it to the n-grams on the right hand side. 
In this case, I will try to map  a, b, c, ab, bc, abc to a, b, d, ab, bd, abd. For each possible translation pair, I will calculate some similarity measure and will use that to find the 
possible translation for the corresponding n-gram in x y z.

so suppose one possible translation pair is a -> a b (edit distance = 1). So I will find possible translations for x -> ? which are 1 edit distance away from x. The search space will be
all possible n-grams you can form from alphabet a-z. Now for giving scores to each translation pair, alpha^( sim_measure + diff_indexes )  
sim_measure = edit_distance/sum of length of translations (penalizing long translations)  
diff_indexes = difference of the corresponding starting indexes of the translated phrase pair in consideration (penalizing if the translated phrase pair in consideration are relatively far away)


This will give me the phrase translation table, which I use in the [decoder](http://people.csail.mit.edu/koehn/publications/pharaoh-amta2004-slides.pdf) to generate the possible translations.


