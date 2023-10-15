---
title: "Jailbreaking Black Box Large Language Models in Twenty Queries"
authors: "Patrick Chao, Alexander Robey, Edgar Dobriban, Hamed Hassani, George J. Pappas, Eric Wong"
venue: "Preprint"
date: 2023-10-12
pdf: "https://arxiv.org/pdf/2310.08419.pdf"
draft: false
github: "#"
---

**Abstract.** There is growing interest in ensuring that large language models (LLMs) align with human values. However, the alignment of such models is vulnerable to adversarial jailbreaks, which coax LLMs into overriding their safety guardrails. The identification of these vulnerabilities is therefore instrumental in understanding inherent weaknesses and preventing future misuse.  To this end, we propose *Prompt Automatic Iterative Refinement* (PAIR), an algorithm that generates semantic jailbreaks with only black-box access to an LLM. PAIR---which is inspired by social engineering attacks---uses an attacker LLM to automatically generate jailbreaks for a separate targeted LLM without human intervention. In this way, the attacker LLM iteratively queries the target LLM to update and refine a candidate jailbreak. Empirically, PAIR often requires fewer than twenty queries to produce a jailbreak, which is orders of magnitude more efficient than existing algorithms.  PAIR also achieves competitive jailbreaking success rates and transferability on open and closed-source LLMs, including GPT-3.5/4, Vicuna, and PaLM-2.