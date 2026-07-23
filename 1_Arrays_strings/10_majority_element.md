### 📘 Chapter: Arrays & Strings  
### 📌 Problem 10: Majority Element (LeetCode 169)

---

**Input**  
- `nums`: integer array of size `n`.

**Output**  
- The **majority element** — the element that appears **more than** `⌊n / 2⌋` times.

**Constraints**  
- `n == nums.length`  
- `1 <= n <= 5 × 10⁴`  
- `-10⁹ <= nums[i] <= 10⁹`  
- A majority element **always exists** in the input.

**Example**  
```
Input:  nums = [3, 2, 3]
Output: 3
Explanation: 3 appears 2 times > ⌊3/2⌋ = 1.

Input:  nums = [2, 2, 1, 1, 1, 2, 2]
Output: 2
Explanation: 2 appears 4 times > ⌊7/2⌋ = 3.

Input:  nums = [1]
Output: 1
```

**Follow-up**  
- Can you solve the problem in **O(n) time** and **O(1) space**?

---

### 🧠 Core Idea

Find an element appearing **more than half** the time. The guarantee of existence enables clever elimination strategies.

- **Brute force (nested loops):** For each element, count occurrences by scanning the entire array. O(n²).
- **Sorting:** Sort the array; the majority element **must** occupy the middle index `n/2`. O(n log n).
- **HashMap:** Count frequencies in one pass. O(n) time, O(n) space. ❌ Fails O(1) space follow-up.
- **Boyer-Moore Voting (optimal):** Maintain a `candidate` and `count`. Cancel opposing pairs; the majority element **always survives**. O(n) time, O(1) space. ✅

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACHES

---

## 1A. Naive Nested Loops (O(n²) Time, O(1) Space)

**Idea:** For each element `nums[i]`, scan the **entire array** to count how many times it appears. If count > `n/2`, return it.

**Time:** O(n²) — for each of n elements, scan n elements.  
**Space:** O(1).

```java
public int majorityElement(int[] nums) {
    int n = nums.length;

    for (int i = 0; i < n; i++) {
        int count = 0;
        for (int j = 0; j < n; j++) {
            if (nums[j] == nums[i]) {
                count++;
            }
        }
        if (count > n / 2) {
            return nums[i];
        }
    }

    return -1; // unreachable (majority always exists)
}
```

### 🔍 Sample Iteration

**Input:** `nums = [2, 2, 1, 1, 1, 2, 2]`, n = 7, threshold = ⌊7/2⌋ = 3 (need count > 3, i.e., ≥ 4)

| Outer i | nums[i] | Inner loop: count occurrences | count | count > 3? | Action |
|---------|---------|-------------------------------|-------|------------|--------|
| 0 | 2 | j=0:2✓, j=1:2✓, j=2:1✗, j=3:1✗, j=4:1✗, j=5:2✓, j=6:2✓ | **4** | 4 > 3 ✅ | **RETURN 2** |

> 📌 In this case, we got lucky and found it at `i=0`. But in the worst case (majority element is last), we'd scan the full array for every preceding element → O(n²). For n = 5×10⁴, that's 2.5 × 10⁹ operations — **too slow**.

**Worst-case example:** `nums = [1, 1, 1, 1, 1, 3, 3, 3, 3, 2]` (majority = 1, but if 1 were at the end...)

| Outer i | nums[i] | count | count > n/2? |
|---------|---------|-------|--------------|
| 0 | 3 | 4 | 4 > 5? No |
| 1 | 3 | 4 | No |
| 2 | 3 | 4 | No |
| 3 | 3 | 4 | No |
| 4 | 2 | 1 | No |
| 5 | 1 | 6 | 6 > 5? ✅ RETURN 1 |

→ 6 full scans of 10 elements = 60 operations. Scales to O(n²).

---

## 1B. Sorting Approach (O(n log n) Time, O(1) Space)

**Idea:** Sort the array. The majority element appears more than `n/2` times, so it **must** occupy index `⌊n/2⌋` (the middle position). Simply return `nums[n/2]`.

**Why it works:** If an element occupies more than half the positions, it must span the middle index regardless of arrangement.

