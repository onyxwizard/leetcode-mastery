### 📘 Chapter: Two Pointers  
### 📌 Problem 8: Remove Duplicates from Sorted Array (LeetCode 26)

---

**Input**  
- `nums`: an integer array sorted in **non-decreasing order**.

**Output**  
- An integer `k` — the number of unique elements.  
- The first `k` elements of `nums` must contain the unique elements in sorted order. Elements beyond index `k-1` are irrelevant.

**Constraints**  
- `1 <= nums.length <= 3 × 10⁴`  
- `-100 <= nums[i] <= 100`  
- `nums` is sorted in non-decreasing order.

**Example**  
```
Input:  nums = [1, 1, 2]
Output: k = 2, nums = [1, 2, _]
Explanation: First 2 elements [1, 2] are unique. The '_' can be anything.

Input:  nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
Output: k = 5, nums = [0, 1, 2, 3, 4, _, _, _, _, _]
Explanation: First 5 elements are the unique values in sorted order.

Input:  nums = [1]
Output: k = 1, nums = [1]
```

**Follow-up**  
- No explicit follow-up. (Common extension: *"Allow at most two duplicates"* — LeetCode 80.)

---

### 🧠 Core Idea

The array is **sorted**, so all duplicates are **adjacent**. We need to **compress** the array in-place, keeping only one copy of each distinct value.

- **Brute force (shifting):** For each duplicate found, shift the entire tail left. O(n²).
- **Extra array:** Copy uniques to a new array, write back. O(n) time, O(n) space. Violates in-place spirit.
- **Two Pointers / Slow-Fast (optimal):** A `write` pointer marks where the next unique goes. A `read` pointer scans. When a new value is found, write it forward. O(n) time, O(1) space. ✅

**Key insight:** Since the array is sorted, `nums[i] != nums[write]` means we've encountered a **new distinct value** — no HashSet needed.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACHES

---

## 1A. Shift-on-Duplicate (O(n²) Time, O(1) Space)

**Idea:** Scan the array. When `nums[i] == nums[i+1]` (duplicate found), shift all elements from `i+2` onward one position left, reduce effective length `n`, and recheck index `i`.

**Time:** O(n²) — each duplicate triggers an O(n) shift.  
**Space:** O(1).

```java
public int removeDuplicates(int[] nums) {
    int n = nums.length;
    if (n == 0) return 0;

    int i = 0;
    while (i < n - 1) {
        if (nums[i] == nums[i + 1]) {
            // Shift everything after i+1 one position left
            for (int j = i + 1; j < n - 1; j++) {
                nums[j] = nums[j + 1];
            }
            n--;  // effective length reduced
            // Do NOT increment i — recheck same position
        } else {
            i++;
        }
    }

    return n;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]`, n = 10

| Step | i | n | nums[i] vs nums[i+1] | Action | Array state (first n elements) |
|------|---|---|----------------------|--------|-------------------------------|
| 1 | 0 | 10 | 0 == 0 → **DUP** | Shift left from index 1. n=9. | `[0, 1, 1, 1, 2, 2, 3, 3, 4]` |
| 2 | 0 | 9 | 0 ≠ 1 → ok | i++. | `[0, 1, 1, 1, 2, 2, 3, 3, 4]` |
| 3 | 1 | 9 | 1 == 1 → **DUP** | Shift left from index 2. n=8. | `[0, 1, 1, 2, 2, 3, 3, 4]` |
| 4 | 1 | 8 | 1 == 1 → **DUP** | Shift left from index 2. n=7. | `[0, 1, 2, 2, 3, 3, 4]` |
| 5 | 1 | 7 | 1 ≠ 2 → ok | i++. | `[0, 1, 2, 2, 3, 3, 4]` |
| 6 | 2 | 7 | 2 == 2 → **DUP** | Shift left from index 3. n=6. | `[0, 1, 2, 3, 3, 4]` |
| 7 | 2 | 6 | 2 ≠ 3 → ok | i++. | `[0, 1, 2, 3, 3, 4]` |
| 8 | 3 | 6 | 3 == 3 → **DUP** | Shift left from index 4. n=5. | `[0, 1, 2, 3, 4]` |
| 9 | 3 | 5 | 3 ≠ 4 → ok | i++. | `[0, 1, 2, 3, 4]` |
| 10 | 4 | 5 | i ≥ n-1 → **STOP** | — | `[0, 1, 2, 3, 4]` |

**Result:** k = **5**, first 5 elements = `[0, 1, 2, 3, 4]` ✅

