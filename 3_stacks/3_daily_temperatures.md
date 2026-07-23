### 📘 Chapter: Stack  
### 📌 Problem 3: Daily Temperatures (LeetCode 739)

---

**Input**  
- `temperatures`: integer array of daily temperatures.

**Output**  
- `answer[i]`: number of days you have to wait **after** day `i` to get a warmer temperature.  
- If there is no future warmer day, `answer[i] = 0`.

**Constraints**  
- `1 <= temperatures.length <= 10⁵`  
- `30 <= temperatures[i] <= 100`

**Example**  
```
Input:  temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1, 1, 4, 2, 1, 1, 0, 0]

Input:  temperatures = [30, 40, 50, 60]
Output: [1, 1, 1, 0]

Input:  temperatures = [30, 60, 90]
Output: [1, 1, 0]
```

**Follow‑up**  
- The problem's natural follow‑up is **space optimization**: can you solve it with **O(1) extra space** (or very little extra memory) by exploiting the limited temperature range [30, 100]?

---

### 🧠 Core Idea

We need the **first greater element to the right** for every index.

- **Brute force:** For each day, scan forward until a warmer day is found. O(n²) — too slow for n = 10⁵.
- **Monotonic Stack (optimal):** Maintain a stack of indices with **decreasing** temperatures. When a warmer day arrives, it **resolves** all colder days below it in one sweep. O(n) time, O(n) space.
- **Reverse Traversal + Next Array (space-optimal):** Exploit the bounded range [30, 100]. Traverse right-to-left, maintaining the earliest index for each temperature. O(n × 70) ≈ O(n) time, O(1) extra space.

---

---

# 🔄 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Brute Force (Nested Loops)

**Idea:** For each day `i`, scan forward day by day until finding the first `j > i` where `temperatures[j] > temperatures[i]`. Set `answer[i] = j - i`. If none found, `answer[i] = 0`.

**Time:** O(n²) — worst case (strictly descending temps), every element scans to the end.  
**Space:** O(1) — only the output array (required, not counted as extra).

```java
public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (temperatures[j] > temperatures[i]) {
                answer[i] = j - i;
                break;
            }
        }
        // if no warmer day found, answer[i] stays 0 (default)
    }

    return answer;
}
```

### 🔍 Sample Iteration

**Input:** `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`

| i | temp[i] | Inner loop (j scans forward) | First warmer day | answer[i] |
|---|---------|------------------------------|------------------|-----------|
| 0 | 73 | j=1: 74 > 73 ✅ | j=1 | 1−0 = **1** |
| 1 | 74 | j=2: 75 > 74 ✅ | j=2 | 2−1 = **1** |
| 2 | 75 | j=3: 71 ✗, j=4: 69 ✗, j=5: 72 ✗, j=6: 76 > 75 ✅ | j=6 | 6−2 = **4** |
| 3 | 71 | j=4: 69 ✗, j=5: 72 > 71 ✅ | j=5 | 5−3 = **2** |
| 4 | 69 | j=5: 72 > 69 ✅ | j=5 | 5−4 = **1** |
| 5 | 72 | j=6: 76 > 72 ✅ | j=6 | 6−5 = **1** |
| 6 | 76 | j=7: 73 ✗ → end | none | **0** |
| 7 | 73 | no j left | none | **0** |

**Result:** `[1, 1, 4, 2, 1, 1, 0, 0]`

> ⚠️ For `i=2` (temp=75), the inner loop scanned **4 elements** before finding 76. In the worst case (e.g., `[100, 99, 98, ..., 30]`), every element scans to the end → O(n²) total. For n = 10⁵, that's ~10¹⁰ operations — **too slow**.

---

---

# ⚡ SECTION 2: OPTIMIZED ITERATIVE APPROACHES

---

## 2A. Monotonic Stack (O(n) Time, O(n) Space)

**Idea:**  
- Maintain a **stack of indices** whose temperatures are in **strictly decreasing** order (top = coldest unresolved day).  
- Iterate left to right. For each day `i`:  
  - **While** the stack is non-empty AND `temperatures[i] > temperatures[stack.peek()]`:  
    - Pop index `prev`. Day `i` is the first warmer day for `prev`. Set `answer[prev] = i - prev`.  
  - Push `i` onto the stack.  
- Indices remaining in the stack at the end have **no** future warmer day → answer stays 0.

**Why it works:** Each index is pushed once and popped at most once → total operations = O(n).

**Time:** O(n) — each index pushed and popped at most once.  
**Space:** O(n) — stack holds at most n indices.

```java
import java.util.ArrayDeque;
import java.util.Deque;

public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    Deque<Integer> stack = new ArrayDeque<>(); // stores indices

    for (int i = 0; i < n; i++) {
        // Resolve all colder days that today warms up
        while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
            int prev = stack.pop();
            answer[prev] = i - prev;
        }
        stack.push(i);
    }
    // Remaining indices in stack → no warmer future day → answer stays 0

    return answer;
}
```

