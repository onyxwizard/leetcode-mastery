### 📘 Chapter: Two Pointers  
### 📌 Problem 2: 3Sum (LeetCode 15)

---

**Input**  
- `nums`: integer array of length `n`.

**Output**  
- All **unique triplets** `[nums[i], nums[j], nums[k]]` such that `i ≠ j ≠ k` and `nums[i] + nums[j] + nums[k] == 0`. No duplicate triplets in the output.

**Constraints**  
- `3 <= nums.length <= 3000`  
- `-10⁵ <= nums[i] <= 10⁵`

**Example**  
```
Input:  nums = [-1, 0, 1, 2, -1, -4]
Output: [[-1, -1, 2], [-1, 0, 1]]
Explanation: 
  (-1) + (-1) + 2 = 0
  (-1) + 0 + 1 = 0
  No other unique triplets sum to 0.

Input:  nums = [0, 1, 1]
Output: []
Explanation: No triplet sums to 0.

Input:  nums = [0, 0, 0]
Output: [[0, 0, 0]]
```

**Follow-up**  
- The problem inherently requires better than O(n³). The standard goal is **O(n²) time** with correct duplicate handling.

---

### 🧠 Core Idea

This is an extension of **Two Sum** to three numbers, with the added challenge of returning **all unique triplets**.

- **Brute force:** Try all O(n³) triplets, use a Set to deduplicate. Too slow for n = 3000.
- **Sorting + Two Pointers (optimal):** Sort first. Fix one element `nums[i]`, then use two pointers to find pairs summing to `-nums[i]` in O(n). Skip duplicates by advancing past identical values. O(n²) time, O(1) extra space.
- **Sorting + HashSet:** Fix `nums[i]`, iterate `j`, check if complement exists in a HashSet. O(n²) time, O(n) space. Messier duplicate handling.

**Why sorting is the key enabler:**
1. Enables the **two-pointer technique** (O(n) pair search instead of O(n²)).
2. Makes **duplicate skipping trivial** (identical values become adjacent).

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Three Nested Loops + HashSet for Dedup (O(n³) Time)

**Idea:** Try every triplet `(i, j, k)` with `i < j < k`. If the sum is 0, sort the triplet and add to a `Set<List<Integer>>` to eliminate duplicates.

**Time:** O(n³) — C(n,3) triplets checked.  
**Space:** O(n) — HashSet stores unique triplets.

```java
import java.util.*;

public List<List<Integer>> threeSum(int[] nums) {
    int n = nums.length;
    Set<List<Integer>> resultSet = new HashSet<>();

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            for (int k = j + 1; k < n; k++) {
                if (nums[i] + nums[j] + nums[k] == 0) {
                    List<Integer> triplet = Arrays.asList(nums[i], nums[j], nums[k]);
                    Collections.sort(triplet);  // normalize for dedup
                    resultSet.add(triplet);
                }
            }
        }
    }

    return new ArrayList<>(resultSet);
}
```

### 🔍 Sample Iteration

**Input:** `nums = [-1, 0, 1, 2, -1, -4]`, n = 6

