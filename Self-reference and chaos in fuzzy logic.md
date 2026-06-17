1
IEEE TRANSACTIONS ON FUZZY SYSTEMS. VOL. I. NO. 4, NOVEMBER 1993 237
Self-Reference and Chaos in Fuzzy Logic
Patrick Grim
Abstract-The purpose of this paper is to open for investigation
a range of phenomena familiar from dynamical systems or
chaos theory which appear in a simple fuzzy logic with the
introduction of self-reference. Within that logic, self-referential
sentences exhibit properties of fixed point attractors, fixed point
repellers, and full chaos on the [0, 11 interval. Strange attractors
and fractals appear in two dimensions in the graphing of pairs
of mutually referential sentences and appear in three dimensions
in the graphing of mutually referential triples.
I. INTRODUCTION
HAOS theory and fuzzy logics form two of themost C intriguing and promising areas of current mathematical
research. In what follows, I want to explore a region of fuzzy
logic which exhibits some of the phenomena of chaos theory--
a region found, interestingly enough, in a consideration of the
fuzzy dynamical semantics of self-referential paradoxes and
related sentences.
A familiar fuzzy logic is outlined in Section I. In section
11, the classical example of the Liar paradox is used to sketch
the use of iterated algorithms to model self-reference. Self
referential sentences in fuzzy logic displaying the dynamical
semantics of fixed-point attractors and fixed-point repellers
are then outlined in Section 111. Section IV is devoted to the
Chaotic Liar, a fuzzy self-referential sentence the dynamical
semantics of which is fully chaotic in the precise mathematical
sense. Section V traces similar results with regard to pairs of
mutually referential sentences, introducing strange attractors
and fractals in two dimensions. In Section VI, the exploration
is extended to triples of mutually referential sentences and
corresponding dynamical phenomena in three dimensions.
Here, my purpose is merely to call attention to some of the
dynamic phenomena of self-referential fuzzy logics, and I will
proceed for the most part by simple example. In the somewhat
different context of [ 11, a hope was expressed that a next step
in research would reveal fuzzy systems with chaotic behavior
“and then we can define, and study, fuzzy fractals” [2], 131.
The work that follows seems to fulfill that hope, here inthe
context of a study of the dynamical semantics of self-reference
within fuzzy logic.
Given the affinity of many of the examples that follow
to the traditional semantic paradoxes, it should perhaps be
emphasized that this paper is not to be construed as an attempt
to solve the paradoxes. Two thousand years of attempted
solutions can hardly be said to have met with conspicuous
success, and I do not expect fuzzy logics to be any less
Manuscript received January 16, 1992; revised May 11, 1993.
The author is with the Group for Logic and Formal Semantics, Department
IEEE Log Number 9213142.
of Philosophy, SUNY at Stony Brook, Stony Brook. NY
vulnerable to strengthened versions of the Liar, say, than
are three-valued, multivalued, infinite-valued, gapped, and
antifoundational logics (for a critical survey, see for example
[4, ch. 11). In the end, a solution to the phenomena of selfreference may simply be the wrong thing to look for. In
something of the spirit of [5]-[7], the attempt here is rather
to open for investigation the semantical dynamics of selfreference and self referential reasoning in their own right,
here within a fuzzy logic and with an emphasis on pattems
of semantic instability.
Although I attempt at various points to draw some speculative conclusions, it is clear that much remains to be done in
terms of generalization and interpretation. Intriguing and perhaps even beautiful formal phenomena appear in the semantics
of certain self-referential sentences within fuzzy logic, but it
is not always clear why they appear, how they generalize, or
what such formal phenomena actually mean. It is known that
there are a range of metamathematical results closely related to
aspects of the current work, including extensions of classical
limitative results to both chaos theory and fuzzy logic [8], 191.
I leave a more complete discussion of those topics, however,
to another paper.
11. A SIMPLE FUZZY LOGIC
The basic fuzzy logic to be used in what follows is perhaps thesimplest possible: the familiar Lukasiewicz LN1. Our
numerical truth values are taken to be the reals in the [0, 11
interval, using as connectives:
where g(p) denotes the numerical truth value of a proposition
Formal considerations cast a strong presumption in favor
of minand max for conjunction and disjunction [12], and an
only slightly weaker presumption in favor of the treatment
of negation employed here. The same cannot be said for the
Lukasiewicz implication: here, it must simply be admitted that
P [lo], [I 11.
1063-6706/93$03.00 0 1993 IEEE
238 IEEE TRANSACTIONS ON FUZZY SYSTEMS, VOL. 1, NO. 4, NOVEMBER 1993
there are a number of alternatives.’ Nonetheless, it is clear
that LN1 can currently claim to be the srundurd basis for fuzzy
logic.
The distinguishing mark of true fuzzy logics, as opposed
to mere infinite-valued logics, is the use of a denumerable set
of “linguistic” truth values beyond the numerical truth values
- v(p) used above.’ Linguistic truth values are themselves represented by fuzzy sets, standardly generated from a fuzzy set
“true” and its converse “false” through recursive application
of algorithmic hedges such as “very,” “more or less,” “slight,”
and the like [ll], [15]-[19].
Nothing in the basic Lukasiewicz logic, however, dictates
what shape a basic fuzzy set for “true” is to take. Here, as in the
case of implication, there are clearly alternatives. For present
purposes, I want to use what may be the simplest and most
clearly justified fuzzy set for “true,” generated by importing
the familiar Tarski convention T directly into LN1.
Following 1201, and using T(p) for the claim that“$ is true,
T(P) * P.
Using the Lukasiewicz biconditional,
V(7’(P) * P) = I!((T(P) ---$ P) A (P ---$
= 1 - abs(V(7’(P)) - V(P)).
Assuming that the Tarskian schema itself takes the value of
“1,” for absolute truth, it must be the case that:
I!(T(P)) = V(P)
Ptrue(ZI) = v.
or, for those more familiar with Zadeh’s symbolism,
What direct importation of the Tarskian T schema into LN1
gives us is the basic fuzzy set for “true” of 1171, [181, 1211,
[22]. With “false” as the complement of “true” and modeling
“very” and “fairly” or “more or less” in terms of squares and
square roots, respectively-a treatment fairly consistent across
the literature-we get the basic set of linguistic truth values
indicated in Fig. l.3
This treatment of “true” does, of course, have alternatives--
most notably that of [ 111, in which a fuzzy set for “true” is
characterized as:
PLtrueO) = 0 foro I v I Q:
‘In [SI, for example, we use an implication definable as (- p V q), which
gives us Rescher’s S,> [lo], first developed in [13]. As [I41 notes, this
approach offers a direct fuzzification of predicate calculus.
It should also be noted that a stronger intuitive argument might be made
for the tukasiewicz biconditional than for the conditional itself. It is the
biconditional rather than the conditional that is most directly relied on in
what follows.
?-See [I41 on different senses of “fuzzy logic.”
3Here, I do not mean to suggest that the standard modeling for “very” and
“fairly” is any way beyond question, of course. On this, see the discussions
in Sections IV and footnote 17.
fairly false
very false
false
linguistic
truth-values
0 1
Y(P)
Fig. 1.
1
fairly true
tNe
very true
very true
linguistic
truth-values 7 ,i, , ,&, , ,
very false
0 1
Y(P)
Fig 2.
where a is a parameter “which indicates the subjective judgment about the minimum value of in order to consider a
statement as “true” at all” [19]. A sketch of Zadeh’s basic
fuzzy sets for “true” and “false” (where pfalse(g) = ptrue(l -
- v)), using an (Y of 0.6 along with the corresponding sets for
“very” and “fairly,” appears in Fig. 2.
The results of this paper are built on Baldwin’s fuzzy
logic rather than Zadeh’s for reasons of simplicity: Baldwin’s
outline for “true” is simpler not only in algorithmic and graphic
terms but in terms of its justification as a direct importation
of the Tarski 7’-schema into Lukasiewicz LN1. It is clear that
a range of results similar to those described later, however,
would emerge from a consideration of Zadeh’s logic or other
more complicated fuzzy logics as well; at several points results
are indicated which will hold for any fuzzy logic with LN~ as
a base.
It is important to note that although the underlying semantics
(or model) of our logic is expressed in terms of numerical truth
values, the propositions admissable in the language of the logic
itself can use only linguistic truth values, “p is very true” is,
thus, a type of sentence for which our fuzzy logic provides
a valuation scheme; “p is 0.75 true” is not. The perceived
artificiality of sentences of the latter sort does, in fact, seem to
be have been part of Zadeh’s initial motivation for moving to
linguistic truth values [ 111, and much of the common suspicion
of the “artificial numbers” of fuzzy logics can be dealt with by
viewing those numbers merely as an artifact of the semantic
model. The language for which that model is designed need
not contain numerical truth values at all.4
4Here, the case of set-theoretical semantics is perfectly parallel. The fact
that our semantic model is written in terms of sets need not commit us to
thinking that the sentences modeled are themselves about sets at all.
GRIM: SELF-REFERENCE AND CHAOS IN FUZZY LOGIC 239
Consider also a language, however, in which we are allowed
to claim numerical truth values for particular propositions--“p
is 0.75 true”-just as we normally do within the semantics of
fuzzy logic. Suppose, moreover, that we have a claim q that
we know to be 0.75 true. In that case, the claim that “p is
0.75 true” will intuitively be as true as the claim that p has
the same value as q. For this particular case, and using the
biconditional quite naturally to represent “has the same value
as,” we can express that basic intuition as:
pis0.75true * (p ++ q).
In general, let [w] represent a proposition with fixed numerical
value U. By the same reasoning, the claim that ‘‘p is II true”
will be as true as the claim that p has the same value as [U].
This we can express in terms of a biconditional as:
pis w true H (p H [w]).
If this general intuitive principle is itself thought of as having
a value of 1, the tukasiewicz biconditional gives us:
- v(piswtrue) = 1 - abs(v(p) - ~([v]))
or simply
= 1 - abs(g(p) - U).
This, it tums out, is Rescher’s truth value assignment operator
for infinite-valued logic [lo]. In terms of Rescher’s schema,
the value for a proposition Vvp to the effect that a proposition
p has a numerical truth value w is given by:
- v(Vvp) = 1 - abs(v - ~(p)).
This relation between Baldwin’s fuzzy sets for linguistic
truth values and Rescher’s Vvp schema for attributions of
numerical truth values is perhaps even clearer when envisaged
graphically. With numerical values on axes, the graph for a
proposition “Vlp” to the effect that a proposition p has value
1, given Rescher’s treatment, is precisely Baldwin’s graph for
“p is true” in Fig. 1. The Rescher graph for “VOp” corresponds
to Baldwin’s graph for “p is false.”
The infinite-valued Rescher scheme is central to [8], [9],
[23]. Here, I want to focus on dynamical semantic phenomena
within the more strictly fuzzy logic outlined.
111. SELF-REFERENCE AS ITERATION:
THE EXAMPLE OF THE LIAR
Consider, for a moment, the Liar sentence in the context of
a classical logic:
This sentence is false. (1)
If true, (1) must be false. If false, since the Liar says it is
false, it must be true. When one first approaches the Liar, one
is forced into an intuitive pattem of reasoning that seems to
oscillate in conclusion between “true” and “false:” if true, the
Liar must be false . . . but then if false, it must be true. . . but
then if true, it must be false?
T, F , T , F , T , F, . .
In these familiar intuitive terms, this altemation is quite
literally a temporal one: one is first drawn to the conclusion
that the Liar must be true, later forced to the conclusion
that it must be false, and so forth. It is also the case that
finite reasoners such as ourselves are generally smart enoughor logically unprincipled enough, or both-to break out of
such a series rather than to continue it indefinitely. In what
follows, however, I wish to abstract from both of these points.
The dynamical semantics of a sentence such as the Liar
can be thought of as a series of revised semantic values
forced by something like the standard Liar argument. As
such, the points of oscillation represent not so much discrete
times as discrete abstract steps in a pattem of protracted
reasoning.6 If we think of these as values arrived at by a
reasoner, that reasoner should be thought of as an idealized
reasoner acting without time constraints and purely on logical
principle.’
5Semantic paradox has had, of course, a long and distinguished career
in philosophical and mathematical logic. It lies at the core of Cantor’s
diagonal argument and the paradise of transfinite infinities it offers. Russell’s
paradox, discovered as a simplification of Cantor’s argument, was historically
instrumental in motivating axiomatic set theory. Godel [24] explicitly uses the
Liar paradox (and a relative known as the Richard paradox) to motivate his
incompleteness theorems, and the limitative theorems of [20], [25], [26] can
all be seen as exploiting the basic reasoning of the Liar. In the mid-l960’s,
Chaitin [27] developed an interpretation of Godel’s theorem in terms of the
notion of algorithmic randomness by formalizing the Berry paradox, itself a
simplication of the Richard.
In recent years, philosophers have repeatedly attempted to find solutions to
the semantic paradoxes by seeking patterns of semantic stability--hence, the
proliferation of “truth-value gap solutions” of the 1960’s and 1970’s [28]-[30].
Efforts in the direction of finding patterns of stability within the paradoxes
continued in the 1980’s with the work of H. Herzberger [5] and A. Gupta [6].
Recent work in this vein also includes that of J. Banvise and J. Etchemendy
[31], using Aczel set theory with an antifoundation axiom to characterize
Liar-like cycles.
The work of this paper, in contrast, like that of [8], [9], can be seen as
an attempt to study complex patterns of insfability in the general domain of
self-reference and paradox.
61n [32, p. 2181, dynamical systems are spoken of intuitively as the
description of the time behavior of a point moving about on some sort
of surface according to a rule that describes how one point is to follow
another. Here, as in other contexts, I think that restriction to time cannot be
taken too literally. Within ecological studies, iterative “times” may in fact be
generations; within epidemiological studies, “times” may be (variable) periods
of vulnerability to infection and, of course, the pure mathematics of iterated
functions need not be thought of in terms of literal time at all.
Many attempts to solve the Liar and similar paradoxes, of course, rely on
denying that there is a genuine oscillation here by insisting that, at each
step, one is using a distinct truth predicate or has ascended to a higher
metalanguage. That move itself, however, is quite clearly counterintuitive.
(As Banvise and Etchemendy note, “When we think about the Liar on an
intuitive level, there is an inclination to claim that the truth value “flips back
and forth.” First, we see that it is false, then that it is true, then that it is false,
and so forth.” [31, p. 1361). Here and throughout, as noted in the Introduction,
my attempt (like that of 151-171) is to track the intuitive dynamical semantics
of self-referential sentences rather than to sacrifice semantic intuitions in a
too-quick search for a “solution” to the paradoxes.
’The idealizations and abstractions at issue clearly make our semantic
model “objectivist” in spirit. For a critique of objectivist approaches, in
general, see [33, esp. 205 ff.1.
240 IEEE TRANSACTIONS ON FUZZY SYSTEMS, VOL. 1. NO. 4, NOVEMBER 1993
iterations
Fig. 3
,E
iterations
Fig. 4
Using 1 for truth and 0 for falsity, we can then model the
classical semantic behavior of the Liar in terms of a sequence
of values xn, where 50 is an initial or “seed” value and
2,+1 = 1 - 5,.
With a seed value of 1, the dynamic semantics of the Liar
within a classical logic can, thus, be graphed as in Fig. 3.
A seed value of 0, of course, shows an identical oscillationshifted one iteration to the left. In what follows,
iterated algorithms of this type will be used to model the
dynamical semantics of self-referential sentences quite generally.
As a first example, consider the Liar sentence within the
context of the fuzzy logic outlined--a variation we might term
the Fuzzy Liar. Given the Baldwin fuzzy set for “false,” our
algorithm remains the same, though now of course we need
to consider numerical truth values in the full [O, 11 interval.
For a seed value of 0.3, the Fuzzy Liar gives an oscillation
between 0.3 and 0.7 (see Fig. 4).
For any seed value 5, in fact, the dynamical semantics of the
Fuzzy Liar will be a simple oscillation between z and (1 - T).
The one fixed point is 0.5.
Often, the dynamical semantics of self-referential sentences
is better,illustrated using a web diagram. In a graph such as
that in Fig. 5, we start with a plotted function for, say, “false.”
An initial seed value a (0.3, in this case) is plotted as (a.()),
and a line drawn from that point vertically to the function
f(z) [Fig. 5(a)]. We read off our y value as indicating that
f(5) for 5 = 0.3 is 0.7. In order to represent the iteration
of that function, we now draw a horizontal line to a point
[f(u), f(u)] on the diagonal z = y--thereby converting our
previous y value to a new 5 value--and then draw a vertical
line again from that point to our function at [f(a).f(f(u))]
1
the Fuzzy Liar for .3 the Fuzzy Liar for .86
Fig. 6.
[Fig. 5(b)]. The y value of this intersection point indicates
that f(5) for 5 = 0.7 is 0.3 [Fig. 5(b)]. We graph the results
of repeated iteration by continuing the process, at each step
converting our y value to an 5 value by reflecting off the
z = y diagonal, giving us a new point of intersection with
our plotted function.
Within such a web diagram, it is clear that a seed value of
0.3 for Fuzzy Liar will give us a simple box, representing the
period two oscillation between 0.3 and 0.7. A seed value of
0.86 gives us a broader box (Fig. 6).
Because the Fuzzy Liar sets up an oscillational dynamical
semantics of this type, statements which are not self-referential
but which attribute some linguistic truth value to the Fuzzy
Liar will have semantics with the same pattern. In this sense,
the dynamical semantics of the Fuzzy Liar prove contagious.
Consider, for example, the following fuzzy statement about
the fuzzy Liar:
The Fuzzy Liar is very true
or the second satement of the pair:
This sentence is false. (1)
(1) is very true. (2)
For a seed value of 0.3, we have seen the Fuzzy Liar alternate
between 0.3 and 0.7. Using the standard squaring function for
“very true,” the value of (2) will then alternate between 0.09
and 0.49. For a seed value of 0.54, to use another example, the
GRIM: SELF-REFERENCE AND CHAOS IN FUZZY LOGIC 24 1
iterations
Fig. 7.
Fig. 9.
Fig. 8
Fuzzy Liar alternates between 0.54 and 0.46. In that case, (2)
will correspondingly alternate between 0.2916 and 0.21 16.*
The derivative semantic behavior of (2) can be thought of in
terms of a web diagram as follows. Let us start with an initial
seed value of 0.3 for the Fuzzy Liar, represented on the z axis
as (0.3,O). If (I), thus, has a value of 0.3, (2) will have a value
of 0.09, reflected by the fact that a line drawn vertically from
(0.3, 0) intersects our function for “very true” at (0.3, 0.09).
Given a seed value of 0.3, however, we will also be forced
to a revised value for the Fuzzy Liar of 0.7, reflected by the
fact that our vertical line intersects the function for the Fuzzy
Liar at (0.3, 0.7) (see Fig. 7).
Here, we are interested in successive values for (2). In order
to obtain the next value for (2), however, we cannot simply
reflect (0.3, 0.09) off the 2 = y diagonal as before. We have
instead to work from the revised value 0.7 for the Fuzzy Liar,
reflect that off the z = y diagonal, and then drop a line
vertically to again intersect our “very true” function for (2).
For reasons discussed at a slightly later point in the paper,
we can also graph progressive values for (2) directly by
reflecting the y value of our earlier point (0.3, 0.09) off not
the z = y diagonal but the mirror image left to right of our
graph for (2).
‘On the pattern of the Liar, the intuitive reasoning here will proceed
something as follows. If we assume that (1) has a value of 0.3, then (2)
will be fairly false with a value of 0.09. On the assumption that (1) has a
value of 0.3, however, since (I) says it is false, (1) will be fairly true--it will
have a value of 0.7. However, (2) will not be so far off after all, receiving a
value of 0.49. If (1) has a value of 0.7 . . .. Despite this alternation, the spirit of
Zadeh’s extension principle [I 1, 416 ff.]) appears to be preserved at each step.
The intuition that we should, nonetheless, be- able to say something constant
about (1)’s truth value, despite its oscillation, can perhaps be addressed only
in a language in which we explicitly introduce predicates such as “is not
consistently true” or “has no constant truth value.” In this paper, I have
concentrated on chaotic relatives of the Liar; in that stronger language, I
believe we should expect chaotic relatives of the Strengthened Liar.
Fig. IO.
An initial value of 0.41 for the Fuzzy Liar gives us a graph
for (2) shown on the left in Fig. 8. An initial value of 0.8
gives us the graph on the right.
In each case, our graph again shows a box, though here in
a different position, reflecting the fact that semantic values for
sentences which attribute truth values to the Fuzzy Liar will
oscillate in the same way that semantic values for the Fuzzy
Liar itself do.
Iv. ATTRACTOR AND REPELLER FIXED POINTS
IN THE PHENOMENA OF SELF-REFERENCE
To this point, we have concentrated on the simple Liar
within fuzzy logic. The same basic techniques also allow us
to model a wider spectrum of self-referential sentences with a
wider class of dynamic semantic behaviors.
Consider, for example,
This sentence is fairly false. (3)
I will refer to (3) as the Modest Liar. In terms of our basic
logic, the dynamical semantics of (3) can be modeled using
the following algorithm:
z,+1 = 41 - 2,
In a simple bounce diagram, for a seed value of 0.314, this
gives us Fig. 9:
The semantical behavior of the Modest Liar is still clearer,
however, in a web digram (Fig. 10).
1
242 IEEE TRANSACTIONS ON FUZZY SYSTEMS, VOL. 1. NO. 4, NOVEMBER 1993
?
/
Fig. 11
For any seed value, it tums out, the Modest Liar converges
inexorably on a fixed point attractor of (-1 + &)/2.9Fig. 11
shows the Modest Liar with a seed value of 0.99.
The fact that the Modest Liar has a semantics with a fixed
point attractor of this sort means that it is, in a sense, a selfreferential limiting case with regard to fuzziness. Whatever
element of a fuzzy range of numerical values we might assign
to such a sentence initially, repeated calculation will force us
to a very precise and single value: the Modest Liar seems to
convert fuzziness to precision.
It is clear that the precise behavior of the Modest Liar relies
on the use of a square root function to model “fairly.” Although
thet use is fairly consistent across the literature, as noted, it
is also clearly open to challenge: why insist on square root in
particular? The use of q, d, or the like would give us semantic
behavior similar to that of the Modest Liar, though converging
on a different fixed point. Here, I leave as open questions
what the fixed point would be for an arbitrary n root and
whether that has anything to tell us about the appropriateness
or inappropriateness of different roots in modeling hedges such
as “fairly.”
Consider also an Emphatic Liar:
This sentence is very false.
%+1 = (1 - Gd2.
(4)
Semantic values for the Emphatic Liar will be determined by:
For a seed value of 0.3, the Emphatic Liar forces a series
of revised values which eventually converge on the familiar
oscillation between 0 and 1 characteristic of the classical Liar
(see Fig. 12).
With one exception, the Emphatic Liar will force any
numerical value in the [O, 11 interval to the oscillation of
9The solution to s = fi is (-1 f fi)/2. Only (-1 f &)/2
appears within our semantic interval [0, I], however. Similar comments apply
with respect to s = (1 - 1)’ and the semantic fixed point (3 - &)/2
for the Emphatic Liar, In an entertaining knights-and-knaves exploration of
some of these ideas, Hellerstein [34] refers to the Modest Liar as the Golden
Liar, pointing out that its attractor fixed point is l/a, where o is the golden
ratio. The repeller fixed point for the Emphatic Liar is similarly 1 - 1/0.
The golden ratio d itself tums up in a number of surprising places: o is
the limit of the Fibonacci series 1/1, 2/1, 3/2, 5/3, 8/5 ... ; d - 1 = l/o;
o = drw.. .; etc. See [35, pp. 203-2061,
Fig. 12.
the classical Liar: the semantical dynamics of the Emphatic
Liar is that of a fixed repeller point at (3 - &)/2. The one
point that is not forced out to the behavior of the classical
Liar is the point (3 - &)/2 itself. The Emphatic Liar can,
thus, be seen as a self-referential limiting case to fuzziness in
much the same way as can the Modest Liar. The Modest Liar,
however, forces convergence on a precise nonclassical value.
With one exception, the Emphatic Liar forces revised values
to a Liar-like oscillation between the two classical values of
0 and 1.’’
The use of squaring to model “very” is, of course, open to
question in ways similar to those indicated regarding the use
of square root for “fairly.” An Emphatic Liar using (1 - 2n)3
or (1 - xn)4 would still converge to a Liar-like oscillation,
though from a different repeller point. Here, again it remains
unclear whether this has anything to tell us about the proper
modeling of hedges such as “very” or “fairly.”
What of statements which attribute fuzzy truth values ro
sentences such as the Modest and Emphatic Liars? Here, as
in the case of the Fuzzy Liar, we will have sentences with a
semantics dependent on that of the Liars themselves. Consider,
for example,
The Modest Liar is very false (5)
or (6):
This sentence is fairly false. (3)
(3) is very false. (6)
“Hellerstein has also suggested an Equivocal Liar:
This sentence is not very true
with an algorithm
.z,,+1 = 1 - 1%.
Here, (-1 + &)/2 is a repelling fixed point, forcing values out to an
oscillation between 0 and 1.
GRIM: SELF-REFERENCE AND CHAOS IN FUZZY LOGIC 243
Not surprisingly, attribution of fuzzy linguistic truth values
to the Modest Liar shows a convergence to the same fixed Modest Liar
point as does the Modest Liar itself.
It is perhaps worth noting why x4 is used as a reflectioncurve in this case. So as to avoid confusion with x and
y values, let us express the algorithms at issue in terms of
variables a and b:
I,, ,\
This sentence is fairly false (3)
Fig. 13. (3) is very false (6)
seed: .314 seed: .1
Fig. 14
For a seed value of 0.3, the Modest Liar gives us the following
series, converging as we have seen on (-1 f &)/2:
0.3,0.83667,0.40415,0.77191;~~”
If the Modest Liar has a value of 0.3, however, the claim
that it is very false takes a value of (1 - 0.3)’ or 0.49. Given
a revised value of 0.83667 for the Modest Liar, we are forced
to revise the value of (6) accordingly, to 0.02668. Thus, the
progressive dynamics of the Modest Liar force a corresponding
dynamics for (6):
0.49,0.02668,0.35503,0.05202, . . . .
This pattem of dependent dynamical semantics can be illustrated in a web diagram as follows. In Fig. 13, we have
graphed functions for both the Modest Liar and “very false.”
For a given seed value x, we draw a line vertically for (z,0)
to intersect the Modest Liar function. The y value of this point
of intersection (2, y) is, of course, our revised numerical truth
value for the Modest Liar, and reflection off the z = y line
will give us the next value for the Modest Liar.
At each step, the value of (6) depends on that of the Modest
Liar and is, in fact, the value at which our line representing
z-value intersects the function line for (6). Thus, we can think
of progressive values for (6) as intersection points on the “very
false” curve directly below the progressive points on the graph
for the Modest Liar.
In this case, we can also graph the dynamics of the dependent sentence (6) more directly, however, by reflecting its
values off the x4 curve. Progressive values for (6) starting with
two different seed values for (3), appears as in Fig. 14.
“Here, I exhibit only approximate values, rounded off for the sake of
simplicity.
b, = (1 - a,)’
For a given value b, for (6), the calculation of the next value
b,+l can be thought of as proceeding in several steps.
We first use the inverse of our algorithm for (6)
for the case of 0 5 b, 5 1 in order to give us a,.
By embedding this result in the algo1 - 6
J1 - (1 - 6) rithm for (3), we then obtain the value a,+l.
(1 - (J1 - (1 - a))) By embedding this result in the
algorithm for (6), we obtain b,+l.
The calculation is captured in a reflective graph as follows.
For 0 5 b, 5 1, (J1 - (1 - 6)) amounts to K. For
the purposes of our web diagram, we need to exchange x and
y values, however--the function of our x = y line originally.
We, thus, solve for x = ~, giving us y = x4, which therefore
serves as our reflective curve in the web diagram.
Reflective curves for other cases of sentences derivative
or parasitic on self-referential sentences can be computed
similarly. For pairs of sentences with algorithms f’ and f
and inverses f -’ and f-l within the limits of our semantic
interval [O, 11, given a value b, for the derivative sentence
modeled by f, b,+l can be calculated by reflecting a y value
representing b, off the function given by:
and recalculating the new x value in terms of our function f.12
To this point, we have concentrated on fuzzy relatives of the
Liar. We should, however, also mention fuzzy relatives of the
Truth-teller. Within classical logic, (7) proves troublesome in
a manner different from but related to the troubles of the Liar:
This sentence is true. (7)
Unlike the Liar, the difficulty with (7) is not that it cannot
consistently be assigned a value of either T or F. The difficulty
with (7) is rather that it can consistently be assigned either
value, and there seems no basis on which to prefer one over
the other.
Within a fuzzy logic, using the algorithm
zn+1 = zn
the Truth-teller can still consistently be assigned any value-in
the fuzzy context, any numerical value in the [0, 11 interval.
121 leave to another context generalization to more complicated cases and
to deeper chains, including sentences about the semantic value of sentences
about the semantic value of.. . self-referential sentences.
244 IEEE TRANSACTIONS ON FUZZY SYSTEMS, VOL. 1. NO. 4, NOVEMBER 1993
The Modest Truth-teller
for seed .13 The Emphatic Truth-teller for seed .87
truthvalues
iterations
Fig. 16.
Fig. 15.
is not the Fuzzy Liar but the quite different Emphatic Liar that
converges on the familiar oscillation between 0 and 1.
giving us full semantic chaos in the strict mathematical sense.
‘Onside‘ the Modest Truth-te11er and the Emphatic It is also the case that fuzzy self-reference is capable of Truth-teller:
This sentence is fairly true (8)
This sentence is very true
with corresponding algorithms:
(9) V. FUZZY CHAOS
Consider the following sentence, which I will call the
Chaotic Liar [8]:
This sentence is true if and only if it is false. (10) 2,+1 = 2:.
Both Truth-tellers, like their classical predecessor, have fixed
points at 0 and 1. For fuzzy values in between, however, they
vary dramatically and symmetrically. The self-reference of the
Modest Truth-teller drives every intermediate value up to 1.
The Emphatic Truth-teller, on the other hand, drives every
intermediate value down to 0 (Fig. 15).
The Truth-tellers, like the Modest Liar, thus in some sense
force fuzziness to precision through the iteration of semantic
self-reference. In the case of the Truth-tellers, as in the case
of the Emphatic Liar, however, that inexorable self precision
is the more remarkable since the values one is driven to in
each case are classical values. In the case of the Truth-tellers,
moreover, one is driven to stable classical values.
One lesson of sentences such as the Modest Truth-teller
and the Emphatic Truth-teller is that dynamical semantics may
introduce the need for logical categories beyond the traditional
“tautology” and “contradiction.” A classical tautology is one
which (instantly, as it were) takes a value of “1” for any
value assigned its components. A dynamic tautology, we might
propose, is one which converges through iteration on a value of
“1” for any initial value. The Modest Truth-teller might, thus,
be proposed as a dynamic tautology; the Emphatic Truth-teller
as a dynamic contradiction.13
From this first sampling of examples, it is clear that fuzzy
self-reference opens up a realm of dynamical semantics far
richer than anything dreamt of within classical logic. It is
also clear that there are some surprises in the transition from
classical to fuzzy logic. The Fuzzy Liar, for example, is a
quite direct fuzzification of the standard Liar. Nonetheless, it
I3The very different behavior of the Modest Truth-teller and the Emphatic
Truth-teller is inevitable, given a modeling of “very” and “fairly” by squares
and square roots-or, for that matter, by cubes and cube roots or the like. It has
been suggested, however, that this is itself a mark againsr such a modeling:
are “very” and “fairly” so different that “this is fairly true” should converge
on pure truth and “this is very true” should converge on pure falsity?
Using the Lukasiewicz biconditional and modeling selfreference in terms of iterated algorithms, semantic values
for the Chaotic Liar will be given by:
x,+~ = 1 -*abs((l - 2,) - xn).
By expanding our language slightly, we can also express the
Chaotic Liar in other ways. If “p is as true as q” or “the value
of p is the same as the value of q” are treated fairly naturally
as taking the value
for example, then the Chaotic Liar can alternatively be expressed as:
This sentence is as true as it is false. (11)
or
The value of this sentence is the same as its negation. (12)
A seed value of 0.314 for any of these gives us a series of
values that begins as in Fig. 16.
The semantical dynamics of the Chaotic Liar is perhaps
best exhibited by its web diagram, however, here shown in
four progressive stages of de~elopment’~ (Fig. 17).
‘“ne peculiarity of this function is that standard rounding off within the
binary arithmetic of computers disguises its chaoticity: although it is probably
chaotic on the [0, I] interval, it does not show up as such on the computer
screen. In order to graph something closer to the function’s true behavior, it is
thus standard to “cancel out” the effect of rounding off by introducing a small
element of randomness, and that has been done for the illustrations here. On
this point, I am obliged to J. Milnor for discussion.
GRIM: SELF-REFERENCE AND CHAOS IN FUZZY LOGIC 245
--
Fig. 17
The dynamical semantics of the Chaotic Liar qualifies as
chaotic in the precise mathematical sense of [36].15
What this amounts to is a range of surprising semantic
features.
1) The Fuzzy Liar, as we have seen, has a simple period
of 2 for almost all values. For sentences such as the Chaotic
Liar, on the other hand, any repeating period we might care
to choose, however high, will be generated by some initial
value. For such sentences, there is no upper limit to semantic
periodicity.
2) It is also the case that there will be numerical truth values
for such sentences which eventually move from any arbitrarily
small semantic region to any other. There is, thus, no range
of degrees of truth, however small, such that values within
that range assigned to the Chaotic Liar will safely stay there
on iteration. For any such region, some semantic values will
eventually escape to any other semantic region we might name.
3) Finally, no matter what numerical truth value x we might
start off with as an estimate for such sentences, there will
be numerical truth values arbitrarily close to our initial value
which, upon iterative recalculation through our sentences,
eventually move as far from corresponding iterations of x
as we might choose to specify. There is, thus, no initial
range “close enough’ to a starting estimate x that differences
I5Given a set J. f : J t J is chaotic on .I if a) f shows sensitive
dependence on initial conditions,f b) f is topologically transitive, and c)
the set of periodicpoints is dense in d.
Here, let us use the notation F” (s) to stand for the composition or iteration
of the function f(s) n times, i.e.,
f”(s) = .. .f(f(f(. r)))...iitimes
a) f : J + J shows sensitive dependence on initial conditions if there exist
points arbitrarily close to any s E J which eventually separate from .r by
any chosen distance h or more under iteration of f, i.e., there exist (i > 0
such that, for any s E .J and any neighborhood .V of s, there exist y E .Y
and 71 2 0 such that abs (f”(s) - f”(y)) > (1.
b) f : J t d is topologically transitive if it has points which eventually
move under iteration from one arbitrarily small neighborhood to any other,
i.e., for any pair of open sets L-. 1. 2 J there exists some 11 > 0 such that
frL (Li) n V is nonempty.
c) The set of periodic points of J, PER(.J), is the set of all .r E .I such
that f“(1) = s for some natural number n, i.e., PER(.l) = {.r E J :
3nfn(s) = s}. PER(J) is dense in J if PER(.J), together with all its limit
points, is equal to .l.
1
truthvalues
0
iterations
Fig. 18.
within that range will not make a significant difference.
Within any distance from z, however small, is another value
iterations of which will eventually diverge from iterations of z
enormously--as enormously, within the limits of our semantic
range, as we might care to specify.
Although somewhat stronger and weaker characterizations
of chaos appear in the literature, the central element in all
versions is this last feature, known as sensitive dependence on
initial conditions. The graph in Fig. 18 shows the basic idea of
sensitive dependence for the Chaotic Liar. Here, time series
graphs are superimposed for seed values tarting with 0.3 14
and increasing by 0.001.
The basic algorithm for the Chaotic Liar is, in fact, a very
simple and paradigmatically chaotic function, known as a tent
map because of the shape of its graph and more familiar in
the mathematical guise x,+1 = 1 - abs(2z, - 1) or
for 0 5 x < 0.5
2,+1= { :;;- 2,) for 0.5 5 z 5 1
(see [37], 171 ff.]). The semantic role of this function within
self-referential fuzzy logic comes as something of a surprise,
however; the function is, for example, relegated to a mere class
of “mathematical curiosities” in [38].16
Here, let me also offer a second simple sentence which
shows chaotic behavior within fuzzy logic--a sentence I will
call the Fuzzy Logistic:
It is very false that this sentence is true if it is false. (13)
Here, semantic values will be given by:
x,+1 = (1 - (1 - abs((1 - x,) - x,)))*.
Note that the algorithm for the Chaotic Liar is embedded
within that of the Fuzzy Logistic. We can, in fact, obtain the
Fuzzy Logistic from the Chaotic Liar simply by adding the
prefix “It is very false that . . .”.
Here, as before, there are of course altemative phrasings. If
we take “differs in value from” as the negation of “is as true
as,” the Fuzzy Logistic can be phrased as:
It is very true that this sentence differs in value
from its negation. (14)
or
The value of this sentence is very different from that
of its negation. (15)
I6The similar role of that algorithm in a Rescher multivalued logic appears
in [81, PI.
11
246 IEEE TRANSACTIONS ON FUZZY SYSTEMS, VOL. 1. NO. 4. NOVEMBER 1993
Fig. 19.
For values in the [0, 11 interval, our algorithm amounts in
each case to:
This, it turns out, is an inverted form of the logistic or quadratic
equation, perhaps the most familiar and thoroughly studied
sample of chaos.”
For an initial value of 0.314, the web diagram of the Fuzzy
Logistic develops as in Fig. 19.
Chaos can be expected to appear within other fuzzy logics
by way of other self-referential sentences. Though we have
here confined ourselves in general to the simple Baldwin
fuzzy logic outlined in Section 11, it is perhaps worth noting
a route by which chaos will appear within any fuzzy logic
with the standard Lukasiewicz base, regardless of the fuzzy
set it introduces for “true.” Within Zadeh fuzzy logic or
any other based on LN1, consider the prospect of a sentence
p which amounts to a biconditional between itself and its
negation:
P = (P t)N PI.
Given simply the basic Lukasiewicz biconditional,
the algorithm for such a sentence will
be:
z,+1 = 1 - abs((1 - z,) - 2,)
”An additional negation would give us the Logistic without inversion:
It is not very false that this sentence is true if it is false
It is not very true that this sentence differs in value from its negation
or
The value of this sentence is not very different from that of its negation.
I am obliged to N. Hellerstein for his seminal work on the Fuzzy Logistic,
communicated in private correspondence.
or
and any such sentence will, thus, amount to the Chaotic
Liar.I8
VI. FUZZY SELF REFERENCE IN WO DIMENSIONS
Beyond the traditional Liar lies an infinite series of Liarcycles, the simplest of which is perhaps the Dualist. In medieval
form, it appears as an exchange between Socrates and Plato:
Socrates: What Plato is about to say is true.
Plato: Socrates speaks falsely.
More simply, we have two sentences each of which is about
the truth value of the other:
X : Y is true
Y : Xis false.
With the tools of our basic fuzzy logic, we can also introduce
fuzzy variations on the Dualist. Consider, for example,
X:X++Y
Y : Y ++ it is very false thatX
or, equivalently,
X : X is true if and only if Y is
Y : Y is true if and only if X is very false.
In previous sections, we have concentrated on single sentences
which force a series of revised values. Here, the situation is
somewhat more complex: we have a pair of sentences which,
for any initial seed values (50, yo), forces a series of pairs of
revised values. For X and Y, revised values can be calculated
in terms of the following algorithms:
%,+I = 1 - abs(z, - y,)
yn+i = 1 - abs(y, - (1 - 2,)’).
If we start with seed values of 0.25 and 0.25, for example,
we are forced to the following series of revised values:19
(1,0.6875), (0.6875,0.3125), (0.625,0.7852),
(0.8398,0.3555), (0.5156,0.6702) ... .
”For Zadeh fuzzy logic in particular, St. Denis has suggested the following
chaotic sentence:
It is not the case thqt this sentence is fairly not true, or it is not the
case that the negation of this sentence is fairly not true.
Here, our algorithm is:
where Z(s,,) indicates the degree of membership in Zadeh’s fuzzy set “true”
(using 0.5 as a) of a sentence with numerical truth value zn. In a web
diagram, the St. Denis sentence appears as a more slender variation on the
inverse Logistic.
l9 Here again, numbers are rounded off for presentational simplicity.
'1
GRIM: SELF-REFERENCE AND CHAOS IN FUZZY LOGIC 241
I
I
0 1
Fig. 20. I:.
1
I
I ,.
I
0 1
Fig. 21
If we plot these pairs as Cartesian coordinates, the pentagonal
attractor of Fig. 20 appears.
The persistence of such an attractor, for various seed values,
is clear from an overlay diagram for seed values (z, y) where
x and y range from 0 to 1 in intervals of 0.5 (Fig. 21).
Throughout the [0, 11 interval, values are attracted to and
trapped within the same clearly defined region.
Consider, also, a second fuzzy Dualist variation:
X : It is very false that X tf Y
Y : It is fairly false that Y tf N X
or, more colloquially,
X : It is very false that X is true if and only if Y is.
Y : It is fairly false that Y is true if and only if X is false.
Here, successive values can be calculated using the following
algorithms:
X,+I = (1 - (1 - abs(z, - Y,)))'
yn+1 = dl - (1 - abs(y, - (1 - 2,)))
Fig. 22.
Fig. 23
or, more simply,
xn+1 = (X, - Y,)2
yn+i = dabs(y, - (1 - xn)).
Our attractor in this case is shown in an overlay diagram in
Fig. 22.
Here, let me finally offer one further fuzzy Dualist:
X : It is very false that X tf Y
Y : It is very false that X is false if and only if
Y is very true
with successive values
Xn+1 = (5, - Yd2
Yn+l = ((1 - 2,) - Y,) '
22
The attractor for this final variation, once again in overlay
form, appears in Fig. 23.
In our calculation of revised values for the Fuzzy Dualists, it
should be noted we have assumed a simultaneous calculation
of numerical truth values for sentences X and Y in each case.
Given a pair of seed values (x,y), in other words, we have
calculated a new value for X in terms of those values and
248 IEEE TRANSACTIONS ON FUZZY SYSTEMS, VOL. I, NO. 4, NOVEMBER 1993
have simultaneously calculated a new value for Y in terms of
those same values.
Evaluation of the sentences of a Fuzzy Dualist pair might
also be thought of sequentially. It might be argued, for
example, that in at least some contexts a more natural way
to approach such a pair of sentences would be to begin with
seed values (z,y), to calculate the value of X in terms of
those seed values, but then to calculate the value of Y using
the newer or most recent value computed for X.
This second pattern of reasoning, with regard to the same
pairs of sentences, can be represented with a slight change
in our algorithms: In each case, 2, is replaced in the second
algorithm with x,+~.
Our algorithms for the first variation on the Dualist, for
example,
X:X++Y
Y : Y H it is very false thatX
will now be
z,+~ = 1 - abs(z, - yn)
Yn+l = 1 - abs(?h - (1 - z,+1)2).
Using this alternative form of calculation, the same pair of
sentences give us the attractor shown in Fig. 24. A similar
change from a simultaneous to sequential pattern of reasoning,
in the case of our other fuzzy Dualist variations gives us the
following attractors. As shown in Fig. 25:
X : It is very false that X tf Y
Y : It is fairly false that Y t-f -X
zn+1 = (. - Y)*
Yn+l = JWY, - (1 - .,+I)) .
As shown in Fig. 26.
X : It is very false thatX ti Y
Y : It is very false that X is false if and only if
Y is very true
zn+1 = (2, - Yn)2
Yn+l = ((1 - %+1) - Y,) 22
Although these figures graphically illustrate the difference
between simultaneous (or parallel) and sequential updating in
calculating the fuzzy Dualist, it must be confessed that their
interpretation remains much less clear. Simultaneous updating
might be said to be more appropriate to a God’s-eye view of
the informational dynamics of the fuzzy Dualist, in which all
information is received and processed simultaneously at each
step. Sequential updating, on the other hand, might be said to
be more appropriate to beings capable of processing only the
information of a single sentence at a time. In more realistic
applications to repeated sequences of mutually referential
sentences, the difference might be appropriate to contexts in
which two sources of information provide information about
each other, and in which the second source of information
..
Fig. 24.
Fig. 25
Fig. 26.
is or is not immediately aware of reports coming from the
first source. All of this remains at the level of speculation,
however: here, as elsewhere, the graphic display of semantic
characteristics is as yet clearer than are matters of their
interpretation or application.
I
GRIM: SELF-REFERENCE AND CHAOS IN FUZZY LOGIC 249
0 1 Fig. 29
Fig. 21
Fig. 28
Certain aspects of the fuzzy dynamics of Dualist variations
can also be graphed using what are known as escape-time
diagrams. For each pair of points (x,y) on the Cartesian
plane, we can graph in terms of color the number of iterations
required for the series of values, beginning with seed values
(x,~), to reach a certain threshold. Here, one threshold we
might choose is a certain distance from the origin, with the
origin itself representing (0, 0) or “double falsity” for our
two sentences. Within a particular fuzzy Dualist, a pair of
seed values (say 0.1, 0.5) may give us a series of values
which first escapes from a distance of 1 from the origin in
two iterations, for example, in three, in four, or in more. If
that series escapes in two iterations, we might color the initial
point (0.1, 0.5) blue; if three, we might color it green, and
so forth. Another point (say 0.2, 0.4) may give us a series
which escapes our chosen threshold in a different number of
iterations, and will correspondingly be given a different color.
(The general idea of escape-time diagrams should be familiar
Fig. 30
from standard graphing of the Julia and Mandelbrot sets.)
Fig. 27 shows an escape-time diagram of this type for the
first fuzzy Dualist.
Given present printing limitations, however, the fractal
character of such a graph is perhaps clearer if we emphasize
merely the interfaces of different colored areas: points at which
the number of iterations required to pass the chosen threshold
changes. Our escape-time diagram now appears as a tracery
(Fig. 28).
Consider, in contrast, an escape-time diagram for a sequential pattern of reasoning with regard to our first Fuzzy Dualist
(Fig. 29).
Fig. 30 shows escape-time diagrams for simultaneous and
sequential calculations (left and right, respectively) of the
second Dualist variation offered.
X : It is very false that X ti Y.
Y : It is fairly false that Y H N X
In this case, an escape threshold of 0.8 is used.
In all of the escape-time diagrams considered to this point,
we have confined our values (x,y) to the unit interval,
reflecting the fact that the semantics of our fuzzy logic limits
numerical truth values to the [0, 11 interval. In some cases,
however, it is easy to see that the characteristics of points
within the [O, 11 interval are merely part of a larger pattern.
I‘
250 IEEE TRANSACTIONS ON FUZZY SYSTEMS, VOL. I, NO. 4. NOVEMBER 1993
Fig. 31.
Fig. 32.
Fig. 31 shows our third Fuzzy Dualist variation for values
between -1.4 and 2.4 and with a threshold of 0.85:*’
X : It is very false that X H Y
Y : It is very false thatxis false if and only if
Y is very true
Other escape-time diagrams are possible in terms of other
parameters. In all those mentioned, we noted the threshold
used is a particular distance of a pair (z,y) from the origin.
We can also plot escape-time diagrams using other thresholds
as well. Fig. 32 shows an escape-time diagram in which what
we measure is the number of iterations required before a series
starting from a pair of seed values (z.y) reaches a value
(dl y’) such that II: and y are separated by a distance of at
least 0.5.
In many of these images, a deep fractal character--self affinity at descending scales--is clearly evident. This is a familiar
companion to chaos within dynamical systems theory. What
its appearance indicates, however, is the presence of fractal
organization in the dynamical semantics of self-referential
sentences within a fuzzy logic. It is tempting to speculate
that different varieties of self-reference, direct or indirect,
can themselves be thought of as abstractly fractal in some
intuitive sense: self-referential sentences or sets of sentences
semantically contain themselves, or images of themselves, in
much the way that fractals seem to contain themselves on
different scales. It might be proposed that what images such
as those in Fig. 32 really do is give more explicit visual
expression to the inherently fractal semantics of different
patterns of self-reference. This remains speculation, however.
Here, as elsewhere, it proves easier to graph certain semantic
characteristics than to fully understand them.
For a few other small samples, the reader is referred [SI, 191, [33].
”The range of Fuzzy Dualist variations is so immense as to be intimidating.
Fig. 33
Fig. 34
VII. FUZZY TRIPLISTS MODELED IN THREE DIMENSIONS
Beyond the Dualist lie Triplist variations, in which three
mutually referential sentences speak of each others’ truth
values. In the case of Triplists, attractors must be graphed
as three-dimensional rather than two-dimensional objects, and
the correlates to two-dimensional escape-time diagrams will
be three-dimensional escape-time solids. Here again, I simply
offer some examples.
Consider, to begin with, the following set of sentences (a
colon is used to avoid ambiguity):
X : It is very false that: X - N (Y tf 2)
Y : It is very false that: Y H N Z
2 : It is very false that: 2 ++ N (X tf Y).
In the fuzzy Dualists, our sentences forced us through a series
of revisions for initial seed values (2, y) for sentences X and
Y. In the case of this fuzzy Triplist, our sentences will force us
through a similar series of revisions for seed values (zl y, 2).
For these sentences, these revised values can be calculated in
terms of the following algorithms:
II:,+I = (abs(y,, - 2,) - 2,)’
Yn+l = ((1 - 2,) -
z,+1 = (abs(z, - yn) - 2,)’.
If we plot revised values for these sentences starting with seed
values of (0.23, 0.34, 0.45), the attractor of Fig. 33 appears.
In Fig. 33, the attractor is shown in two dimensions (“fullface,” as it were, from the z axis). In Fig. 34, in contrast,
it is rotated in three dimensions. Despite its apparent depth,
it is clear that the attractor for this first fuzzy Triplist is still
confined to. a plane.
Ill
GRIM: SELF-REFERENCE AND CHAOS IN FUZZY LOGIC 25 1
Fig. 35.
Fig. 36.
Here, as before, we can also compute revised values for
oursentences by considering them sequentially rather than
simultaneously, with the following changes in our algorithms:
With a sequential calculation, the looping attractor of Figs. 35
and 36 appears.
Consider a second fuzzy Triplist variation:
X :- (X tt it is very true thatY H 2)
Y :- (Y tt it is very true thatX 2)
2 :N (2 tt it is very true thatX H Y)
with the following algorithms for revised values:
zn+l = abs((1 - abs(y, - 2,))’ - z,)
Y,+I = abs((1 - abs(zn - 2,))’ - yn)
zn+1 = abs((1 - abs(z, - Y,))~ - zn).
Using the same seed values as before, this second fuzzy
Triplist gives us the attractor of Figs. 37 and 38. A sequential
computation, in contrast, gives us Figs. 39 and 40.
For fuzzy Triplists, the analog to two-dimensional escapetime diagrams will be three-dimensional escape-time solids.
We can once again color points in terms of how many iterations
Fig. 31.
1 1.1)
Fig. 38.
I
Fig. 39.
Fig. 40.
are required for a series of revised values starting from that
point to reach a certain threshold. In the case of Triplist
variations, however, we will be coloring points (z,y,z) in
a three-dimensional space.
252 IEEE TRANSACTIONS ON FUZZY SYSTEMS, VOL. I. NO. 4, NOVEMBER 1993
In Figs. 41 and 42, we use sequential calculation for the first
Triplist variation and simultaneous calculation for the second,
with a chosen threshold in each case of Jx2 + y2 + 9 = 1.
Both escape-time solids are shown from two angles, in a space
extending roughly from -2.5 to +5 for each of our three
values:
X : It is very false that: X H - (Y ti 2)
Y : It is very false that Y ti - 2
2 : It is very false that: 2 ts - (X H Y)
X :- (X +i it is very true thatY +-+ 2)
Y : - (Y cf it is very true that X c--) 2)
2 :- (2 ts it is very true thatX H Y).
There is no upper limit to the size of sets of mutually
self-referential sentences that might be considered, of course,
nor any upper limit to the number of dimensions appropriate
for modeling their semantical dynamics. Beyond the threedimensional semantic phenomena of Triplist variations lie the
four-dimensional semantic phenomena of the Quadruplists, the
five-dimensional semantic phenomena of Quintuplists, and so
on.
VIII. CONCLUSION
Here, my attempt has been to introduce, for the most part
by example, a range of dynamical phenomena which appear
in the semantics of a simple fuzzy logic with the introduction
of self-reference. Within such a logic appear sentences the
dynamical semantics of which exhibit the behavior of fixed
point attractors, fixed point repellers, and full chaos on the [0,
11 interval of semantic values. Mutually referential Dualist and
Triplist pairs take the phenomena of chaos and fractals, once
again in a semantic guise, into two and three dimensions.
Fig. 42
A great deal of further formal exploration, generalization,
andapplication clearly remains to be done.21 Perhaps it is
not out of place, however, to close with some admittedly
philosophical speculations.
Logical systems have typically been introduced with certain
semantical expectations, and one thing the introduction of
semantical self-reference often does is to violate those initial
expectations. Here, classical logic is a prime example: within
such a logic, the expectation is that every proposition will
be simply true or false. With the introduction of semantical
self-reference, however, we are confronted with the classical
Liar:
This sentence is false. (1)
The dynamical semantics of such a sentence seems to be
that of an oscillation, and the attempt to assign either of our
supposedly exhaustive semantical categories results in simple
contradiction. A similar story, relying on strengthened versions
of the Liar, can be told for multivalued, infinite-valued,
gapped, and antifoundational logics [I, ch. 11. In each case,
2' One metamathematical application is mentioned in the introduction: [XI,
191 each contain a sketch of Godel-like limitative results for chaos theory in
the context of formal systems for real arithmetic, motivated by a close relative
of the sentence that appears here as the Chaotic Liar. It is clear that one class
of extensions would take these into the context of fuzzy logics.
GRIM: SELF-REFERENCE AND CHAOS IN FUZZY LOGIC 253
self-reference seems to violate initial semantical expectations
by forcing us to recognize categories of semantical behavior
not initially and intuitively provided for.
What the work above seems to show is that something
similar also happens with the introduction of semantical selfconstructed to incorporate an important range of intuitive
[ 151 L. A. Zadeh, “A fuzzy-set-theoretic interpretation of linguistic hedges,”
J. Cybernet.,
[ 161 R. E. Bellman and L. A. Zadeh, “Local and fuzzy logics,” in Modern
Uses of Multiple-Valued Logic, J. Michael Dunn and George Epstein,
Eds. Dordrecht: D. Reidel, 1977.
[171 J. F. Baldwin, “A new approach to approximate reasoning using a fuzzy
logic,” Fuuy Sets and Syst., vol. 2, pp. 309-325, 1979.
Appl., E. H. Mamdani and B. R. Gaines, Eds.
2, PP. 4-349 1972.
reference within logics‘ Fuzzy logic was, Of course? [18] -, “Fuzzy logic and fuzzy reasoning,” in Fuuy Reasoning and its
New York: Academic,
phenomena and to facilitate a range of applications not provided for within more classical logics. One assumption which
appears to have been carried over from its classical predecessors, however, was that semantic values, however fuzzy,
could nonetheless be expected to be tolerably well behaved and
manageably stable. Here again, the introduction of semantical
self-reference seems to violate central semantical expectations:
in the context of fuzzy logic, self-reference seems to introduce
a range of pattems of semantic instability as diverse and
complex as the phenomena of chaos theory generally.
ACKNOWLEDGMENT
The work presented here is an expansion of collaborative
work on infinite-valued logics and chaos which appears in
Mar and Grim 181, Grim and Mar [9], and Grim, Mar, Neiger,
and St. Denis [23]. The author is indebted to P. St. Denis
for programming assistance and for repeatedly bringing my
attention back to the Lukasiewicz biconditional. M. Neiger
developed the programming required for three-dimensional
escape-time solids in Section V. As always, the author is
deeply indebted to G. Mar for fruitful discussion and for
central good ideas. The author would also like to express
thanks to several anonymous referees for detailed and helpful
comments.
REFERENCES
J. J. Buckley, “Fuzzy dynamical systems: I.” in Proc. IFSA ‘91, Brussels,
Belgium, pp. 16-20.
G.-Y. Wang, J.-P. Ou. and P.-Z. Wang, “Dynamic fuzzy sets and fuzzy
processes,” in Proc. 3rd IFSA Cong., Seattle, WA, 1989, pp. 276-279.
P. Diamond, “Chaos and fuzzy representations of dynamical systems,”
in Proc. Int. Symp. Fuuy Syst., Iizuka, Japan, July 1992, pp. 51-58.
P. Grim, The Incomplete Universe. Cambridge, MA: M.I.T. Press,
1991.
H. Herzberger, “Notes on naive semantics,” J. Phil. Log., vol. I I. pp.
61-102, 1982.
A. Gupta, “Truth and paradox,” .I. Phil. Logic, vol. 11, pp. 1-60, 1982.
A. Gupta, and N. Belnap, The Revision Theory of Truth. Cambridge,
MA: M.I.T. Press, 1993.
G. Mar and P. Grim, “Pattern and chaos: New images in the semantics
of paradox,” Noiis, vol. 25, pp. 659-694, 1991.
-, “Chaos, fractals, and the semantics of paradox,” Res. Rep. 91-
01, Group for Logic and Formal Semantics, Dept. of Philos., SUNY at
Stony Brook, 1991.
N. Rescher, Many-Valued Logic.
L. A. Zadeh, “Fuzzy logic and approximate reasoning,” Synrhese, vol.
30, pp. 407428, 1975.
R. E. Bellman and M. Giertz, “On the analytic formalism of the theory
of fuzzy sets,” Inform. Sci., vol. 5, pp. 149-156, 1973.
Z. P. Dienes, “On an implication function in many-valued systems of
logic,” J. Symbol. Log., vol. 14, pp. 95-97, 1949.
B. R. Gaines, “Foundations of fuzzy reasoning,” Int. J. Man-Much.
New York: McGraw-Hill, 1969.
Stud., vol. 8, pp. 623-668, 1976.
1981.
[ 191 H.-J. Zimmerman, Fuuy Set Theory and Its Applicafions. Dordrecht:
Kluwer-Nijhoff, 1985.
[20] A. Tarski, “Der wahrheitsbegriff in den formalisierten sprachen,” Studien
Philosophica, vol. I, pp. 261-405, 1935.
1211 Y. Tsukamoto, “An approach to fuzzy reasoning method,” in Advances
in Fuuy Set Theory and Applications, M. M. Gupta et. al, Eds. NorthHolland: Amsterdam, 1979, pp. 137-149.
[22] L. Ding, Z. Shen, and M. Mukaidono, “A new method for approximate reasoning,” in Proc. 19th Int. Symp. on Multiple-Valued Logic.
Washington, DC: IEEE Comput. Soc. Press, 1989, pp. 179-186.
[23] P. Grim, G. Mar, M. Neiger, and P. St. Denis, “Self-reference and
paradox in two and three dimensions,” Computers and Graphics.
1241 K. Godel, “iiber formal untscheidbare satze der Principia Mathemutica
und verwandter systeme I, ” Monatschefe fur Mathemutik und Physik,
vol. 38, pp. 173-198, 1931.
[25] A. Church, “A note on the entscheidungsproblem,” J. Symbol. Logic,
vol. 1, pp. 40-41, 101-102, 1936.
[26] A. Turing, “On computable numbers, with an application to the entscheidungsproblem,” in Proc. London Mathemat. Soc., 1936, vol. 42, pp.
23Ck265.
[27] G. Chaitin, Information, Randomness, and Incompleteness--Papers on
Algorithmic Information Theory. Singapore, World Scientific, 1990.
[28] B. van Fraassen, “Presupposition, implication, and self-reference,” J.
Philosophy, vol. 65, pp. 13652, 1968.
[29] R. L. Martin, “A category solution to the liar,” in The Paradox of the
Liar, R. L. Martin, Ed.
(301 S. Kripke, “Outline of a theory of truth,‘’ J. Philosophy, vol. 72, pp.
690-716, 1975.
1311 J. Banvise and J. Etchemendy, The Liar. New York: Oxford Univ.
Press, 1987.
[32] J. L. Casti, Alternate Realities. New York: Wiley, 1989.
[33] G. Lakoff, Women, Fire, and Dangerous Things.
of Chicago Press, 1987.
1341 N. Hellerstein, Isle of Paradox and Other Logic Adventures.
[35] C. Pickover, Computers and the Imagination. New York St. Martin’s,
1991.
[36] R. L. Devaney, An Introduction to Chaotic Dynamical Systems. Menlo
Park, CA: Addison-Wesley, 1989.
[ 371 K. Falconer, Fractal Geometry: Mathematical Foundations and Applications. New York: Wiley, 1990.
[38] R. May, “Simple mathematical models with very complicated dynamics,” Nature, vol. 261, pp. 459-467, 1976.
Reseda, CA: Ridgeview, 1970.
Chicago, IL: Univ.
1992.
Patrick Grim received the A.B. degree in philosophy and anthropology from the University of
California, Santa Cruz, in 1971, the B. Phil. degree
from St. Andrews in 1975, and the A.M. and Ph.D.
degrees in philosophy from Boston University in
1976.
He is author of The Incomplete Universe: Totality, Knowledge, and Truth (M.I.T. PressBradford
Books, 1991) and co-editor of fourteen volumes of
The Philosopher’s Annual (Ridgeview Press). He is
an Associate Professor and a member of the Group
for Logic and Formal Semantics within the Department of Philosophy at
the State University of New York at Stony Brook. His current research
interests include alternative logics, game theory, dynamical systems, epistemic
modeling, contemporary metaphysics, and ethics. 