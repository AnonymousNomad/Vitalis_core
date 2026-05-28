import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class SovereignTransformer:
    def __init__(self, model_name: str = "facebook/opt-125m", device: str = None):
        self.device = device or "cpu"
        self.dtype = torch.float32
        print(f"[*] Initializing Sovereign Generative Backbone: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=self.dtype, low_cpu_mem_usage=True
        ).to(self.device)

        if hasattr(torch, "compile"):
            print("[*] JIT-Compiling Sovereign Backbone...")
            self.model = torch.compile(self.model)

        self.model.eval()

    def encode(self, text: str) -> torch.Tensor:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            hidden = self.model.base_model(**inputs, return_dict=True).last_hidden_state
        vec = hidden[:, -1, :]
        return torch.nn.functional.normalize(vec, p=2, dim=-1).squeeze(0)

    @property
    def dim(self) -> int:
        return self.model.config.hidden_size