**Time:** O(n log n) — sorting dominates.  
**Space:** O(1) if in-place sort.  
❌ Does NOT meet O(n) requirement, but is elegant and simple.

```java
import java.util.Arrays;

public int majorityElement(int[] nums) {
    Arrays.sort(nums);
    return nums[nums.length / 2];
}
```

### 🔍 Sample Iteration

**Input:** `nums = [2, 2, 1, 1, 1, 2, 2]`, n = 7

**After sorting:** `[1, 1, 1, 2, 2, 2, 2]`

```
Index:  0  1  2  3  4  5  6
Value:  1  1  1  2  2  2  2
              ↑
         n/2 = 3
```

`nums[7/2] = nums[3] = 2` → **RETURN 2** ✅

**Another example:** `nums = [3, 2, 3]`, n = 3

**After sorting:** `[2, 3, 3]`

```
Index:  0  1  2
Value:  2  3  3
           ↑
      n/2 = 1
```

`nums[3/2] = nums[1] = 3` → **RETURN 3** ✅

> 📌 The sorting approach is a **two-liner** but costs O(n log n). It also **modifies the input array**, which may not be acceptable.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACHES

---

## 2A. HashMap Frequency Count (O(n) Time, O(n) Space)

**Idea:** Use a `HashMap<Integer, Integer>` to count occurrences of each element in a single pass. Return the element whose count exceeds `n/2`.

**Time:** O(n) — single pass, O(1) average per HashMap operation.  
**Space:** O(n) — worst case all elements are distinct (n entries in map).  
❌ Does NOT meet the O(1) space follow-up.

```java
import java.util.HashMap;
import java.util.Map;

public int majorityElement(int[] nums) {
    Map<Integer, Integer> freq = new HashMap<>();
    int n = nums.length;

    for (int num : nums) {
        freq.put(num, freq.getOrDefault(num, 0) + 1);
        if (freq.get(num) > n / 2) {
            return num;  // early exit
        }
    }

    return -1; // unreachable
}
```

### 🔍 Sample Iteration

**Input:** `nums = [2, 2, 1, 1, 1, 2, 2]`, n = 7, threshold = 3

| Step | num | HashMap state (after update) | freq.get(num) | > 3? | Action |
|------|-----|------------------------------|---------------|------|--------|
| 1 | 2 | {2:1} | 1 | No | Continue |
| 2 | 2 | {2:2} | 2 | No | Continue |
| 3 | 1 | {2:2, 1:1} | 1 | No | Continue |
| 4 | 1 | {2:2, 1:2} | 2 | No | Continue |
| 5 | 1 | {2:2, 1:3} | 3 | No (3 > 3 is false) | Continue |
| 6 | 2 | {2:3, 1:3} | 3 | No | Continue |
| **7** | **2** | **{2:4, 1:3}** | **4** | **4 > 3 ✅** | **RETURN 2** |

**Result:** `2` ✅

> 📌 Early exit at step 7 — we don't need to process the rest (though here it's the last element). The HashMap grows to at most `k` entries where `k` = number of distinct elements.

---

## 2B. Boyer-Moore Voting Algorithm (O(n) Time, O(1) Space) ✅

**Idea:**  
Maintain a `candidate` and a `count`. Traverse the array:
- If `count == 0` → adopt current element as new `candidate`.
- If current element == `candidate` → `count++` (support).
- If current element ≠ `candidate` → `count--` (cancel/oppose).

**Why it works:**  
The majority element appears more than `n/2` times. All other elements combined appear fewer than `n/2` times. Even if **every** non-majority element cancels one majority element, the majority still has votes left over. It **cannot** be fully eliminated.

**Time:** O(n) — single pass.  
**Space:** O(1) — only two variables (`candidate`, `count`).

```java
public int majorityElement(int[] nums) {
    int candidate = 0;
    int count = 0;

    for (int num : nums) {
        if (count == 0) {
            candidate = num;  // adopt new candidate
        }
        count += (num == candidate) ? 1 : -1;
    }

    return candidate;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [2, 2, 1, 1, 1, 2, 2]`, n = 7