### 🔍 Sample Iteration

**Input:** `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`  
**Stack convention:** top is shown on the **left**.

| Step (i) | temp[i] | Stack BEFORE (top→bottom) | Action | Stack AFTER | answer update |
|----------|---------|---------------------------|--------|-------------|---------------|
| 0 | 73 | `[]` | Stack empty. Push 0. | `[0]` | — |
| 1 | 74 | `[0]` (temp=73) | 74 > 73 → pop 0. answer[0]=1−0=**1**. Stack empty. Push 1. | `[1]` | answer[0]=1 |
| 2 | 75 | `[1]` (temp=74) | 75 > 74 → pop 1. answer[1]=2−1=**1**. Stack empty. Push 2. | `[2]` | answer[1]=1 |
| 3 | 71 | `[2]` (temp=75) | 71 > 75? **No**. Push 3. | `[3, 2]` | — |
| 4 | 69 | `[3, 2]` (temp=71, 75) | 69 > 71? **No**. Push 4. | `[4, 3, 2]` | — |
| 5 | 72 | `[4, 3, 2]` (temp=69,71,75) | 72 > 69 → pop 4. answer[4]=5−4=**1**. 72 > 71 → pop 3. answer[3]=5−3=**2**. 72 > 75? **No**. Push 5. | `[5, 2]` | answer[4]=1, answer[3]=2 |
| 6 | 76 | `[5, 2]` (temp=72, 75) | 76 > 72 → pop 5. answer[5]=6−5=**1**. 76 > 75 → pop 2. answer[2]=6−2=**4**. Stack empty. Push 6. | `[6]` | answer[5]=1, answer[2]=4 |
| 7 | 73 | `[6]` (temp=76) | 73 > 76? **No**. Push 7. | `[7, 6]` | — |
| END | — | `[7, 6]` remain | No warmer day for indices 7 and 6. | — | answer[6]=0, answer[7]=0 |

**Final answer:** `[1, 1, 4, 2, 1, 1, 0, 0]` ✅

> 📌 **Key insight:** Index 2 (temp=75) sat in the stack from step 2 until step 6 — it waited 4 days. The stack naturally "remembers" unresolved days. Each index is pushed **once** and popped **once** → exactly 2n operations total → O(n).

---

## 2B. Reverse Traversal with "Next Warmer" Array (O(n) Time, O(1) Extra Space)

**Idea:**  
Exploit the constraint `30 ≤ temperatures[i] ≤ 100` (only 71 possible values).  
- Create a fixed array `next[101]` where `next[t]` = the **smallest index** (nearest to the left when scanning right-to-left) where temperature `t` was seen.  
- Initialize all entries to `Integer.MAX_VALUE` (meaning "not seen yet").  
- Traverse from **right to left** (`i` from `n-1` down to `0`):  
  - For current `temp = temperatures[i]`, scan all warmer temperatures `t = temp+1` to `100`.  
  - Find the **minimum** `next[t]` — that's the nearest future day with a warmer temperature.  
  - If found, `answer[i] = minIndex - i`.  
  - Update `next[temp] = i` (overwrite with the current, smaller index).

**Time:** O(n × 70) ≈ O(n) — inner loop runs at most 70 iterations (temps 31–100).  
**Space:** O(1) extra — `next` array is fixed size 101 regardless of input.

```java
import java.util.Arrays;

public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    int[] next = new int[101]; // next[t] = earliest index of temp t (from right)
    Arrays.fill(next, Integer.MAX_VALUE);

    for (int i = n - 1; i >= 0; i--) {
        int temp = temperatures[i];
        int minIndex = Integer.MAX_VALUE;

        // Search all warmer temperatures for the nearest occurrence
        for (int t = temp + 1; t <= 100; t++) {
            if (next[t] < minIndex) {
                minIndex = next[t];
            }
        }

        if (minIndex != Integer.MAX_VALUE) {
            answer[i] = minIndex - i;
        }
        // else answer[i] stays 0

        next[temp] = i; // record this index for current temperature
    }

    return answer;
}
```

### 🔍 Sample Iteration

**Input:** `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`  
**`next` array:** Only showing relevant slots (69–76). All others = `MAX` (∞).

