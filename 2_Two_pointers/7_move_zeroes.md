### 📘 Chapter: Two Pointers  
### 📌 Problem 7: Move Zeroes (LeetCode 283)

---

**Input**  
- `nums`: integer array

**Output**  
- The array is modified **in‑place** such that all `0`s are moved to the end, while the relative order of non‑zero elements is preserved.

**Constraints**  
- `1 <= nums.length <= 10⁴`  
- `-2³¹ <= nums[i] <= 2³¹ - 1`

**Follow‑up**  
- Could you **minimize the total number of operations** done?

---

### 🧠 Why this Approach (Two Pointers)?

We need to move zeroes to the end while keeping non‑zero order.  
- The **two‑pointer technique** (or read/write pointer) is a natural fit:  
  - One pointer (`insertPos`) marks the position where the next non‑zero element should be placed.  
  - The other pointer (`i`) scans the array.  
- When we encounter a non‑zero, we **swap** it with the element at `insertPos` and increment `insertPos`.  
  - This works because `insertPos` is either at `i` (no zeroes yet) or at the first zero in the current prefix. Swapping moves the non‑zero to the front and the zero backwards.  
- This is **O(n) time**, **O(1) space**, and performs **minimal swaps** (each non‑zero is swapped at most once).  
- An optimization: when `insertPos == i` (no leading zero), we can skip the swap to avoid unnecessary operations, directly addressing the follow‑up.

An alternative with two passes (shift then fill) uses no swaps but overwrites elements, but swapping is generally preferred as it preserves element identities (though not required) and can be more efficient in terms of operations.

---

### 🔨 Brute Force Approach (O(n²) Shift)

**Method:**  
Iterate through the array. When a `0` is found, shift all subsequent elements one position left and put a `0` at the end. Adjust pointer to recheck the current index.

**Time:** O(n²) – for each zero, shifting takes O(n).  
**Space:** O(1) – in‑place.

```java
public void moveZeroes(int[] nums) {
    int n = nums.length;
    for (int i = 0; i < n; i++) {
        if (nums[i] == 0) {
            // shift all elements after i left
            for (int j = i + 1; j < n; j++) {
                nums[j - 1] = nums[j];
            }
            nums[n - 1] = 0;
            n--;          // we moved a zero to the end, reduce effective length
            i--;          // recheck the current index (since a new element moved in)
        }
    }
}
```
Too slow for large `n`, though constraints are only 10⁴, it's suboptimal.

---

### ⚡ Optimized Approach – Two Pointers (Optimal Swap)

**Method:**  
- `insertPos = 0` – index where the next non‑zero should be placed.  
- Iterate `i` from `0` to `n-1`:  
  - If `nums[i] != 0`:  
    - swap `nums[i]` and `nums[insertPos]`.  
    - `insertPos++`.

After the loop, all non‑zeros are moved to the front in their original relative order, and all zeroes are pushed to the back.

**Time:** O(n) – single pass.  
**Space:** O(1).  
**Minimizing operations:** We can add an `if (i != insertPos)` before the swap to avoid swapping when we are at the same position (i.e., when all elements so far are non‑zero). This minimizes unnecessary swaps.

```java
public void moveZeroes(int[] nums) {
    int insertPos = 0;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] != 0) {
            if (i != insertPos) {
                // swap
                int temp = nums[i];
                nums[i] = nums[insertPos];
                nums[insertPos] = temp;
            }
            insertPos++;
        }
    }
}
```

Alternatively, a two‑pass approach (non‑swapping) works but does more assignments:  
```java
// pass1: shift non-zero forward, pass2: fill zeroes
int insertPos = 0;
for (int num : nums) {
    if (num != 0) nums[insertPos++] = num;
}
while (insertPos < nums.length) nums[insertPos++] = 0;
```
This uses overwriting, not swapping, but it's still O(n) and O(1) space, with a similar number of operations. The swap version might be slightly better if the non‑zero elements are large objects (not the case here).

---

### 📊 Two‑Solution Comparison & Trade‑offs

| Solution               | Time   | Space | Operations                     | Notes |
|------------------------|--------|-------|-------------------------------|-------|
| Brute force (shift)    | O(n²)  | O(1)  | Many shifts, O(n²) writes.    | Only for conceptual baseline. |
| Two‑pointer swap (optimal) | O(n) | O(1)  | Exactly number of non‑zeros swaps (or fewer if skip when i==insertPos). | **Best** – minimal writes, meets follow‑up. |
| Two‑pass overwrite     | O(n)   | O(1)  | n assignments for non‑zero + number of zero writes. | Simple but slightly more writes; no swaps. |

**Trade‑off:**  
The swap version minimizes operations because it only swaps non‑zero elements that are actually out of place. The two‑pass overwrite is arguably easier to read but performs extra writes for zero‑filling. In an interview, both are acceptable; the swap variant demonstrates deeper understanding of operation‑minimization (the follow‑up).

---

### 🎯 What to Present to the Interviewer

1. Clarify the in‑place constraint and that relative order of non‑zeros must be kept.  
2. Propose the **two‑pointer** approach: one pointer for the next non‑zero position.  
3. Walk through the algorithm: scan the array, when non‑zero found, swap with the insert position (if different), advance insert pointer.  
4. Explain why this works and that it uses O(n) time and O(1) space.  
5. Highlight the **minimal operations** optimization: avoid swapping when `i == insertPos`.  
6. Optionally mention the two‑pass overwrite as an alternative, and compare.  
7. Conclude that the swap solution is optimal for both time and operation count.

**One‑sentence summary:**  
*Use a write pointer to track the next non‑zero position; swap each non‑zero encountered with that position, moving all zeroes to the end in O(n) time and O(1) space while preserving order and minimizing operations.*