| Step | num | count BEFORE | Action | candidate | count AFTER | Explanation |
|------|-----|--------------|--------|-----------|-------------|-------------|
| 1 | 2 | 0 | count==0 → adopt 2 | **2** | +1 → **1** | New candidate |
| 2 | 2 | 1 | 2==candidate → +1 | 2 | **2** | Support |
| 3 | 1 | 2 | 1≠candidate → −1 | 2 | **1** | Cancel |
| 4 | 1 | 1 | 1≠candidate → −1 | 2 | **0** | Cancel → count hits 0! |
| 5 | 1 | 0 | count==0 → adopt 1 | **1** | +1 → **1** | New candidate (usurper!) |
| 6 | 2 | 1 | 2≠candidate → −1 | 1 | **0** | Cancel → count hits 0 again! |
| 7 | 2 | 0 | count==0 → adopt 2 | **2** | +1 → **1** | Majority reclaims throne |

**Final candidate:** `2` ✅  
**Result:** `2` ✅

---

### 🔍 Visual "Battle" Representation

```
Array: [2, 2, 1, 1, 1, 2, 2]

Step 1:  2  →  candidate=2, count=1     [2]
Step 2:  2  →  candidate=2, count=2     [2,2]
Step 3:  1  →  candidate=2, count=1     [2,2] vs [1] → one pair cancelled
Step 4:  1  →  candidate=2, count=0     [2,2] vs [1,1] → ALL cancelled!
Step 5:  1  →  candidate=1, count=1     [1] takes over (count was 0)
Step 6:  2  →  candidate=1, count=0     [1] vs [2] → cancelled!
Step 7:  2  →  candidate=2, count=1     [2] takes over (count was 0)

Survivor: 2 (the true majority) ✅
```

> 📌 Think of it as a **battlefield**: each pair of different elements "kills" each other. The majority element has more soldiers than ALL enemies combined, so it **always** has survivors at the end.

---

### 🔍 Second Example: `nums = [3, 2, 3]`

| Step | num | count BEFORE | Action | candidate | count AFTER |
|------|-----|--------------|--------|-----------|-------------|
| 1 | 3 | 0 | count==0 → adopt 3 | **3** | **1** |
| 2 | 2 | 1 | 2≠3 → −1 | 3 | **0** |
| 3 | 3 | 0 | count==0 → adopt 3 | **3** | **1** |

**Final candidate:** `3` ✅

---

### 🔍 Third Example (Majority barely wins): `nums = [1, 2, 1, 2, 1]`

n = 5, majority = 1 (appears 3 times > 2)

| Step | num | count BEFORE | Action | candidate | count AFTER |
|------|-----|--------------|--------|-----------|-------------|
| 1 | 1 | 0 | adopt 1 | **1** | **1** |
| 2 | 2 | 1 | 2≠1 → −1 | 1 | **0** |
| 3 | 1 | 0 | adopt 1 | **1** | **1** |
| 4 | 2 | 1 | 2≠1 → −1 | 1 | **0** |
| 5 | 1 | 0 | adopt 1 | **1** | **1** |

**Final candidate:** `1` ✅

> 📌 Even though `count` hit 0 **twice**, the majority element (1) always reclaims the candidate position because it has more occurrences than all others combined.

---

### 🔍 Why Boyer-Moore Works (Formal Intuition)

```
Let majority element = M, appearing k times where k > n/2.
Let all other elements combined = n - k < n/2.

Worst case: every non-M element cancels exactly one M element.
Cancelled M elements: at most (n - k)
Remaining M elements: k - (n - k) = 2k - n > 0  (since k > n/2)

∴ At least one M survives → M is the final candidate. ∎
```

---

### 🔍 Optional: Verification Pass (When Existence NOT Guaranteed)

If the problem didn't guarantee a majority exists, add a second pass:

```java
public int majorityElement(int[] nums) {
    // Pass 1: Find candidate (Boyer-Moore)
    int candidate = 0, count = 0;
    for (int num : nums) {
        if (count == 0) candidate = num;
        count += (num == candidate) ? 1 : -1;
    }

    // Pass 2: Verify candidate is truly the majority
    count = 0;
    for (int num : nums) {
        if (num == candidate) count++;
    }

    return (count > nums.length / 2) ? candidate : -1;
}
```

