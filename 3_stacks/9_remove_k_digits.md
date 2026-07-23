### 📘 Chapter: Stack  
### 📌 Problem 9: Remove K Digits (LeetCode 402)

---

**Input**  
- `num`: a string representing a non-negative integer (digits only, no leading zeros except "0" itself).  
- `k`: an integer — the number of digits to remove.

**Output**  
- The **smallest possible integer** (as a string) after removing exactly `k` digits from `num`.  
- Result must not contain leading zeros (except "0" itself).

**Constraints**  
- `1 <= k <= num.length <= 10⁵`  
- `num` consists of only digits `'0'`–`'9'`.  
- `num` has no leading zeros (except for "0" itself).

**Example**  
```
Input:  num = "1432219", k = 3
Output: "1219"
Explanation: Remove '4', '3', '2' (the peaks) → "1219" is the smallest.

Input:  num = "10200", k = 1
Output: "200"
Explanation: Remove '1' → "0200" → strip leading zero → "200".

Input:  num = "10", k = 2
Output: "0"
Explanation: Remove both digits → "" → "0".

Input:  num = "1234567890", k = 9
Output: "0"
Explanation: Keep only '0' → "0".
```

**Follow-up**  
- Achieve O(n) time and O(n) space. (Standard expectation.)

---

### 🧠 Core Idea

To make the number as **small as possible**, we want the **leftmost (most significant) digits** to be as small as possible.

**Greedy insight:**  
If a digit is **larger** than the digit immediately after it, removing the larger digit reduces the number more than removing any digit further right. We should remove such "peaks" greedily from left to right.

```
Example: "1432219", k=3
          ↑
          4 > 3 → remove 4 (reduces the number more than removing 3)
Result:  "132219", k=2
           ↑
           3 > 2 → remove 3
Result:  "12219", k=1
            ↑
            2 > 1? No... but 2 > 1 at position 3 → remove the 2
Result:  "1219", k=0 ✅
```

**Data structure:** A **monotonic increasing stack** naturally implements this:
- Scan digits left to right.
- While the stack top > current digit AND we still have removals (`k > 0`): **pop** (remove the peak).
- Push the current digit.
- If `k` remains after scanning: remove from the **end** (least significant digits are largest in an increasing sequence).

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Backtracking — Generate All Subsequences of Length (n-k) (Exponential)

**Idea:** Try all C(n, n-k) = C(n, k) ways to keep `n-k` digits. For each subsequence, compute its numeric value. Return the minimum.

**Time:** O(C(n, k) × n) — exponential in the worst case.  
**Space:** O(n) — recursion depth + StringBuilder.  
❌ Completely infeasible for n = 10⁵.

```java
// Conceptual pseudo-code (NOT practical)
String result = null;

public String removeKdigits(String num, int k) {
    int keep = num.length() - k;
    generate(num, 0, keep, new StringBuilder());
    return result == null ? "0" : result;
}

private void generate(String num, int idx, int remaining, StringBuilder sb) {
    if (remaining == 0) {
        String candidate = stripLeadingZeros(sb.toString());
        if (result == null || compare(candidate, result) < 0) {
            result = candidate;
        }
        return;
    }
    if (idx == num.length()) return;
    if (num.length() - idx < remaining) return; // not enough digits left

    // Option 1: KEEP this digit
    sb.append(num.charAt(idx));
    generate(num, idx + 1, remaining - 1, sb);
    sb.deleteCharAt(sb.length() - 1);

    // Option 2: SKIP this digit
    generate(num, idx + 1, remaining, sb);
}
```

### 🔍 Sample Iteration (Tiny Example)

**Input:** `num = "143", k = 1` → keep 2 digits. C(3,2) = 3 possibilities.

| Subsequence | Value | Minimum? |
|-------------|-------|----------|
| "14" (keep indices 0,1) | 14 | — |
| "13" (keep indices 0,2) | **13** | ✅ Current min |
| "43" (keep indices 1,2) | 43 | — |

**Result:** `"13"` ✅

> ⚠️ For n = 10⁵, k = 5×10⁴: C(100000, 50000) ≈ 10³⁰⁰⁰⁰. **Astronomically infeasible.**

---

## 1B. Greedy — Remove One Digit at a Time (O(n × k))

**Idea:** Repeat `k` times: scan the number left-to-right, find the first digit that is greater than its right neighbor, and remove it. If no such digit exists (number is non-decreasing), remove the last digit.

