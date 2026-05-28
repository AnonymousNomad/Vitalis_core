import torch
import torch.nn.functional as F
import numpy as np
from typing import Iterable, Tuple
from fluid_transformer import FluidTransformer
from abstract_reasoner import AbstractReasoner
from science_reasoner import ScienceReasoner
from concept_graph import ConceptGraph
from free_energy import FreeEnergyEngine
from ledger import Ledger
from CyberCore import CyberCore

# ----------------------------------------------------------------------
# Tokenizer Helpers
# ----------------------------------------------------------------------
def _tokenize(text: str) -> torch.Tensor:
    tokenizer = _init_transformer().tokenizer
    ids = tokenizer.encode(text, add_special_tokens=True, return_tensors="pt")
    return ids.squeeze(0)

def _decode(ids: torch.Tensor) -> str:
    tokenizer = _init_transformer().tokenizer
    return tokenizer.decode(ids.tolist(), skip_special_tokens=True)

# ----------------------------------------------------------------------
# Teacher Forcing Loop
# ----------------------------------------------------------------------
def execute_teacher_forcing(batch: Iterable[Tuple[str, str]], max_steps: int = 12, learning_rate: float = 1e-4) -> float:
    transformer = _init_transformer()
    transformer.train()
    optimizer = torch.optim.SGD(transformer.parameters(), lr=learning_rate)
    total_loss, n_examples = 0.0, 0
    
    for inp, tgt in batch:
        try:
            final_node, _ = process_input(inp, max_depth=max_steps)
        except Exception as e:
            _init_ledger().record(action="train_reject", payload={"input": inp, "error": str(e)})
            continue

        pred_text = final_node.label
        pred_ids = _tokenize(pred_text).unsqueeze(0)
        tgt_ids = _tokenize(tgt).unsqueeze(0)
        
        pad_id = transformer.tokenizer.pad_token_id
        max_len = max(pred_ids.size(1), tgt_ids.size(1))
        pred_ids = F.pad(pred_ids, (0, max_len - pred_ids.size(1)), value=pad_id)
        tgt_ids = F.pad(tgt_ids, (0, max_len - tgt_ids.size(1)), value=pad_id)
        
        logits = transformer(pred_ids)
        loss = F.cross_entropy(logits.view(-1, logits.size(-1)), tgt_ids.view(-1), ignore_index=pad_id)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        _init_ledger().record(action="train_step", payload={"input": inp, "target": tgt, "prediction": pred_text, "loss": float(loss.item())})
        total_loss += loss.item()
        n_examples += 1
        
    transformer.eval()
    return total_loss / max(1, n_examples)

# ----------------------------------------------------------------------
# Singletons
# ----------------------------------------------------------------------
_transformer = _abstract_reasoner = _science_reasoner = _concept_graph = _free_energy = _ledger = _cybercore = None

def _init_transformer():
    global _transformer
    if _transformer is None:
        _transformer = FluidTransformer.from_pretrained("models/fluid_transformer")
        _transformer.eval()
    return _transformer

def _init_abstract():
    global _abstract_reasoner
    if _abstract_reasoner is None: _abstract_reasoner = AbstractReasoner(chunk_size=8, top_k=6)
    return _abstract_reasoner

def _init_science():
    global _science_reasoner, _concept_graph
    if _science_reasoner is None: _science_reasoner = ScienceReasoner(_init_graph())
    return _science_reasoner

def _init_graph():
    global _concept_graph
    if _concept_graph is None: _concept_graph = ConceptGraph(dim=768, persist_dir="data/concept_graph")
    return _concept_graph

def _init_free_energy():
    global _free_energy
    if _free_energy is None: _free_energy = FreeEnergyEngine()
    return _free_energy

def _init_ledger():
    global _ledger
    if _ledger is None: _ledger = Ledger(chain_name="FSI_Sovereign")
    return _ledger

def _init_cybercore():
    global _cybercore
    if _cybercore is None: _cybercore = CyberCore()
    return _cybercore

def process_input(text: str, max_depth: int = 12):
    if _init_cybercore().is_malicious(text): raise ValueError("Input rejected")
    hidden = _init_transformer().encode(text).squeeze(0).cpu().numpy()
    hidden /= np.linalg.norm(hidden)
    propositions, raw_steps = _init_abstract().reason(hidden)
    final_node = _init_science().infer(propositions, raw_steps, max_depth=max_depth)
    
    involved_cids = {final_node.cid}
    for src, tgt, _w in final_node.edges: involved_cids.add(tgt)
    embeddings = [final_node.embedding] + [_init_graph().get_node(cid).embedding for cid in involved_cids if cid != final_node.cid]
    
    loss = _init_free_energy().compute_loss(embeddings)
    avg = sum(_init_ledger().get_recent_losses(100)) / (len(_init_ledger().get_recent_losses(100)) + 1e-9)
    
    if loss <= avg * 1.10:
        _init_ledger().record(action="commit", payload={"text": text, "final_node": final_node.cid, "label": final_node.label, "confidence": final_node.confidence, "free_energy": loss})
        _init_graph().persist()
    else:
        _init_ledger().record(action="reject", payload={"text": text, "reason": "free_energy_too_high"})
        raise RuntimeError("Knowledge rejected")
    return final_node, raw_steps
