### 📘 Chapter: Arrays & Strings  
### 📌 Problem 8: Longest Consecutive Sequence (LeetCode 128)

---

**Input**  
- `nums`: unsorted integer array

**Output**  
- Length of the longest consecutive elements sequence (consecutive in value, not in position).

**Constraints**  
- `0 <= nums.length <= 10⁵`  
- `-10⁹ <= nums[i] <= 10⁹`

**Requirement**  
- Algorithm must run in **O(n)** time.

---

### 🧠 Why this Data Structure?

The core operation is checking whether a number's *next* consecutive value exists while building sequences.  
- A **HashSet** (`java.util.HashSet<Integer>`) provides **O(1) average** lookup and insertion.  
- We insert all numbers into the set. Then for each element, if it is the **start of a sequence** (`num - 1` is not in the set), we count how long the chain `num+1, num+2, …` exists in the set.  
- Each element is visited only in the outer loop and at most once in an inner while‑loop, giving total **O(n)** time.  
- No sorting is needed, meeting the strict O(n) requirement.

---

### 🔨 Brute Force / Simpler Non‑Optimal Approach (Sorting)

**Method:**  
Sort the array. Then scan linearly, tracking the current consecutive streak. When a gap appears (difference > 1), reset; when equal, skip duplicates; when consecutive, increment.

**Time:** O(n log n) – sorting dominates  
**Space:** O(1) or O(n) depending on sort implementation

❌ Does not meet O(n) requirement, but is easy to implement.

```java
public int longestConsecutive(int[] nums) {
    if (nums.length == 0) return 0;
    Arrays.sort(nums);
    int longest = 1, current = 1;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] == nums[i - 1]) continue;        // skip duplicates
        if (nums[i] == nums[i - 1] + 1) {
            current++;
        } else {
            longest = Math.max(longest, current);
            current = 1;
        }
    }
    return Math.max(longest, current);
}
```

---

### ⚡ Optimized Approach – HashSet (O(n) time)

**Method:**  
1. Add all numbers to a `HashSet`.  
2. For each number, check if it’s a **sequence start** (i.e., `num - 1` not in set).  
3. If yes, count the streak upward (`num+1, num+2, …`) using the set.  
4. Track the maximum streak length.

Each number is processed at most twice (once as a start-check, once in a while loop), guaranteeing O(n) overall.

**Time:** O(n) – each element is touched a constant number of times  
**Space:** O(n) – the HashSet stores all numbers

```java
public int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int num : nums) set.add(num);

    int longest = 0;
    for (int num : set) {
        // only start counting if num is the beginning of a sequence
        if (!set.contains(num - 1)) {
            int currentNum = num;
            int currentStreak = 1;
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

---

### 📊 Solution Comparison & Trade-offs

| Solution       | Time   | Space | Meets O(n)? | Notes |
|----------------|--------|-------|-------------|-------|
| Sorting        | O(n log n) | O(1) or O(n) | ❌ No    | Simple to code, acceptable if O(n log n) were allowed. |
| HashSet        | O(n)   | O(n)  | ✅ Yes      | **Only solution meeting the problem’s O(n) requirement**. Intuitive “sequence start” logic. |

**Trade‑off:**  
- The sorting solution is more memory‑frugal (if in‑place sort) but fails the O(n) constraint.  
- The HashSet solution uses O(n) extra memory but achieves true linear time and elegantly handles duplicates and arbitrary ranges.  
- In an interview, lead with the HashSet approach and mention sorting as a fallback if O(n) were not required.

---

### 🎯 What to Present to the Interviewer

1. Immediately note the O(n) requirement and that sorting would be O(n log n) – disqualifying it.  
2. Propose the **HashSet** idea: insert all numbers, then only expand from numbers that have no left neighbour (`num-1`).  
3. Walk through the code, stressing that the inner while‑loop runs at most `n` times total across the whole function.  
4. Mention that this is an **amortised O(n)** analysis – each element is visited only when starting a sequence and then at most once when it is part of another sequence.  
5. If time, contrast with sorting to show understanding of trade‑offs.

**One‑sentence summary:**  
*Use a HashSet for O(1) lookups and expand sequences only from numbers without a predecessor, achieving O(n) time.*