### 📘 Chapter: Two Pointers  
### 📌 Problem 6: Sort Colors (LeetCode 75)

---

**Input**  
- `nums`: an integer array where `nums[i]` is `0`, `1`, or `2` (representing red, white, and blue respectively).

**Output**  
- The array sorted **in-place** so that all `0`s come first, then all `1`s, then all `2`s. (No return value; modify `nums` directly.)

**Constraints**  
- `n == nums.length`  
- `1 <= n <= 300`  
- `nums[i]` is either `0`, `1`, or `2`.

**Example**  
```
Input:  nums = [2, 0, 2, 1, 1, 0]
Output: [0, 0, 1, 1, 2, 2]

Input:  nums = [2, 0, 1]
Output: [0, 1, 2]

Input:  nums = [0]
Output: [0]
```

**Follow-up**  
- Could you come up with a **one-pass** algorithm using **only constant extra space**?

---

### 🧠 Core Idea

We need to sort an array with only **three distinct values** in-place.

- **General sort (bubble/selection):** O(n²) — ignores the constraint that only 3 values exist.
- **Counting sort (two-pass):** Count 0s, 1s, 2s, then overwrite. O(n) time, O(1) space, but **two passes**.
- **Dutch National Flag (one-pass, optimal):** Three pointers (`low`, `mid`, `high`) partition the array into three regions in a **single pass**. O(n) time, O(1) space. ✅

**The three regions maintained by the Dutch National Flag:**
```
[0, low)       → all 0s (red)     ← sorted, finalized
[low, mid)     → all 1s (white)   ← sorted, finalized
[mid, high]    → unknown          ← yet to be processed
(high, n-1]    → all 2s (blue)    ← sorted, finalized
```

---

---

# 🔨 SECTION 1: BRUTE FORCE / SIMPLE APPROACHES

---

## 1A. General In-Place Sort (Bubble Sort) — O(n²)

**Idea:** Apply any standard sorting algorithm (bubble sort, selection sort, etc.) to sort the array in-place. This completely ignores the fact that only 3 values exist.

**Time:** O(n²).  
**Space:** O(1).

```java
public void sortColors(int[] nums) {
    int n = nums.length;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (nums[j] > nums[j + 1]) {
                int temp = nums[j];
                nums[j] = nums[j + 1];
                nums[j + 1] = temp;
            }
        }
    }
}
```

### 🔍 Sample Iteration

**Input:** `nums = [2, 0, 2, 1, 1, 0]`

| Pass i | Comparisons & Swaps | Array state after pass |
|--------|---------------------|----------------------|
| 0 | (2,0)→swap, (2,2)→ok, (2,1)→swap, (2,1)→swap, (2,0)→swap | `[0, 2, 1, 1, 0, 2]` |
| 1 | (0,2)→ok, (2,1)→swap, (2,1)→swap, (2,0)→swap | `[0, 1, 1, 0, 2, 2]` |
| 2 | (0,1)→ok, (1,1)→ok, (1,0)→swap | `[0, 1, 0, 1, 2, 2]` |
| 3 | (0,1)→ok, (1,0)→swap | `[0, 0, 1, 1, 2, 2]` |
| 4 | (0,0)→ok | `[0, 0, 1, 1, 2, 2]` |

**Result:** `[0, 0, 1, 1, 2, 2]` ✅

> ⚠️ 5 passes × up to 5 comparisons = ~14 operations for n=6. For n=300: ~45,000 operations. Works, but **wasteful** — we're using a general O(n²) sort on an array with only 3 possible values.

---

## 1B. Counting Sort (Two-Pass, O(n) Time, O(1) Space)

**Idea:**  
1. **Pass 1:** Count occurrences of 0, 1, and 2.  
2. **Pass 2:** Overwrite the array: first `count0` positions with 0, next `count1` with 1, rest with 2.

**Time:** O(n) — two linear passes.  
**Space:** O(1) — three counter variables.  
❌ Does NOT meet the one-pass follow-up.

```java
public void sortColors(int[] nums) {
    int count0 = 0, count1 = 0, count2 = 0;

    // Pass 1: Count
    for (int num : nums) {
        if (num == 0) count0++;
        else if (num == 1) count1++;
        else count2++;
    }

    // Pass 2: Overwrite
    int i = 0;
    while (count0-- > 0) nums[i++] = 0;
    while (count1-- > 0) nums[i++] = 1;
    while (count2-- > 0) nums[i++] = 2;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [2, 0, 2, 1, 1, 0]`

**Pass 1: Count**

| Index | Value | count0 | count1 | count2 |
|-------|-------|--------|--------|--------|
| 0 | 2 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 2 | 2 | 1 | 0 | 2 |
| 3 | 1 | 1 | 1 | 2 |
| 4 | 1 | 1 | 2 | 2 |
| 5 | 0 | **2** | **2** | **2** |