**Time:** O(n × k) — k passes, each scanning up to n digits.  
**Space:** O(n) — mutable string.

```java
public String removeKdigits(String num, int k) {
    StringBuilder sb = new StringBuilder(num);

    for (int removal = 0; removal < k; removal++) {
        int i = 0;
        // Find first digit greater than its right neighbor
        while (i < sb.length() - 1 && sb.charAt(i) <= sb.charAt(i + 1)) {
            i++;
        }
        sb.deleteCharAt(i);  // remove the peak (or last digit if non-decreasing)
    }

    // Strip leading zeros
    int start = 0;
    while (start < sb.length() && sb.charAt(start) == '0') start++;
    return (start == sb.length()) ? "0" : sb.substring(start);
}
```

### 🔍 Sample Iteration

**Input:** `num = "1432219", k = 3`

| Removal | sb (before) | Scan: first i where sb[i] > sb[i+1] | Remove | sb (after) |
|---------|-------------|--------------------------------------|--------|-----------|
| 1 | `"1432219"` | i=1: '4' > '3' ✅ | Remove '4' | `"132219"` |
| 2 | `"132219"` | i=1: '3' > '2' ✅ | Remove '3' | `"12219"` |
| 3 | `"12219"` | i=2: '2' > '1' ✅ | Remove '2' | `"1219"` |

**Result:** `"1219"` ✅

> ⚠️ For n = 10⁵, k = 5×10⁴: ~5×10⁹ operations. **Too slow.** The monotonic stack does it in a single O(n) pass.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. Greedy Monotonic Stack — Deque (O(n) Time, O(n) Space) ✅

**Idea:**  
- Use a `Deque<Character>` as a **monotonic increasing stack**.  
- For each digit `c` in `num`:  
  - While stack is not empty AND `k > 0` AND `stack.peek() > c`: **pop** (remove the larger digit).  
  - Push `c`.  
- After processing all digits: if `k > 0` remains, pop `k` more from the top (remove trailing largest digits).  
- Build result from bottom-to-top. Strip leading zeros.

**Time:** O(n) — each digit pushed once, popped at most once.  
**Space:** O(n) — stack holds up to n digits.

```java
import java.util.*;

public String removeKdigits(String num, int k) {
    Deque<Character> stack = new ArrayDeque<>();

    for (char c : num.toCharArray()) {
        // Remove larger digits from the top while we can
        while (!stack.isEmpty() && k > 0 && stack.peek() > c) {
            stack.pop();
            k--;
        }
        stack.push(c);
    }

    // If k removals remain, remove from the end (largest digits in increasing stack)
    while (k-- > 0 && !stack.isEmpty()) {
        stack.pop();
    }

    // Build result from bottom to top
    StringBuilder sb = new StringBuilder();
    while (!stack.isEmpty()) {
        sb.append(stack.removeLast());  // bottom of stack = leftmost digit
    }

    // Strip leading zeros
    int start = 0;
    while (start < sb.length() && sb.charAt(start) == '0') start++;

    return (start == sb.length()) ? "0" : sb.substring(start);
}
```

### 🔍 Sample Iteration

**Input:** `num = "1432219", k = 3`

| Step | Digit | Stack BEFORE (top→bottom) | k | Action | Stack AFTER | k after |
|------|-------|---------------------------|---|--------|-------------|---------|
| 1 | '1' | `[]` | 3 | Stack empty → push '1' | `[1]` | 3 |
| 2 | '4' | `[1]` | 3 | Top='1' > '4'? No → push '4' | `[4, 1]` | 3 |
| 3 | '3' | `[4, 1]` | 3 | Top='4' > '3'? **Yes** → pop '4', k=2. Top='1' > '3'? No → push '3' | `[3, 1]` | 2 |
| 4 | '2' | `[3, 1]` | 2 | Top='3' > '2'? **Yes** → pop '3', k=1. Top='1' > '2'? No → push '2' | `[2, 1]` | 1 |
| 5 | '2' | `[2, 1]` | 1 | Top='2' > '2'? No → push '2' | `[2, 2, 1]` | 1 |
| 6 | '1' | `[2, 2, 1]` | 1 | Top='2' > '1'? **Yes** → pop '2', k=0. k=0 → stop while. Push '1' | `[1, 2, 1]` | 0 |
| 7 | '9' | `[1, 2, 1]` | 0 | k=0 → no popping. Push '9' | `[9, 1, 2, 1]` | 0 |

