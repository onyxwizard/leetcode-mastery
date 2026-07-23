### 📘 Chapter: Two Pointers  
### 📌 Problem 3: Container With Most Water (LeetCode 11)

---

**Input**  
- `height`: an integer array of length `n`, where `height[i]` represents the height of a vertical line at position `i`.

**Output**  
- The **maximum area** of water that can be contained between any two lines (with the x-axis as the bottom).

**Constraints**  
- `n == height.length`  
- `2 <= n <= 10⁵`  
- `0 <= height[i] <= 10⁴`

**Example**  
```
Input:  height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
Explanation: Choose lines at index 1 (height=8) and index 8 (height=7).
             Area = min(8, 7) × (8 - 1) = 7 × 7 = 49.

Input:  height = [1, 1]
Output: 1
Explanation: Area = min(1, 1) × (1 - 0) = 1.

Input:  height = [4, 3, 2, 1, 4]
Output: 16
Explanation: Choose lines at index 0 (height=4) and index 4 (height=4).
             Area = min(4, 4) × (4 - 0) = 4 × 4 = 16.
```

**Follow-up**  
- None explicitly stated. The optimal solution is expected to run in **O(n) time** and **O(1) space**.

---

### 🧠 Core Idea

The area between lines at indices `i` and `j` is:

```
area = min(height[i], height[j]) × (j - i)
       ─────────────────────────   ─────────
       limited by shorter line     width (distance)
```

- **Brute force:** Check all O(n²) pairs. Too slow for n = 10⁵.
- **Two Pointers (optimal):** Start with the **widest** container (`left=0`, `right=n-1`). The area is limited by the **shorter** line. Moving the taller line inward can only **decrease** width without increasing the height limit. So the **only** chance to improve is to move the **shorter** line inward, hoping to find a taller one. O(n) time, O(1) space.

**Key Insight (Greedy Elimination):**  
If `height[left] < height[right]`, then for ANY `j` between `left` and `right`:
- `min(height[left], height[j]) ≤ height[left]` (the shorter line still caps the height)
- `(j - left) < (right - left)` (width is smaller)
- Therefore `area(left, j) < area(left, right)` — no pair involving `left` and an inner line can beat the current container.

∴ We can safely discard `left` and move it inward.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. All Pairs (O(n²) Time, O(1) Space)

**Idea:** Try every pair `(i, j)` with `i < j`. Compute the area and track the maximum.

**Time:** O(n²) — C(n, 2) pairs.  
**Space:** O(1).

```java
public int maxArea(int[] height) {
    int n = height.length;
    int maxArea = 0;

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int area = Math.min(height[i], height[j]) * (j - i);
            maxArea = Math.max(maxArea, area);
        }
    }

    return maxArea;
}
```

### 🔍 Sample Iteration (Key Pairs)

**Input:** `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`, n = 9

```
Index:  0  1  2  3  4  5  6  7  8
Height: 1  8  6  2  5  4  8  3  7
```

| i | j | min(h[i], h[j]) | width (j-i) | area | maxArea |
|---|---|-----------------|-------------|------|---------|
| 0 | 1 | min(1,8)=1 | 1 | 1 | 1 |
| 0 | 2 | min(1,6)=1 | 2 | 2 | 2 |
| 0 | 3 | min(1,2)=1 | 3 | 3 | 3 |
| 0 | 4 | min(1,5)=1 | 4 | 4 | 4 |
| 0 | 5 | min(1,4)=1 | 5 | 5 | 5 |
| 0 | 6 | min(1,8)=1 | 6 | 6 | 6 |
| 0 | 7 | min(1,3)=1 | 7 | 7 | 7 |
| 0 | 8 | min(1,7)=1 | 8 | 8 | 8 |
| 1 | 2 | min(8,6)=6 | 1 | 6 | 8 |
| 1 | 3 | min(8,2)=2 | 2 | 4 | 8 |
| 1 | 4 | min(8,5)=5 | 3 | 15 | **15** |
| 1 | 5 | min(8,4)=4 | 4 | 16 | **16** |
| 1 | 6 | min(8,8)=8 | 5 | 40 | **40** |
| 1 | 7 | min(8,3)=3 | 6 | 18 | 40 |
| **1** | **8** | **min(8,7)=7** | **7** | **49** | **49** |
| 2 | 3 | min(6,2)=2 | 1 | 2 | 49 |
| 2 | 4 | min(6,5)=5 | 2 | 10 | 49 |
| 2 | 5 | min(6,4)=4 | 3 | 12 | 49 |
| 2 | 6 | min(6,8)=6 | 4 | 24 | 49 |
| 2 | 7 | min(6,3)=3 | 5 | 15 | 49 |
| 2 | 8 | min(6,7)=6 | 6 | 36 | 49 |
| 3 | 4 | min(2,5)=2 | 1 | 2 | 49 |
| ... | ... | ... | ... | ... | 49 |
| 6 | 8 | min(8,7)=7 | 2 | 14 | 49 |
| 7 | 8 | min(3,7)=3 | 1 | 3 | 49 |

