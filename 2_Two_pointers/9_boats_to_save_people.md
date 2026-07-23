### 📘 Chapter: Two Pointers  
### 📌 Problem 9: Boats to Save People (LeetCode 881)

---

**Input**  
- `people`: integer array of positive weights.  
- `limit`: maximum weight a single boat can carry.

**Output**  
- The **minimum number of boats** required to rescue everyone, given:  
  - Each boat carries **at most 2 people**.  
  - The sum of their weights must be ≤ `limit`.

**Constraints**  
- `1 <= people.length <= 5 × 10⁴`  
- `1 <= people[i] <= limit <= 3 × 10⁴`

**Example**  
```
Input:  people = [1, 2], limit = 3
Output: 1
Explanation: One boat carries both (1 + 2 = 3 ≤ 3).

Input:  people = [3, 2, 2, 1], limit = 3
Output: 3
Explanation: Boats: (1,2), (2), (3). Three boats total.

Input:  people = [3, 5, 3, 4], limit = 5
Output: 4
Explanation: No two people can share (min pair = 3+3=6 > 5). Each goes alone.
```

**Follow-up**  
- Prove the greedy choice is optimal (exchange argument).  
- What if a boat could carry more than 2 people? (Becomes bin packing — NP-hard.)

---

### 🧠 Core Idea

Each boat carries **at most 2 people** with combined weight ≤ `limit`. Minimize the number of boats.

- **Brute force (backtracking):** Try all possible pairings. Exponential — infeasible for n = 5×10⁴.
- **Greedy + Sorting + Two Pointers (optimal):** Sort weights. Pair the **heaviest** with the **lightest** if their sum ≤ limit. Otherwise, the heaviest goes alone. O(n log n) time, O(1) space.

**Greedy Insight:**  
The heaviest person is the **hardest to pair** (least likely to fit with anyone). The lightest person is the **easiest to pair** (most likely to fit with anyone). If the heaviest can't pair with the lightest, they can't pair with **anyone** → must go alone. If they CAN pair, pairing them together is optimal because it "uses up" the hardest-to-place person while consuming the most flexible partner.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACHES

---

## 1A. Backtracking — Try All Pairings (Exponential)

**Idea:** For each person, decide: go alone, or pair with one of the remaining unassigned people. Explore all possibilities and find the minimum boat count.

**Time:** O(2ⁿ) to O(n!) — exponential.  
**Space:** O(n) recursion stack.  
❌ Completely infeasible for n = 5×10⁴.

```java
// Conceptual pseudo-code (NOT practical for large n)
public int numRescueBoats(int[] people, int limit) {
    boolean[] used = new boolean[people.length];
    return backtrack(people, used, limit, 0);
}

private int backtrack(int[] people, boolean[] used, int limit, int idx) {
    // Skip already assigned people
    while (idx < people.length && used[idx]) idx++;
    if (idx == people.length) return 0;  // everyone assigned

    int minBoats = Integer.MAX_VALUE;

    // Option 1: person[idx] goes ALONE
    used[idx] = true;
    minBoats = Math.min(minBoats, 1 + backtrack(people, used, limit, idx + 1));
    used[idx] = false;

    // Option 2: person[idx] pairs with person[j]
    for (int j = idx + 1; j < people.length; j++) {
        if (!used[j] && people[idx] + people[j] <= limit) {
            used[idx] = true;
            used[j] = true;
            minBoats = Math.min(minBoats, 1 + backtrack(people, used, limit, idx + 1));
            used[idx] = false;
            used[j] = false;
        }
    }

    return minBoats;
}
```

### 🔍 Sample Iteration (Small Example)

**Input:** `people = [3, 2, 2, 1]`, `limit = 3`

```
backtrack(idx=0, person=3):
├─ Option 1: 3 goes ALONE → boats=1 + backtrack(idx=1)
│  ├─ person=2, Option 1: 2 ALONE → boats=1 + backtrack(idx=2)
│  │  ├─ person=2, Option 1: 2 ALONE → boats=1 + backtrack(idx=3)
│  │  │  └─ person=1, ALONE → boats=1. Total: 1+1+1+1 = 4
│  │  └─ person=2, pair with person=1 (2+1=3≤3) → boats=1. Total: 1+1+1 = 3
│  └─ person=2, pair with person=1 (2+1=3≤3) → boats=1 + backtrack(idx=2)
│     └─ person=2, ALONE → boats=1. Total: 1+1+1 = 3
├─ Option 2: 3 pairs with j=1? (3+2=5>3) ❌
├─ Option 2: 3 pairs with j=2? (3+2=5>3) ❌
└─ Option 2: 3 pairs with j=3? (3+1=4>3) ❌

Minimum = 3 boats ✅
```

