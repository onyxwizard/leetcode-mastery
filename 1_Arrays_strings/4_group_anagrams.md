### 📘 Chapter: Arrays & Strings  
### 📌 Problem 4: Group Anagrams (LeetCode 49)

---

**Input**  
- `strs`: an array of strings

**Output**  
- A list of lists, where each inner list contains all strings that are anagrams of each other. Order of groups and order within groups does not matter.

**Constraints**  
- `1 <= strs.length <= 10⁴`  
- `0 <= strs[i].length <= 100`  
- Strings contain only lowercase English letters.

**Follow-up**  
- Not explicitly given in the problem.

---

### 🧠 Why this Data Structure?

**HashMap** (`java.util.HashMap<String, List<String>>`)  
The core task is to group strings that have identical character frequencies. A **hash map** lets us use a canonical representation of the anagram (key) and collect all matching strings (value).  

- **Key generation**: Two common approaches:  
  1. **Sorted string**: Sort the characters of the string → anagrams produce the same sorted string.  
     - Time per string: O(k log k) (k = string length, max 100).  
     - Simple and readable.  
  2. **Frequency string/code**: Build a string like `"1#2#0...#"` from the character counts of 'a' to 'z'.  
     - Time per string: O(k) — no sorting needed.  
     - Slightly more code, but faster asymptotically (though not noticeable for k ≤ 100).  

- Both approaches provide O(n * (k log k)) or O(n * k) total time.  
- The hash map groups them in **O(1)** average insert time per string.

For interviews, the **sorted‑string key** is the most common and perfectly acceptable given the constraints.

---

### 🔨 Brute Force Approach

**Method:**  
Compare each string with every other string. For each pair, check if they are anagrams (by sorting both or counting). Use a boolean array to mark already‑grouped strings.

**Time:** O(n² * k log k) — comparing all pairs with sorting each time  
**Space:** O(n) for visited flags + temporary storage

```java
// Pseudo-approach – not recommended for implementation
for i from 0 to n-1:
    if visited[i]: continue
    create new group with strs[i]
    for j from i+1 to n-1:
        if not visited[j] and areAnagrams(strs[i], strs[j]):
            add strs[j] to group, visited[j]=true
```

---

### ⚡ Optimized Approach 1 – HashMap with Sorted Key

**Method:**  
- Iterate over `strs`.  
- For each string, convert to char array, sort it, build a key string.  
- Use `map.computeIfAbsent(key, k -> new ArrayList<>()).add(str)`.  
- Return `new ArrayList<>(map.values())`.

**Time:** O(n * k log k) — sorting each string of max length 100.  
**Space:** O(n * k) — storing all strings in the map.

```java
import java.util.*;

public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String str : strs) {
        char[] chars = str.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(str);
    }
    return new ArrayList<>(map.values());
}
```

---

### ⚡ Optimized Approach 2 – HashMap with Frequency Key (No Sorting)

**Method:**  
- For each string, build a frequency array of size 26.  
- Convert to a string key (e.g., `"1,2,0,…"`) or use a `StringBuilder` with delimiters.  
- Group as before.

**Time:** O(n * k) — no sorting, just counting.  
**Space:** O(n * k) — same as above.

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String str : strs) {
        int[] count = new int[26];
        for (char c : str.toCharArray()) {
            count[c - 'a']++;
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 26; i++) {
            sb.append('#').append(count[i]); // delimiter avoids ambiguity
        }
        String key = sb.toString();
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(str);
    }
    return new ArrayList<>(map.values());
}
```

---

### 📊 Solution Comparison & Trade-offs

| Solution                | Time       | Space   | Notes |
|-------------------------|------------|---------|-------|
| Brute force (pairwise)  | O(n²·k log k) | O(n)    | Impractical for n=10⁴. |
| HashMap + Sorted key    | O(n·k log k)  | O(n·k)  | **Easiest to implement**, perfectly fine for k ≤ 100. |
| HashMap + Frequency key | O(n·k)        | O(n·k)  | Faster in theory, avoids sorting. Slightly more code. |

**Trade‑off:**  
- For `k ≤ 100`, the `log k` factor is tiny (≈7), so both are fast.  
- The sorted‑string key is simpler and more readable; frequency‑count key is a micro‑optimization that shines for very long strings.  
- In interviews, the sorted‑key version is almost always enough, but mentioning the count‑based alternative shows deeper understanding.

---

### 🎯 What to Present to the Interviewer

- Clarify the definition of an anagram: same character frequencies.  
- Propose a **HashMap** to group by a canonical key.  
- Start with the **sorted‑string key** as the primary solution — clean and easy to explain.  
- Walk through the code.  
- Then, mention the alternative frequency‑count key that runs in O(n·k) time, and explain the trade‑off.  
- Emphasize that both are linear in `n` (the number of strings) with respect to the constant‑sized alphabet.

**One‑sentence summary:**  
*Use a HashMap with a canonical key (sorted string or frequency string) to collect anagrams together in O(n·k) or O(n·k log k) time.*