### 📘 Chapter: Two Pointers  
### 📌 Problem 4: Trapping Rain Water (LeetCode 42)

---

**Input**  
- `height`: an integer array of `n` non-negative integers representing an elevation map where each bar has width = 1.

**Output**  
- Total units of water trapped after raining (an integer).

**Constraints**  
- `n == height.length`  
- `1 <= n <= 2 × 10⁴`  
- `0 <= height[i] <= 10⁵`

**Example**  
```
Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6

Visual:
        |
    |   ||#|
 |  |#|#||||#|
_|__|#|#||||#|_
0 1 0 2 1 0 1 3 2 1 2 1

(# = trapped water, total = 6 units)

Input:  height = [4,2,0,3,2,5]
Output: 9

Input:  height = [1,2,3,4,5]
Output: 0  (ascending → no water trapped)
```

**Follow-up**  
- Achieve **O(n) time** AND **O(1) extra space**.

---

### 🧠 Core Idea

The water trapped at index `i` is:

```
water[i] = max(0, min(maxLeft[i], maxRight[i]) - height[i])
                  ─────────────────────────────   ──────────
                  water level at i                bar height
```

Where:
- `maxLeft[i]` = maximum height from index `0` to `i` (inclusive).
- `maxRight[i]` = maximum height from index `i` to `n-1` (inclusive).

The **water level** at any point is determined by the **shorter** of the two "walls" (max to the left and max to the right). Water fills up to that level minus the bar's own height.

**Approaches:**
- **Brute force:** For each index, scan left and right to find max. O(n²).
- **Prefix/Suffix arrays:** Precompute `leftMax[]` and `rightMax[]` in two passes. O(n) time, O(n) space.
- **Two Pointers (optimal):** Maintain running `leftMax` and `rightMax` with two pointers moving inward. O(n) time, **O(1) space**.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Nested Loops — Scan Left & Right for Each Index (O(n²) Time)

**Idea:** For each index `i`:
1. Scan leftward (0 to i) to find `maxLeft`.
2. Scan rightward (i to n-1) to find `maxRight`.
3. `water[i] = max(0, min(maxLeft, maxRight) - height[i])`.

Sum all `water[i]`.

**Time:** O(n²) — for each of n indices, two scans of up to n elements.  
**Space:** O(1).

```java
public int trap(int[] height) {
    int n = height.length;
    int total = 0;

    for (int i = 0; i < n; i++) {
        int maxLeft = 0, maxRight = 0;

        // Scan left (including i)
        for (int j = 0; j <= i; j++) {
            maxLeft = Math.max(maxLeft, height[j]);
        }
        // Scan right (including i)
        for (int j = i; j < n; j++) {
            maxRight = Math.max(maxRight, height[j]);
        }

        total += Math.max(0, Math.min(maxLeft, maxRight) - height[i]);
    }

    return total;
}
```

### 🔍 Sample Iteration

**Input:** `height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]`, n = 12

```
Index:  0  1  2  3  4  5  6  7  8  9  10  11
Height: 0  1  0  2  1  0  1  3  2  1   2   1
```

| i | height[i] | maxLeft (scan 0..i) | maxRight (scan i..11) | min(L,R) | water[i] = min - height[i] | total |
|---|-----------|---------------------|----------------------|----------|----------------------------|-------|
| 0 | 0 | 0 | 3 | 0 | 0 - 0 = **0** | 0 |
| 1 | 1 | 1 | 3 | 1 | 1 - 1 = **0** | 0 |
| 2 | 0 | 1 | 3 | 1 | 1 - 0 = **1** | 1 |
| 3 | 2 | 2 | 3 | 2 | 2 - 2 = **0** | 1 |
| 4 | 1 | 2 | 3 | 2 | 2 - 1 = **1** | 2 |
| 5 | 0 | 2 | 3 | 2 | 2 - 0 = **2** | 4 |
| 6 | 1 | 2 | 3 | 2 | 2 - 1 = **1** | 5 |
| 7 | 3 | 3 | 3 | 3 | 3 - 3 = **0** | 5 |
| 8 | 2 | 3 | 2 | 2 | 2 - 2 = **0** | 5 |
| 9 | 1 | 3 | 2 | 2 | 2 - 1 = **1** | 6 |
| 10 | 2 | 3 | 2 | 2 | 2 - 2 = **0** | 6 |
| 11 | 1 | 3 | 1 | 1 | 1 - 1 = **0** | 6 |

**Result:** `6` ✅