**Total pairs checked:** C(9,2) = **36**  
**Result:** `49` ✅ (found at pair (1, 8))

> ⚠️ For n = 10⁵: C(100000, 2) ≈ **5 × 10⁹** pairs. **Far too slow.** Most pairs are "doomed" — they can never beat the current max because the shorter line caps the height.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACH

---

## 2A. Two Pointers — Greedy Elimination (O(n) Time, O(1) Space) ✅

**Idea:**  
- Start with the **widest** container: `left = 0`, `right = n - 1`.  
- Compute area, update max.  
- **Move the pointer at the shorter line** inward (the only way to potentially increase area).  
- Repeat until pointers meet.

**Why moving the shorter pointer is correct:**  
If `height[left] < height[right]`:
- Any container `(left, j)` where `j < right` has:
  - Height ≤ `height[left]` (the shorter line still caps it)
  - Width < `right - left` (narrower)
- So `area(left, j) < area(left, right)` for ALL inner `j`.  
- ∴ Line `left` can never form a better container with anyone. **Discard it.**

**Time:** O(n) — each pointer moves at most n-1 steps total.  
**Space:** O(1) — two pointers + one variable.

```java
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1;
    int maxArea = 0;

    while (left < right) {
        int width = right - left;
        int h = Math.min(height[left], height[right]);
        maxArea = Math.max(maxArea, h * width);

        // Move the shorter line inward
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }

    return maxArea;
}
```

### 🔍 Sample Iteration

**Input:** `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`, n = 9

```
Index:  0  1  2  3  4  5  6  7  8
Height: 1  8  6  2  5  4  8  3  7
```

| Step | left | right | h[left] | h[right] | min | width | area | maxArea | Move | Reason |
|------|------|-------|---------|----------|-----|-------|------|---------|------|--------|
| 1 | 0 | 8 | 1 | 7 | 1 | 8 | 8 | **8** | left++ | h[0]=1 < h[8]=7 |
| 2 | 1 | 8 | 8 | 7 | 7 | 7 | **49** | **49** | right-- | h[1]=8 > h[8]=7 |
| 3 | 1 | 7 | 8 | 3 | 3 | 6 | 18 | 49 | right-- | h[1]=8 > h[7]=3 |
| 4 | 1 | 6 | 8 | 8 | 8 | 5 | 40 | 49 | right-- | h[1]=8 ≤ h[6]=8 (equal → move right) |
| 5 | 1 | 5 | 8 | 4 | 4 | 4 | 16 | 49 | right-- | h[1]=8 > h[5]=4 |
| 6 | 1 | 4 | 8 | 5 | 5 | 3 | 15 | 49 | right-- | h[1]=8 > h[4]=5 |
| 7 | 1 | 3 | 8 | 2 | 2 | 2 | 4 | 49 | right-- | h[1]=8 > h[3]=2 |
| 8 | 1 | 2 | 8 | 6 | 6 | 1 | 6 | 49 | right-- | h[1]=8 > h[2]=6 |
| 9 | 1 | 1 | — | — | — | — | — | 49 | **STOP** | left ≥ right |

**Result:** `49` ✅

> 📌 Only **8 iterations** instead of 36 pairs! The algorithm found the optimal answer at step 2 and then confirmed no better solution exists by eliminating one pointer at a time.

---

### 🔍 Visual Pointer Movement

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

Step 1:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
          L→→→→→→→→→→→→→→→→→→→→→R    area = 1×8 = 8. Move L (shorter).

