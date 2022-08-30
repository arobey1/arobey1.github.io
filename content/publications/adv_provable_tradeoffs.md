---
title: "Provable tradeoffs in adversarially robust classification"
authors: "Edgar Dobriban, Hamed Hassani, David Hong, Alexander Robey"
venue: "IEEE Transactions on Information Theory"
date: 2021-07-22
pdf: "https://arxiv.org/pdf/2006.05161.pdf"
draft: false
github: "#"
mathjax: true
---


**Abstract.** It is well known that machine learning methods can be vulnerable to adversarially-chosen perturbations of their inputs. Despite significant progress in the area, foundational open problems remain. In this paper, we address several key questions. We derive exact and approximate Bayes-optimal robust classifiers for the important setting of two- and three-class Gaussian classification problems with arbitrary imbalance, for $\ell_2$ and $\ell_\infty$ adversaries. In contrast to classical Bayes-optimal classifiers, determining the optimal decisions here cannot be made pointwise and new theoretical approaches are needed. We develop and leverage new tools, including recent breakthroughs from probability theory on robust isoperimetry, which, to our knowledge, have not yet been used in the area. Our results reveal fundamental tradeoffs between standard and robust accuracy that grow when data is imbalanced. We also show further results, including an analysis of classification calibration for convex losses in certain models, and finite sample rates for the robust risk.