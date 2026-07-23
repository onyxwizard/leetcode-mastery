### 📘 Chapter: Stack  
### 📌 Problem 10: Next Greater Element I (LeetCode 496)

---

**Input**  
- `nums1`: an array of unique integers (a subset of `nums2`).  
- `nums2`: an array of unique integers containing all elements of `nums1`.

**Output**  
- An array `ans` of length `nums1.length` where `ans[i]` is the **next greater element** of `nums1[i]` as found in `nums2`.  
- The next greater element of value `x` in `nums2` is the **first element to the right** of `x` that is greater than `x`.  
- If no such element exists, `ans[i] = -1`.

**Constraints**  
- `1 <= nums1.length <= nums2.length <= 1000`  
- `0 <= nums1[i], nums2[i] <= 10⁴`  
- All integers in `nums1` and `nums2` are unique.  
- Every element of `nums1` appears in `nums2`.

**Example**  
```
Input:  nums1 = [4, 1, 2], nums2 = [1, 3, 4, 2]
Output: [-1, 3, -1]
Explanation:
  4 in nums2: nothing to the right is greater → -1
  1 in nums2: next greater is 3 → 3
  2 in nums2: nothing to the right is greater → -1

Input:  nums1 = [2, 4], nums2 = [1, 2, 3, 4]
Output: [3, -1]
Explanation:
  2 in nums2: next greater is 3 → 3
  4 in nums2: nothing to the right → -1
```

**Follow-up**  
- Could you find an **O(nums1.length + nums2.length)** solution?

---

### 🧠 Core Idea

The core task: for every element in `nums2`, find the **first greater element to its right**. Then answer queries for the subset `nums1`.

- **Brute force:** For each query element, find its position in `nums2`, then scan right. O(m × n).
- **Monotonic Stack + HashMap (optimal):** Process `nums2` once with a decreasing stack. When a larger element appears, it "resolves" the next greater for all smaller elements on the stack. Store results in a HashMap. Answer `nums1` queries in O(1) each. Total: **O(n + m)**.