**Pass 2: Overwrite**

| Step | Write | i | Array state |
|------|-------|---|-------------|
| 1 | nums[0] = 0 | 1 | [**0**, 0, 2, 1, 1, 0] |
| 2 | nums[1] = 0 | 2 | [0, **0**, 2, 1, 1, 0] |
| 3 | nums[2] = 1 | 3 | [0, 0, **1**, 1, 1, 0] |
| 4 | nums[3] = 1 | 4 | [0, 0, 1, **1**, 1, 0] |
| 5 | nums[4] = 2 | 5 | [0, 0, 1, 1, **2**, 0] |
| 6 | nums[5] = 2 | 6 | [0, 0, 1, 1, 2, **2**] |

**Result:** `[0, 0, 1, 1, 2, 2]` ✅

> 📌 Simple and correct, but requires **two passes** over the data. The follow-up explicitly asks for one pass.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. Dutch National Flag — Three Pointers (One Pass, O(1) Space) ✅

**Idea:**  
Maintain three pointers that define three regions:

```
┌─────────────────────────────────────────────────────────┐
│  0  0  0  │  1  1  1  │  ?  ?  ?  │  2  2  2  │
│  ← 0s →  │  ← 1s →  │ ← unknown→ │  ← 2s →  │
└─────────────────────────────────────────────────────────┘
0         low         mid         high         n-1
          ↑           ↑           ↑
       next 0 goes  current    next 2 goes
       here         scanner    here
```

**Rules:**
- `nums[mid] == 0`: Swap with `nums[low]`. Increment both `low` and `mid`.  
  *(The element swapped from `low` to `mid` is guaranteed to be 0 or 1 — already processed.)*
- `nums[mid] == 1`: Just increment `mid`.  
  *(1 is already in the correct region.)*