> ⚠️ For n = 2×10⁴: ~4×10⁸ operations (two inner loops per index). Borderline TLE. The redundant scanning is the bottleneck.

---

### 🔍 Visual: Water at Each Index

```
Height:  0  1  0  2  1  0  1  3  2  1  2  1
Level:   0  1  1  2  2  2  2  3  2  2  2  1  ← min(maxLeft, maxRight)
Water:   0  0  1  0  1  2  1  0  0  1  0  0  ← Level - Height
                                     Total = 6

Visual grid (row = height level, top to bottom):
Level 3:  .  .  .  .  .  .  .  █  .  .  .  .
Level 2:  .  .  .  █  .  .  .  █  █  .  █  .
Level 1:  .  █  .  █  █  .  █  █  █  █  █  █
Level 0:  .  .  .  .  .  .  .  .  .  .  .  .
          ─────────────────────────────────────
Index:    0  1  2  3  4  5  6  7  8  9  10 11

Water (░):
Level 2:  .  .  .  █  ░  ░  ░  █  █  ░  █  .
Level 1:  .  █  ░  █  █  ░  █  █  █  █  █  █

Trapped water (░) = 1 + 1 + 2 + 1 + 1 = 6 units
```

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACHES

---

## 2A. Prefix/Suffix Arrays (O(n) Time, O(n) Space)

**Idea:**  
1. **Pass 1 (left → right):** Build `leftMax[i]` = max(height[0..i]).
2. **Pass 2 (right → left):** Build `rightMax[i]` = max(height[i..n-1]).
3. **Pass 3:** For each `i`, `water[i] = min(leftMax[i], rightMax[i]) - height[i]`.

**Time:** O(n) — three linear passes.  
**Space:** O(n) — two extra arrays.

```java
public int trap(int[] height) {
    int n = height.length;
    if (n == 0) return 0;

    int[] leftMax = new int[n];
    int[] rightMax = new int[n];

    // Pass 1: leftMax[i] = max height from 0 to i
    leftMax[0] = height[0];
    for (int i = 1; i < n; i++) {
        leftMax[i] = Math.max(leftMax[i - 1], height[i]);
    }

    // Pass 2: rightMax[i] = max height from i to n-1
    rightMax[n - 1] = height[n - 1];
    for (int i = n - 2; i >= 0; i--) {
        rightMax[i] = Math.max(rightMax[i + 1], height[i]);
    }

    // Pass 3: compute total water
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += Math.min(leftMax[i], rightMax[i]) - height[i];
    }

    return total;
}
```

### 🔍 Sample Iteration

**Input:** `height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]`

**Pass 1: Build leftMax[]**

| i | height[i] | leftMax[i] = max(leftMax[i-1], height[i]) |
|---|-----------|-------------------------------------------|
| 0 | 0 | **0** |
| 1 | 1 | max(0, 1) = **1** |
| 2 | 0 | max(1, 0) = **1** |
| 3 | 2 | max(1, 2) = **2** |
| 4 | 1 | max(2, 1) = **2** |
| 5 | 0 | max(2, 0) = **2** |
| 6 | 1 | max(2, 1) = **2** |
| 7 | 3 | max(2, 3) = **3** |
| 8 | 2 | max(3, 2) = **3** |
| 9 | 1 | max(3, 1) = **3** |
| 10 | 2 | max(3, 2) = **3** |
| 11 | 1 | max(3, 1) = **3** |

`leftMax = [0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]`

**Pass 2: Build rightMax[]**

| i | height[i] | rightMax[i] = max(rightMax[i+1], height[i]) |
|---|-----------|---------------------------------------------|
| 11 | 1 | **1** |
| 10 | 2 | max(1, 2) = **2** |
| 9 | 1 | max(2, 1) = **2** |
| 8 | 2 | max(2, 2) = **2** |
| 7 | 3 | max(2, 3) = **3** |
| 6 | 1 | max(3, 1) = **3** |
| 5 | 0 | max(3, 0) = **3** |
| 4 | 1 | max(3, 1) = **3** |
| 3 | 2 | max(3, 2) = **3** |
| 2 | 0 | max(3, 0) = **3** |
| 1 | 1 | max(3, 1) = **3** |
| 0 | 0 | max(3, 0) = **3** |

`rightMax = [3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 1]`

**Pass 3: Compute Water**