| i | j | k | nums[i]+nums[j]+nums[k] | Sum==0? | Triplet (sorted) | resultSet |
|---|---|---|-------------------------|---------|------------------|-----------|
| 0 | 1 | 2 | -1+0+1 = **0** | ✅ | [-1, 0, 1] | {[-1,0,1]} |
| 0 | 1 | 3 | -1+0+2 = 1 | ❌ | — | — |
| 0 | 1 | 4 | -1+0+(-1) = -2 | ❌ | — | — |
| 0 | 1 | 5 | -1+0+(-4) = -5 | ❌ | — | — |
| 0 | 2 | 3 | -1+1+2 = 2 | ❌ | — | — |
| 0 | 2 | 4 | -1+1+(-1) = -1 | ❌ | — | — |
| 0 | 2 | 5 | -1+1+(-4) = -4 | ❌ | — | — |
| 0 | 3 | 4 | -1+2+(-1) = **0** | ✅ | [-1, -1, 2] | {[-1,0,1], [-1,-1,2]} |
| 0 | 3 | 5 | -1+2+(-4) = -3 | ❌ | — | — |
| 0 | 4 | 5 | -1+(-1)+(-4) = -6 | ❌ | — | — |
| 1 | 2 | 3 | 0+1+2 = 3 | ❌ | — | — |
| 1 | 2 | 4 | 0+1+(-1) = **0** | ✅ | [-1, 0, 1] | {[-1,0,1], [-1,-1,2]} *(dup!)* |
| 1 | 2 | 5 | 0+1+(-4) = -3 | ❌ | — | — |
| 1 | 3 | 4 | 0+2+(-1) = 1 | ❌ | — | — |
| 1 | 3 | 5 | 0+2+(-4) = -2 | ❌ | — | — |
| 1 | 4 | 5 | 0+(-1)+(-4) = -5 | ❌ | — | — |
| 2 | 3 | 4 | 1+2+(-1) = 2 | ❌ | — | — |
| 2 | 3 | 5 | 1+2+(-4) = -1 | ❌ | — | — |
| 2 | 4 | 5 | 1+(-1)+(-4) = -4 | ❌ | — | — |
| 3 | 4 | 5 | 2+(-1)+(-4) = -3 | ❌ | — | — |

**Total triplets checked:** C(6,3) = **20**  
**Valid triplets found:** 3 (but one is a duplicate)  
**Unique result:** `[[-1, -1, 2], [-1, 0, 1]]` ✅

> ⚠️ For n = 3000: C(3000, 3) ≈ **4.5 × 10⁹** triplets. **Far too slow.** Plus, sorting each triplet for dedup adds overhead.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACHES

---

## 2A. Sorting + Two Pointers (O(n²) Time, O(1) Extra Space) ✅

**Idea:**  
1. **Sort** the array.  
2. Iterate `i` from `0` to `n-3` (fix the first element of the triplet).  
   - Skip duplicate `i` values: if `nums[i] == nums[i-1]`, continue.  
   - **Early termination:** if `nums[i] > 0`, no further triplet can sum to 0 (all remaining are positive).  
3. Set `left = i+1`, `right = n-1`. While `left < right`:  
   - Compute `sum = nums[i] + nums[left] + nums[right]`.  
   - If `sum == 0`: add triplet. Skip duplicates for `left` and `right`. Move both inward.  
   - If `sum < 0`: need a larger value → `left++`.  
   - If `sum > 0`: need a smaller value → `right--`.

**Time:** O(n²) — outer loop O(n), inner two-pointer O(n) per iteration.  
**Space:** O(1) extra (ignoring output; sorting uses O(log n) stack).

```java
import java.util.*;

public List<List<Integer>> threeSum(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(nums);
    int n = nums.length;

    for (int i = 0; i < n - 2; i++) {
        // Skip duplicate first elements
        if (i > 0 && nums[i] == nums[i - 1]) continue;

        // Early termination: if smallest element > 0, no triplet can sum to 0
        if (nums[i] > 0) break;

        int left = i + 1, right = n - 1;

        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];

            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));

                // Skip duplicates for left pointer
                while (left < right && nums[left] == nums[left + 1]) left++;
                // Skip duplicates for right pointer
                while (left < right && nums[right] == nums[right - 1]) right--;

                left++;
                right--;
            } else if (sum < 0) {
                left++;   // need larger sum
            } else {
                right--;  // need smaller sum
            }
        }
    }

    return result;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [-1, 0, 1, 2, -1, -4]`  
**After sorting:** `[-4, -1, -1, 0, 1, 2]`

```
Index:  0   1   2   3   4   5
Value: -4  -1  -1   0   1   2
```

---

#### Outer loop: i = 0, nums[i] = -4

| left | right | sum = -4 + nums[L] + nums[R] | Comparison | Action |
|------|-------|------------------------------|------------|--------|
| 1 | 5 | -4 + (-1) + 2 = **-3** | < 0 | left++ |
| 2 | 5 | -4 + (-1) + 2 = **-3** | < 0 | left++ |
| 3 | 5 | -4 + 0 + 2 = **-2** | < 0 | left++ |
| 4 | 5 | -4 + 1 + 2 = **-1** | < 0 | left++ |
| 5 | 5 | left ≥ right → **STOP** | — | — |

