# Together-LLM

Build your personal language assistant and co-evolve with others assistants.

## LLM

### Model Architecture

**Encoder**

- [Bert](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/bert)
- [RoBERTa](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/roberta)
- [DistilBERT](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/distilbert)
- [ALBERT](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/albert)
- [DeBERTa](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/deberta)
- [Longformer](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/longformer)

**Decoder**

- GPT
- [GPT-J](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/gptj)
- [OPT](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/opt)
- [BLOOM](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/bloom)

- [llama](https://github.com/facebookresearch/llama)

**Encoder-Decoder**

- [BART](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/bart)
- [T5](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/t5)
- [Pegasus](https://huggingface.co/docs/transformers/v4.27.2/en/model_doc/pegasus)

### Dataset

**Unlabelled**

**Labelled**

### Deployment

**Quantification**

- [llama.cpp](https://github.com/ggerganov/llama.cpp)

**API Deployment**

- [llama.cpp2python](https://github.com/LostRuins/llamacpp-for-kobold)
- [chatgpt-web](https://github.com/Chanzhaoyu/chatgpt-web)
- [Gradio](https://gradio.app/)

**Processing**

- Pre-processing

- Post-processing

## Together

### Training

### Fine-tuning

**Dataset**
- [self-instruct](https://github.com/yizhongw/self-instruct)
- [Belle](https://huggingface.co/BelleGroup) & [Github](https://github.com/LianjiaTech/BELLE)


**Method**

- [PEFT](https://github.com/huggingface/peft)
    - LoRA: <a href="https://arxiv.org/pdf/2106.09685.pdf" rel="nofollow">LORA: LOW-RANK ADAPTATION OF LARGE LANGUAGE MODELS</a>
    - Prefix Tuning: <a href="https://aclanthology.org/2021.acl-long.353/" rel="nofollow">Prefix-Tuning: Optimizing Continuous Prompts for Generation</a>, <a href="https://arxiv.org/pdf/2110.07602.pdf" rel="nofollow">P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks</a>
    - P-Tuning: <a href="https://arxiv.org/pdf/2103.10385.pdf" rel="nofollow">GPT Understands, Too</a>
    - Prompt Tuning: <a href="https://arxiv.org/pdf/2104.08691.pdf" rel="nofollow">The Power of Scale for Parameter-Efficient Prompt Tuning</a>

- Self-Instruct
    - <a href="https://arxiv.org/abs/2212.10560">Self-Instruct: Aligning Language Model with Self Generated Instructions</a>

- FLAN
    - <a href="https://arxiv.org/abs/2210.11416">Scaling Instruction-Finetuned Language Models</a>

### Evolution

- [together](https://www.together.xyz/)
- [nebullvm](https://github.com/nebuly-ai/nebullvm)
- Distributed Learning
- Federated Learning

## Reference

- https://huggingface.co/

## Reading List

- [What Is ChatGPT Doing … and Why Does It Work?](https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/#circle=on)
- [A simple Python implementation of the ReAct pattern for LLMs](https://til.simonwillison.net/llms/python-react-pattern)
- [Language Models are Changing AI: The Need for Holistic Evaluation](https://crfm.stanford.edu/2022/11/17/helm.html)