> ⚠️ For n=4, we explored ~7 branches. For n=50,000, this is **astronomically** infeasible. The number of possible pairings grows as (n-1)!! (double factorial).

---

## 1B. Naive Greedy — Pair Adjacent After Sorting (Suboptimal)

**Idea:** Sort the array, then greedily pair adjacent elements `(0,1), (2,3), (4,5), ...` if they fit.

**Time:** O(n log n).  
**Space:** O(1).  
❌ **NOT always optimal** — pairing adjacent elements doesn't minimize boats.

```java
// INCORRECT approach — for illustration only
public int numRescueBoats(int[] people, int limit) {
    Arrays.sort(people);
    int boats = 0;
    int i = 0;
    while (i < people.length) {
        if (i + 1 < people.length && people[i] + people[i + 1] <= limit) {
            i += 2;  // pair adjacent
        } else {
            i++;     // alone
        }
        boats++;
    }
    return boats;
}
```

### 🔍 Sample Showing Failure

**Input:** `people = [1, 1, 1, 3]`, `limit = 4`

**Sorted:** `[1, 1, 1, 3]`

| Step | i | Pair? | Boats |
|------|---|-------|-------|
| 1 | 0 | people[0]+people[1] = 1+1=2 ≤ 4 → pair (1,1) | 1 |
| 2 | 2 | people[2]+people[3] = 1+3=4 ≤ 4 → pair (1,3) | 2 |

**Naive result:** 2 boats. **Correct answer:** 2 boats. (Happens to work here.)

**Counter-example:** `people = [1, 2, 2, 3]`, `limit = 4`

**Sorted:** `[1, 2, 2, 3]`

| Step | i | Pair? | Boats |
|------|---|-------|-------|
| 1 | 0 | 1+2=3 ≤ 4 → pair (1,2) | 1 |
| 2 | 2 | 2+3=5 > 4 → 2 goes alone | 2 |
| 3 | 3 | 3 goes alone | 3 |

**Naive result:** 3 boats.  
**Optimal:** Pair (1,3)=4≤4 and (2,2)=4≤4 → **2 boats!** ❌ Naive fails!

> ⚠️ Pairing adjacent elements wastes the lightest person on a medium-weight partner, leaving the heaviest stranded. The correct greedy pairs **heaviest with lightest**.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. Sorting + Greedy Two Pointers (O(n log n) Time, O(1) Space) ✅

**Idea:**  
1. **Sort** the array.  
2. Use two pointers: `left = 0` (lightest), `right = n-1` (heaviest).  
3. While `left <= right`:  
   - If `people[left] + people[right] <= limit`: both board together → `left++`, `right--`.  
   - Else: heaviest goes alone → `right--`.  
   - `boats++` (one boat used per iteration).  
4. Return `boats`.

**Why it's optimal (Exchange Argument):**  
- Consider the heaviest person `H`.  
- If `H + lightest > limit`: H can't pair with **anyone** (everyone else is ≥ lightest). H must go alone. Greedy is forced.  
- If `H + lightest ≤ limit`: H CAN pair. Pairing H with the lightest is at least as good as pairing H with anyone else, because the lightest is the most "expendable" partner (easiest to pair with others later). Any optimal solution that pairs H with someone heavier can be modified to pair H with the lightest instead, without increasing boat count. ∎

**Time:** O(n log n) for sorting + O(n) for two-pointer pass.  
**Space:** O(1) extra (in-place sort).

```java
import java.util.Arrays;

public int numRescueBoats(int[] people, int limit) {
    Arrays.sort(people);
    int left = 0, right = people.length - 1;
    int boats = 0;

    while (left <= right) {
        // If lightest + heaviest fit together, pair them
        if (people[left] + people[right] <= limit) {
            left++;   // lightest boards
        }
        // Heaviest ALWAYS boards (either paired or alone)
        right--;
        boats++;
    }

    return boats;
}
```