**After loop:** k=0, no more removals needed.  
**Build result (bottom→top):** `"1219"`  
**Strip leading zeros:** none.  
**Result:** `"1219"` ✅

---

### 🔍 Visual Stack Trace

```
num = "1432219", k = 3

Step 1: '1' → push
  ┌───┐
  │ 1 │
  └───┘

Step 2: '4' → 1 < 4, push
  ┌───┐
  │ 4 │ ← top
  ├───┤
  │ 1 │
  └───┘

Step 3: '3' → 4 > 3 → POP 4 (k=2). 1 < 3, push 3.
  ┌───┐
  │ 3 │ ← top
  ├───┤
  │ 1 │
  └───┘

Step 4: '2' → 3 > 2 → POP 3 (k=1). 1 < 2, push 2.
  ┌───┐
  │ 2 │ ← top
  ├───┤
  │ 1 │
  └───┘

Step 5: '2' → 2 ≤ 2, push
  ┌───┐
  │ 2 │ ← top
  ├───┤
  │ 2 │
  ├───┤
  │ 1 │
  └───┘

Step 6: '1' → 2 > 1 → POP 2 (k=0). k=0, stop. Push 1.
  ┌───┐
  │ 1 │ ← top
  ├───┤
  │ 2 │
  ├───┤
  │ 1 │
  └───┘

Step 7: '9' → k=0, just push.
  ┌───┐
  │ 9 │ ← top
  ├───┤
  │ 1 │
  ├───┤
  │ 2 │
  ├───┤
  │ 1 │
  └───┘

Result (bottom→top): 1, 2, 1, 9 → "1219" ✅
```

---

### 🔍 Sample Iteration 2 (Leading Zeros)

**Input:** `num = "10200", k = 1`

| Step | Digit | Stack (top→bottom) | k | Action |
|------|-------|--------------------|---|--------|
| 1 | '1' | `[1]` | 1 | Push |
| 2 | '0' | `[1]` | 1 | '1' > '0' → **pop '1'**, k=0. Push '0'. → `[0]` |
| 3 | '2' | `[0]` | 0 | k=0, push '2' → `[2, 0]` |
| 4 | '0' | `[2, 0]` | 0 | k=0, push '0' → `[0, 2, 0]` |
| 5 | '0' | `[0, 2, 0]` | 0 | k=0, push '0' → `[0, 0, 2, 0]` |

**Build result:** `"0200"`  
**Strip leading zeros:** `"200"`  
**Result:** `"200"` ✅

---

### 🔍 Sample Iteration 3 (All Removed)

**Input:** `num = "10", k = 2`

| Step | Digit | Stack | k | Action |
|------|-------|-------|---|--------|
| 1 | '1' | `[1]` | 2 | Push |
| 2 | '0' | `[1]` | 2 | '1' > '0' → pop '1', k=1. Push '0'. → `[0]` |
| END | — | `[0]` | 1 | k=1 > 0 → pop '0', k=0. Stack: `[]` |

**Build result:** `""` (empty)  
**Return:** `"0"` ✅

---

### 🔍 Sample Iteration 4 (k Remaining After Scan — Remove from End)

**Input:** `num = "12345", k = 3`

| Step | Digit | Stack (top→bottom) | k | Action |
|------|-------|--------------------|---|--------|
| 1 | '1' | `[1]` | 3 | Push (no pop: stack empty) |
| 2 | '2' | `[2, 1]` | 3 | '1' > '2'? No → push |
| 3 | '3' | `[3, 2, 1]` | 3 | '2' > '3'? No → push |
| 4 | '4' | `[4, 3, 2, 1]` | 3 | '3' > '4'? No → push |
| 5 | '5' | `[5, 4, 3, 2, 1]` | 3 | '4' > '5'? No → push |

**After loop:** k=3 still remaining! Stack is `[5,4,3,2,1]` (monotonic increasing bottom→top).  
**Remove k=3 from top:** pop '5', pop '4', pop '3'. Stack: `[2, 1]`.  
**Build result:** `"12"`  
**Result:** `"12"` ✅

> 📌 When the number is already non-decreasing (no peaks), the greedy can't remove anything during the scan. The remaining removals take from the **end** (least significant = largest digits in the increasing stack).

---

### 🔍 Sample Iteration 5 (Complex)

**Input:** `num = "1234567890", k = 9`

