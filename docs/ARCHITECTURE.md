# FSI Mathematical Architecture

## 1. Cognitive Core (TinyGatedRNN)
The core operates on a gated recurrence relation:
h_next = (1 - z) * h_prev + z * tanh(W_h * [h_prev; x])
Where 'z' acts as a learnable forget/update gate, modeled after the gated recurrent unit topology but optimized for low-compute environments.

## 2. Bayesian Confidence Gate
Trust is computed as a scalar probability (0 to 1). 
- If P(confidence) < 0.8: System triggers THROT_ACTIVE.
- This creates an intrinsic self-regulation mechanism that prevents output when the RNN's internal state lacks alignment with verified data.

## 3. Weight Serialization
Weights are stored as serialized numpy arrays (model.bin), allowing for model snapshots and persistent personality/knowledge retention.