### 🔍 Sample Iteration

**Input:** `people = [3, 2, 2, 1]`, `limit = 3`  
**After sorting:** `[1, 2, 2, 3]`

| Step | left | right | people[left] | people[right] | Sum | ≤ limit? | Action | boats |
|------|------|-------|--------------|---------------|-----|----------|--------|-------|
| 1 | 0 | 3 | 1 | 3 | 4 | 4 > 3 ❌ | 3 goes **alone**. right=2. | **1** |
| 2 | 0 | 2 | 1 | 2 | 3 | 3 ≤ 3 ✅ | **Pair (1,2)**. left=1, right=1. | **2** |
| 3 | 1 | 1 | 2 | 2 | — | left==right | 2 goes **alone**. right=0. | **3** |
| 4 | 1 | 0 | — | — | — | left > right → **STOP** | — | **3** |

**Result:** `3` boats ✅  
**Boats:** (3), (1,2), (2)

---

### 🔍 Visual Pointer Movement

```
Sorted: [1, 2, 2, 3], limit = 3

Step 1:  [1, 2, 2, 3]
          L        R    1+3=4 > 3 → 3 alone. R--.
                         Boat 1: (3)

Step 2:  [1, 2, 2, 3]
          L     R       1+2=3 ≤ 3 → PAIR! L++, R--.
                         Boat 2: (1, 2)

Step 3:  [1, 2, 2, 3]
             L=R        left==right → 2 alone. R--.
                         Boat 3: (2)

Step 4:  L > R → DONE.

Total: 3 boats ✅
```

---

### 🔍 Second Example: `people = [3, 5, 3, 4]`, `limit = 5`

**After sorting:** `[3, 3, 4, 5]`

| Step | left | right | people[left] | people[right] | Sum | ≤ 5? | Action | boats |
|------|------|-------|--------------|---------------|-----|------|--------|-------|
| 1 | 0 | 3 | 3 | 5 | 8 | ❌ | 5 alone. right=2. | 1 |
| 2 | 0 | 2 | 3 | 4 | 7 | ❌ | 4 alone. right=1. | 2 |
| 3 | 0 | 1 | 3 | 3 | 6 | ❌ | 3 alone. right=0. | 3 |
| 4 | 0 | 0 | 3 | 3 | — | left==right | 3 alone. right=-1. | 4 |
| 5 | 0 | -1 | — | — | — | left > right → STOP | — | **4** |

**Result:** `4` boats ✅ (no two people can share — minimum pair sum is 3+3=6 > 5)

---

### 🔍 Third Example: `people = [1, 2]`, `limit = 3`

**After sorting:** `[1, 2]`

| Step | left | right | Sum | ≤ 3? | Action | boats |
|------|------|-------|-----|------|--------|-------|
| 1 | 0 | 1 | 1+2=3 | ✅ | **Pair (1,2)**. left=1, right=0. | 1 |
| 2 | 1 | 0 | — | — | left > right → STOP | **1** |

**Result:** `1` boat ✅

---

### 🔍 Fourth Example (All Can Pair): `people = [1, 1, 1, 1]`, `limit = 2`

**After sorting:** `[1, 1, 1, 1]`

| Step | left | right | Sum | ≤ 2? | Action | boats |
|------|------|-------|-----|------|--------|-------|
| 1 | 0 | 3 | 1+1=2 | ✅ | Pair. left=1, right=2. | 1 |
| 2 | 1 | 2 | 1+1=2 | ✅ | Pair. left=2, right=1. | 2 |
| 3 | 2 | 1 | — | — | left > right → STOP | **2** |

**Result:** `2` boats ✅ (4 people, 2 per boat)

---

### 🔍 Fifth Example (Counter to Naive Adjacent): `people = [1, 2, 2, 3]`, `limit = 4`

**After sorting:** `[1, 2, 2, 3]`

| Step | left | right | Sum | ≤ 4? | Action | boats |
|------|------|-------|-----|------|--------|-------|
| 1 | 0 | 3 | 1+3=4 | ✅ | **Pair (1,3)**. left=1, right=2. | 1 |
| 2 | 1 | 2 | 2+2=4 | ✅ | **Pair (2,2)**. left=2, right=1. | 2 |
| 3 | 2 | 1 | — | — | left > right → STOP | **2** |

