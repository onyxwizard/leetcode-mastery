### 📘 Chapter: Arrays & Strings  
### 📌 Problem 8: Longest Consecutive Sequence (LeetCode 128)

---

**Input**  
- `nums`: an unsorted integer array (may contain duplicates).

**Output**  
- Length of the **longest consecutive elements sequence** (consecutive in **value**, not in position).

**Constraints**  
- `0 <= nums.length <= 10⁵`  
- `-10⁹ <= nums[i] <= 10⁹`

**Requirement**  
- Algorithm must run in **O(n)** time.

**Example**  
```
Input:  nums = [100, 4, 200, 1, 3, 2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4]. Length = 4.

Input:  nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
Output: 9
Explanation: The longest consecutive sequence is [0, 1, 2, 3, 4, 5, 6, 7, 8]. Length = 9.

Input:  nums = []
Output: 0
```

**Follow-up**  
- What if the array is a stream (numbers arrive one at a time)? (Use a HashMap storing interval boundaries.)
- What if duplicates are guaranteed absent? (Simplifies slightly, but algorithm is unchanged.)

---

### 🧠 Core Idea

We need the longest chain of **numerically consecutive** values (e.g., 1→2→3→4), regardless of their positions in the array.

- **Brute force (nested scan):** For each number, repeatedly search the array for `num+1`, `num+2`, etc. O(n²)–O(n³).
- **Sorting:** Sort first, then linear scan for streaks. O(n log n). ❌ Violates the O(n) requirement.
- **HashSet + Sequence-Start Detection (optimal):** Insert all numbers into a HashSet. For each number, check if it's the **start** of a sequence (`num-1` NOT in set). If yes, count upward. Each element is visited at most **twice** total → O(n). ✅

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACHES

---

## 1A. Naive Nested Scan (O(n²) to O(n³))

**Idea:** For each element `nums[i]`, try to build the consecutive sequence starting at `nums[i]` by repeatedly searching the **entire array** for `nums[i]+1`, `nums[i]+2`, etc. Track the longest streak found.

**Time:** O(n²) average, O(n³) worst case (if many overlapping sequences).  
**Space:** O(1).

```java
public int longestConsecutive(int[] nums) {
    int longest = 0;

    for (int i = 0; i < nums.length; i++) {
        int currentNum = nums[i];
        int currentStreak = 1;

        // Search for the next consecutive number by scanning the whole array
        while (arrayContains(nums, currentNum + 1)) {
            currentNum++;
            currentStreak++;
        }

        longest = Math.max(longest, currentStreak);
    }

    return longest;
}

private boolean arrayContains(int[] arr, int target) {
    for (int val : arr) {
        if (val == target) return true;
    }
    return false;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [100, 4, 200, 1, 3, 2]`

| Outer i | nums[i] | Inner while: search for next | Streak | longest |
|---------|---------|------------------------------|--------|---------|
| 0 | 100 | Search for 101 → scan all 6 elements → NOT found | 1 | 1 |
| 1 | 4 | Search for 5 → scan all 6 → NOT found | 1 | 1 |
| 2 | 200 | Search for 201 → scan all 6 → NOT found | 1 | 1 |
| 3 | 1 | Search for 2 → scan → **found!** currentNum=2. Search for 3 → **found!** currentNum=3. Search for 4 → **found!** currentNum=4. Search for 5 → NOT found. | **4** | **4** |
| 4 | 3 | Search for 4 → found. Search for 5 → NOT found. | 2 | 4 |
| 5 | 2 | Search for 3 → found. Search for 4 → found. Search for 5 → NOT found. | 3 | 4 |

**Result:** `4`

> ⚠️ **Massive redundancy:** The sequence `1→2→3→4` is counted **four times** (starting from 1, 2, 3, and 4). Each "search for next" scans the entire array → O(n) per lookup. Total: O(n²) to O(n³).

---

## 1B. Sorting Approach (O(n log n))

**Idea:** Sort the array. Then scan linearly:
- If `nums[i] == nums[i-1]` → skip (duplicate).
- If `nums[i] == nums[i-1] + 1` → extend current streak.
- Otherwise → reset streak to 1.

Track the maximum streak.

