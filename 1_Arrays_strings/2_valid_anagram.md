### 📘 Chapter: Arrays & Strings  
### 📌 Problem 2: Valid Anagram (LeetCode 242)

---

**Input**  
- `s`, `t`: two strings

**Output**  
- `true` if `t` is an anagram of `s`, `false` otherwise

**Constraints**  
- `1 <= s.length, t.length <= 5 * 10⁴`  
- `s` and `t` consist of lowercase English letters only (for the base problem)

**Follow-up**  
- What if the inputs contain Unicode characters? How would you adapt your solution?

---

### 🧠 Why this Data Structure?

We need to check if two strings have identical character frequencies. The core operation is **frequency counting**.

- **Array of size 26** (for lowercase letters):  
  - Direct mapping `char - 'a'` gives O(1) indexing.  
  - Time O(n), Space O(1) – the array size is fixed.

- **HashMap** (for Unicode follow‑up):  
  - Handles any character set.  
  - O(1) average for `get`/`put`.  
  - Space O(k), where k is number of distinct characters (worst case O(n)).  

Sorting is also possible but slower. The frequency‑based approaches directly address the problem with optimal time.

---

### 🔨 Brute Force Approach (Sorting)

**Method:**  
Convert both strings to character arrays, sort them, then compare equality.  
Anagrams produce the same sorted sequence.

**Time:** O(n log n) – sorting dominates  
**Space:** O(n) – `toCharArray()` creates copies

```java
import java.util.Arrays;

public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    char[] sArr = s.toCharArray();
    char[] tArr = t.toCharArray();
    Arrays.sort(sArr);
    Arrays.sort(tArr);
    return Arrays.equals(sArr, tArr);
}
```

---

### ⚡ Optimized Approach (Frequency Array – One Pass with Early Exit)

**Method:**  
Use an integer array of size 26 to count occurrences in `s`.  
Then iterate over `t`, decrementing counts. If any count goes negative, `t` has an extra character ⇒ `false`.  
Because lengths are equal, no need for a final check.

**Time:** O(n) – two linear passes  
**Space:** O(1) – fixed array of size 26

```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] count = new int[26];
    for (char c : s.toCharArray()) {
        count[c - 'a']++;
    }
    for (char c : t.toCharArray()) {
        if (--count[c - 'a'] < 0) return false;
    }
    return true;
}
```

---

### 🌍 Follow‑up: Handling Unicode Characters

**Adaptation:** Replace the fixed array with a `HashMap<Character, Integer>`.  
- Works for any character set, including Unicode.  
- Same O(n) time, but space is O(k) where k is the number of distinct characters.

```java
import java.util.HashMap;
import java.util.Map;

public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    Map<Character, Integer> freq = new HashMap<>();
    for (char c : s.toCharArray()) {
        freq.put(c, freq.getOrDefault(c, 0) + 1);
    }
    for (char c : t.toCharArray()) {
        int count = freq.getOrDefault(c, 0);
        if (count == 0) return false;
        freq.put(c, count - 1);
    }
    return true;
}
```

---

### 📊 Solution Comparison & Trade-offs

| Solution              | Time      | Space    | Suitable for                     |
|-----------------------|-----------|----------|----------------------------------|
| Sorting               | O(n log n)| O(n)     | Simple, readable; good for small strings or if sorting is allowed. |
| Frequency array (26)  | O(n)      | O(1)     | **Best for ASCII lowercase** letters (the problem’s original constraints). |
| HashMap (Unicode)     | O(n)      | O(k)     | **Only when character set is large/unknown** (follow‑up). Adds overhead. |

**Trade‑off:**  
- Sorting gives clean code but is slower.  
- Frequency array is fastest and space‑efficient but only works for limited alphabets.  
- HashMap generalizes to Unicode at the cost of higher constant factors and space.

---

### 🎯 What to Present to the Interviewer

- Start by verifying lengths are equal; if not, return `false` immediately.  
- Propose the **frequency array** for O(n) time and O(1) space, leveraging the lowercase constraint.  
- Mention the sorting alternative as a fallback but explain its O(n log n) limitation.  
- For the follow‑up, switch to a `HashMap` to support Unicode characters while preserving O(n) time.  
- Emphasize that the frequency‑counting approach is linear and therefore optimal for this problem.

**One‑sentence summary:**  
*Count character frequencies with an array (or HashMap for Unicode) in O(n) time – anagrams must have identical counts.*