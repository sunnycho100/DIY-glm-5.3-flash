"""Byte tokenizer: every UTF-8 byte is one token, shifted past 4 special tokens.

Adapted from vukrosic/glm-5.3-flash-from-scratch (MIT).
"""
from __future__ import annotations


class ByteTokenizer:
    pad_id = 0
    bos_id = 1
    eos_id = 2
    sep_id = 3
    byte_offset = 4
    vocab_size = 260

    def encode(self, text: str, *, bos: bool = False, eos: bool = False) -> list[int]:
        ids = [self.byte_offset + value for value in text.encode("utf-8")]
        if bos:
            ids.insert(0, self.bos_id)
        if eos:
            ids.append(self.eos_id)
        return ids

    def decode(self, ids: list[int]) -> str:
        values = bytearray()
        for token in ids:
            if token == self.eos_id:
                break
            if token >= self.byte_offset:
                values.append(token - self.byte_offset)
        return values.decode("utf-8", errors="replace")


if __name__ == "__main__":
    tok = ByteTokenizer()
    ids = tok.encode("def f", bos=True, eos=True)
    print(ids)
    assert ids == [1, 104, 105, 106, 36, 106, 2]
    assert tok.decode(ids) == "def f"
    print("tokenizer ok")
