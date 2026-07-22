### 📘 Chapter: Arrays & Strings  
### 📌 Problem 3: Contains Duplicate (LeetCode 217)

---

**Input**  
- `nums`: integer array

**Output**  
- `true` if any value appears at least twice,  
- `false` if all elements are distinct.

**Constraints**  
- `1 <= nums.length <= 10⁵`  
- `-10⁹ <= nums[i] <= 10⁹`

**Follow-up**  
- Not applicable (no explicit follow‑up in the problem statement).

---

### 🧠 Why this Data Structure?

**HashSet** (`java.util.HashSet<Integer>`)  
The core operation is checking for existence of a value that has already been seen.  
- `add()` and `contains()` run in **O(1) average** time.  
- While iterating the array, we try to insert each element into the set.  
- If an element is already present, we immediately return `true`.  
- This gives an **O(n)** time solution with **O(n)** space.

*Alternative considered:* Sorting the array. After sorting, duplicates become adjacent and can be found in a single scan.  
- Time: O(n log n) due to sorting.  
- Space: O(1) if we ignore sorting stack / use in‑place sort (Java’s `Arrays.sort()` on `int[]` is in‑place with O(log n) stack, often treated as O(1) extra).  
- Sorting is a valid trade‑off when memory is tight, but for most interviews the HashSet approach is preferred for its linear time and simplicity.

---

### 🔨 Brute Force Approach

**Method:** Nested loops  
Compare every pair `(i, j)` with `i < j`. If `nums[i] == nums[j]`, return `true`.

**Time:** O(n²)  
**Space:** O(1)

```java
public boolean containsDuplicate(int[] nums) {
    int n = nums.length;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (nums[i] == nums[j]) {
                return true;
            }
        }
    }
    return false;
}
```

---

### ⚡ Optimized Approach (HashSet)

**Method:**  
Use a `HashSet`. For each element, attempt to add it.  
`add()` returns `false` if the element already exists → duplicate found.

**Time:** O(n) – single pass with O(1) per add.  
**Space:** O(n) – set stores up to n distinct elements.

```java
import java.util.HashSet;
import java.util.Set;

public boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int num : nums) {
        if (!seen.add(num)) { // add() returns false if element already present
            return true;
        }
    }
    return false;
}
```

*Variation using `contains` + `add`:*
```java
if (seen.contains(num)) return true;
seen.add(num);
```

---

### 📊 Two-Solution Comparison & Trade-offs

| Solution           | Time   | Space  | Notes                                 |
|--------------------|--------|--------|---------------------------------------|
| Brute force (nested)| O(n²)  | O(1)   | Only for small n; too slow for 10⁵.   |
| HashSet (optimal)  | O(n)   | O(n)   | **Interview standard**; simple, linear. |

*(Sorting approach: O(n log n) time, O(1) extra space. Not shown as a main solution here to keep the two‑option focus, but worth mentioning if space is extremely limited.)*

**Trade‑off:** HashSet trades O(n) extra space for O(n) time. If space is a hard constraint and O(n) memory is not allowed, sorting becomes the better choice despite its O(n log n) time. In most coding interviews, the HashSet solution is expected.

---

### 🎯 What to Present to the Interviewer

- Start with the obvious brute‑force O(n²) to show baseline understanding.  
- Immediately improve to O(n) time using a `HashSet`.  
- Implement the `HashSet` solution cleanly, using the `add()` return value trick for conciseness.  
- Discuss the trade‑off: O(n) time requires O(n) space. If space must be O(1), mention sorting as a fallback.  
- Clarify that the HashSet approach is optimal in time and is the typical answer for this problem.

**One‑sentence summary:**  
*Use a HashSet to detect duplicates in O(n) time by leveraging O(1) lookups/adds; return true the moment an element is already in the set.*