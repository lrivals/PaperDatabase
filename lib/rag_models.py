"""The two pinned local Qwen models (GPU route). Imported only for dense indexing/search.

Optional: the default route is CPU (lib/rag.py, bge-small). The Qwen models are used only
when the user turns the GPU route on (`bin/pdb gpu on`, or PDB_GPU=1) and CUDA is present;
see enabled() and status(). numpy/torch/transformers are imported lazily, so this module
loads on a CPU-only install (requirements.txt).
"""

import importlib.util
import json
import os
from pathlib import Path

EMBED = "Qwen/Qwen3-Embedding-4B"
EMBED_REV = "5cf2132abc99cad020ac570b19d031efec650f2b"
RERANK = "Qwen/Qwen3-Reranker-4B"
RERANK_REV = "22e683669bc0f0bd69640a1354a6d0aebcfeede5"
TASK = "Given a web search query, retrieve relevant passages that answer the query"


def config_path(env=None):
    """Machine-level setting, next to the base registry (lib/registry.py)."""
    from lib import registry
    return registry.path(env).with_name("config.json")


def _config(env=None):
    p = config_path(env)
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    except (OSError, json.JSONDecodeError):
        return {}


def set_wanted(on, env=None):
    """Turn the GPU route on/off for this machine (bin/pdb gpu on|off)."""
    p = config_path(env)
    conf = _config(env)
    conf["gpu"] = bool(on)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(conf, indent=1) + "\n", encoding="utf-8")


def wanted(env=None):
    """Has the user asked for the GPU route? PDB_GPU (1/0) overrides the saved setting."""
    env = os.environ if env is None else env
    flag = env.get("PDB_GPU", "").strip().lower()
    if flag:
        return flag not in ("0", "false", "no", "off", "non")
    return bool(_config(env).get("gpu"))


def installed():
    return all(importlib.util.find_spec(m) is not None for m in ("numpy", "torch", "transformers"))


def unavailable():
    """None if the Qwen models can run here, else the reason (French, for the CLI)."""
    if not installed():
        return "torch/transformers absents (pip install -r requirements-rag.txt)"
    import torch
    if not torch.cuda.is_available():
        return "aucun GPU CUDA détecté"
    return None


def models_cached():
    hub = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
    return all((hub / f"models--{m.replace('/', '--')}").exists() for m in (EMBED, RERANK))


def enabled():
    """(use_gpu, reason): the GPU route is used when wanted and available."""
    if not wanted():
        return False, "route GPU désactivée (bin/pdb gpu on pour l'activer)"
    reason = unavailable()
    return (reason is None), reason


def download_models():
    """Populate the local cache for both models used by default hybrid search."""
    from huggingface_hub import snapshot_download
    snapshot_download(EMBED, revision=EMBED_REV)
    snapshot_download(RERANK, revision=RERANK_REV)


def tokenizer(download=False):
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(EMBED, revision=EMBED_REV,
                                         local_files_only=not download, padding_side="left")


def _device():
    import torch
    if not torch.cuda.is_available():
        raise RuntimeError("Qwen3-4B retrieval requires CUDA here; use --mode lexical")
    return "cuda"


def embed_texts(texts, query=False, download=False, batch_size=8):
    """Official last-token pooling and query instruction; float32 unit vectors."""
    import numpy as np
    import torch
    from transformers import AutoModel
    if not texts:
        return np.empty((0, 2560), dtype=np.float32)
    device = _device()
    tok = tokenizer(download)
    model = AutoModel.from_pretrained(EMBED, revision=EMBED_REV,
                                      local_files_only=not download, dtype=torch.bfloat16,
                                      attn_implementation="sdpa").to(device).eval()
    if query:
        texts = [f"Instruct: {TASK}\nQuery: {s}" for s in texts]
    vectors = []
    try:
        with torch.inference_mode():
            for i in range(0, len(texts), batch_size):
                batch = tok(texts[i:i + batch_size], padding=True, truncation=True,
                            max_length=8192, return_tensors="pt").to(device)
                if max(batch["attention_mask"].sum(dim=1)).item() >= 8192:
                    raise ValueError("embedding input reached the model limit")
                out = model(**batch).last_hidden_state[:, -1, :].float()
                out = torch.nn.functional.normalize(out, p=2, dim=1)
                vectors.extend(out.cpu().numpy())
    finally:
        del model
        torch.cuda.empty_cache()
    return np.asarray(vectors, dtype=np.float32)


def rerank(query, documents, batch_size=2):
    """Official Qwen yes/no next-token relevance score, not scientific confidence."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    if not documents:
        return []
    device = _device()
    tok = AutoTokenizer.from_pretrained(RERANK, revision=RERANK_REV,
                                        local_files_only=True, padding_side="left")
    model = AutoModelForCausalLM.from_pretrained(RERANK, revision=RERANK_REV,
                                                 local_files_only=True, dtype=torch.bfloat16,
                                                 attn_implementation="sdpa").to(device).eval()
    model.config.use_cache = False
    prefix = '<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
    suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
    pre = tok.encode(prefix, add_special_tokens=False)
    post = tok.encode(suffix, add_special_tokens=False)
    yes, no = tok.convert_tokens_to_ids("yes"), tok.convert_tokens_to_ids("no")
    scores = []
    try:
        with torch.inference_mode():
            for i in range(0, len(documents), batch_size):
                pairs = [f"<Instruct>: {TASK}\n<Query>: {query}\n<Document>: {d}"
                         for d in documents[i:i + batch_size]]
                ids = tok(pairs, add_special_tokens=False, truncation=True,
                          max_length=8192 - len(pre) - len(post))["input_ids"]
                padded = tok.pad({"input_ids": [pre + x + post for x in ids]},
                                 padding=True, return_tensors="pt").to(device)
                logits = model(**padded, logits_to_keep=1).logits[:, -1, :]
                scores += torch.softmax(torch.stack((logits[:, no], logits[:, yes]), dim=1).float(),
                                        dim=1)[:, 1].cpu().tolist()
    finally:
        del model
        torch.cuda.empty_cache()
    return scores
