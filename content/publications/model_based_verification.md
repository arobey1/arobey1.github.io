---
title: "Toward Certified Robustness Against Real-World Distribution Shifts"
authors: "Haoze Wu*, Teruhiro Tagomori*, Alexander Robey*, Fengjun Yang*, Nikolai Matni, George J. Pappas, Hamed Hassani, Corina Pasareanu, Clark Barrett"
venue: "IEEE Conference on Secure and Trustworthy Machine Learning"
date: 2023-02-08
pdf: "https://arxiv.org/pdf/2206.03669.pdf"
draft: false
github: "https://github.com/anwu1219/MUNIT-VNN"
mathjax: true
---

**Abstract.** We consider the problem of certifying the robustness of deep neural networks against real-world distribution shifts.  To do so, we bridge the gap between hand-crafted specifications and realistic deployment settings by proposing a novel neural-symbolic verification framework, in which we train a generative model to learn perturbations from data and define specifications with respect to the output of the learned model.  A unique challenge arising from this setting is that existing verifiers cannot tightly approximate sigmoid activations, which are fundamental to many state-of-the-art generative models.
To address this challenge, we propose a general meta-algorithm for handling sigmoid activations which leverages classical notions of counter-example-guided abstraction refinement. The key idea is to ``lazily'' refine the abstraction of sigmoid functions to exclude spurious counter-examples found in the previous abstraction, thus guaranteeing progress in the verification process while keeping the state-space small. Experiments on the MNIST and CIFAR-10 datasets show that our framework significantly outperforms existing methods on a range of challenging distribution shifts.