- `nums[mid] == 2`: Swap with `nums[high]`. Decrement `high`. **Do NOT increment `mid`**.  
  *(The element swapped from `high` to `mid` is UNKNOWN — hasn't been processed yet.)*

**Time:** O(n) — single pass, `mid` advances at most n times.  
**Space:** O(1) — three pointer variables.

```java
public void sortColors(int[] nums) {
    int low = 0, mid = 0, high = nums.length - 1;

    while (mid <= high) {
        if (nums[mid] == 0) {
            swap(nums, low, mid);
            low++;
            mid++;
        } else if (nums[mid] == 1) {
            mid++;
        } else { // nums[mid] == 2
            swap(nums, mid, high);
            high--;
            // DO NOT increment mid — swapped element is unknown
        }
    }
}

private void swap(int[] nums, int i, int j) {
    int temp = nums[i];
    nums[i] = nums[j];
    nums[j] = temp;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [2, 0, 2, 1, 1, 0]`

| Step | low | mid | high | nums[mid] | Action | Array state | Regions |
|------|-----|-----|------|-----------|--------|-------------|---------|
| 0 | 0 | 0 | 5 | — | Initial | `[2, 0, 2, 1, 1, 0]` | All unknown |
| 1 | 0 | 0 | 5 | **2** | Swap(mid=0, high=5). high--. **mid stays.** | `[0, 0, 2, 1, 1, 2]` | 2s: [5] |
| 2 | 0 | 0 | 4 | **0** | Swap(mid=0, low=0) → no-op. low++. mid++. | `[0, 0, 2, 1, 1, 2]` | 0s: [0] |
| 3 | 1 | 1 | 4 | **0** | Swap(mid=1, low=1) → no-op. low++. mid++. | `[0, 0, 2, 1, 1, 2]` | 0s: [0,1] |
| 4 | 2 | 2 | 4 | **2** | Swap(mid=2, high=4). high--. **mid stays.** | `[0, 0, 1, 1, 2, 2]` | 2s: [4,5] |
| 5 | 2 | 2 | 3 | **1** | mid++ (1 is correct here). | `[0, 0, 1, 1, 2, 2]` | 1s: [2] |
| 6 | 2 | 3 | 3 | **1** | mid++ (1 is correct here). | `[0, 0, 1, 1, 2, 2]` | 1s: [2,3] |
| 7 | 2 | 4 | 3 | — | mid(4) > high(3) → **STOP** | `[0, 0, 1, 1, 2, 2]` | ✅ DONE |

**Result:** `[0, 0, 1, 1, 2, 2]` ✅

---

### 🔍 Visual Region Tracking

```
Initial:  [2, 0, 2, 1, 1, 0]
           ─────────────────
           all unknown

Step 1:   [0, 0, 2, 1, 1, 2]    swapped nums[0]↔nums[5], high--
           ?  ?  ?  ?  ?  | 2
           ←── unknown ──→  2s

Step 2:   [0, 0, 2, 1, 1, 2]    nums[0]=0 → swap with low (no-op), low++, mid++
           0  |  ?  ?  ?  ?  | 2
           0s   ←─ unknown ─→  2s

Step 3:   [0, 0, 2, 1, 1, 2]    nums[1]=0 → swap with low (no-op), low++, mid++
           0  0  |  ?  ?  ?  | 2
           0s     ← unknown →  2s

Step 4:   [0, 0, 1, 1, 2, 2]    nums[2]=2 → swap with high, high--, mid STAYS
           0  0  |  ?  ?  | 2  2
           0s     ← unk →  2s

Step 5:   [0, 0, 1, 1, 2, 2]    nums[2]=1 → mid++
           0  0  |  1  |  ?  | 2  2
           0s      1s    unk   2s

Step 6:   [0, 0, 1, 1, 2, 2]    nums[3]=1 → mid++
           0  0  |  1  1  |  ?  | 2  2
           0s      1s      unk   2s

Step 7:   mid(4) > high(3) → DONE!
           0  0  |  1  1  |  2  2
           0s      1s       2s     ✅ SORTED
```

---

### 🔍 Why `mid` Does NOT Increment When Swapping with `high`

```
Case: nums[mid] == 2, swap with nums[high]

BEFORE swap:
  nums[mid] = 2 (known, needs to go right)
  nums[high] = ??? (UNKNOWN — could be 0, 1, or 2)

AFTER swap:
  nums[mid] = ??? (the unknown element from high is NOW at mid)
  nums[high] = 2 (correctly placed)

If we incremented mid, we'd SKIP the unknown element without processing it!
So we MUST keep mid in place to examine the newly swapped element.
```

**Contrast with swapping with `low`:**
```
Case: nums[mid] == 0, swap with nums[low]

BEFORE swap:
  nums[mid] = 0 (known)
  nums[low] = 0 or 1 (ALREADY PROCESSED — it's in the [low, mid) region which is all 1s,
              or low == mid so it's the same element)

AFTER swap:
  nums[mid] = 0 or 1 (already processed, safe to skip)
  nums[low] = 0 (correctly placed)

So we CAN safely increment mid — the swapped element is guaranteed processed.
```

---

### 🔍 Second Example: `nums = [2, 0, 1]`

| Step | low | mid | high | nums[mid] | Action | Array |
|------|-----|-----|------|-----------|--------|-------|
| 0 | 0 | 0 | 2 | — | Initial | `[2, 0, 1]` |
| 1 | 0 | 0 | 2 | **2** | Swap(0,2). high=1. mid stays. | `[1, 0, 2]` |
| 2 | 0 | 0 | 1 | **1** | mid++. | `[1, 0, 2]` |
| 3 | 0 | 1 | 1 | **0** | Swap(1,0). low=1. mid=2. | `[0, 1, 2]` |
| 4 | 1 | 2 | 1 | — | mid(2) > high(1) → **STOP** | `[0, 1, 2]` ✅ |

---

### 🔍 Third Example (All Same): `nums = [1, 1, 1, 1]`

| Step | low | mid | high | nums[mid] | Action | Array |
|------|-----|-----|------|-----------|--------|-------|
| 1 | 0 | 0 | 3 | 1 | mid++ | `[1,1,1,1]` |
| 2 | 0 | 1 | 3 | 1 | mid++ | `[1,1,1,1]` |
| 3 | 0 | 2 | 3 | 1 | mid++ | `[1,1,1,1]` |
| 4 | 0 | 3 | 3 | 1 | mid++ | `[1,1,1,1]` |
| 5 | 0 | 4 | 3 | — | mid > high → STOP | `[1,1,1,1]` ✅ |

> 📌 No swaps at all — just `mid` advancing through all 1s. O(n) with zero writes.

---

### 🔍 Fourth Example (Reverse Sorted): `nums = [2, 2, 1, 1, 0, 0]`

| Step | low | mid | high | nums[mid] | Action | Array |
|------|-----|-----|------|-----------|--------|-------|
| 1 | 0 | 0 | 5 | **2** | Swap(0,5). high=4. mid stays. | `[0, 2, 1, 1, 0, 2]` |
| 2 | 0 | 0 | 4 | **0** | Swap(0,0)→no-op. low=1, mid=1. | `[0, 2, 1, 1, 0, 2]` |
| 3 | 1 | 1 | 4 | **2** | Swap(1,4). high=3. mid stays. | `[0, 0, 1, 1, 2, 2]` |
| 4 | 1 | 1 | 3 | **0** | Swap(1,1)→no-op. low=2, mid=2. | `[0, 0, 1, 1, 2, 2]` |
| 5 | 2 | 2 | 3 | **1** | mid++. | `[0, 0, 1, 1, 2, 2]` |
| 6 | 2 | 3 | 3 | **1** | mid++. | `[0, 0, 1, 1, 2, 2]` |
| 7 | 2 | 4 | 3 | — | mid > high → STOP | `[0, 0, 1, 1, 2, 2]` ✅ |

> 📌 Even the worst case (fully reversed) takes only **6 steps** for n=6. Each element is swapped at most once into its final position.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Bubble Sort vs Counting Sort vs Dutch National Flag

| Metric | Bubble Sort | Counting Sort | Dutch National Flag |
|--------|-------------|---------------|---------------------|
| Time | O(n²) | O(n) | **O(n)** |
| Space | O(1) | O(1) | **O(1)** |
| Passes | n passes | 2 passes | **1 pass** |
| Writes to array | O(n²) swaps | n writes | ≤ n swaps |
| Meets one-pass follow-up? | ❌ | ❌ | **✅** |
| Exploits 3-value constraint? | ❌ (general sort) | ✅ (counts 3 values) | ✅ (partitions 3 regions) |
| Code complexity | Simple | Very simple | Moderate (pointer logic) |

---

## Counting Sort vs Dutch National Flag (Head-to-Head)

| Metric | Counting Sort | Dutch National Flag |
|--------|---------------|---------------------|
| Time | O(n) | O(n) |
| Passes | **2** | **1** |
| Space | O(1) | O(1) |
| Modifies array in-place? | ✅ (overwrites) | ✅ (swaps) |
| Stable? | ✅ (preserves relative order within same value) | ❌ (swaps can reorder same values) |
| Works for streaming data? | ✅ (count first, write later) | ❌ (needs random access for swaps) |
| Interview value | Shows basic thinking | **Shows algorithmic elegance** |
| When to use | If two passes are acceptable | **When one-pass is required** |

**Verdict:** Both are O(n) time, O(1) space. Dutch National Flag wins on the **one-pass** requirement. Counting sort wins on **simplicity** and **stability**.

---

## Why `mid` Behavior Differs for 0 vs 2

| Scenario | Swap partner | Is swapped element known? | Increment `mid`? | Reason |
|----------|-------------|--------------------------|-------------------|--------|
| `nums[mid] == 0` | `nums[low]` | **Yes** (it's 0 or 1, already in processed region) | ✅ Yes | Safe to skip — already handled |
| `nums[mid] == 2` | `nums[high]` | **No** (it's from the unknown region) | ❌ No | Must re-examine the new element at `mid` |

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Passes | One-Pass? | Key Insight |
|----------|------|-------|--------|-----------|-------------|
| Bubble/Selection Sort | O(n²) | O(1) | n | ❌ | General sort (ignores 3-value constraint) |
| Counting Sort | O(n) | O(1) | 2 | ❌ | Count then overwrite |
| **Dutch National Flag** | **O(n)** | **O(1)** | **1** | **✅** | **Three pointers partition into 0s/1s/2s regions** |

---

### 🎯 What to Present to the Interviewer

1. **Recognize** the array has only 3 values → no need for a general O(n log n) sort.
2. **Propose counting sort** as the straightforward baseline: count 0s, 1s, 2s, overwrite. O(n) time, O(1) space, but two passes.
3. **Acknowledge the follow-up:** "One pass with constant space → Dutch National Flag."
4. **Explain the three regions:**
   - `[0, low)` = all 0s (finalized)
   - `[low, mid)` = all 1s (finalized)
   - `[mid, high]` = unknown (to be processed)
   - `(high, n-1]` = all 2s (finalized)
5. **Walk through the algorithm** with `[2, 0, 2, 1, 1, 0]`:
   - Step 1: `nums[0]=2` → swap with high. Array becomes `[0,0,2,1,1,2]`. high--. **mid stays** (unknown element now at mid).
   - Step 2: `nums[0]=0` → swap with low (no-op). low++, mid++.
   - Continue...
6. **Emphasize the critical detail:** "When we swap a 2 with `high`, we do NOT increment `mid` because the element that came from `high` is unknown and must be examined."
7. **State complexity:** O(n) time (each element processed once), O(1) space (three pointers). Exactly one pass.
8. **If asked about stability:** "This algorithm is NOT stable — swaps can reorder elements with the same value. If stability matters, use counting sort."

**One‑sentence summary:**  
*Use the Dutch National Flag algorithm with three pointers (low, mid, high) to partition the array into 0s, 1s, and 2s regions in a single pass with O(1) extra space — swapping 0s to the front, 2s to the back, and letting 1s settle in the middle.*