| Step | Digit | Stack (top→bottom) | k | Action |
|------|-------|--------------------|----|--------|
| 1 | '1' | `[1]` | 9 | Push |
| 2 | '2' | `[2,1]` | 9 | Push |
| 3 | '3' | `[3,2,1]` | 9 | Push |
| 4 | '4' | `[4,3,2,1]` | 9 | Push |
| 5 | '5' | `[5,4,3,2,1]` | 9 | Push |
| 6 | '6' | `[6,5,4,3,2,1]` | 9 | Push |
| 7 | '7' | `[7,6,5,4,3,2,1]` | 9 | Push |
| 8 | '8' | `[8,7,6,5,4,3,2,1]` | 9 | Push |
| 9 | '9' | `[9,8,7,6,5,4,3,2,1]` | 9 | Push |
| 10 | '0' | `[9,...,1]` | 9 | '9'>'0'→pop,k=8. '8'>'0'→pop,k=7. ... '1'>'0'→pop,k=0. Push '0'. | `[0]` |

**After loop:** k=0. Stack: `[0]`.  
**Build result:** `"0"`  
**Strip leading zeros:** empty → return `"0"` ✅

---

## 2B. StringBuilder as Stack (Simpler Variant, O(n) Time, O(n) Space)

**Idea:** Same algorithm, but use a `StringBuilder` where the **end** is the top of the stack. Avoids explicit `Deque` and simplifies result construction.

```java
public String removeKdigits(String num, int k) {
    StringBuilder sb = new StringBuilder();  // acts as stack (top = end)

    for (char c : num.toCharArray()) {
        // Remove larger digits from the "top" (end of sb)
        while (sb.length() > 0 && k > 0 && sb.charAt(sb.length() - 1) > c) {
            sb.deleteCharAt(sb.length() - 1);
            k--;
        }
        sb.append(c);
    }

    // Remove remaining k digits from the end
    while (k-- > 0 && sb.length() > 0) {
        sb.deleteCharAt(sb.length() - 1);
    }

    // Strip leading zeros
    int start = 0;
    while (start < sb.length() && sb.charAt(start) == '0') start++;

    return (start == sb.length()) ? "0" : sb.substring(start);
}
```

### 🔍 Sample Iteration (Same Example)

**Input:** `num = "1432219", k = 3`

| Step | c | sb (before) | k | Condition: last > c? | Action | sb (after) | k |
|------|---|-------------|---|---------------------|--------|-----------|---|
| 1 | '1' | `""` | 3 | (empty) | Append '1' | `"1"` | 3 |
| 2 | '4' | `"1"` | 3 | '1'>'4'? No | Append '4' | `"14"` | 3 |
| 3 | '3' | `"14"` | 3 | '4'>'3'? **Yes** | Delete '4', k=2. '1'>'3'? No. Append '3'. | `"13"` | 2 |
| 4 | '2' | `"13"` | 2 | '3'>'2'? **Yes** | Delete '3', k=1. '1'>'2'? No. Append '2'. | `"12"` | 1 |
| 5 | '2' | `"12"` | 1 | '2'>'2'? No | Append '2' | `"122"` | 1 |
| 6 | '1' | `"122"` | 1 | '2'>'1'? **Yes** | Delete '2', k=0. Stop. Append '1'. | `"121"` | 0 |
| 7 | '9' | `"121"` | 0 | k=0 | Append '9' | `"1219"` | 0 |

**Strip leading zeros:** none.  
**Result:** `"1219"` ✅

> 📌 The StringBuilder IS the result — no need to build from a separate stack. Cleaner and more memory-efficient (no boxing of `Character` objects).

---

### 🔍 Why the Greedy is Correct (Proof Sketch)

```
Claim: Removing the leftmost "peak" (digit > its right neighbor) is always optimal.

Proof by contradiction:
  Suppose the optimal solution does NOT remove the leftmost peak at position i
  (where num[i] > num[i+1]).
  
  Then the optimal keeps num[i] and removes some other digit.
  
  Consider the result: at position i, it has num[i] (the larger digit).
  If instead we remove num[i] and keep num[i+1] (the smaller digit),
  the resulting number is SMALLER (because position i is more significant
  than any position where the other removal happened).
  
  Contradiction: the "optimal" solution wasn't optimal.
  
  ∴ Removing the leftmost peak is always at least as good as any other choice. ∎
```

---

### 🔍 Amortized O(n) Analysis

```
Each digit is:
  - APPENDED to the stack/SB exactly once → n appends total.
  - DELETED from the stack/SB at most once → at most n deletes total.

Total operations: n appends + n deletes = 2n → O(n).

The while loop inside the for loop may seem expensive, but across ALL iterations,
the total number of pops/deletes is bounded by n (you can't pop more than you pushed).
```

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Greedy One-at-a-Time vs Monotonic Stack

