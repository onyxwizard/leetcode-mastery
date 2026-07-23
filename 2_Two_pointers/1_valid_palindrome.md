### 📘 Chapter: Two Pointers  
### 📌 Problem 1: Valid Palindrome (LeetCode 125)

---

**Input**  
- `s`: a string containing printable ASCII characters.

**Output**  
- `true` if, after converting all uppercase to lowercase and removing all non-alphanumeric characters, the string reads the same forward and backward; otherwise `false`.

**Constraints**  
- `1 <= s.length <= 2 × 10⁵`  
- `s` consists only of printable ASCII characters.

**Example**  
```
Input:  s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Input:  s = "race a car"
Output: false
Explanation: "raceacar" is NOT a palindrome.

Input:  s = " "
Output: true
Explanation: After removing non-alphanumeric, s is an empty string "" → palindrome by definition.
```

**Follow-up**  
- None explicitly stated. (Common extensions: What if the string is a stream? What about Unicode?)

---

### 🧠 Core Idea

A palindrome check naturally suggests **two pointers** starting from the ends and moving inward. The twist: we must **ignore non-alphanumeric characters** and compare **case-insensitively**.

- **Brute force (filter first):** Build a cleaned lowercase string, then check palindrome. O(n) time, O(n) space.
- **Optimal (in-place two pointers):** Skip non-alphanumeric characters on the fly using `Character.isLetterOrDigit()`, compare using `Character.toLowerCase()`. O(n) time, **O(1) space**.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACHES

---

## 1A. Filter + Reverse Comparison (O(n) Time, O(n) Space)

**Idea:**  
1. Build a cleaned string: iterate through `s`, keep only alphanumeric characters, convert to lowercase.  
2. Reverse the cleaned string.  
3. Compare original cleaned string with its reverse.

**Time:** O(n) — one pass to filter + one pass to reverse + one pass to compare.  
**Space:** O(n) — storing the cleaned string and its reverse.

```java
public boolean isPalindrome(String s) {
    StringBuilder clean = new StringBuilder();
    for (char c : s.toCharArray()) {
        if (Character.isLetterOrDigit(c)) {
            clean.append(Character.toLowerCase(c));
        }
    }

    String original = clean.toString();
    String reversed = clean.reverse().toString();

    return original.equals(reversed);
}
```

### 🔍 Sample Iteration

**Input:** `s = "A man, a plan, a canal: Panama"`

**Step 1: Filter + Lowercase**

| Index | char | isLetterOrDigit? | Action | clean (so far) |
|-------|------|------------------|--------|----------------|
| 0 | 'A' | ✅ | append 'a' | "a" |
| 1 | ' ' | ❌ | skip | "a" |
| 2 | 'm' | ✅ | append 'm' | "am" |
| 3 | 'a' | ✅ | append 'a' | "ama" |
| 4 | 'n' | ✅ | append 'n' | "aman" |
| 5 | ',' | ❌ | skip | "aman" |
| 6 | ' ' | ❌ | skip | "aman" |
| 7 | 'a' | ✅ | append 'a' | "amana" |
| ... | ... | ... | ... | ... |
| 30 | 'a' | ✅ | append 'a' | "amanaplanacanalpanama" |

**Cleaned string:** `"amanaplanacanalpanama"` (length 21)

**Step 2: Reverse**  
`reversed = "amanaplanacanalpanama"`

**Step 3: Compare**  
`"amanaplanacanalpanama".equals("amanaplanacanalpanama")` → **true** ✅

---

**Non-palindrome example:** `s = "race a car"`

**Cleaned:** `"raceacar"` (length 8)  
**Reversed:** `"racaecar"`  

Wait, let me redo: `"raceacar"` reversed = `"raceacar"` → actually let me check character by character:

```
Original:  r a c e a c a r
Reversed:  r a c a e c a r
```

`"raceacar" ≠ "racaecar"` → **false** ✅

> ⚠️ This approach allocates **two** strings of length up to n. For n = 2×10⁵, that's ~400 KB of extra memory. Not terrible, but unnecessary.

---

## 1B. Filter + Two Pointers on Cleaned String (O(n) Time, O(n) Space)

**Idea:**  
1. Build the cleaned lowercase string (same as above).  
2. Use two pointers on the cleaned string: `left = 0`, `right = clean.length() - 1`.  
3. Compare characters at `left` and `right`; move inward.

**Time:** O(n).  
**Space:** O(n) — the cleaned string.

```java
public boolean isPalindrome(String s) {
    StringBuilder clean = new StringBuilder();
    for (char c : s.toCharArray()) {
        if (Character.isLetterOrDigit(c)) {
            clean.append(Character.toLowerCase(c));
        }
    }

    int left = 0, right = clean.length() - 1;
    while (left < right) {
        if (clean.charAt(left) != clean.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
```

### 🔍 Sample Iteration

**Input:** `s = "race a car"` → **Cleaned:** `"raceacar"`