→ No triplet with -4.

---

#### Outer loop: i = 1, nums[i] = -1

*(i=1 > 0 and nums[1] == nums[0]? -1 ≠ -4 → no skip)*

| left | right | sum = -1 + nums[L] + nums[R] | Comparison | Action |
|------|-------|------------------------------|------------|--------|
| 2 | 5 | -1 + (-1) + 2 = **0** | == 0 ✅ | **ADD [-1, -1, 2]**. Skip dups: nums[2]==nums[3]? -1≠0, no skip. nums[5]==nums[4]? 2≠1, no skip. left=3, right=4. |
| 3 | 4 | -1 + 0 + 1 = **0** | == 0 ✅ | **ADD [-1, 0, 1]**. Skip dups: nums[3]==nums[4]? 0≠1, no skip. left=4, right=3. |
| 4 | 3 | left ≥ right → **STOP** | — | — |

→ Found 2 triplets.

---

#### Outer loop: i = 2, nums[i] = -1

*(i=2 > 0 and nums[2] == nums[1]? -1 == -1 → **SKIP!** Duplicate first element.)*

→ Skipped entirely.

---

#### Outer loop: i = 3, nums[i] = 0

| left | right | sum = 0 + nums[L] + nums[R] | Comparison | Action |
|------|-------|------------------------------|------------|--------|
| 4 | 5 | 0 + 1 + 2 = **3** | > 0 | right-- |
| 4 | 4 | left ≥ right → **STOP** | — | — |

→ No triplet with 0 as first element.

---

#### Outer loop: i = 4, nums[i] = 1

*(nums[4] = 1 > 0 → **BREAK!** All remaining elements are positive; no triplet can sum to 0.)*

---

**Final result:** `[[-1, -1, 2], [-1, 0, 1]]` ✅

---

### 🔍 Visual Pointer Movement

```
Sorted: [-4, -1, -1, 0, 1, 2]

i=0 (val=-4):
  [-4, -1, -1, 0, 1, 2]
   i   L→→→→→→→→→R     sum always < 0, left advances until meeting right

i=1 (val=-1):
  [-4, -1, -1, 0, 1, 2]
       i   L         R   sum = -1+(-1)+2 = 0 ✅ ADD [-1,-1,2]
       i      L   R      sum = -1+0+1 = 0 ✅ ADD [-1,0,1]
       i        L=R       STOP

i=2 (val=-1):
  [-4, -1, -1, 0, 1, 2]
           i              SKIP (same as i=1)

i=3 (val=0):
  [-4, -1, -1, 0, 1, 2]
               i  L  R   sum = 0+1+2 = 3 > 0, right-- → STOP

i=4 (val=1):
  BREAK (nums[i] > 0)
```

---

### 🔍 Duplicate Skipping — Detailed Trace

**Why duplicates occur:** After sorting, identical values are adjacent. If we don't skip them, we generate the same triplet multiple times.

**Three levels of dedup:**

| Level | Where | How | Example |
|-------|-------|-----|---------|
| First element (`i`) | Outer loop | `if (i > 0 && nums[i] == nums[i-1]) continue` | i=2 skipped because nums[2]==nums[1]==-1 |
| Second element (`left`) | After finding sum==0 | `while (left < right && nums[left] == nums[left+1]) left++` | If nums = [-2,0,0,2,2], after finding [-2,0,2], skip the second 0 |
| Third element (`right`) | After finding sum==0 | `while (left < right && nums[right] == nums[right-1]) right--` | Same example: skip the second 2 |

**Example with heavy duplicates:** `nums = [-2, 0, 0, 2, 2]`

Sorted: `[-2, 0, 0, 2, 2]`