| i | height[i] | leftMax[i] | rightMax[i] | min(L,R) | water[i] | total |
|---|-----------|------------|-------------|----------|----------|-------|
| 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| 1 | 1 | 1 | 3 | 1 | 0 | 0 |
| 2 | 0 | 1 | 3 | 1 | **1** | 1 |
| 3 | 2 | 2 | 3 | 2 | 0 | 1 |
| 4 | 1 | 2 | 3 | 2 | **1** | 2 |
| 5 | 0 | 2 | 3 | 2 | **2** | 4 |
| 6 | 1 | 2 | 3 | 2 | **1** | 5 |
| 7 | 3 | 3 | 3 | 3 | 0 | 5 |
| 8 | 2 | 3 | 2 | 2 | 0 | 5 |
| 9 | 1 | 3 | 2 | 2 | **1** | 6 |
| 10 | 2 | 3 | 2 | 2 | 0 | 6 |
| 11 | 1 | 3 | 1 | 1 | 0 | 6 |

**Result:** `6` ✅

> 📌 Three clean passes, each O(n). Easy to understand and verify. But uses 2 extra arrays of size n.

---

## 2B. Two Pointers (O(n) Time, O(1) Space) ✅

**Idea:**  
Instead of precomputing full arrays, maintain **running** `leftMax` and `rightMax` with two pointers:

- `left = 0`, `right = n-1`, `leftMax = 0`, `rightMax = 0`.
- While `left < right`:
  - If `height[left] < height[right]`:
    - The water level at `left` is bounded by `leftMax` (because we **know** there's a wall ≥ `height[right]` on the right, and `height[right] > height[left]`, so the right side is not the bottleneck).
    - If `height[left] >= leftMax` → update `leftMax` (this bar IS the new wall).
    - Else → trap `leftMax - height[left]` units of water.
    - `left++`.
  - Else (symmetric for right):
    - If `height[right] >= rightMax` → update `rightMax`.
    - Else → trap `rightMax - height[right]`.
    - `right--`.

**Key Insight:**  
When `height[left] < height[right]`, we **know** the right side has a wall at least as tall as `height[right]` (which is > `height[left]`). So the water level at `left` is determined **solely** by `leftMax`. We don't need to know the exact `rightMax` — we just need to know it's ≥ `height[right]` > `height[left]`.

**Time:** O(n) — single pass, each pointer moves at most n-1 steps.  
**Space:** O(1) — four variables.

```java
public int trap(int[] height) {
    int left = 0, right = height.length - 1;
    int leftMax = 0, rightMax = 0;
    int total = 0;

    while (left < right) {
        if (height[left] < height[right]) {
            if (height[left] >= leftMax) {
                leftMax = height[left];   // new wall, no water here
            } else {
                total += leftMax - height[left];  // trap water
            }
            left++;
        } else {
            if (height[right] >= rightMax) {
                rightMax = height[right];  // new wall, no water here
            } else {
                total += rightMax - height[right];  // trap water
            }
            right--;
        }
    }

    return total;
}
```

### 🔍 Sample Iteration

**Input:** `height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]`, n = 12

```
Index:  0  1  2  3  4  5  6  7  8  9  10  11
Height: 0  1  0  2  1  0  1  3  2  1   2   1
```

| Step | left | right | h[left] | h[right] | h[L] < h[R]? | Action | leftMax | rightMax | Water Added | total |
|------|------|-------|---------|----------|--------------|--------|---------|----------|-------------|-------|
| 1 | 0 | 11 | 0 | 1 | **Yes** | h[0]=0 < leftMax=0? No (≥) → update leftMax=0. left++. | **0** | 0 | 0 | 0 |
| 2 | 1 | 11 | 1 | 1 | No (≥) | h[11]=1 ≥ rightMax=0 → update rightMax=1. right--. | 0 | **1** | 0 | 0 |
| 3 | 1 | 10 | 1 | 2 | **Yes** | h[1]=1 ≥ leftMax=0 → update leftMax=1. left++. | **1** | 1 | 0 | 0 |
| 4 | 2 | 10 | 0 | 2 | **Yes** | h[2]=0 < leftMax=1 → trap 1-0=**1**. left++. | 1 | 1 | **1** | **1** |
| 5 | 3 | 10 | 2 | 2 | No (≥) | h[10]=2 ≥ rightMax=1 → update rightMax=2. right--. | 1 | **2** | 0 | 1 |
| 6 | 3 | 9 | 2 | 1 | No (≥) | h[9]=1 < rightMax=2 → trap 2-1=**1**. right--. | 1 | 2 | **1** | **2** |
| 7 | 3 | 8 | 2 | 2 | No (≥) | h[8]=2 ≥ rightMax=2 → update rightMax=2. right--. | 1 | 2 | 0 | 2 |
| 8 | 3 | 7 | 2 | 3 | **Yes** | h[3]=2 ≥ leftMax=1 → update leftMax=2. left++. | **2** | 2 | 0 | 2 |
| 9 | 4 | 7 | 1 | 3 | **Yes** | h[4]=1 < leftMax=2 → trap 2-1=**1**. left++. | 2 | 2 | **1** | **3** |
| 10 | 5 | 7 | 0 | 3 | **Yes** | h[5]=0 < leftMax=2 → trap 2-0=**2**. left++. | 2 | 2 | **2** | **5** |
| 11 | 6 | 7 | 1 | 3 | **Yes** | h[6]=1 < leftMax=2 → trap 2-1=**1**. left++. | 2 | 2 | **1** | **6** |
| 12 | 7 | 7 | — | — | — | left ≥ right → **STOP** | 2 | 2 | — | **6** |

**Result:** `6` ✅

---

### 🔍 Visual Pointer Movement

```
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

Step 1:  L→                              ←R   h[0]=0 < h[11]=1 → process L, leftMax=0
Step 2:     L                            ←R   h[1]=1 ≥ h[10]=2? No → process R, rightMax=1
Step 3:     L→                           ←R   h[1]=1 ≥ leftMax → leftMax=1
Step 4:        L→                        ←R   h[2]=0 < leftMax=1 → TRAP 1 ★
Step 5:           L                      ←R   h[10]=2 ≥ rightMax → rightMax=2
Step 6:           L                   ←R      h[9]=1 < rightMax=2 → TRAP 1 ★
Step 7:           L                ←R         h[8]=2 ≥ rightMax → rightMax=2
Step 8:           L→             ←R           h[3]=2 ≥ leftMax → leftMax=2
Step 9:              L→          ←R           h[4]=1 < leftMax=2 → TRAP 1 ★
Step 10:                L→       ←R           h[5]=0 < leftMax=2 → TRAP 2 ★★
Step 11:                   L→    ←R           h[6]=1 < leftMax=2 → TRAP 1 ★
Step 12:                      L=R             STOP

Total trapped: 1 + 1 + 1 + 2 + 1 = 6 ★
```

---

### 🔍 Why Two Pointers Work — The Critical Insight

```
When height[left] < height[right]:

  We KNOW: there exists a wall on the right (at index `right`) with height ≥ height[right].
  And:     height[right] > height[left].
  
  Therefore: the water level at `left` is bounded by leftMax (from the left side).
  The right side is guaranteed to be tall enough — it's NOT the bottleneck.
  
  So: water at `left` = leftMax - height[left] (if positive).
  We DON'T need to know the exact rightMax — just that it's ≥ height[right] > height[left].

This is why we can process the LEFT pointer without having computed the full rightMax array!
```

**Symmetric argument:** When `height[left] ≥ height[right]`, the left side is guaranteed tall enough, so the water level at `right` is bounded by `rightMax`.

---

### 🔍 Second Example: `height = [4, 2, 0, 3, 2, 5]`

```
Index:  0  1  2  3  4  5
Height: 4  2  0  3  2  5
```

| Step | left | right | h[L] | h[R] | h[L]<h[R]? | Action | leftMax | rightMax | Water | total |
|------|------|-------|------|------|------------|--------|---------|----------|-------|-------|
| 1 | 0 | 5 | 4 | 5 | **Yes** | h[0]=4 ≥ leftMax=0 → leftMax=4. left++. | **4** | 0 | 0 | 0 |
| 2 | 1 | 5 | 2 | 5 | **Yes** | h[1]=2 < leftMax=4 → trap 4-2=**2**. left++. | 4 | 0 | 2 | **2** |
| 3 | 2 | 5 | 0 | 5 | **Yes** | h[2]=0 < leftMax=4 → trap 4-0=**4**. left++. | 4 | 0 | 4 | **6** |
| 4 | 3 | 5 | 3 | 5 | **Yes** | h[3]=3 < leftMax=4 → trap 4-3=**1**. left++. | 4 | 0 | 1 | **7** |
| 5 | 4 | 5 | 2 | 5 | **Yes** | h[4]=2 < leftMax=4 → trap 4-2=**2**. left++. | 4 | 0 | 2 | **9** |
| 6 | 5 | 5 | — | — | — | left ≥ right → **STOP** | 4 | 0 | — | **9** |

**Result:** `9` ✅

```
Visual:
Level 5:  .  .  .  .  .  █
Level 4:  █  .  .  .  .  █
Level 3:  █  .  .  █  .  █
Level 2:  █  █  .  █  █  █
Level 1:  █  █  .  █  █  █
Level 0:  █  █  .  █  █  █
          ─────────────────
Index:    0  1  2  3  4  5

Water (░):
Level 4:  █  ░  ░  ░  ░  █   ← 4 units
Level 3:  █  ░  ░  █  ░  █   ← 3 units
Level 2:  █  █  ░  █  █  █   ← 1 unit
                             Total = 4+3+1+1 = 9? 

Actually: index 1: 4-2=2, index 2: 4-0=4, index 3: 4-3=1, index 4: 4-2=2 → 2+4+1+2=9 ✅
```

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Prefix/Suffix vs Two Pointers

| Metric | Brute Force | Prefix/Suffix Arrays | Two Pointers |
|--------|-------------|---------------------|--------------|
| Time | O(n²) | O(n) | **O(n)** |
| Space | O(1) | O(n) — two arrays | **O(1)** |
| Passes over data | n (each with 2 inner scans) | 3 | **1** |
| For n=2×10⁴ | ~8×10⁸ ops → slow | ~6×10⁴ ops → fast | ~2×10⁴ ops → **fastest** |
| Code complexity | Simple | Moderate | Moderate (logic subtle) |
| Interview value | Baseline only | Good stepping stone | **Gold standard** |

---

## Prefix/Suffix vs Two Pointers (Head-to-Head)

| Metric | Prefix/Suffix Arrays | Two Pointers |
|--------|---------------------|--------------|
| Time | O(n) | O(n) |
| Space | O(n) — 2 arrays × n ints | **O(1)** — 4 variables |
| Memory for n=2×10⁴ | ~160 KB (2 × 20000 × 4 bytes) | **16 bytes** |
| Conceptual difficulty | Easier (explicit arrays) | Harder (why does it work?) |
| Number of passes | 3 | **1** |
| Cache performance | Good (sequential access) | **Better** (single pass) |
| When to present | First (shows understanding) | Second (shows optimization) |

**Verdict:** Two pointers is strictly better in space and passes. Prefix/suffix is easier to explain and verify. Present prefix/suffix first, then optimize to two pointers.

---

## Why the Two-Pointer Decision Rule Works

| Condition | What we know | What we do | Why it's safe |
|-----------|-------------|------------|---------------|
| `h[left] < h[right]` | Right wall ≥ h[right] > h[left]. Left side is the bottleneck. | Process `left` using `leftMax`. Move `left++`. | Water at `left` = `leftMax - h[left]`. Right side is guaranteed tall enough. |
| `h[left] ≥ h[right]` | Left wall ≥ h[left] ≥ h[right]. Right side is the bottleneck. | Process `right` using `rightMax`. Move `right--`. | Water at `right` = `rightMax - h[right]`. Left side is guaranteed tall enough. |

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Passes | Key Insight |
|----------|------|-------|--------|-------------|
| Brute Force | O(n²) | O(1) | n (nested) | Scan left+right for each index |
| Prefix/Suffix Arrays | O(n) | O(n) | 3 | Precompute max from both sides |
| **Two Pointers** | **O(n)** | **O(1)** | **1** | **Process the shorter side; the other side is guaranteed tall enough** |

---

### 🎯 What to Present to the Interviewer

1. **Explain the water formula:** `water[i] = min(maxLeft, maxRight) - height[i]`. Draw a small diagram.
2. **Present brute force** O(n²): for each index, scan left and right. Baseline.
3. **Optimize to prefix/suffix arrays:**
   - "Instead of re-scanning, precompute `leftMax[]` and `rightMax[]` in two passes."
   - O(n) time, O(n) space. Clear and verifiable.
4. **Then optimize space (the follow-up):**
   - "We don't need the full arrays. We only need the **running** max on the side we're processing."
   - Introduce two pointers: `left=0`, `right=n-1`, `leftMax=0`, `rightMax=0`.
   - "When `h[left] < h[right]`, the right side is guaranteed to be a sufficient wall. So water at `left` depends only on `leftMax`."
5. **Walk through** the example step by step, showing how water accumulates.
6. **State complexity:** O(n) time, O(1) space. Single pass. Optimal.
7. **If asked to prove correctness:** "At each step, the shorter side is the bottleneck. We process it because its water level is fully determined by the running max on that side. The taller side guarantees the water won't 'leak'."

**One‑sentence summary:**  
*Use two pointers converging inward, always processing the shorter side (whose water level is determined by its running max since the opposite side is guaranteed taller), accumulating trapped water in O(n) time and O(1) space.*