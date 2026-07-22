### 📘 Chapter: Two Pointers  
### 📌 Problem 8: Remove Duplicates from Sorted Array (LeetCode 26)

---

**Input**  
- `nums`: an integer array sorted in **non‑decreasing order**

**Output**  
- An integer `k` — the number of unique elements in `nums`  
- The first `k` elements of the modified `nums` must contain the unique elements in the same sorted order; the remaining elements (from index `k` onward) can be ignored.

**Constraints**  
- `1 <= nums.length <= 3 * 10⁴`  
- `-100 <= nums[i] <= 100`  
- `nums` is sorted in non‑decreasing order.

**Follow-up**  
- No explicit follow‑up in the problem statement. (A common extension is *“allow at most two duplicates”*, but that is a different LeetCode problem.)

---

### 🧠 Why this Approach (Two Pointers)?

The array is **already sorted**, so all equal elements appear consecutively. The task is essentially to **compress** the array by keeping only one copy of each value while preserving order and doing it **in‑place** in O(1) extra space.

- **Two pointers** (also called “slow‑fast” pointers) are perfectly suited here:  
  - **Slow pointer (`j`)** points to the last position where a unique element has been placed.  
  - **Fast pointer (`i`)** scans through the array.  
  - Whenever `nums[i] != nums[j]` (i.e., a new distinct value is found), we increment `j` and copy `nums[i]` into `nums[j]`.  
- This yields **O(n) time** and **O(1) space**, with no need for any extra data structure.

---

### 🔨 Brute Force Approach (Extra Space / Shifting)

**Method 1: Using extra array**  
Copy unique elements into a new array, then write them back. Not in‑place, violates the problem’s implicit in‑place requirement.

**Method 2: Shifting after finding duplicates**  
When a duplicate is found, shift the rest of the array left by one position.  
This results in O(n²) time because every duplicate removal triggers an O(n) shift.

**Time:** O(n²)  
**Space:** O(1)

```java
// Example: shifting approach (not efficient)
public int removeDuplicates(int[] nums) {
    int n = nums.length;
    if (n == 0) return 0;
    int i = 0;
    while (i < n - 1) {
        if (nums[i] == nums[i + 1]) {
            // shift left
            for (int j = i + 1; j < n - 1; j++) {
                nums[j] = nums[j + 1];
            }
            n--;
        } else {
            i++;
        }
    }
    return n;
}
```
Too slow for large input; O(n²) is unnecessary when the array is sorted.

---

### ⚡ Optimized Approach – Two Pointers (O(n) time, O(1) space)

**Method:**  
- If the array is empty, return 0.  
- Initialize `j = 0` (slow pointer, index of the last unique element).  
- Iterate with `i` from 1 to end (fast pointer):  
  - If `nums[i] != nums[j]`: we’ve found a new unique number.  
    - Increment `j`.  
    - Set `nums[j] = nums[i]`.  
- After the loop, the first `j + 1` elements are the distinct elements in sorted order. Return `j + 1`.

**Time:** O(n) – single pass  
**Space:** O(1) – in‑place

```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int j = 0; // index of the last unique element
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] != nums[j]) {
            j++;
            nums[j] = nums[i];
        }
    }
    return j + 1;
}
```

**Example walkthrough:**  
`nums = [0,0,1,1,1,2,2,3,3,4]`  
- `j = 0` (value 0)  
- `i=1`: duplicate → skip  
- `i=2`: `nums[2]=1` != `nums[0]` → `j=1, nums[1]=1`  
- `i=3,4`: duplicates → skip  
- `i=5`: `2` != `nums[1]` → `j=2, nums[2]=2`  
… final `j=4`, return `5`, first five elements: `[0,1,2,3,4]`.

---

### 📊 Solution Comparison & Trade‑offs

| Solution                  | Time   | Space | In‑place? | Notes |
|---------------------------|--------|-------|-----------|-------|
| Brute force (shifting)    | O(n²)  | O(1)  | Yes       | Only for small n; inefficient. |
| Two‑pointers (slow‑fast)  | O(n)   | O(1)  | Yes       | **Optimal** and industry standard. |

**Trade‑off:**  
There is no meaningful trade‑off – the two‑pointer approach is strictly better. The shifting approach is just a conceptual baseline that reinforces why exploiting the sorted order is necessary.

---

### 🎯 What to Present to the Interviewer

1. Immediately note that the array is sorted, so duplicates are adjacent.  
2. Propose the **slow‑fast two‑pointer** technique: one pointer to place unique elements, another to scan.  
3. Walk through a small example to illustrate the logic.  
4. Write the concise O(n) code.  
5. Emphasise that it modifies the array in‑place and uses O(1) extra space.  
6. Mention that the same idea extends to “at most two duplicates” by checking `nums[i] != nums[j-1]` etc., showing ability to generalise.

**One‑sentence summary:**  
*Exploit the sorted array by using two pointers (slow for placement, fast for scanning) to overwrite duplicate elements in O(n) time and O(1) space.*