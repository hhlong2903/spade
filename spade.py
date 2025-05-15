# spade/spade.py
import itertools
from collections import defaultdict

def read_sequences(data_lines):
    sequences = defaultdict(list)
    for line in data_lines:
        sid, eid, item = line.strip().split()
        sid = int(sid)
        sequences[sid].append((int(eid), item))

    result = {}
    for sid, events in sequences.items():
        event_dict = defaultdict(list)
        for eid, item in events:
            event_dict[eid].append(item)
        result[sid] = [event_dict[eid] for eid in sorted(event_dict)]
    return result

def generate_subsequences(sequence, max_len=3):
    subsequences = set()

    def dfs(seq, path, idx):
        if path:
            subsequences.add(tuple(path))
        if len(path) == max_len:
            return
        for i in range(idx, len(seq)):
            event = seq[i]
            # Xét tất cả tập con không rỗng trong event (có thể là 1 item, 2 item...)
            for subset_size in range(1, len(event) + 1):
                for subset in itertools.combinations(event, subset_size):
                    dfs(seq, path + [subset if len(subset) > 1 else subset[0]], i + 1)

    dfs(sequence, [], 0)
    return subsequences


def spade_mine(sequences, min_support=2, max_len=3):
    pattern_counts = defaultdict(int)
    for seq in sequences.values():
        seen = set()
        for pattern in generate_subsequences(seq, max_len):
            if pattern not in seen:
                pattern_counts[pattern] += 1
                seen.add(pattern)
    # Chỉ trả về các pattern có độ phổ biến ≥ min_support
    return {p: c for p, c in pattern_counts.items() if c >= min_support}