| Step (i) | temp | next[] BEFORE (relevant slots) | Scan t=temp+1..100, find min | minIndex | answer[i] | next[] AFTER |
|----------|------|-------------------------------|------------------------------|----------|-----------|--------------|
| 7 | 73 | all ∞ | t=74..100: all ∞ | ∞ | **0** | next[73]=7 |
| 6 | 76 | next[73]=7, rest ∞ | t=77..100: all ∞ | ∞ | **0** | next[76]=6 |
| 5 | 72 | next[73]=7, next[76]=6 | t=73: 7, t=74: ∞, t=75: ∞, t=76: 6 → min=**6** | 6 | 6−5=**1** | next[72]=5 |
| 4 | 69 | next[72]=5, next[73]=7, next[76]=6 | t=70: ∞, t=71: ∞, t=72: **5**, t=73: 7, t=76: 6 → min=**5** | 5 | 5−4=**1** | next[69]=4 |
| 3 | 71 | next[69]=4, next[72]=5, next[73]=7, next[76]=6 | t=72: **5**, t=73: 7, t=76: 6 → min=**5** | 5 | 5−3=**2** | next[71]=3 |
| 2 | 75 | next[69]=4, next[71]=3, next[72]=5, next[73]=7, next[76]=6 | t=76: **6** → min=**6** | 6 | 6−2=**4** | next[75]=2 |
| 1 | 74 | next[69]=4, next[71]=3, next[72]=5, next[73]=7, next[75]=2, next[76]=6 | t=75: **2**, t=76: 6 → min=**2** | 2 | 2−1=**1** | next[74]=1 |
| 0 | 73 | next[69]=4, next[71]=3, next[72]=5, next[73]=7, next[74]=1, next[75]=2, next[76]=6 | t=74: **1**, t=75: 2, t=76: 6 → min=**1** | 1 | 1−0=**1** | next[73]=0 |

**Final answer:** `[1, 1, 4, 2, 1, 1, 0, 0]` ✅

> 📌 **Key insight:** When processing `i=2` (temp=75), we look at `next[76]=6` — the only warmer temperature seen to the right. So the answer is `6−2=4`. The `next` array acts as a **lookup table** for "where is the nearest day with temperature exactly `t`?"

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Monotonic Stack

| Metric | Brute Force (Nested Loops) | Monotonic Stack |
|--------|---------------------------|-----------------|
| Time | O(n²) | O(n) |
| For n=10⁵ | ~10¹⁰ ops → **TLE** | ~2×10⁵ ops → instant |
| Space | O(1) | O(n) |
| Works for any value range? | ✅ Yes | ✅ Yes |
| Code complexity | Trivial | Moderate (stack logic) |
| Interview value | Baseline only | **Expected answer** |

**Verdict:** Stack is strictly superior in time. The O(n) space is acceptable for n=10⁵.

---

## Monotonic Stack vs Reverse Traversal + Next Array

| Metric | Monotonic Stack | Reverse + Next Array |
|--------|----------------|---------------------|
| Time | O(n) | O(n × 70) ≈ O(n) |
| Extra Space | O(n) — stack of indices | **O(1)** — fixed 101-slot array |
| Depends on value range? | ❌ No (works for any integers) | ✅ Yes (requires bounded range [30,100]) |
| Traversal direction | Left → Right | Right → Left |
| Data structure | Stack (LIFO) | Array (random access) |
| Practical speed | Fast (simple push/pop) | Slightly slower (70-iteration inner loop) |
| Interview value | **Standard expected answer** | Shows constraint-awareness (bonus) |

**Verdict:** Stack is the **general, universal** solution. The next-array method is a **constraint-specific optimization** that trades a small constant factor in time for O(1) space. Present it as a follow-up to impress.

---

## 🏁 Final Master Comparison Table

| Approach | Time | Extra Space | General? | Key Insight |
|----------|------|-------------|----------|-------------|
| Brute Force (nested loops) | O(n²) | O(1) | ✅ | Scan forward for each day |
| **Monotonic Stack** | **O(n)** | **O(n)** | **✅** | Decreasing stack; warmer day resolves all colder below |
| **Reverse + Next Array** | **O(n × 70) ≈ O(n)** | **O(1)** | ❌ (needs bounded range) | Fixed lookup table for nearest warmer temp |

---

### 🎯 What to Present to the Interviewer

1. **Recognise** this as a "Next Greater Element" variant — the classic monotonic stack problem.
2. **Mention brute force** O(n²) as the baseline (scan forward for each day).
3. **Introduce the monotonic stack:**
   - Store indices, maintain decreasing temperature order.
   - When a warmer day `i` arrives, pop and resolve all colder days.
   - Each index pushed/popped once → O(n) time.
4. **Walk through** the stack trace for the example `[73,74,75,71,69,72,76,73]`, showing how index 2 (temp=75) waits until index 6 (temp=76) resolves it.
5. **Write clean Java code** with `ArrayDeque<Integer>`.
6. **After the interviewer is satisfied**, point out the constraint `30 ≤ temp ≤ 100` and offer the **O(1) space** solution:
   - Reverse traversal + `next[101]` array.
   - For each day, scan 70 warmer buckets to find the nearest index.
7. **Discuss trade-offs:** Stack is general and clean; next-array exploits constraints for constant space.
8. **Conclude:** Both are linear-time. Stack is the go-to; the array method shows deep constraint awareness.

**One‑sentence summary:**  
*Use a monotonic decreasing stack of indices to resolve each day's "next warmer" in O(n) time, or exploit the bounded temperature range [30,100] with a reverse-traversal lookup array for O(1) extra space.*