| i | left | right | sum | Action |
|---|------|-------|-----|--------|
| 0 (val=-2) | 1 | 4 | -2+0+2=0 ✅ | ADD [-2,0,2]. Skip: nums[1]==nums[2]? 0==0 → left=2. nums[4]==nums[3]? 2==2 → right=3. Then left=3, right=2 → STOP. |

→ Only **one** triplet `[-2, 0, 2]` despite two 0s and two 2s. ✅

---

## 2B. Sorting + HashSet (O(n²) Time, O(n) Space)

**Idea:**  
1. Sort the array (for dedup of first element).  
2. For each `i` (skipping duplicates), iterate `j` from `i+1` to end.  
3. Maintain a `HashSet<Integer>` of values seen in the inner loop.  
4. Compute `complement = -nums[i] - nums[j]`. If complement is in the set → triplet found.  
5. Use a `Set<List<Integer>>` for the result to handle remaining duplicates.

**Time:** O(n²) — outer O(n), inner O(n) with O(1) HashSet lookup.  
**Space:** O(n) — HashSet for inner loop + result set for dedup.

```java
import java.util.*;

public List<List<Integer>> threeSum(int[] nums) {
    Set<List<Integer>> resultSet = new HashSet<>();
    Arrays.sort(nums);
    int n = nums.length;

    for (int i = 0; i < n - 2; i++) {
        // Skip duplicate first elements
        if (i > 0 && nums[i] == nums[i - 1]) continue;

        Set<Integer> seen = new HashSet<>();
        for (int j = i + 1; j < n; j++) {
            int complement = -nums[i] - nums[j];
            if (seen.contains(complement)) {
                // Triplet found: nums[i], complement, nums[j] (sorted order)
                resultSet.add(Arrays.asList(nums[i], complement, nums[j]));
            }
            seen.add(nums[j]);
        }
    }

    return new ArrayList<>(resultSet);
}
```

### 🔍 Sample Iteration

**Input:** `nums = [-1, 0, 1, 2, -1, -4]`  
**After sorting:** `[-4, -1, -1, 0, 1, 2]`

---

#### i = 0, nums[i] = -4

| j | nums[j] | complement = -(-4) - nums[j] = 4 - nums[j] | seen (before) | complement in seen? | Action | seen (after) |
|---|---------|---------------------------------------------|---------------|---------------------|--------|--------------|
| 1 | -1 | 4-(-1) = 5 | {} | No | — | {-1} |
| 2 | -1 | 5 | {-1} | No | — | {-1} |
| 3 | 0 | 4 | {-1} | No | — | {-1, 0} |
| 4 | 1 | 3 | {-1, 0} | No | — | {-1, 0, 1} |
| 5 | 2 | 2 | {-1, 0, 1} | No | — | {-1, 0, 1, 2} |

→ No triplet with -4.

---

#### i = 1, nums[i] = -1

| j | nums[j] | complement = 1 - nums[j] | seen (before) | In seen? | Action | seen (after) |
|---|---------|--------------------------|---------------|----------|--------|--------------|
| 2 | -1 | 1-(-1) = 2 | {} | No | — | {-1} |
| 3 | 0 | 1-0 = 1 | {-1} | No | — | {-1, 0} |
| 4 | 1 | 1-1 = 0 | {-1, 0} | **Yes!** | **ADD [-1, 0, 1]** | {-1, 0, 1} |
| 5 | 2 | 1-2 = -1 | {-1, 0, 1} | **Yes!** | **ADD [-1, -1, 2]** | {-1, 0, 1, 2} |

→ Found 2 triplets.

---

#### i = 2, nums[i] = -1

*(nums[2] == nums[1] → **SKIP**)*

---

#### i = 3, nums[i] = 0

| j | nums[j] | complement = 0 - nums[j] | seen | In seen? | Action |
|---|---------|--------------------------|------|----------|--------|
| 4 | 1 | -1 | {} | No | — |
| 5 | 2 | -2 | {1} | No | — |

→ No triplet.

---

**resultSet:** `{[-1, 0, 1], [-1, -1, 2]}`  
**Final result:** `[[-1, -1, 2], [-1, 0, 1]]` ✅