> ⚠️ **5 duplicates removed**, each requiring a shift of up to 8 elements. Total shift operations: 9+7+6+5+4 = **31 writes**. For n = 3×10⁴ with many duplicates, this becomes O(n²) — far too slow.

---

## 1B. Extra Array (O(n) Time, O(n) Space)

**Idea:** Create a new array. Iterate through `nums`, copying each element only if it differs from the last copied element. Write the result back to `nums`.

**Time:** O(n).  
**Space:** O(n) — extra array.  
❌ Violates the in-place O(1) space requirement.

```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;

    int[] unique = new int[nums.length];
    int k = 1;
    unique[0] = nums[0];

    for (int i = 1; i < nums.length; i++) {
        if (nums[i] != nums[i - 1]) {
            unique[k++] = nums[i];
        }
    }

    // Copy back
    for (int i = 0; i < k; i++) {
        nums[i] = unique[i];
    }

    return k;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]`

| i | nums[i] | nums[i-1] | Duplicate? | unique[] | k |
|---|---------|-----------|------------|----------|---|
| 0 | 0 | — | (first) | [0] | 1 |
| 1 | 0 | 0 | **Yes** → skip | [0] | 1 |
| 2 | 1 | 0 | No → copy | [0, 1] | 2 |
| 3 | 1 | 1 | **Yes** → skip | [0, 1] | 2 |
| 4 | 1 | 1 | **Yes** → skip | [0, 1] | 2 |
| 5 | 2 | 1 | No → copy | [0, 1, 2] | 3 |
| 6 | 2 | 2 | **Yes** → skip | [0, 1, 2] | 3 |
| 7 | 3 | 2 | No → copy | [0, 1, 2, 3] | 4 |
| 8 | 3 | 3 | **Yes** → skip | [0, 1, 2, 3] | 4 |
| 9 | 4 | 3 | No → copy | [0, 1, 2, 3, 4] | 5 |

**Result:** k = **5**, `unique = [0, 1, 2, 3, 4]` ✅

> 📌 Correct and O(n) time, but allocates an extra array of size n. The problem expects O(1) space.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. Two Pointers — Slow/Fast (O(n) Time, O(1) Space) ✅

**Idea:**  
- **`write` (slow pointer):** Index where the next unique element should be placed. Starts at 0.
- **`read` (fast pointer):** Scans the array from index 1 onward.
- When `nums[read] != nums[write]`: a new distinct value is found.
  - Increment `write`.
  - Copy: `nums[write] = nums[read]`.
- At the end, `write + 1` = number of unique elements.

**Invariant:** `nums[0..write]` always contains the unique elements found so far, in sorted order.

**Time:** O(n) — single pass.  
**Space:** O(1) — in-place, two pointer variables.

```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;

    int write = 0;  // index of last unique element

    for (int read = 1; read < nums.length; read++) {
        if (nums[read] != nums[write]) {
            write++;
            nums[write] = nums[read];
        }
    }

    return write + 1;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]`

| Step | read | write | nums[read] | nums[write] | New unique? | Action | Array state (relevant portion) |
|------|------|-------|------------|-------------|-------------|--------|-------------------------------|
| 0 | — | 0 | — | 0 | — | Initial | `[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]` |
| 1 | 1 | 0 | 0 | 0 | **No** (0==0) | Skip. | `[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]` |
| 2 | 2 | 0 | 1 | 0 | **Yes** (1≠0) | write=1. nums[1]=1. | `[0, 1, 1, 1, 1, 2, 2, 3, 3, 4]` |
| 3 | 3 | 1 | 1 | 1 | **No** (1==1) | Skip. | `[0, 1, 1, 1, 1, 2, 2, 3, 3, 4]` |
| 4 | 4 | 1 | 1 | 1 | **No** (1==1) | Skip. | `[0, 1, 1, 1, 1, 2, 2, 3, 3, 4]` |
| 5 | 5 | 1 | 2 | 1 | **Yes** (2≠1) | write=2. nums[2]=2. | `[0, 1, 2, 1, 1, 2, 2, 3, 3, 4]` |
| 6 | 6 | 2 | 2 | 2 | **No** (2==2) | Skip. | `[0, 1, 2, 1, 1, 2, 2, 3, 3, 4]` |
| 7 | 7 | 2 | 3 | 2 | **Yes** (3≠2) | write=3. nums[3]=3. | `[0, 1, 2, 3, 1, 2, 2, 3, 3, 4]` |
| 8 | 8 | 3 | 3 | 3 | **No** (3==3) | Skip. | `[0, 1, 2, 3, 1, 2, 2, 3, 3, 4]` |
| 9 | 9 | 3 | 4 | 3 | **Yes** (4≠3) | write=4. nums[4]=4. | `[0, 1, 2, 3, 4, 2, 2, 3, 3, 4]` |