| Metric | Backtracking | Greedy (one removal at a time) | Monotonic Stack |
|--------|-------------|-------------------------------|-----------------|
| Time | O(C(n,k) × n) — exponential | O(n × k) | **O(n)** |
| For n=10⁵, k=5×10⁴ | ~10³⁰⁰⁰⁰ ❌ | ~5×10⁹ ❌ | ~2×10⁵ ✅ |
| Space | O(n) | O(n) | **O(n)** |
| Correctness | ✅ (exhaustive) | ✅ (greedy proof) | **✅ (same greedy, single pass)** |
| Code complexity | High (recursion) | Moderate (nested loop) | **Simple (one loop + while)** |

---

## Deque vs StringBuilder (Head-to-Head)

| Metric | Deque<Character> | StringBuilder |
|--------|-----------------|---------------|
| Time | O(n) | O(n) |
| Space | O(n) + Character boxing overhead | **O(n) — primitive char array** |
| Result construction | Need to read bottom-to-top | **Already in correct order** |
| Code clarity | Explicit stack semantics | Slightly less obvious (end = top) |
| Performance | Slower (object boxing) | **Faster (no boxing)** |
| Interview preference | Shows "stack" thinking | **Preferred for conciseness** |

**Verdict:** StringBuilder is the production-optimal choice. Deque is more explicit about the "stack" pattern. Both are O(n). Present StringBuilder for code, mention Deque for conceptual clarity.

---

## Edge Cases Summary

| Case | Input | Output | Why |
|------|-------|--------|-----|
| Remove all digits | `"10", k=2` | `"0"` | Empty result → "0" |
| Leading zeros after removal | `"10200", k=1` | `"200"` | Strip leading '0' |
| Already smallest (non-decreasing) | `"12345", k=3` | `"12"` | Remove from end |
| All same digits | `"1111", k=2` | `"11"` | No peaks; remove from end |
| Single digit remains | `"1234567890", k=9` | `"0"` | Only '0' left |
| k = 0 (not in constraints but defensive) | `"123", k=0` | `"123"` | No removals |

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Practical (n=10⁵)? | Key Insight |
|----------|------|-------|--------------------|----|
| Backtracking | Exponential | O(n) | ❌ Never | Try all C(n,k) subsequences |
| Greedy (one at a time) | O(n×k) | O(n) | ❌ Too slow | Remove leftmost peak, repeat k times |
| **Monotonic Stack (Deque)** | **O(n)** | **O(n)** | **✅** | **Pop larger digits in one pass** |
| **Monotonic Stack (StringBuilder)** | **O(n)** | **O(n)** | **✅** | **Same logic, no boxing, cleaner output** |

---

### 🎯 What to Present to the Interviewer

1. **Explain the greedy intuition:** "To minimize the number, we want the leftmost digits to be as small as possible. If a digit is larger than the one after it, removing it reduces the number more than removing anything to its right."
2. **Introduce the monotonic increasing stack:**
   - "Scan left to right. While the stack top is greater than the current digit and we have removals left, pop the stack (remove the peak)."
   - "This ensures the stack is always non-decreasing — the smallest possible prefix."
3. **Walk through** `"1432219", k=3`:
   - Push '1', push '4'. See '3': 4>3, pop 4 (k=2). Push '3'.
   - See '2': 3>2, pop 3 (k=1). Push '2'.
   - See '2': 2≤2, push. See '1': 2>1, pop 2 (k=0). Push '1'.
   - See '9': k=0, push.
   - Result: "1219".
4. **Handle remaining k:** "If the number was non-decreasing (no peaks), k removals remain. Remove from the end (least significant = largest in the increasing stack)."
5. **Handle leading zeros:** "Strip them. If result is empty, return '0'."
6. **Write the StringBuilder version** for conciseness.
7. **State complexity:** O(n) time (amortized — each digit pushed/popped once), O(n) space.
8. **If asked to prove correctness:** "Removing the leftmost peak is always optimal by exchange argument: keeping a larger digit in a more significant position is always worse than replacing it with the smaller digit to its right."

**One‑sentence summary:**  
*Use a monotonic increasing stack (greedy): scan digits left to right, popping any digit larger than the current one while removals remain, ensuring the smallest possible number after exactly k deletions in O(n) time.*