**Result:** `2` boats ✅  
*(The naive adjacent approach gave 3 boats — this greedy gives the correct 2!)*

---

### 🔍 Why the Greedy Works — Exchange Argument (Detailed)

```
Claim: Pairing the heaviest (H) with the lightest (L) when H+L ≤ limit is always optimal.

Proof:
  Consider any optimal solution OPT.
  
  Case 1: H goes alone in OPT.
    → Our greedy also sends H alone (if H+L > limit) or pairs H with L (if H+L ≤ limit).
    → If H+L ≤ limit but OPT sends H alone, then L is paired with someone else (say X) or alone.
    → Modify OPT: pair H with L instead. X now goes alone or pairs with L's old partner.
    → Boat count doesn't increase. Our greedy is at least as good.
  
  Case 2: H is paired with someone Y (Y ≠ L) in OPT.
    → Since L ≤ Y (L is lightest), H+L ≤ H+Y ≤ limit. So H can pair with L.
    → Modify OPT: pair H with L. Y is now free.
    → Y was paired with H before; now Y goes alone or pairs with whoever L was paired with.
    → Boat count doesn't increase.
  
  ∴ There always exists an optimal solution where H is paired with L (or H goes alone if H+L > limit).
  ∴ The greedy choice is safe. By induction on remaining people, the full algorithm is optimal. ∎
```

---

### 🔍 Loop Invariant

```
At the start of each iteration:
  - people[0..left-1] have been assigned to boats (paired with heavy people).
  - people[right+1..n-1] have been assigned to boats (went alone or paired).
  - people[left..right] are UNASSIGNED.
  - boats = number of boats used so far.

Each iteration assigns at least one person (the heaviest at `right`) to a boat.
∴ The loop runs at most n times. ∎
```

---

## 2B. Counting Sort + Two Pointers (O(n + limit) Time, O(limit) Space)

**Idea:** Since `1 <= people[i] <= limit <= 30000`, we can use **counting sort** instead of comparison sort. Build a frequency array of size `limit+1`, then use two pointers on the weight values.

**Time:** O(n + limit) — linear in both input size and weight range.  
**Space:** O(limit) — frequency array.

```java
public int numRescueBoats(int[] people, int limit) {
    int[] count = new int[limit + 1];
    for (int w : people) count[w]++;

    int left = 1, right = limit;
    int boats = 0;

    while (left <= right) {
        // Find next lightest weight with people remaining
        while (left <= right && count[left] == 0) left++;
        // Find next heaviest weight with people remaining
        while (left <= right && count[right] == 0) right--;

        if (left > right) break;

        // Try to pair lightest and heaviest
        if (left + right <= limit) {
            count[left]--;
            count[right]--;
        } else {
            count[right]--;  // heaviest goes alone
        }
        boats++;
    }

    return boats;
}
```

### 🔍 Sample Iteration

**Input:** `people = [3, 2, 2, 1]`, `limit = 3`  
**Count array:** `count[1]=1, count[2]=2, count[3]=1`

| Step | left | right | count[left] | count[right] | left+right | ≤ 3? | Action | boats |
|------|------|-------|-------------|--------------|------------|------|--------|-------|
| 1 | 1 | 3 | 1 | 1 | 4 | ❌ | count[3]--. right stays. | 1 |
| 2 | 1 | 3→2 | 1 | 2 | 3 | ✅ | count[1]--, count[2]--. | 2 |
| 3 | 1→2 | 2 | 1 | 1 | 4 | ❌ | count[2]--. | 3 |
| 4 | 2 | 2→1 | 0 | — | — | — | left > right → STOP | **3** |

**Result:** `3` boats ✅

> 📌 This avoids the O(n log n) sort, but the code is more complex. For n = 5×10⁴ and limit = 3×10⁴, both approaches are fast. The standard sort-based solution is preferred in interviews for clarity.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Naive Adjacent vs Greedy Two Pointers