| Step | left | right | clean[left] | clean[right] | Match? | Action |
|------|------|-------|-------------|--------------|--------|--------|
| 1 | 0 | 7 | 'r' | 'r' | ✅ | left++, right-- |
| 2 | 1 | 6 | 'a' | 'a' | ✅ | left++, right-- |
| 3 | 2 | 5 | 'c' | 'c' | ✅ | left++, right-- |
| 4 | 3 | 4 | **'e'** | **'a'** | ❌ | **RETURN FALSE** |

**Result:** `false` ✅

> 📌 We detected the mismatch at step 4 without checking all 8 characters. But we still paid O(n) space to build the cleaned string.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. In-Place Two Pointers (O(n) Time, O(1) Space)

**Idea:**  
Use two pointers **directly on the original string**. Skip non-alphanumeric characters on the fly. Compare case-insensitively. No extra string is ever created.

- `left = 0`, `right = s.length() - 1`.
- While `left < right`:
  - Advance `left` past non-alphanumeric characters.
  - Decrement `right` past non-alphanumeric characters.
  - Compare `toLowerCase(s[left])` with `toLowerCase(s[right])`.
  - If mismatch → return `false`.
  - Else → move both inward.

**Time:** O(n) — each character examined at most once.  
**Space:** O(1) — only two integer pointers.

```java
public boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;

    while (left < right) {
        // Skip non-alphanumeric from the left
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
            left++;
        }
        // Skip non-alphanumeric from the right
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
            right--;
        }

        // Compare case-insensitively
        if (Character.toLowerCase(s.charAt(left)) !=
            Character.toLowerCase(s.charAt(right))) {
            return false;
        }

        left++;
        right--;
    }

    return true;
}
```

### 🔍 Sample Iteration (Palindrome)

**Input:** `s = "A man, a plan, a canal: Panama"` (length 31)

```
Index: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
Char:  A  _  m  a  n  ,  _  a  _  p  l  a  n  ,  _  a  _  c  a  n  a  l  :  _  P  a  n  a  m  a
       (_ = space)
```

| Step | left | right | s[left] | s[right] | Skip? | Compare (lowercase) | Match? | Action |
|------|------|-------|---------|----------|-------|---------------------|--------|--------|
| 1 | 0 | 30 | 'A' | 'a' | No skip needed | 'a' vs 'a' | ✅ | left=1, right=29 |
| 2 | 1 | 29 | ' ' | 'm' | left skips ' ' → left=2 | 'm' vs 'm' | ✅ | left=3, right=28 |
| 3 | 3 | 28 | 'a' | 'a' | No skip | 'a' vs 'a' | ✅ | left=4, right=27 |
| 4 | 4 | 27 | 'n' | 'n' | No skip | 'n' vs 'n' | ✅ | left=5, right=26 |
| 5 | 5 | 26 | ',' | 'a' | left skips ',' → left=6; left skips ' ' → left=7 | 'a' vs 'a' | ✅ | left=8, right=25 |
| 6 | 8 | 25 | ' ' | 'P' | left skips ' ' → left=9 | 'p' vs 'p' | ✅ | left=10, right=24 |
| 7 | 10 | 24 | 'l' | 'a' | right skips ' ' → right=23; right skips ':' → right=22; right skips ' ' → right=21 | 'l' vs 'l' | ✅ | left=11, right=20 |
| 8 | 11 | 20 | 'a' | 'a' | No skip | 'a' vs 'a' | ✅ | left=12, right=19 |
| 9 | 12 | 19 | 'n' | 'n' | No skip | 'n' vs 'n' | ✅ | left=13, right=18 |
| 10 | 13 | 18 | ',' | 'a' | left skips ',' → 14; skips ' ' → 15 | 'a' vs 'a' | ✅ | left=16, right=17 |
| 11 | 16 | 17 | ' ' | 'c' | left skips ' ' → 17 | left ≥ right → **LOOP ENDS** | — | — |

**Result:** `true` ✅

> 📌 11 comparisons for a 31-character string. Non-alphanumeric characters (spaces, commas, colon) were **skipped on the fly** — never stored anywhere.

---

### 🔍 Sample Iteration (Non-Palindrome)

**Input:** `s = "race a car"` (length 10)

```
Index: 0  1  2  3  4  5  6  7  8  9
Char:  r  a  c  e  _  a  _  c  a  r
```

| Step | left | right | s[left] | s[right] | Skip? | Compare | Match? | Action |
|------|------|-------|---------|----------|-------|---------|--------|--------|
| 1 | 0 | 9 | 'r' | 'r' | No | 'r' vs 'r' | ✅ | left=1, right=8 |
| 2 | 1 | 8 | 'a' | 'a' | No | 'a' vs 'a' | ✅ | left=2, right=7 |
| 3 | 2 | 7 | 'c' | 'c' | No | 'c' vs 'c' | ✅ | left=3, right=6 |
| 4 | 3 | 6 | 'e' | ' ' | right skips ' ' → right=5 | 'e' vs 'a' | ❌ | **RETURN FALSE** |

**Result:** `false` ✅

> 📌 Mismatch detected at step 4. We only examined 8 out of 10 characters. The space at index 6 was skipped by the right pointer automatically.

---

### 🔍 Edge Case: All Non-Alphanumeric

