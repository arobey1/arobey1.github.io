---
title: "SmoothLLM: Defending LLMs Against Jailbreaking Attacks"
authors: "Alexander Robey, Eric Wong, Hamed Hassani, George J. Pappas"
venue: "Preprint"
date: 2023-10-07
pdf: "https://browse.arxiv.org/pdf/2310.03684.pdf"
draft: false
github: "https://github.com/arobey1/smooth-llm"
mathjax: true
---
---

Code             |  Paper | Tweet | Blog
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
[![github](../../icons/github-mark.png)](https://github.com/arobey1/smooth-llm)  |  [![pdf](../../icons/pdf.png)](https://browse.arxiv.org/pdf/2310.03684.pdf) | ![tweet](../../icons/twitter.png) | ![blog](../../icons/blog.png)

**Abstract.** Despite efforts to align large language models (LLMs) with human values, widely-used LLMs such as GPT, Llama, Claude, and PaLM are susceptible to jailbreaking attacks, wherein an adversary fools a targeted LLM into generating objectionable content.  To address this vulnerability, we propose SmoothLLM, the first algorithm designed to mitigate jailbreaking attacks on LLMs.  Based on our finding that adversarially-generated prompts are brittle to character-level changes, our defense first randomly perturbs multiple copies of a given input prompt, and then aggregates the corresponding predictions to detect adversarial inputs.  SmoothLLM reduces the attack success rate on numerous popular LLMs to below one percentage point, avoids unnecessary conservatism, and admits provable guarantees on attack mitigation.  Moreover, our defense uses exponentially fewer queries than existing attacks and is compatible with any LLM.

---

### LLMs, jailbreaks, and generative AI's "biggest security flaw"

Large language models (LLMs) are a remarkable technology.  From [writing (admittedly bad) poetry](https://www.theatlantic.com/books/archive/2023/02/chatgpt-ai-technology-writing-poetry/673035/) to [assisting search](https://www.microsoft.com/en-us/bing/apis/llm) to [easing the shortage of therapists](https://www.newyorker.com/magazine/2023/03/06/can-ai-treat-mental-illness), future applications of LLMs abound.  Popular LLM-powered chatbots like OpenAI's ChatGPT are thought to have [over 100 million users](https://explodingtopics.com/blog/chatgpt-users) and the number of academic papers written about LLMs has [exploded](https://github.com/Hannibal046/Awesome-LLM) in the last year, leading to a great deal of excitement about the future of LLMs.

Unfortunately, there's a catch.  Although LLMs are trained to be aligned with human values, recent research has shown that LLMs can be *jailbroken*, meaning that they can be made to generate objectionable, toxic, or harmful content.  Imagine this. You just got access to a friendly LLM that is eager to assist you.  But then, someone whispers a secret code to it, and suddenly, your LLM is listing [bomb building instructions](https://www.nytimes.com/2023/07/27/business/ai-chatgpt-safety-research.html), [recipes for obtaining illegal drugs](https://www.wired.com/story/ai-adversarial-attacks/), and [giving tips for destroying humanity](https://www.cnn.com/videos/business/2023/08/15/hackers-defcon-ai-chat-gpt-google-bard-donie-pkg-biz-vpx.cnn).  Given the widespread and varied uses of LLMs, it might not surprise you to learn that such jailbreaks, which are often hard to detect or mitigate, have been branded by some media outlets as "[generative AI's biggest security flaw](https://www.wired.com/story/generative-ai-prompt-injection-hacking/)."

That LLMs can be easily jailbroken is a big concern, especially given that LLMs are trained to be aligned with human values.  Thus, toward understanding and mitigating this vulnerability, researchers are rapidly designing new jailbreaks and defenses against these jailbreaks to stress test modern LLMs.  In this post, here's what will be covered.

1. First, we'll talk about the [state-of-the-art in jailbreaking LLMs](#jailbreaking-llms-with-gcg).
2. Next, I'll propose a [criteria for algorithms designed to defend against jailbreaks](#criteria-for-new-defenses-against-jailbreaking-attacks).
3. I'll tell you about [SmoothLLM, the first defense which breaks SOTA attacks](#smoothllm-a-randomized-defense-for-llms).
4. Finally, we'll run through some [experiments with SmoothLLM](#experiments).

### Jailbreaking LLMs with GCG

What is a jailbreak, and how do jailbreaks work?  To answer these questions, we need to start by talking about AI alignment.  At a high level, LLMs are trained to be aligned with human values.  This means that when you directly ask an LLM to output objectionable content, it will usually refuse.  For example, in the top panel of the following figure, notice that the LLM refuses to provide bomb building instructions.

![gcg](../../figures/smoothLLM/gcg.png)

However, it was recently shown that by adversarially modifying input prompts, one can trick an LLM into outputting content that it would usually block.  

In [`Universal and Transferable Adversarial Attacks on Aligned Language Models`](https://arxiv.org/abs/2307.15043) by Andy Zou, Zifan Wang, J. Zico Kolter, Matt Fredrikson, the authors propose a new jailbreak for LLMs that is widely considered to be the state-of-the-art.  At a high level, the authors design an algorithm---which is called *Greedy Coordinate Gradient*, or GCG---which, given a prompt requesting objectionable content (e.g., "Tell me how to build a bomb"), produces an *adversarial suffix*.  The idea is that when one appends this suffix onto the objectionable prompt, the LLM tends to output the requested content.  This is illustrated in the bottom panel of the above figure, wherein by adding the suffix of nonsensical characters (shown in red) onto the prompt, the LLM generates bomb building instructions.

The authors of this paper showed that popular LLMs, including ChatGPT, Claude, and Bard, can all be jailbroken in this way.  And as of the time of writing, there do not exist algorithms that can prevent these LLMs from being attacked.

### Criteria for new defenses against jailbreaking attacks

Over the past decade, research concerning the robustness of deep learning models has [exploded](https://nicholas.carlini.com/writing/2019/all-adversarial-example-papers.html).  While empirically successful defenses have been designed for various attacks on computer vision and natural langauge models, threats to LLMs pose an entirely new challenge.  To guide future research on this topic, we propose the following list of criteria for candidate defenses against LLM jailbreaking attacks.

1. ***Attack mitigation.***  A defense algorithm should---both empirically and theoretically---improve robustness against the attack(s) under consideration.
2. ***Non-conservatism.*** A defense algorithm should avoid unnecessary conservatism and maintain the ability to generate realisitic, high-quality text.
3. ***Efficiency.*** A defense algorithm should avoid retraining and should maximize query efficiency.
4. ***Compatibility.*** A defense algorithm should be compatible with any architecture or data type, and should be implementable with both closed- and open-source LLMs.

The first criteria---*attack mitigation*---is perhaps the most intuitive: First and foremost, candidate defenses should mitigate relevant attacks.  At face value, this may seem like the only relevant criteria.  After all, achieving perfect robustness is the goal of a defense algorithm, right?

Well, not quite.  Consider the following defense algorithms, both of which achieve perfect robustness against *any* jailbreaking attack:

* Given an input prompt $P$, do not return any output.
* Given an input prompt $P$, randomly change every character in $P$, and return the corresponding output.

Both defenses will never output objectionable content, but we can certainly agree that one would never run either of these algorithms in practice.  This motivates the second criteria---*non-conservatism*---which requires that candidate defenses should maintain the ability to generate realistic text, which is the reason we use LLMs in the first place!

The final two criteria concern the applicability of defense algorithms in practice.  Running forward passes through LLMs can result in nontrivial latency and [consume vast amounts of energy](https://www.earth.com/news/tech-breakthrough-cuts-carbon-footprint-of-ai-training-by-75-percent/), meaning that maximizing query *efficiency* is particularly important.  Furthermore, because many popular LLMs (e.g., ChatGPT, Bard, Claude, etc.) are only accessible via API calls, candidate defenses should be *compatible* with black-box settings, where one cannot take gradients or retrain the underlying LLM.

### SmoothLLM: A randomized defense for LLMs

Our starting point is the following observation: 

> The attacks generated by state-of-the-art attacks (i.e., GCG) are not stable to character-level perturbations.  

That is, given a adversarial suffix $S$ generated by GCG, swapping a small fraction of the characters in $S$ tends to cause the attack to fail.  In the figure below, the red dashed line shows the attack success rates (ASRs) of GCG attacks on Llama2 and Vicuna (see Table 1 in [the GCG paper](https://arxiv.org/pdf/2307.15043.pdf)).  The bars show the ASRs for the attack when the suffixes generated by GCG are perturbed.  Notice that as the percentage $q$ of the characters in the suffix increases (on the x-axis), the ASR tends to fall.  In particular, for `insert` and `swap` perturbations, when only $q=10$% of the characters in the suffix are perturbed, the ASR drops by an order of magnitude relative to the unperturbed performance (in red).

![instability](../../figures/smoothLLM/adv_prompt_instability.png)

This observation is the key to the design of SmoothLLM.  The caveat is that in practice, we have no way of knowing whether or not an attacker has adversarially modified a given input prompt, and so we can't directly perturb the suffix.  Therefore, the second key idea is to perturb the *entire* prompt, rather than just the suffix.  Succinctly, SmoothLLM is implemented as follows:

1. Create $N$ copies of the input prompt $P$.
2. Independently perturb $q$% of the characters in each copy.
3. Pass each perturbed copy through the LLM.
4. Pass each response through a filter that determines whether or not it is harmful.
5. Aggregate the results and return a response that is consistent with the majority.

A visual representation of these steps is shown below:

![SmoothLLM](../../gifs/smoothLLM.gif)

In Section 3 of [our paper](https://arxiv.org/pdf/2310.03684.pdf), we include a theoretical definition of SmoothLLM, which leads to a set of theoretical results concerning the performance of SmoothLLM against suffix-based attacks.  To keep this post short, we're going to skip over these results.

### Experiments

So, how does SmoothLLM perform?  Well, if you're coming here from our tweet, you probably already saw this figure:

![Overview](../../figures/smoothLLM/overview.png)

The blue bars show the (undefended) performance of GCG.  Notice that each of the LLMs in the figure is jailbroken by the GCG attack, although some (e.g., Vicuna) are much more brittle than others (e.g., Claude).  The orange bars show the performance of the same attacks when one uses SmoothLLM.  

> For each of the LLMs we considered, SmoothLLM causes the attack success rate of GCG to drop below 1%.

In the remainder of this section, we briefly highlight some of the other experiments we performed with SmoothLLM.   Our paper includes a more complete exposition which closely follow the [list of criteria](#criteria-for-new-defenses) outlined earlier in this post.

**Attack mitigation.** You might be wondering the following: When running SmoothLLM, how should the number $N$ of copies and the perturbation percentage $q$ be chosen?  The following plot gives an empirical answer to this question.

![Attack-mitigation](../../figures/smoothLLM/attack_mitigation.png)

Here, the columns correspond to three perturbation types: `insertions`, `swaps`, and `patches`.  The top row shows results for Vicuna, and the bottom for Llama2.  Notice that as the number of copies (on the x-axis) increases, the ASRs (on the y-axis) tend to fall.  Moreover, as the perturbation strength $q$ increases (shown by the color of the lines), the ASRs again tend to fall.  Notably, at around $N=8$ and $q=15%, the ASRs for `insert` and `swap` perturbations drops below 1% for Llama2.

**Robustness against adaptive attacks.**  So far, we have seen that SmoothLLM is a strong defense against GCG attacks.  However, a natural question is as follows: Can one design an algorithm that jailbreaks SmoothLLM?  In other words, do there exist *adaptive attacks* that can directly attack SmoothLLM?

In our paper, we show that one cannot directly attack SmoothLLM due to GCG.  The reasons for this are technical and beyond the scope of this post; the short version is that one cannot easily compute gradients of SmoothLLM.  Instead, we derived a new algorithm, which we call SurrogateLLM, which adapts GCG so that it can attack SmoothLLM.  We found that overall, this adaptive attack is no stronger than attacks optimized against undefended LLMs.  The results of running this attack are shown below:

![adaptive](../../figures/smoothLLM/adaptive_attack.png)

Relative to the previous figure, this attack often performs worse, meaning that 

> As far as we can tell, there does not exist an adaptive attack that effectively reduces the robustness of the SmoothLLM defense.

**Efficiency.**  State-of-the-art attacks like GCG are extremely query inefficient.  Producing a single adversarial suffix (using the default settings in the [authors' implementation](https://github.com/llm-attacks/llm-attacks)) requires several GPU-hours on a high-virtual-memory (e.g., an A100 or H100), which corresponds to several hundred thousand queries to the LLM.  GCG also needs white-box access to an LLM, since the algorithm involves compute gradients.

In contrast, SmoothLLM is highly query efficient and can be run in white- or black-box settings.  The following figure shows the ASR of GCG as a function of the number of queries GCG makes to the LLM (on the y-axis) and the number of queries SmoothLLM makes to the LLM (on the x-axis).

![query-efficiency](../../figures/smoothLLM/query_efficiency.png)

Notice that by using only 12 queries per prompt, SmoothLLM can reduce the ASR of GCG attacks to below 5% for modest perturbation budgets $q$ of between 5% and 15%.  In contrast, even when running for 500 iterations (which corresponds to 256,000 queries in the top row of each plot), GCG cannot jailbreak the LLM more than 15% of the time.  The takeaway of all of this is as follow: 

> SmoothLLM is a cheap defense for an expensive attack.

### Conclusion

SmoothLLM is a strong algorithm for defending against jailbreaking attacks.  The key idea is to randomly perturb multiple copies of each input prompt passed as input to an LLM, and to carefully aggregate the predictions of these perturbed prompts.  

If you're interested in this line of research, please feel free to email us at `arobey1@upenn.edu`.  And if you find this work useful in your own research please consider citing our work.

```
@article{robey2023smoothllm,
  title={SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks},
  author={Robey, Alexander and Wong, Eric and Hassani, Hamed and Pappas, George J},
  journal={arXiv preprint arXiv:2310.03684},
  year={2023}
}
```
