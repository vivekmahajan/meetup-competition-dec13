meetup-competition-dec13
========================

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