**Result:** k = write + 1 = **5**  
**First 5 elements:** `[0, 1, 2, 3, 4]` ✅  
*(Elements at indices 5–9 are irrelevant: `[2, 2, 3, 3, 4]` — ignored by the judge.)*

---

### 🔍 Visual Pointer Movement

```
nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]

Step 0:  [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
          W
          R→  0==0, skip

Step 2:  [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
          W     R→  1≠0, WRITE! nums[1]=1, W++

Step 3-4:[0, 1, 1, 1, 1, 2, 2, 3, 3, 4]
             W  R→→  1==1, skip. 1==1, skip.

Step 5:  [0, 1, 1, 1, 1, 2, 2, 3, 3, 4]
             W           R→  2≠1, WRITE! nums[2]=2, W++

Step 6:  [0, 1, 2, 1, 1, 2, 2, 3, 3, 4]
                W        R→  2==2, skip.

Step 7:  [0, 1, 2, 1, 1, 2, 2, 3, 3, 4]
                W              R→  3≠2, WRITE! nums[3]=3, W++

Step 8:  [0, 1, 2, 3, 1, 2, 2, 3, 3, 4]
                   W           R→  3==3, skip.

Step 9:  [0, 1, 2, 3, 1, 2, 2, 3, 3, 4]
                   W                 R→  4≠3, WRITE! nums[4]=4, W++

FINAL:   [0, 1, 2, 3, 4, | 2, 2, 3, 3, 4]
          ←── k=5 ──→      ←── ignored ──→
```

---

### 🔍 Simpler Example: `nums = [1, 1, 2]`

| Step | read | write | nums[read] | nums[write] | Action | Array |
|------|------|-------|------------|-------------|--------|-------|
| 0 | — | 0 | — | 1 | Initial | `[1, 1, 2]` |
| 1 | 1 | 0 | 1 | 1 | 1==1 → skip | `[1, 1, 2]` |
| 2 | 2 | 0 | 2 | 1 | 2≠1 → write=1, nums[1]=2 | `[1, 2, 2]` |

**Result:** k = **2**, first 2 elements = `[1, 2]` ✅

---

### 🔍 Edge Case: All Same Elements

**Input:** `nums = [5, 5, 5, 5, 5]`

| Step | read | write | nums[read] | Action | Array |
|------|------|-------|------------|--------|-------|
| 1 | 1 | 0 | 5 | 5==5 → skip | `[5,5,5,5,5]` |
| 2 | 2 | 0 | 5 | 5==5 → skip | `[5,5,5,5,5]` |
| 3 | 3 | 0 | 5 | 5==5 → skip | `[5,5,5,5,5]` |
| 4 | 4 | 0 | 5 | 5==5 → skip | `[5,5,5,5,5]` |

**Result:** k = **1**, first element = `[5]` ✅  
**Writes performed: 0** (no new unique elements found after the first)

---

### 🔍 Edge Case: All Unique (No Duplicates)

**Input:** `nums = [1, 2, 3, 4, 5]`

| Step | read | write | nums[read] | nums[write] | Action | Array |
|------|------|-------|------------|-------------|--------|-------|
| 1 | 1 | 0 | 2 | 1 | 2≠1 → write=1, nums[1]=2 | `[1,2,3,4,5]` |
| 2 | 2 | 1 | 3 | 2 | 3≠2 → write=2, nums[2]=3 | `[1,2,3,4,5]` |
| 3 | 3 | 2 | 4 | 3 | 4≠3 → write=3, nums[3]=4 | `[1,2,3,4,5]` |
| 4 | 4 | 3 | 5 | 4 | 5≠4 → write=4, nums[4]=5 | `[1,2,3,4,5]` |

**Result:** k = **5**, array unchanged ✅  
> 📌 Every element is written to its **own** position (write+1 == read at each step). No data is actually moved — just "confirmed" in place.

---

### 🔍 Edge Case: Single Element

**Input:** `nums = [7]`

| Step | Action |
|------|--------|
| — | Loop doesn't execute (read starts at 1, length=1). |

**Result:** k = write + 1 = **1** ✅

---

### 🔍 Why This Works — The Sorted Property

```
Sorted array: [0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 4, 4]
               ─────────  ────  ─────────────  ─  ───
               group of 0  grp 1  group of 2    3  grp 4

Key property: All occurrences of a value are CONTIGUOUS.
∴ nums[read] != nums[write] ⟺ we've entered a NEW group (new distinct value).
∴ No HashSet, no extra memory needed — just compare adjacent "group leaders".
```

