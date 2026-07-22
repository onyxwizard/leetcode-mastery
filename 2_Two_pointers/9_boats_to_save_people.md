### 📘 Chapter: Two Pointers  
### 📌 Problem 9: Boats to Save People (LeetCode 881)

---

**Input**  
- `people`: integer array of positive weights  
- `limit`: maximum weight a boat can carry

**Output**  
- The **minimum number of boats** required to rescue everyone, given:  
  - Each boat can carry **at most two people**.  
  - The sum of their weights must be ≤ `limit`.

**Constraints**  
- `1 <= people.length <= 5 * 10⁴`  
- `1 <= people[i] <= limit <= 3 * 10⁴`

**Follow-up**  
- The problem is self‑contained; the natural follow‑up in an interview is to prove the greedy choice is optimal or to handle a boat capacity > 2 (which would require DP).

---

### 🧠 Why this Approach (Sorting + Two Pointers / Greedy)

The core decision: for the heaviest remaining person, is it better to pair them with the lightest possible person, or let them go alone?  

- **Greedy insight:**  
  If the heaviest person can share a boat with the lightest person, they should – because the lightest person is the easiest to pair, and pairing them with the heaviest “saves” a boat.  
  If they cannot share (sum > limit), the heaviest person must go alone anyway.  
- Sorting the array enables us to always pick the current lightest and heaviest in O(1) with two pointers.  
- This greedy algorithm **provably** yields the minimum number of boats (standard exchange argument).  
- Time complexity: O(n log n) due to sorting. With a counting/bucket sort (since weights ≤ limit ≤ 30000), we could achieve O(n + limit) but in practice sorting is simpler.

**Data structures:** Just the sorted array and two index pointers – no extra heap or set required.

---

### 🔨 Brute Force / Naive Approach (Backtracking / Exponential)

**Method:**  
Try all possible ways to partition the people into boats (each boat ≤ 2 people) and find the minimum number of boats. This is essentially a combinatorial explosion – trying to decide for each person which boat to place them in.  

**Time:** O(2ⁿ) (exponential) – completely impractical for `n = 5×10⁴`.  
**Space:** O(n) recursion stack.  

We can illustrate it conceptually but will not provide a full implementation because it’s not viable.

```java
// Pseudo-code: backtracking (not runnable for large n)
int minBoats = Integer.MAX_VALUE;
void backtrack(int idx, int[] people, boolean[] used, int boatCount, int currentLoad, int limit) {
    if (idx == people.length) {
        minBoats = Math.min(minBoats, boatCount);
        return;
    }
    if (used[idx]) backtrack(idx+1, ...);
    else {
        // Option 1: alone
        used[idx]=true;
        backtrack(idx+1, ..., boatCount+1, 0, limit);
        used[idx]=false;
        // Option 2: pair with an unused person j > idx
        for (int j=idx+1; j<people.length; j++) {
            if (!used[j] && people[idx]+people[j]<=limit) {
                used[idx]=used[j]=true;
                backtrack(idx+1, ..., boatCount+1, ...);
                used[idx]=used[j]=false;
            }
        }
    }
}
```
This is only mentioned to contrast with the optimal solution.

---

### ⚡ Optimized Approach – Greedy + Two Pointers (after Sorting)

**Method:**  
1. Sort the array `people`.  
2. `left = 0`, `right = n-1`, `boats = 0`.  
3. While `left <= right`:  
   - If `people[left] + people[right] <= limit`:  
     → Both can board the same boat: `left++`, `right--`.  
   - Else:  
     → The heaviest person goes alone: `right--`.  
   - `boats++`.  
4. Return `boats`.

**Why it works:**  
Every time we take the heaviest remaining person, we try to pair them with the lightest (to maximise chance of success). If the sum exceeds the limit, no one can pair with the heaviest, so they must go alone. If the sum fits, pairing them is optimal because it removes the heaviest (who is the most difficult to pair) together with the easiest-to-pair lightest, leaving more flexible people behind.

**Time:** O(n log n) for sorting, then O(n) two-pointer pass.  
**Space:** O(1) extra, ignoring the input array (or O(1) if we sort in place).

```java
import java.util.Arrays;

public int numRescueBoats(int[] people, int limit) {
    Arrays.sort(people);
    int left = 0, right = people.length - 1;
    int boats = 0;

    while (left <= right) {
        if (people[left] + people[right] <= limit) {
            left++;   // lightest person boarded
        }
        // heaviest always boards
        right--;
        boats++;
    }
    return boats;
}
```

*Note:* The `left` only increments when the pair is possible; `right` always decrements because the heaviest person boards a boat in every iteration.

---

### 📊 Solution Comparison & Trade‑offs

| Solution                       | Time       | Space | Feasibility |
|--------------------------------|------------|-------|-------------|
| Brute force (backtracking)     | Exponential | O(n)  | Impractical beyond tiny n. |
| Sorting + Greedy Two Pointers  | O(n log n) | O(1)  | **Optimal** – proven greedy, efficient. |
| Counting sort + Two Pointers   | O(n + limit) | O(limit) | Faster in theory if limit is small, but coding overhead. |

**Trade‑off:**  
- Sorting is the standard solution, and for `n = 5×10⁴`, O(n log n) is fast enough.  
- If the weight range is much smaller than n, bucket/counting sort can reduce the asymptotic time, but in most interviews, the sort-based solution is perfect. The greedy proof is the key to showcase understanding.

---

### 🎯 What to Present to the Interviewer

1. Start by clarifying the problem: each boat ≤ 2 people, total weight ≤ limit. We need the minimum number of boats.  
2. Mention that a brute‑force exploration of all pairings is exponential and infeasible.  
3. Introduce the **greedy strategy**: sort the people, then pair the heaviest with the lightest if possible.  
4. Walk through a small example to demonstrate why this is optimal (exchange argument: if the heaviest can share with someone, making them share with the lightest never reduces the number of boats needed).  
5. Write the two‑pointer code cleanly in Java.  
6. State complexity: O(n log n) time, O(1) space (or O(n) if not in‑place).  
7. (Optional) Mention that if a boat could hold more than two people, the problem becomes much harder (bin packing), but this greedy is valid because of the “at most two” constraint.

**One‑sentence summary:**  
*Sort the array, then greedily pair the heaviest person with the lightest if their sum is within limit – otherwise send the heaviest alone – to achieve the minimum number of boats in O(n log n) time.*