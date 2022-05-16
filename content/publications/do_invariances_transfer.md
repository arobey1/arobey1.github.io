---
title: "Do deep networks transfer invariances across classes?"
authors: "Allan Zhou*, Fahim Tajwar*, Alexander Robey, Tom Knowles, George J. Pappas, Hamed Hassani, Chelsea Finn"
venue: "ICLR 2022"
date: 2022-01-20
pdf: "https://openreview.net/forum?id=Fn7i_r5rR0q&noteId=jyUyeiKrkN6"
draft: false
github: "https://github.com/AllanYangZhou/invariant-perturbations"
mathjax: true
---

**Abstract.** To generalize well, classifiers must learn to be invariant to nuisance transformations that do not alter an input's class.  Many problems have ``class-agnostic'' nuisance transformations that apply similarly to all classes, such as lighting and background changes for image classification. Neural networks can learn these invariances given sufficient data, but many real-world datasets are heavily class imbalanced and contain only a few examples for most of the classes. We therefore pose the question: how well do neural networks transfer class-agnostic invariances learned from the large classes to the small ones? Through careful experimentation, we observe that invariance to class-agnostic transformations is still heavily dependent on class size, with the networks being much less invariant on smaller classes. This result holds even when using data balancing techniques, and suggests poor invariance transfer across classes. Our results provide one explanation for why classifiers generalize poorly on unbalanced and long-tailed distributions. Based on this analysis, we show how a generative model approach for learning the nuisance transformations can help transfer invariances across classes and improve performance on a set of imbalanced image classification benchmarks.