---

### 🔍 Extension: Allow At Most Two Duplicates (LeetCode 80)

The same two-pointer idea generalizes. Instead of comparing with `nums[write]`, compare with `nums[write - 1]`:

```java
// LeetCode 80: Remove Duplicates from Sorted Array II (allow at most 2)
public int removeDuplicates(int[] nums) {
    if (nums.length <= 2) return nums.length;

    int write = 2;  // first two elements are always valid
    for (int read = 2; read < nums.length; read++) {
        if (nums[read] != nums[write - 2]) {
            nums[write] = nums[read];
            write++;
        }
    }
    return write;
}
```

> 📌 The pattern generalizes: for "at most `k` duplicates", initialize `write = k` and compare `nums[read] != nums[write - k]`.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force (Shift) vs Extra Array vs Two Pointers

| Metric | Shift-on-Duplicate | Extra Array | Two Pointers (Slow/Fast) |
|--------|-------------------|-------------|--------------------------|
| Time | O(n²) | O(n) | **O(n)** |
| Space | O(1) | O(n) | **O(1)** |
| In-place? | ✅ | ❌ (extra array) | **✅** |
| Passes | 1 (with inner loops) | 2 (copy + write back) | **1** |
| Writes | O(n²) worst case | n (copy) + k (write back) | k (only unique placements) |
| Exploits sorted order? | Partially (detects adjacent dups) | ✅ | **✅** |
| Code complexity | Moderate (shift logic) | Simple | **Very simple (6 lines)** |

---

## Extra Array vs Two Pointers (Head-to-Head)

| Metric | Extra Array | Two Pointers |
|--------|-------------|--------------|
| Time | O(n) | O(n) |
| Space | O(n) | **O(1)** |
| Allocates memory? | ✅ (new int[n]) | **❌** |
| GC pressure | Creates one large array | **Zero** |
| Modifies original during scan? | No (reads original, writes to copy) | Yes (overwrites in-place) |
| Interview value | Shows understanding | **Expected optimal answer** |

**Verdict:** Two pointers is strictly better — same time, zero extra space, single pass.

---

## Operation Count Analysis

**Input:** `nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]` (n=10, k=5 unique)

| Approach | Writes to array |
|----------|----------------|
| Shift-on-Duplicate | 9+7+6+5+4 = **31 writes** |
| Extra Array | 5 (to unique[]) + 5 (copy back) = **10 writes** |
| **Two Pointers** | **4 writes** (only when new unique found: steps 2,5,7,9) |

> 📌 Two pointers performs the **minimum possible writes** — one per new unique element (minus the first, which is already in place).

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | In-Place? | Writes | Key Insight |
|----------|------|-------|-----------|--------|-------------|
| Shift-on-Duplicate | O(n²) | O(1) | ✅ | O(n²) | Remove dup, shift tail left |
| Extra Array | O(n) | O(n) | ❌ | O(n) | Copy uniques to new array |
| **Two Pointers (Slow/Fast)** | **O(n)** | **O(1)** | **✅** | **O(k)** | **Compare with write pointer; overwrite in-place** |

---

### 🎯 What to Present to the Interviewer

1. **Immediately note:** "The array is sorted, so all duplicates are adjacent. We can detect a new unique value by comparing with the last placed unique."
2. **Mention brute force** briefly: shifting elements on each duplicate is O(n²). Unnecessary.
3. **Propose the two-pointer (slow/fast) approach:**
   - `write` = index of last unique element placed.
   - `read` scans from index 1.
   - If `nums[read] != nums[write]` → new unique → `write++`, `nums[write] = nums[read]`.
4. **Walk through** `[0,0,1,1,1,2,2,3,3,4]`:
   - read=1: 0==0, skip.
   - read=2: 1≠0, write to index 1.
   - read=3,4: 1==1, skip.
   - read=5: 2≠1, write to index 2.
   - ... final k=5.
5. **Emphasize:** O(n) time, O(1) space, in-place, single pass. Modifies only the first k positions.
6. **Mention the generalization:** "For 'at most two duplicates' (LeetCode 80), initialize write=2 and compare `nums[read] != nums[write-2]`. Same pattern."
7. **If asked about the tail:** "Elements beyond index k-1 are irrelevant per the problem statement. We don't need to zero them out."

**One‑sentence summary:**  
*Exploit the sorted property with a slow pointer (write position) and fast pointer (scanner): whenever a new distinct value is found, place it at the next write position, compressing the array in O(n) time and O(1) space.*