---
title: "Adversarial Robustness with Semi-Infinite Constrained Learning"
authors: "Alexander Robey, Luiz F. O. Chamon, George J. Pappas, Hamed Hassani, Alejandro Ribeiro"
venue: "NeurIPS 2021"
date: 2021-11-26
pdf: "https://proceedings.neurips.cc/paper/2021/file/312ecfdfa8b239e076b114498ce21905-Paper.pdf"
draft: false
github: "https://github.com/arobey1/advbench"
---

**Abstract.**  Despite strong performance in numerous applications, the fragility of deep learning to input perturbations has raised serious questions about its use in safety-critical domains. While adversarial training can mitigate this issue in practice, state-of- the-art methods are increasingly application-dependent, heuristic in nature, and suffer from fundamental trade-offs between nominal performance and robustness. Moreover, the problem of finding worst-case perturbations is non-convex and underparameterized, both of which engender a non-favorable optimization landscape. Thus, there is a gap between the theory and practice of adversarial training, particularly with respect to when and why adversarial training works. In this paper, we take a constrained learning approach to address these questions and to provide a theoretical foundation for robust learning. In particular, we leverage semi-infinite optimization and non-convex duality theory to show that adversarial training is equivalent to a statistical problem over perturbation distributions, which we characterize completely. Notably, we show that a myriad of previous robust training techniques can be recovered for particular, sub-optimal choices of these distributions. Using these insights, we then propose a hybrid Langevin Monte Carlo approach of which several common algorithms (e.g., PGD) are special cases. Finally, we show that our approach can mitigate the trade-off between nominal and robust performance, yielding state-of-the-art results on MNIST and CIFAR-10. Our code is available at: https://github.com/arobey1/advbench.

---

In this paper, we revisit the classicial problem of training a classifier to be robust against small perturbations of data.

$$\min_\theta \mathbb{E}_{(x,y)} \left[ \max_{\delta\in\Delta} \ell(f_\theta(x+\delta),y) \right]$$