### 📘 Chapter: Two Pointers  
### 📌 Problem 6: Sort Colors (LeetCode 75)

---

**Input**  
- `nums`: an integer array where `nums[i]` is `0`, `1`, or `2` (representing red, white, blue respectively).

**Output**  
- The array sorted **in‑place** so that all `0`s come first, then all `1`s, then all `2`s.

**Constraints**  
- `n == nums.length`  
- `1 <= n <= 300`  
- `nums[i]` is either `0`, `1`, or `2`.

**Follow‑up**  
- Could you come up with a **one‑pass** algorithm using **only constant extra space**?

---

### 🧠 Why this Approach (Three Pointers / Dutch National Flag)?

We need to sort an array of only three distinct values in‑place.  
- A **counting sort** (two‑pass) is straightforward: count the occurrences of 0, 1, 2, then overwrite the array. It uses O(1) extra space but requires **two passes**.  
- The **Dutch National Flag algorithm** uses **three pointers** (`low`, `mid`, `high`) to partition the array into three sections in a **single pass**:
  - `[0, low)` – all `0`s  
  - `[low, mid)` – all `1`s  
  - `(high, n-1]` – all `2`s  
- `mid` scans the array; when it sees `0` it swaps with `low` and increments both; when it sees `2` it swaps with `high` and decrements `high`; when it sees `1` it just moves `mid` forward.  
- This yields **O(n) time** and **O(1) space** in one pass, perfectly matching the follow‑up.

No libraries, no extra arrays – just pointer moves and swaps.

---

### 🔨 Simple Approach – Counting Sort (Two Pass, O(1) space)

**Method:**  
1. First pass: count how many `0`s, `1`s, and `2`s exist.  
2. Second pass: overwrite the array with the counted numbers of `0`s, then `1`s, then `2`s.

**Time:** O(n) – two passes.  
**Space:** O(1) – three counter variables.

```java
public void sortColors(int[] nums) {
    int count0 = 0, count1 = 0, count2 = 0;
    for (int num : nums) {
        if (num == 0) count0++;
        else if (num == 1) count1++;
        else count2++;
    }
    int i = 0;
    while (count0-- > 0) nums[i++] = 0;
    while (count1-- > 0) nums[i++] = 1;
    while (count2-- > 0) nums[i++] = 2;
}
```

---

### ⚡ Optimized Approach – Dutch National Flag (One Pass, O(1) space)

**Method:**  
- Initialize `low = 0`, `mid = 0`, `high = nums.length - 1`.  
- While `mid <= high`:  
  - If `nums[mid] == 0`: swap `nums[mid]` with `nums[low]`, then `low++` and `mid++`.  
  - Else if `nums[mid] == 1`: just `mid++`.  
  - Else (`nums[mid] == 2`): swap `nums[mid]` with `nums[high]`, then `high--` (do **not** increment `mid` because the swapped element from `high` hasn’t been processed yet).

**Time:** O(n) – single pass.  
**Space:** O(1).

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
        }
    }
}

private void swap(int[] nums, int i, int j) {
    int temp = nums[i];
    nums[i] = nums[j];
    nums[j] = temp;
}
```

---

### 📊 Two‑Solution Comparison & Trade‑offs

| Solution                | Time | Space | Passes | Notes |
|-------------------------|------|-------|--------|-------|
| Counting sort           | O(n) | O(1)  | 2      | Extremely simple, but does **not** meet the one‑pass follow‑up. |
| Dutch National Flag     | O(n) | O(1)  | 1      | **Optimal**; satisfies the follow‑up. Slightly more pointer‑care needed. |

**Trade‑off:**  
- Counting sort is easier to code and perfectly fine when a second pass is allowed, but it doesn’t demonstrate the elegant in‑place partitioning that the follow‑up expects.  
- Dutch National Flag is the **canonical** solution for this problem. The interviewer will look for it explicitly. It uses no extra passes and shows strong command of pointer manipulation.

---

### 🎯 What to Present to the Interviewer

1. Recognize that the array contains only three values, so sorting can be done without a general‑purpose sort.  
2. Propose the **counting sort** approach first (two‑pass, O(1) space) as a straightforward baseline.  
3. Mention the follow‑up and then introduce the **Dutch National Flag algorithm** – explain the three regions (`0s`, `1s`, `2s`) and the roles of `low`, `mid`, `high`.  
4. Walk through the algorithm with an example, especially emphasizing why `mid` is **not** incremented when swapping a `2` (the new element from `high` is unknown).  
5. Code the one‑pass solution cleanly.  
6. Conclude that it’s O(n) time, O(1) space, and exactly one pass – meeting all constraints.

**One‑sentence summary:**  
*Partition the array into three sections using low, mid, high pointers (Dutch National Flag algorithm) to sort in one pass with constant extra space.*