**Why a monotonic decreasing stack?**  
The stack holds elements that **haven't found their next greater yet**. They're in decreasing order (top = smallest unresolved). When a new element `x` arrives:
- Any stack element smaller than `x` has found its next greater → pop and record.
- Then push `x` (it hasn't found ITS next greater yet).

Each element is pushed once and popped at most once → O(n) total.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Direct Search for Each Query Element (O(m × n) Time)

**Idea:** For each element `val` in `nums1`:
1. Find `val`'s index in `nums2` (linear scan).
2. From that index, scan right to find the first element greater than `val`.
3. If found, record it. Otherwise, record `-1`.

**Time:** O(m × n) — for each of m queries, scan up to n elements.  
**Space:** O(1) extra (excluding output).

```java
public int[] nextGreaterElement(int[] nums1, int[] nums2) {
    int[] ans = new int[nums1.length];

    for (int i = 0; i < nums1.length; i++) {
        int val = nums1[i];

        // Step 1: Find val's position in nums2
        int j = 0;
        while (nums2[j] != val) j++;

        // Step 2: Scan right for the first greater element
        int nextGreater = -1;
        for (int k = j + 1; k < nums2.length; k++) {
            if (nums2[k] > val) {
                nextGreater = nums2[k];
                break;
            }
        }

        ans[i] = nextGreater;
    }

    return ans;
}
```

### 🔍 Sample Iteration

**Input:** `nums1 = [4, 1, 2]`, `nums2 = [1, 3, 4, 2]`

| i | val | Position in nums2 | Scan right | First greater? | ans[i] |
|---|-----|-------------------|------------|----------------|--------|
| 0 | 4 | index 2 | nums2[3]=2. 2 > 4? **No**. End. | None | **-1** |
| 1 | 1 | index 0 | nums2[1]=3. 3 > 1? **Yes!** | 3 | **3** |
| 2 | 2 | index 3 | No elements to the right. | None | **-1** |

**Result:** `[-1, 3, -1]` ✅

> ⚠️ For m = n = 1000: up to 10⁶ operations. Acceptable for these constraints, but doesn't meet the O(n+m) follow-up. For larger inputs, this becomes the bottleneck.

---

## 1B. Precompute with Nested Loops on nums2 (O(n²) Time)

**Idea:** For every element in `nums2`, scan right to find its next greater. Store in a HashMap. Then answer `nums1` queries.

**Time:** O(n²) — n elements, each scanning up to n positions.  
**Space:** O(n) — HashMap.

```java
public int[] nextGreaterElement(int[] nums1, int[] nums2) {
    Map<Integer, Integer> map = new HashMap<>();
    int n = nums2.length;

    for (int i = 0; i < n; i++) {
        int nextGreater = -1;
        for (int j = i + 1; j < n; j++) {
            if (nums2[j] > nums2[i]) {
                nextGreater = nums2[j];
                break;
            }
        }
        map.put(nums2[i], nextGreater);
    }

    int[] ans = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) {
        ans[i] = map.get(nums1[i]);
    }
    return ans;
}
```

### 🔍 Sample Iteration

**Input:** `nums2 = [1, 3, 4, 2]`

| i | nums2[i] | Scan right | nextGreater | map |
|---|----------|------------|-------------|-----|
| 0 | 1 | nums2[1]=3 > 1 ✅ | 3 | {1:3} |
| 1 | 3 | nums2[2]=4 > 3 ✅ | 4 | {1:3, 3:4} |
| 2 | 4 | nums2[3]=2 > 4? No. End. | -1 | {1:3, 3:4, 4:-1} |
| 3 | 2 | No elements right. | -1 | {1:3, 3:4, 4:-1, 2:-1} |

**Query nums1 = [4, 1, 2]:** map[4]=-1, map[1]=3, map[2]=-1 → `[-1, 3, -1]` ✅

> 📌 Better than 1A (precomputes once), but still O(n²) for the precomputation. The stack reduces this to O(n).

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. Monotonic Decreasing Stack + HashMap (O(n + m) Time, O(n) Space) ✅

**Idea:**  
1. Use a `Deque<Integer>` as a **monotonically decreasing stack** (top = smallest unresolved element).  
2. Iterate over `nums2` left to right:  
   - While stack is not empty AND `current > stack.peek()`:  
     - Pop the top. Its next greater element is `current`. Record in HashMap.  
   - Push `current`.  
3. Elements remaining in the stack have **no** next greater element → implicitly map to `-1`.  
4. For each element in `nums1`, look up the HashMap. If not found → `-1`.

**Time:** O(n + m) — each element in `nums2` pushed/popped once (O(n)); each `nums1` lookup is O(1) (O(m)).  
**Space:** O(n) — stack + HashMap.

```java
import java.util.*;

public int[] nextGreaterElement(int[] nums1, int[] nums2) {
    Map<Integer, Integer> nextGreaterMap = new HashMap<>();
    Deque<Integer> stack = new ArrayDeque<>();  // monotonic decreasing

    // Process nums2: find next greater for every element
    for (int num : nums2) {
        // Current num is the next greater for all smaller elements on the stack
        while (!stack.isEmpty() && stack.peek() < num) {
            nextGreaterMap.put(stack.pop(), num);
        }
        stack.push(num);
    }
    // Elements left in stack have no next greater → implicitly -1

    // Answer queries for nums1
    int[] ans = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) {
        ans[i] = nextGreaterMap.getOrDefault(nums1[i], -1);
    }

    return ans;
}
```

### 🔍 Sample Iteration

**Input:** `nums1 = [4, 1, 2]`, `nums2 = [1, 3, 4, 2]`

**Processing nums2 with stack:**

| Step | num | Stack BEFORE (top→bottom) | Condition: peek < num? | Action | Stack AFTER | Map update |
|------|-----|---------------------------|------------------------|--------|-------------|------------|
| 1 | 1 | `[]` | (empty) | Push 1 | `[1]` | — |
| 2 | 3 | `[1]` | 1 < 3? **Yes** → pop 1 | Map[1]=3. Push 3. | `[3]` | {1:3} |
| 3 | 4 | `[3]` | 3 < 4? **Yes** → pop 3 | Map[3]=4. Push 4. | `[4]` | {1:3, 3:4} |
| 4 | 2 | `[4]` | 4 < 2? **No** | Push 2 | `[2, 4]` | — |
| END | — | `[2, 4]` remain | — | No next greater for 2 and 4 | — | {1:3, 3:4} |

**Answering nums1 queries:**

| i | nums1[i] | Map lookup | ans[i] |
|---|----------|------------|--------|
| 0 | 4 | map.get(4) → not found → **-1** | -1 |
| 1 | 1 | map.get(1) → **3** | 3 |
| 2 | 2 | map.get(2) → not found → **-1** | -1 |

**Result:** `[-1, 3, -1]` ✅

---

### 🔍 Visual Stack Trace

```
nums2 = [1, 3, 4, 2]

Step 1: num=1
  ┌───┐
  │ 1 │  ← no next greater yet
  └───┘

Step 2: num=3
  3 > 1 → 1's next greater is 3! Pop 1, record map[1]=3.
  ┌───┐
  │ 3 │  ← push 3
  └───┘

Step 3: num=4
  4 > 3 → 3's next greater is 4! Pop 3, record map[3]=4.
  ┌───┐
  │ 4 │  ← push 4
  └───┘

Step 4: num=2
  2 < 4 → 4 is NOT resolved. Push 2 on top.
  ┌───┐
  │ 2 │  ← top (no next greater yet)
  ├───┤
  │ 4 │  ← (no next greater yet)
  └───┘

END: Stack has [2, 4] → both have no next greater → map to -1.

Final map: {1→3, 3→4}
Elements NOT in map (2, 4) → -1
```

---

### 🔍 Second Example: `nums1 = [2, 4], nums2 = [1, 2, 3, 4]`

**Processing nums2:**

| Step | num | Stack BEFORE | peek < num? | Action | Stack AFTER | Map |
|------|-----|--------------|-------------|--------|-------------|-----|
| 1 | 1 | `[]` | — | Push 1 | `[1]` | {} |
| 2 | 2 | `[1]` | 1<2 ✅ | Pop 1, map[1]=2. Push 2. | `[2]` | {1:2} |
| 3 | 3 | `[2]` | 2<3 ✅ | Pop 2, map[2]=3. Push 3. | `[3]` | {1:2, 2:3} |
| 4 | 4 | `[3]` | 3<4 ✅ | Pop 3, map[3]=4. Push 4. | `[4]` | {1:2, 2:3, 3:4} |
| END | — | `[4]` | — | 4 has no next greater | — | {1:2, 2:3, 3:4} |

**Query nums1 = [2, 4]:** map[2]=3, map[4]→not found→-1  
**Result:** `[3, -1]` ✅

---

### 🔍 Third Example (Multiple Pops in One Step)

**Input:** `nums2 = [2, 1, 3, 5, 4]`

| Step | num | Stack BEFORE | Pops | Stack AFTER | Map updates |
|------|-----|--------------|------|-------------|-------------|
| 1 | 2 | `[]` | — | `[2]` | — |
| 2 | 1 | `[2]` | 2<1? No | `[1, 2]` | — |
| 3 | 3 | `[1, 2]` | 1<3→pop. 2<3→pop. | `[3]` | map[1]=3, map[2]=3 |
| 4 | 5 | `[3]` | 3<5→pop. | `[5]` | map[3]=5 |
| 5 | 4 | `[5]` | 5<4? No | `[4, 5]` | — |
| END | — | `[4, 5]` | — | — | 4→-1, 5→-1 |

**Final map:** {1:3, 2:3, 3:5}  
**Elements not in map:** 4→-1, 5→-1

> 📌 At step 3, `num=3` resolves **two** elements at once (1 and 2). This is the power of the monotonic stack — one element can resolve multiple predecessors in a single step.

---

### 🔍 Why the Stack is Monotonically Decreasing

```
After each push, the stack maintains: bottom ≥ ... ≥ top

Why? We pop ALL elements smaller than the current before pushing.
So the current element is ≤ everything remaining on the stack.
∴ Stack is always in decreasing order (bottom to top).

Example: [2, 1, 3, 5, 4]
  After step 2: [1, 2] → decreasing (2 > 1) ✅
  After step 3: [3] → trivially decreasing ✅
  After step 5: [4, 5] → decreasing (5 > 4) ✅
```

---

### 🔍 Amortized O(n) Proof

```
Each element in nums2 is:
  - PUSHED onto the stack exactly once → n pushes.
  - POPPED from the stack at most once → at most n pops.

Total stack operations: ≤ 2n → O(n).
HashMap insertions: ≤ n → O(n).
nums1 lookups: m → O(m).

Total: O(n + m). ✅
```

---

### 🔍 Relationship to "Next Greater Element" Family

| Problem | Approach | Time |
|---------|----------|------|
| **NGE I (LeetCode 496)** | Stack + HashMap (subset queries) | **O(n + m)** |
| NGE II (LeetCode 503) | Stack on circular array (iterate 2n) | O(n) |
| Daily Temperatures (LeetCode 739) | Stack of indices (distance variant) | O(n) |
| Online Stock Span (LeetCode 901) | Stack of (price, span) pairs | O(n) amortized |

> 📌 All use the same core pattern: **monotonic decreasing stack** that resolves elements when a larger one appears.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force (Per Query) vs Precompute (Nested) vs Stack + HashMap

| Metric | Per-Query Scan | Precompute (Nested Loops) | Stack + HashMap |
|--------|---------------|--------------------------|-----------------|
| Time | O(m × n) | O(n² + m) | **O(n + m)** |
| For m=n=1000 | ~10⁶ | ~10⁶ | ~2000 |
| Space | O(1) | O(n) | O(n) |
| Preprocessing? | None | O(n²) | **O(n)** |
| Query time | O(n) per query | O(1) per query | **O(1) per query** |
| Meets follow-up? | ❌ | ❌ (O(n²) precompute) | **✅** |

---

## Why Stack + HashMap is Strictly Better

| Aspect | Nested Loop Precompute | Stack + HashMap |
|--------|----------------------|-----------------|
| Precomputation | O(n²) — scan right for each element | **O(n)** — single pass with stack |
| Key insight | None (brute search) | **Monotonic stack resolves multiple elements at once** |
| Scales to n=10⁵? | ❌ (10¹⁰ ops) | **✅ (2×10⁵ ops)** |
| Code complexity | Simple | Moderate (stack logic) |
| Interview value | Baseline | **Expected optimal answer** |

---

## Stack Direction: Why Decreasing (Not Increasing)?

| Stack type | What it finds | Use case |
|------------|--------------|----------|
| **Monotonic Decreasing** | Next **Greater** Element | This problem, Daily Temperatures |
| Monotonic Increasing | Next **Smaller** Element | "Next smaller to the right" problems |

```
Decreasing stack: [5, 3, 1] (bottom to top)
  When 4 arrives: pops 1 (1<4), pops 3 (3<4), stops at 5 (5>4).
  → 4 is the next greater for 1 and 3.
  → 5 is NOT resolved (5 > 4).
```

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Follow-up? | Key Insight |
|----------|------|-------|------------|-------------|
| Per-Query Scan | O(m×n) | O(1) | ❌ | Find position, scan right |
| Nested Precompute | O(n²+m) | O(n) | ❌ | Precompute all NGEs with nested loops |
| **Stack + HashMap** | **O(n+m)** | **O(n)** | **✅** | **Decreasing stack resolves NGEs in one pass** |

---

### 🎯 What to Present to the Interviewer

1. **Recognize the pattern:** "This is the classic Next Greater Element problem. The optimal tool is a monotonic decreasing stack."
2. **Describe the brute force:** "For each element in nums1, find it in nums2 and scan right. O(m×n)."
3. **Propose the optimal:**
   - "Process nums2 once with a decreasing stack."
   - "When a larger element appears, it resolves the next greater for all smaller elements on the stack."
   - "Store results in a HashMap for O(1) lookup."
4. **Walk through** `nums2 = [1, 3, 4, 2]`:
   - Push 1. See 3: 1<3, pop 1, map[1]=3. Push 3.
   - See 4: 3<4, pop 3, map[3]=4. Push 4.
   - See 2: 4>2, push 2. Stack: [2, 4].
   - End: 2 and 4 have no next greater → -1.
5. **Answer queries:** nums1=[4,1,2] → map[4]=-1, map[1]=3, map[2]=-1 → [-1, 3, -1].
6. **Emphasize amortized O(n):** "Each element pushed once, popped at most once. Total stack operations = 2n."
7. **State complexity:** O(n + m) time, O(n) space. Meets the follow-up.
8. **If asked about the stack invariant:** "The stack is always monotonically decreasing (bottom to top). Elements on the stack haven't found their next greater yet."

**One‑sentence summary:**  
*Use a monotonic decreasing stack to compute the next greater element for every value in nums2 in a single O(n) pass — when a larger element arrives, it resolves all smaller elements on the stack — then store results in a HashMap for O(1) lookup per nums1 query, achieving O(n + m) total time.*