> 📌 The HashSet approach finds the same triplets but uses O(n) extra space for the `seen` set and the `resultSet`. The two-pointer approach avoids both.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Two Pointers vs HashSet

| Metric | Three Nested Loops | Sorting + Two Pointers | Sorting + HashSet |
|--------|-------------------|----------------------|-------------------|
| Time | O(n³) | **O(n²)** | O(n²) |
| For n=3000 | ~4.5 × 10⁹ ops → **TLE** | ~9 × 10⁶ ops → fast | ~9 × 10⁶ ops → fast |
| Extra Space | O(k) for result set | **O(1)** | O(n) for seen + result set |
| Duplicate handling | Sort each triplet + Set | Skip adjacent duplicates (elegant) | Set for results (less elegant) |
| Modifies input? | No | Yes (sorts) | Yes (sorts) |
| Code clarity | Simple but slow | Clean, standard | Moderate (complement logic) |

---

## Two Pointers vs HashSet (Head-to-Head)

| Metric | Two Pointers | HashSet |
|--------|-------------|---------|
| Time | O(n²) | O(n²) |
| Space | **O(1)** | O(n) |
| Duplicate handling | **Pointer skipping** (no extra data structure) | Requires `Set<List<Integer>>` for result |
| Inner loop mechanism | Two pointers converging | Linear scan + HashSet lookup |
| Constant factor | Lower (array access only) | Higher (hashing overhead) |
| Interview preference | **Expected gold standard** | Acceptable alternative |
| When to use | Always (for this problem) | If you can't think of two pointers |

**Verdict:** Two pointers is strictly superior — same time, less space, cleaner dedup.

---

## Why Sorting Enables Everything

| Benefit | How |
|---------|-----|
| Two-pointer pair search | Sorted order means: if sum < target → move left right (increase); if sum > target → move right left (decrease). |
| Duplicate skipping | Identical values are adjacent → skip with a simple `while` loop. |
| Early termination | If `nums[i] > 0`, all subsequent values are also > 0 → no triplet can sum to 0. |
| Triplet ordering | Triplets are naturally in sorted order → no need to sort each triplet. |

---

## 🏁 Final Master Comparison Table

| Approach | Time | Extra Space | Dedup Method | Practical? |
|----------|------|-------------|--------------|------------|
| Three Nested Loops + Set | O(n³) | O(k) | Sort triplet + HashSet | ❌ TLE for n=3000 |
| **Sorting + Two Pointers** | **O(n²)** | **O(1)** | **Skip adjacent duplicates** | **✅ Gold standard** |
| Sorting + HashSet | O(n²) | O(n) | ResultSet + skip `i` | ✅ Acceptable |

---

### 🎯 What to Present to the Interviewer

1. **State the baseline:** O(n³) brute force — try all triplets, deduplicate with a Set. Too slow for n=3000.
2. **Propose sorting** as the key enabler: it allows two-pointer pair search and makes duplicate skipping trivial.
3. **Walk through the two-pointer algorithm:**
   - Fix `i` (outer loop). Skip if `nums[i] == nums[i-1]`.
   - Set `left = i+1`, `right = n-1`.
   - Adjust pointers based on sum vs 0.
   - On match: add triplet, skip duplicates for both `left` and `right`, move inward.
4. **Emphasize three levels of dedup:**
   - Skip duplicate `i` in outer loop.
   - Skip duplicate `left` after a match.
   - Skip duplicate `right` after a match.
5. **Mention early termination:** if `nums[i] > 0`, break (all remaining are positive).
6. **Code cleanly** with `Arrays.sort` + while loops.
7. **If asked about alternatives:** mention the HashSet approach (fix `i`, iterate `j`, check complement in set). Note it's O(n²) but uses O(n) space and has messier dedup.
8. **Complexity:** O(n²) time (n outer × n inner), O(1) extra space (or O(log n) for sort stack).

**One‑sentence summary:**  
*Sort the array, then for each element fix it as the first of the triplet and use two converging pointers to find complementary pairs summing to its negation, skipping adjacent duplicates at all three positions to collect unique triplets in O(n²) time and O(1) space.*