| Metric | Backtracking | Naive Adjacent Pairing | Greedy (Heaviest + Lightest) |
|--------|-------------|----------------------|------------------------------|
| Time | O(2ⁿ) / O(n!) | O(n log n) | **O(n log n)** |
| Space | O(n) | O(1) | **O(1)** |
| Correct? | ✅ (finds true optimum) | ❌ (can be suboptimal) | **✅ (provably optimal)** |
| Feasible for n=5×10⁴? | ❌ Never | ✅ | **✅** |
| Key insight | Try everything | Pair neighbors | **Pair extremes (heaviest + lightest)** |

---

## Greedy Two Pointers vs Counting Sort + Two Pointers

| Metric | Comparison Sort + Greedy | Counting Sort + Greedy |
|--------|-------------------------|----------------------|
| Time | O(n log n) | O(n + limit) |
| Space | O(1) (in-place sort) | O(limit) — up to 30001 ints |
| Code complexity | **Simple (8 lines)** | Moderate (frequency array + pointer logic) |
| When faster? | When n log n < n + limit | When limit << n log n |
| For n=5×10⁴, limit=3×10⁴ | ~8×10⁵ ops | ~8×10⁴ ops |
| Interview preference | **Expected standard answer** | Bonus optimization if asked |

**Verdict:** The sort-based greedy is the **standard interview answer**. Counting sort is a theoretical improvement but adds code complexity for marginal gain at these constraints.

---

## Why "Heaviest + Lightest" Beats "Adjacent Pairing"

| Strategy | Logic | Failure case |
|----------|-------|--------------|
| Adjacent pairing | Pair (sorted[0], sorted[1]), (sorted[2], sorted[3]), ... | `[1,2,2,3], limit=4`: pairs (1,2) and (2,3→fails) → 3 boats |
| **Heaviest + Lightest** | Pair sorted[0] with sorted[n-1], then recurse inward | `[1,2,2,3], limit=4`: pairs (1,3)✓ and (2,2)✓ → **2 boats** |

> 📌 The heaviest person is the **bottleneck**. If we don't pair them with the lightest, we waste the lightest on someone easier to pair, and the heaviest might end up alone.

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Correct? | Practical? | Key Insight |
|----------|------|-------|----------|------------|-------------|
| Backtracking | O(2ⁿ) | O(n) | ✅ | ❌ | Try all pairings |
| Naive Adjacent | O(n log n) | O(1) | ❌ | — | Pair neighbors (fails!) |
| **Sort + Greedy Two Pointers** | **O(n log n)** | **O(1)** | **✅** | **✅** | **Pair heaviest with lightest** |
| Counting Sort + Two Pointers | O(n + limit) | O(limit) | ✅ | ✅ | Avoid comparison sort |

---

### 🎯 What to Present to the Interviewer

1. **Clarify the problem:** Each boat ≤ 2 people, total weight ≤ limit. Minimize boats.
2. **Mention brute force** is exponential (try all pairings) — infeasible.
3. **Introduce the greedy strategy:**
   - "Sort the people. The heaviest person is the hardest to pair."
   - "Try to pair them with the lightest. If it works, great — we save a boat. If not, the heaviest must go alone (no one lighter exists to help)."
   - "This is optimal by exchange argument: any solution pairing the heaviest with a non-lightest person can be modified to pair with the lightest instead, without increasing boats."
4. **Walk through** `[3, 2, 2, 1], limit = 3`:
   - Sorted: `[1, 2, 2, 3]`.
   - 1+3=4 > 3 → 3 alone. Boat 1.
   - 1+2=3 ≤ 3 → pair (1,2). Boat 2.
   - Remaining 2 alone. Boat 3.
   - Total: 3.
5. **Write the code:** Sort + while loop with `left` and `right`. Emphasize that `right` ALWAYS decrements (heaviest always boards), `left` only increments when pairing succeeds.
6. **State complexity:** O(n log n) time (sort dominates), O(1) space.
7. **If asked about boat capacity > 2:** "This becomes the bin packing problem, which is NP-hard. The 'at most 2' constraint is what makes the greedy valid."
8. **If asked to prove optimality:** Present the exchange argument (swap any non-lightest partner of the heaviest with the lightest; boat count doesn't increase).

**One‑sentence summary:**  
*Sort the weights, then greedily pair the heaviest remaining person with the lightest if their combined weight fits within the limit — otherwise send the heaviest alone — achieving the minimum number of boats in O(n log n) time via a provably optimal exchange argument.*