**Input:** `s = " ,.:;"` (length 5)

| Step | left | right | Action |
|------|------|-------|--------|
| 1 | 0 | 4 | left skips ' ' → 1; skips ',' → 2; skips '.' → 3; skips ':' → 4; skips ';' → 5. Now left=5 ≥ right=4. **LOOP NEVER EXECUTES.** |

**Result:** `true` ✅ (empty cleaned string is a palindrome by definition)

---

### 🔍 Edge Case: Single Character

**Input:** `s = "a"`

| Step | left | right | Action |
|------|------|-------|--------|
| — | 0 | 0 | left < right? 0 < 0? **No.** Loop never executes. |

**Result:** `true` ✅

---

### 🔍 Visual Pointer Movement

```
s = "A man, a plan, a canal: Panama"

Step 1:  [A] man, a plan, a canal: Panam[a]   → 'a' == 'a' ✅
Step 2:  A [m]an, a plan, a canal: Pana[m]a   → 'm' == 'm' ✅
Step 3:  A m[a]n, a plan, a canal: Pan[a]ma   → 'a' == 'a' ✅
Step 4:  A ma[n], a plan, a canal: Pa[n]ama   → 'n' == 'n' ✅
Step 5:  A man[,] a plan, a canal: P[a]nama   → skip ',' and ' '
         A man, [a] plan, a canal: P[a]nama   → 'a' == 'a' ✅
Step 6:  A man, a[ ]plan, a canal: [P]anama   → skip ' '
         A man, a [p]lan, a canal: [P]anama   → 'p' == 'p' ✅
Step 7:  A man, a p[l]an, a canal[: ]Panama   → skip ':', ' '
         A man, a p[l]an, a cana[l]: Panama   → 'l' == 'l' ✅
...
         Pointers meet in the middle → DONE ✅
```

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Filter + Reverse vs Filter + Two Pointers vs In-Place Two Pointers

| Metric | Filter + Reverse | Filter + Two Pointers | In-Place Two Pointers |
|--------|-----------------|----------------------|----------------------|
| Time | O(n) | O(n) | O(n) |
| Space | O(n) — cleaned + reversed strings | O(n) — cleaned string | **O(1)** |
| Allocations | 2 StringBuilder/String objects | 1 StringBuilder object | **Zero** |
| Code clarity | Very simple | Simple | Moderate (skip logic) |
| Early termination? | ❌ (must build full string first) | ✅ (can stop at first mismatch) | ✅ (can stop at first mismatch) |
| Handles large input (2×10⁵)? | ✅ but wasteful | ✅ but wasteful | ✅ **optimal** |

---

## Filter Approaches vs In-Place (Head-to-Head)

| Metric | Filter (any variant) | In-Place Two Pointers |
|--------|---------------------|----------------------|
| Extra memory | O(n) — up to 200 KB for n=2×10⁵ | **O(1)** — two integers |
| GC pressure | Creates StringBuilder + String objects | **Zero** object creation |
| Readability | Slightly easier (cleaned string is explicit) | Requires understanding skip logic |
| Interview value | Acceptable baseline | **Expected optimal answer** |
| Bug risk | Low | Low (but must handle `left < right` in skip loops) |

**Verdict:** In-place two pointers is the **gold standard** for this problem. The filter approach is a valid first step to show understanding, then optimize to O(1) space.

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Early Exit? | Key Insight |
|----------|------|-------|-------------|-------------|
| Filter + Reverse | O(n) | O(n) | ❌ | Build clean string, compare with reverse |
| Filter + Two Pointers | O(n) | O(n) | ✅ | Build clean string, two-pointer check |
| **In-Place Two Pointers** | **O(n)** | **O(1)** | **✅** | **Skip non-alnum on the fly, compare lowercase** |

---

### 🎯 What to Present to the Interviewer

1. **Recognise** this as a palindrome check → two pointers from both ends.
2. **Mention the filter approach** as a quick baseline: build cleaned lowercase string, then check palindrome. O(n) time, O(n) space.
3. **Optimize to in-place:** "We don't actually need to build the cleaned string. We can skip non-alphanumeric characters on the fly using `Character.isLetterOrDigit()` and compare using `Character.toLowerCase()`."
4. **Write the code** with two while-loops for skipping and one comparison.
5. **Walk through** the example `"A man, a plan, a canal: Panama"`:
   - Pointers start at 'A' and 'a' → match.
   - Left skips space, right skips nothing → 'm' vs 'm' → match.
   - Continue inward, skipping commas, spaces, colon.
   - Pointers meet → return true.
6. **Highlight O(1) space:** No extra string, no StringBuilder, no array. Just two integer pointers.
7. **Mention edge cases:** Empty/all-punctuation string → true. Single character → true. Case insensitivity handled by `toLowerCase`.
8. **Be ready** to discuss `Character.isLetterOrDigit()` (checks Unicode letters and digits) and `Character.toLowerCase()` (handles ASCII and beyond).

**One‑sentence summary:**  
*Use two pointers on the original string, skipping non-alphanumeric characters on the fly and comparing lowercase values, achieving O(n) time and O(1) space — no extra string allocation needed.*