> 📌 Still O(n) time, O(1) space. The problem guarantees existence, so Pass 2 is technically unnecessary here — but mentioning it shows thoroughness.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Sorting vs HashMap vs Boyer-Moore

| Metric | Nested Loops | Sorting | HashMap | Boyer-Moore |
|--------|-------------|---------|---------|-------------|
| Time | O(n²) | O(n log n) | O(n) | **O(n)** |
| Space | O(1) | O(1) | O(n) | **O(1)** |
| Meets O(n) time? | ❌ | ❌ | ✅ | ✅ |
| Meets O(1) space? | ✅ | ✅ | ❌ | ✅ |
| Modifies input? | No | **Yes** | No | No |
| Works without majority guarantee? | ✅ | ✅ | ✅ | ❌ (needs verification pass) |
| Code complexity | Trivial | One-liner | Simple | Elegant but non-obvious |

---

## HashMap vs Boyer-Moore (Head-to-Head)

| Metric | HashMap | Boyer-Moore |
|--------|---------|-------------|
| Time | O(n) | O(n) |
| Space | O(n) — up to n distinct keys | **O(1)** — two integers |
| Intuition | "Count everything, find the max" | "Cancel pairs, survivor wins" |
| Handles no-majority case? | ✅ (just check max freq) | ❌ (needs 2nd pass) |
| Interview value | Shows basic competence | **Shows algorithmic insight** |
| When to use | General frequency problems | **This exact problem** (majority guaranteed) |

**Verdict:** Boyer-Moore is the **expected interview answer** for this problem. HashMap is the safe fallback.

---

## Sorting vs Boyer-Moore

| Metric | Sorting | Boyer-Moore |
|--------|---------|-------------|
| Time | O(n log n) | **O(n)** |
| Space | O(1) in-place | O(1) |
| Modifies input? | **Yes** | No |
| Code length | 2 lines | 6 lines |
| Insight required | Low (observe middle element) | High (cancellation argument) |
| Meets follow-up? | ❌ (not O(n) time) | ✅ |

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | O(n) + O(1)? | Key Insight |
|----------|------|-------|--------------|-------------|
| Nested Loops | O(n²) | O(1) | ❌ | Count each element by full scan |
| Sorting | O(n log n) | O(1) | ❌ | Majority must sit at index n/2 |
| HashMap | O(n) | O(n) | ❌ (space) | Frequency counting |
| **Boyer-Moore Voting** | **O(n)** | **O(1)** | **✅** | **Cancel opposing pairs; majority survives** |

---

### 🎯 What to Present to the Interviewer

1. **Start simple:** Mention the HashMap counting approach — O(n) time, O(n) space. Shows you can solve it.
2. **Acknowledge the follow-up:** "The O(1) space requirement rules out HashMap. This calls for Boyer-Moore Voting."
3. **Explain Boyer-Moore intuitively:**
   - "Imagine a battlefield. Each pair of different elements cancels out. The majority element has more soldiers than all enemies combined, so it always has survivors."
   - Maintain `candidate` and `count`. When count hits 0, the next element becomes the new candidate.
4. **Write the concise code** (6 lines).
5. **Walk through** the example `[2,2,1,1,1,2,2]` showing how count oscillates and the majority reclaims the throne.
6. **Prove correctness:** Majority appears > n/2 times. Even if every other element cancels one majority element, at least one majority element remains → it's the final candidate.
7. **If asked about verification:** Mention the optional second pass to confirm (not needed here due to the guarantee, but shows awareness).
8. **Mention sorting** as a clever O(n log n) alternative (return `nums[n/2]`), but note it violates O(n) time and modifies input.

**One‑sentence summary:**  
*Use the Boyer-Moore Voting Algorithm: maintain a candidate and count, cancel opposing pairs, and the majority element — appearing more than n/2 times — always survives as the final candidate in O(n) time and O(1) space.*