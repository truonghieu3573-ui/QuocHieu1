class RailFenceCipher:
    def rail_fence_encrypt(self, text, key):
        fence = [[] for _ in range(key)]
        rail = 0
        direction = 1
        for char in text:
            fence[rail].append(char)
            if rail == 0:
                direction = 1
            elif rail == key - 1:
                direction = -1
            rail += direction
        return ''.join(''.join(r) for r in fence)

    def rail_fence_decrypt(self, text, key):
        n = len(text)
        fence = [[] for _ in range(key)]
        rail = 0
        direction = 1
        pattern = []
        for i in range(n):
            pattern.append(rail)
            if rail == 0:
                direction = 1
            elif rail == key - 1:
                direction = -1
            rail += direction
        lengths = [pattern.count(r) for r in range(key)]
        idx = 0
        rows = []
        for l in lengths:
            rows.append(list(text[idx:idx+l]))
            idx += l
        result = []
        counters = [0] * key
        for r in pattern:
            result.append(rows[r][counters[r]])
            counters[r] += 1
        return ''.join(result)