---
title: "Defending Large Language Models against Jailbreak Attacks via Semantic Smoothing"
authors: "Jiabao Ji*, Bairu Hou*, Alexander Robey*, George J Pappas, Hamed Hassani, Yang Zhang, Eric Wong, Shiyu Chang"
venue: "Preprint"
date: 2024-02-25
pdf: "https://arxiv.org/pdf/2402.16192.pdf"
draft: false
github: "https://github.com/UCSB-NLP-Chang/SemanticSmooth"
mathjax: true
---

**Abstract.** Aligned large language models (LLMs) are vulnerable to jailbreaking attacks, which bypass the safeguards of targeted LLMs and fool them into generating objectionable content. While initial defenses show promise against token-based threat models, there do not exist defenses that provide robustness against semantic attacks and avoid unfavorable trade-offs between robustness and nominal performance. To meet this need, we propose SemanticSmooth, a smoothing-based defense that aggregates the predictions of multiple semantically transformed copies of a given input prompt. Experimental results demonstrate that SemanticSmooth achieves state-of-the-art robustness against GCG, PAIR, and AutoDAN attacks while maintaining strong nominal performance on instruction following benchmarks such as InstructionFollowing and AlpacaEval. The codes will be publicly available at https://github.com/UCSB-NLP-Chang/SemanticSmooth.