**Time:** O(n log n) — sorting dominates.  
**Space:** O(1) if in-place sort (or O(n) for Java's `Arrays.sort` on objects).  
❌ **Does NOT meet the O(n) requirement.**

```java
import java.util.Arrays;

public int longestConsecutive(int[] nums) {
    if (nums.length == 0) return 0;

    Arrays.sort(nums);

    int longest = 1;
    int current = 1;

    for (int i = 1; i < nums.length; i++) {
        if (nums[i] == nums[i - 1]) {
            continue;  // skip duplicates
        }
        if (nums[i] == nums[i - 1] + 1) {
            current++;  // extend streak
        } else {
            longest = Math.max(longest, current);
            current = 1;  // reset
        }
    }

    return Math.max(longest, current);
}
```

### 🔍 Sample Iteration

**Input:** `nums = [100, 4, 200, 1, 3, 2]`  
**After sorting:** `[1, 2, 3, 4, 100, 200]`

| i | nums[i] | nums[i-1] | Condition | current | longest |
|---|---------|-----------|-----------|---------|---------|
| 1 | 2 | 1 | 2 == 1+1 ✅ consecutive | 2 | 1 |
| 2 | 3 | 2 | 3 == 2+1 ✅ consecutive | 3 | 1 |
| 3 | 4 | 3 | 4 == 3+1 ✅ consecutive | 4 | 1 |
| 4 | 100 | 4 | 100 ≠ 4+1 → gap! | reset → 1 | max(1,4) = **4** |
| 5 | 200 | 100 | 200 ≠ 100+1 → gap! | reset → 1 | max(4,1) = **4** |
| END | — | — | — | — | max(4,1) = **4** |

**Result:** `4` ✅

**With duplicates:** `nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]`  
**After sorting:** `[0, 0, 1, 2, 3, 4, 5, 6, 7, 8]`

| i | nums[i] | nums[i-1] | Condition | current | longest |
|---|---------|-----------|-----------|---------|---------|
| 1 | 0 | 0 | **Equal → skip** (duplicate) | 1 | 1 |
| 2 | 1 | 0 | 1 == 0+1 ✅ | 2 | 1 |
| 3 | 2 | 1 | 2 == 1+1 ✅ | 3 | 1 |
| 4 | 3 | 2 | 3 == 2+1 ✅ | 4 | 1 |
| 5 | 4 | 3 | 4 == 3+1 ✅ | 5 | 1 |
| 6 | 5 | 4 | 5 == 4+1 ✅ | 6 | 1 |
| 7 | 6 | 5 | 6 == 5+1 ✅ | 7 | 1 |
| 8 | 7 | 6 | 7 == 6+1 ✅ | 8 | 1 |
| 9 | 8 | 7 | 8 == 7+1 ✅ | 9 | 1 |
| END | — | — | — | — | max(1,9) = **9** |

**Result:** `9` ✅

> ⚠️ Sorting takes O(n log n). For n = 10⁵, that's ~1.7 million comparisons. The problem **explicitly requires O(n)**, so this approach is disqualified despite being correct.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. HashSet + Sequence-Start Detection (O(n) Time)

**Idea:**  
1. Insert **all** numbers into a `HashSet` → O(1) lookup.
2. For each number `num` in the set:
   - **Check if it's a sequence start:** `num - 1` is NOT in the set.
   - If NOT a start → skip (it will be counted when we process the actual start).
   - If IS a start → count upward: `num+1`, `num+2`, ... while they exist in the set.
3. Track the maximum streak.

**Why O(n)?**  
- The outer loop visits each element once: O(n).
- The inner `while` loop **only fires for sequence starts**. Across ALL starts, the total inner iterations = n (each element is part of exactly one sequence and is counted once).
- Total: O(n) + O(n) = **O(n)**.

**Time:** O(n) — each element touched at most twice (once in outer loop, once in a while loop).  
**Space:** O(n) — HashSet stores all unique numbers.

```java
import java.util.HashSet;
import java.util.Set;

public int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int num : nums) {
        set.add(num);
    }

    int longest = 0;

    for (int num : set) {
        // Only start counting if num is the BEGINNING of a sequence
        if (!set.contains(num - 1)) {
            int currentNum = num;
            int currentStreak = 1;

            // Count upward
            while (set.contains(currentNum + 1)) {
                currentNum++;
                currentStreak++;
            }

            longest = Math.max(longest, currentStreak);
        }
    }

    return longest;
}
```

### 🔍 Sample Iteration

**Input:** `nums = [100, 4, 200, 1, 3, 2]`  
**HashSet:** `{100, 4, 200, 1, 3, 2}`

| Outer num | `num-1` in set? | Sequence start? | Inner while (count upward) | Streak | longest |
|-----------|-----------------|-----------------|----------------------------|--------|---------|
| 100 | 99 in set? **No** | ✅ YES | 101 in set? No → stop | 1 | 1 |
| 4 | 3 in set? **Yes** | ❌ NO → **SKIP** | — | — | 1 |
| 200 | 199 in set? **No** | ✅ YES | 201 in set? No → stop | 1 | 1 |
| 1 | 0 in set? **No** | ✅ YES | 2 in set? **Yes** → currentNum=2, streak=2. 3 in set? **Yes** → currentNum=3, streak=3. 4 in set? **Yes** → currentNum=4, streak=4. 5 in set? No → stop. | **4** | **4** |
| 3 | 2 in set? **Yes** | ❌ NO → **SKIP** | — | — | 4 |
| 2 | 1 in set? **Yes** | ❌ NO → **SKIP** | — | — | 4 |

**Result:** `4` ✅

> 📌 **Key insight:** Numbers 2, 3, 4 are **skipped** in the outer loop because `num-1` exists in the set. Only `1` (the true start) triggers the inner while loop. The sequence `1→2→3→4` is counted **exactly once**.

---

### 🔍 Detailed Inner While Loop Trace (starting from num=1)

```
num = 1, num-1 = 0 NOT in set → START!

  currentNum = 1, currentStreak = 1
  │
  ├─ set.contains(2)? YES → currentNum = 2, currentStreak = 2
  │
  ├─ set.contains(3)? YES → currentNum = 3, currentStreak = 3
  │
  ├─ set.contains(4)? YES → currentNum = 4, currentStreak = 4
  │
  └─ set.contains(5)? NO → STOP

  longest = max(0, 4) = 4
```

---

### 🔍 Sample Iteration (With Duplicates)

**Input:** `nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]`  
**HashSet (duplicates removed):** `{0, 1, 2, 3, 4, 5, 6, 7, 8}`

| Outer num | `num-1` in set? | Start? | Inner while | Streak | longest |
|-----------|-----------------|--------|-------------|--------|---------|
| 0 | -1 in set? **No** | ✅ YES | 1✓→2✓→3✓→4✓→5✓→6✓→7✓→8✓→9✗ | **9** | **9** |
| 1 | 0 in set? **Yes** | ❌ SKIP | — | — | 9 |
| 2 | 1 in set? **Yes** | ❌ SKIP | — | — | 9 |
| 3 | 2 in set? **Yes** | ❌ SKIP | — | — | 9 |
| 4 | 3 in set? **Yes** | ❌ SKIP | — | — | 9 |
| 5 | 4 in set? **Yes** | ❌ SKIP | — | — | 9 |
| 6 | 5 in set? **Yes** | ❌ SKIP | — | — | 9 |
| 7 | 6 in set? **Yes** | ❌ SKIP | — | — | 9 |
| 8 | 7 in set? **Yes** | ❌ SKIP | — | — | 9 |

**Result:** `9` ✅

> 📌 The inner while loop fires **only once** (for `num=0`). All other 8 elements are skipped. Total operations: 9 (outer) + 8 (inner) = 17 ≈ O(n).

---

### 🔍 Amortized O(n) Proof (Visual)

```
Array: [100, 4, 200, 1, 3, 2]
Set:   {1, 2, 3, 4, 100, 200}

Sequences in the set:
  [1, 2, 3, 4]   ← length 4, start = 1
  [100]          ← length 1, start = 100
  [200]          ← length 1, start = 200

Outer loop visits: 6 elements (each checked for "is start?")
Inner loop visits: 4 + 1 + 1 = 6 elements total (each counted once in its sequence)

Total work: 6 + 6 = 12 = O(n) ✓
```

**General argument:**  
- Outer loop: iterates over each unique element once → O(n).  
- Inner while loop: across ALL sequence starts, the total iterations = (sum of all sequence lengths) = n.  
- Combined: O(n) + O(n) = **O(n)**.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force (Nested Scan) vs Sorting vs HashSet

| Metric | Naive Nested Scan | Sorting | HashSet + Start Detection |
|--------|-------------------|---------|--------------------------|
| Time | O(n²) to O(n³) | O(n log n) | **O(n)** |
| Space | O(1) | O(1) or O(n) | O(n) |
| Meets O(n) requirement? | ❌ No | ❌ No | ✅ **Yes** |
| Handles duplicates? | ❌ Overcounts | ✅ (skip logic) | ✅ (Set deduplicates) |
| Handles negatives/large range? | ✅ | ✅ | ✅ |
| Code complexity | Simple but slow | Moderate | Moderate |

---

## Sorting vs HashSet (Head-to-Head)

| Metric | Sorting | HashSet |
|--------|---------|---------|
| Time | O(n log n) | **O(n)** |
| Space | O(1) in-place | O(n) |
| Modifies input? | ✅ Yes (sorts in place) | ❌ No |
| Duplicate handling | Explicit skip (`nums[i]==nums[i-1]`) | Automatic (Set) |
| Interview value | Shows baseline thinking | **Expected answer** |
| When acceptable | If O(n) constraint is relaxed | **Always preferred here** |

**Verdict:** HashSet is the **only** approach meeting the O(n) requirement. Sorting is a valid fallback if the constraint were O(n log n).

---

## HashSet: With vs Without "Start" Optimization

| Metric | Without Start Check | With Start Check |
|--------|--------------------|--------------------|
| Logic | For EVERY num, count upward | Only count from sequence **starts** |
| Worst-case time | O(n²) — e.g., `[1,2,3,...,n]` counts from every element | **O(n)** — counts only from `1` |
| Inner loop total | n + (n-1) + ... + 1 = O(n²) | n (each element counted once) |
| Code difference | Remove the `if (!set.contains(num-1))` guard | Keep the guard |

> ⚠️ Without the start-check, the input `[1, 2, 3, ..., 100000]` would trigger the inner while loop 100,000 times (from 1, from 2, from 3, ...) → O(n²). The single `if (!set.contains(num - 1))` guard is what makes it O(n).

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | O(n)? | Key Insight |
|----------|------|-------|-------|-------------|
| Naive Nested Scan | O(n²)–O(n³) | O(1) | ❌ | Search entire array for each next value |
| Sorting | O(n log n) | O(1) | ❌ | Sort → linear scan for streaks |
| HashSet (no start check) | O(n²) worst | O(n) | ❌ | Count from every element (redundant) |
| **HashSet + Start Detection** | **O(n)** | **O(n)** | **✅** | **Only expand from sequence starts (`num-1` absent)** |

---

### 🎯 What to Present to the Interviewer

1. **Immediately acknowledge** the O(n) requirement → sorting (O(n log n)) is disqualified.
2. **Propose the HashSet idea:**
   - Insert all numbers → O(1) lookup.
   - For each number, check if it's a **sequence start** (`num - 1` NOT in set).
   - If yes, count upward (`num+1`, `num+2`, ...) while they exist.
3. **Stress the amortized O(n) argument:**
   - Outer loop: O(n) iterations.
   - Inner while loop: fires only for starts; total inner iterations across all starts = n.
   - Combined: O(n).
4. **Walk through** the example `[100, 4, 200, 1, 3, 2]`:
   - 100 → start (99 absent) → streak 1.
   - 4 → NOT start (3 exists) → skip.
   - 200 → start → streak 1.
   - 1 → start (0 absent) → streak 4 (1→2→3→4).
   - 3, 2 → NOT start → skip.
5. **Mention sorting** as a simpler O(n log n) fallback if the constraint were relaxed.
6. **If asked about duplicates:** The HashSet automatically deduplicates; no extra logic needed.
7. **If asked about edge cases:** Empty array → return 0. Single element → return 1. All duplicates → return 1.

**One‑sentence summary:**  
*Insert all numbers into a HashSet, then expand sequences only from elements whose predecessor (`num-1`) is absent — each element is visited at most twice, achieving true O(n) time.*