Step 2:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
             L→→→→→→→→→→→→→→→→→R    area = 7×7 = 49 ★ MAX! Move R (shorter).

Step 3:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
             L→→→→→→→→→→→→→→→R      area = 3×6 = 18. Move R.

Step 4:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
             L→→→→→→→→→→→→→R        area = 8×5 = 40. Move R (equal heights).

Step 5:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
             L→→→→→→→→→→→R          area = 4×4 = 16. Move R.

Step 6:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
             L→→→→→→→→→R            area = 5×3 = 15. Move R.

Step 7:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
             L→→→→→→→R              area = 2×2 = 4. Move R.

Step 8:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
             L→→→→→R                area = 6×1 = 6. Move R.

Step 9:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
             L=R                    STOP.

Answer: 49 (from step 2: lines at index 1 and 8)
```

---

### 🔍 Why We NEVER Miss the Optimal Pair (Proof)

**Claim:** The two-pointer approach always finds the maximum area.

**Proof by contradiction:**  
Suppose the optimal pair is `(i*, j*)` with `i* < j*`. Assume our algorithm skips it.

- The algorithm starts with `(0, n-1)` — the widest possible container.
- Pointers only move **inward**. For the algorithm to skip `(i*, j*)`, it must have moved `left` past `i*` or `right` past `j*` before they met.
- WLOG, suppose `left` moved past `i*` while `right` was still ≥ `j*`. This means at some step, `left = i*` and `height[i*] < height[right]` (so we moved `left`).
- But then `area(i*, right) ≥ area(i*, j*)` because:
  - `height[right] ≥ height[j*]` (since `right ≥ j*` and we haven't moved right past j* yet... actually this needs more care).

**Simpler argument:**  
At any step, if `height[left] < height[right]`, then for ALL `j` with `left < j < right`:
- `min(height[left], height[j]) ≤ height[left]`
- `j - left < right - left`
- ∴ `area(left, j) ≤ height[left] × (j - left) < height[left] × (right - left) = area(left, right)`

So NO pair involving `left` and any inner index can beat `area(left, right)`. We safely discard `left`. By induction, we never discard a pointer that's part of the optimal solution unless we've already recorded a better or equal area. ∎

---

### 🔍 Edge Case: Equal Heights

**Input:** `height = [4, 3, 2, 1, 4]`

| Step | left | right | h[left] | h[right] | min | width | area | maxArea | Move |
|------|------|-------|---------|----------|-----|-------|------|---------|------|
| 1 | 0 | 4 | 4 | 4 | 4 | 4 | **16** | **16** | right-- (equal → either works) |
| 2 | 0 | 3 | 4 | 1 | 1 | 3 | 3 | 16 | right-- |
| 3 | 0 | 2 | 4 | 2 | 2 | 2 | 4 | 16 | right-- |
| 4 | 0 | 1 | 4 | 3 | 3 | 1 | 3 | 16 | right-- |
| 5 | 0 | 0 | — | — | — | — | — | 16 | STOP |

**Result:** `16` ✅

> 📌 When heights are equal, moving either pointer is safe. The current area is already the best possible for this pair (max width × this height). Moving one pointer might find a taller line; staying is pointless.

---

### 🔍 Edge Case: Minimum Input

**Input:** `height = [1, 1]`

| Step | left | right | h[left] | h[right] | area | maxArea | Move |
|------|------|-------|---------|----------|------|---------|------|
| 1 | 0 | 1 | 1 | 1 | 1×1=1 | 1 | right-- |
| 2 | 0 | 0 | — | — | — | 1 | STOP |

**Result:** `1` ✅

---

### 🔍 Trace: What Gets Eliminated and Why

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

Step 1: L=0, R=8. h[0]=1 is shorter.
  ELIMINATED: All pairs (0, j) for j=1..7.
  REASON: min(1, h[j]) ≤ 1, and width < 8. Max possible = 1×7 = 7 < 8 = current area.
  
Step 2: L=1, R=8. h[8]=7 is shorter.
  ELIMINATED: All pairs (j, 8) for j=2..7.
  REASON: min(h[j], 7) ≤ 7, and width < 7. Max possible = 7×6 = 42 < 49 = current area.

Step 3: L=1, R=7. h[7]=3 is shorter.
  ELIMINATED: All pairs (j, 7) for j=2..6.
  REASON: min(h[j], 3) ≤ 3, and width < 6. Max possible = 3×5 = 15 < 49.

... and so on. Each step eliminates an entire row/column of the pair matrix.
```

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Two Pointers

