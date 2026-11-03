"""Small adapter around the Hugging Face Transformers text watermark API."""

from __future__ import annotations

import math
import random
import re
from dataclasses import dataclass
from typing import Any

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    WatermarkDetector,
    WatermarkingConfig,
)


MODEL_ID = "openai-community/gpt2"


@dataclass
class WatermarkEngine:
    tokenizer: Any
    model: Any
    detector: Any
    watermark_config: Any
    device: str

    @classmethod
    def load(cls, model_id: str = MODEL_ID) -> "WatermarkEngine":
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        # GPT-2 has no pad token; EOS is safe for batched generation here.
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token = tokenizer.eos_token
        model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
        model.eval()
        config = WatermarkingConfig(
            greenlist_ratio=0.25,
            bias=2.0,
            hashing_key=15485863,
            seeding_scheme="lefthash",
        )
        detector = WatermarkDetector(
            model_config=model.config,
            device=device,
            watermarking_config=config,
        )
        return cls(tokenizer, model, detector, config, device)

    def generate(self, prompt: str, max_new_tokens: int = 60,
                 temperature: float = 0.8, watermarked: bool = True) -> str:
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Enter a prompt before generating text.")
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        kwargs = {
            **inputs,
            "do_sample": True,
            "temperature": max(float(temperature), 0.05),
            "top_p": 0.9,
            "top_k": 50,
            "repetition_penalty": 1.15,
            "no_repeat_ngram_size": 3,
            "max_new_tokens": int(max_new_tokens),
            "pad_token_id": self.tokenizer.eos_token_id,
        }
        if watermarked:
            kwargs["watermarking_config"] = self.watermark_config
        with torch.no_grad():
            output_ids = self.model.generate(**kwargs)
        # Display only newly generated content; retain prompt separately in UI.
        return self.tokenizer.decode(
            output_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True
        ).strip()

    def detect(self, text: str) -> dict[str, Any]:
        if not text.strip():
            raise ValueError("Enter text to analyze.")
        encoded = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=1024
        )["input_ids"]
        # Transformers' built-in detector expects [batch, sequence], not a 1D row.
        result = self.detector(encoded, return_dict=True)
        def scalar(name: str, default: Any = None) -> Any:
            value = getattr(result, name, default)
            if value is None:
                return default
            if hasattr(value, "detach"):
                value = value.detach().cpu().numpy()
            if hasattr(value, "item"):
                try:
                    return value.item()
                except ValueError:
                    pass
            try:
                return value[0].item() if hasattr(value[0], "item") else value[0]
            except (TypeError, IndexError, KeyError):
                return value

        p_value = float(scalar("p_value", float("nan")))
        # Some API versions return zero for underflow; present it as below resolution.
        return {
            "tokens_scored": int(scalar("num_tokens_scored", 0)),
            "green_tokens": int(scalar("num_green_tokens", 0)),
            "green_fraction": float(scalar("green_fraction", float("nan"))),
            "z_score": float(scalar("z_score", float("nan"))),
            "p_value": p_value,
            "p_value_display": "< 1e-300" if p_value == 0 else f"{p_value:.3g}",
            "detected": bool(scalar("prediction", False)),
        }

    def delete_words(self, text: str, deletion_percent: int, seed: int = 7) -> str:
        words = text.split()
        if len(words) < 2 or deletion_percent <= 0:
            return text
        count = min(len(words) - 1, round(len(words) * deletion_percent / 100))
        rng = random.Random(seed)
        remove = set(rng.sample(range(len(words)), count))
        return " ".join(word for i, word in enumerate(words) if i not in remove)

    def edit_text(self, text: str, edit_type: str, percent: int = 30,
                  seed: int = 7) -> str:
        """Apply a reproducible text edit for the robustness demo."""
        words = text.split()
        if not words:
            return text
        rng = random.Random(seed)

        if edit_type == "Random word deletion":
            return self.delete_words(text, percent, seed)
        if edit_type == "Truncate from the end":
            keep_count = max(1, round(len(words) * (100 - percent) / 100))
            return " ".join(words[:keep_count])
        if edit_type == "Insert extra words":
            insert_count = max(1, round(len(words) * percent / 100))
            filler = ["however", "also", "for example", "in addition"]
            for _ in range(insert_count):
                words.insert(rng.randrange(len(words) + 1), rng.choice(filler))
            return " ".join(words)
        if edit_type == "Reorder sentences":
            sentences = [
                part.strip()
                for part in re.split(r"(?<=[.!?])\s+", text.strip())
                if part.strip()
            ]
            if len(sentences) < 2:
                return text
            rng.shuffle(sentences)
            return " ".join(sentences)
        if edit_type == "Lowercase and remove punctuation":
            return re.sub(r"[^\w\s]", "", text.lower())
        raise ValueError(f"Unknown text edit: {edit_type}")