| Metric | Brute Force (All Pairs) | Two Pointers |
|--------|------------------------|--------------|
| Time | O(n²) | **O(n)** |
| For n=10⁵ | ~5 × 10⁹ pairs → **TLE** | ~10⁵ steps → instant |
| Space | O(1) | O(1) |
| Pairs examined | C(n,2) = n(n-1)/2 | At most n-1 |
| For n=9 (example) | 36 pairs | **8 steps** |
| Correctness argument | Trivially correct (checks everything) | Greedy elimination proof |
| Code complexity | Trivial (nested loops) | Simple (single while loop) |

**Verdict:** Two pointers is **strictly superior** — same space, dramatically better time. There is no trade-off; it's the only acceptable solution for n = 10⁵.

---

## Why No Other Approach Works Better

| Alternative | Why it doesn't apply |
|-------------|---------------------|
| HashMap / HashSet | No "complement" to look up; area depends on both height AND distance |
| Sorting | Would destroy positional information (width = index difference) |
| Divide and Conquer | Possible but O(n log n) — worse than two pointers |
| Stack (monotonic) | Not a "next greater element" problem; no sequential dependency |
| Dynamic Programming | No overlapping subproblems; each pair is independent |

> 📌 The two-pointer greedy is the **unique optimal** approach for this problem structure.

---

## Two-Pointer Movement: Why Shorter, Not Taller?

| If we move... | What happens |
|---------------|--------------|
| **Shorter line** (correct) | Width decreases by 1, but height **might increase** (new line could be taller). Area might improve. |
| Taller line (wrong) | Width decreases by 1, height **cannot exceed** the old shorter line (it still caps). Area **guaranteed to decrease or stay same**. |
| Both (wrong) | Skips potential solutions. |

**Example:** `height[left]=3, height[right]=8, width=10 → area=30`
- Move left (shorter): new left might be height 9 → area = min(9,8)×9 = 72 ✅ improvement possible!
- Move right (taller): new right ≤ 8, height still capped at 3, width=9 → area ≤ 27 ❌ guaranteed worse!

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Steps (n=9) | Steps (n=10⁵) | Practical? |
|----------|------|-------|-------------|---------------|------------|
| Brute Force | O(n²) | O(1) | 36 | ~5×10⁹ | ❌ TLE |
| **Two Pointers** | **O(n)** | **O(1)** | **8** | **~10⁵** | **✅ Optimal** |

---

### 🎯 What to Present to the Interviewer

1. **State the area formula:** `min(h[i], h[j]) × (j - i)`. Brute force checks all O(n²) pairs.
2. **Introduce the key insight:**
   - "The area is limited by the **shorter** line."
   - "Starting with the widest container, the only way to potentially increase area is to find a **taller** shorter-line."
   - "Moving the taller pointer inward **cannot help** — width shrinks and height is still capped by the shorter line."
3. **Present the two-pointer algorithm:**
   - `left = 0`, `right = n-1`.
   - Compute area, update max.
   - Move the pointer at the shorter line.
   - Repeat until pointers meet.
4. **Walk through** the example `[1,8,6,2,5,4,8,3,7]`:
   - Step 1: area = 1×8 = 8. Move left (height 1 < 7).
   - Step 2: area = 7×7 = **49**. Move right (height 7 < 8).
   - Continue... max stays 49.
5. **Prove correctness** (briefly): "If `h[left] < h[right]`, then for any inner `j`, `area(left, j) ≤ h[left] × (j-left) < h[left] × (right-left) = area(left, right)`. So `left` can never form a better pair. Safe to discard."
6. **State complexity:** O(n) time (each pointer moves at most n-1 times), O(1) space.
7. **If asked about equal heights:** "Moving either is fine — the current area is already the best for this height, and we need to explore inward for potentially taller lines."

**One‑sentence summary:**  
*Start with the widest container (pointers at both ends) and greedily narrow it by always moving the pointer at the shorter line — since the shorter line caps the height, discarding it is the only way to potentially find a taller boundary and a larger area, achieving O(n) time and O(1) space.*