### 📘 Chapter: Stack  
### 📌 Problem 7: Car Fleet (LeetCode 853)

---

**Input**  
- `target`: integer, the destination mile.  
- `position`: integer array of starting positions of `n` cars (miles from start 0).  
- `speed`: integer array of speeds (miles per hour) corresponding to each car.

**Output**  
- The number of **car fleets** that will arrive at the destination.

**Definition**  
- Cars cannot pass each other; a faster car catching up to a slower car forms a fleet that travels at the slower car’s speed.  
- A car fleet is a group of cars traveling together.  
- If a car catches up to a fleet exactly at the destination, it’s still part of that fleet.

**Constraints**  
- `n == position.length == speed.length`  
- `1 <= n <= 10⁵`  
- `0 < target <= 10⁶`  
- `0 <= position[i] < target`, all positions are unique.  
- `0 < speed[i] <= 10⁶`

**Follow‑up**  
- None explicitly; the problem itself demands an O(n log n) solution or better. The optimal approach is O(n log n) due to sorting.

---

### 🧠 Why this Data Structure (Monotonic Stack)?

The key insight: **time to reach the target** for a car (if there were no other cars) is `(target - position) / speed`.  
A car can only merge with a car (or fleet) **ahead** of it. If we process cars from the one closest to the target backward (descending position), we can simulate fleet formation:

- The car closest to the target defines a potential fleet. Its arrival time is `time_1`.  
- The next car (further back) has `time_2`.  
  - If `time_2 <= time_1`, this faster/farther car will catch up to the fleet ahead before the target, so it merges into that fleet (does **not** create a new fleet).  
  - If `time_2 > time_1`, this car is too slow to catch the fleet ahead; it will arrive later and form a **new fleet**.  

Thus, we need a structure that holds the **arrival times of fleets** that haven't been caught. A **stack** naturally tracks these times in increasing order (monotonic increasing from bottom to top).  
- For each car (sorted by position descending), compute its time.  
- While its time ≤ top of stack, it catches the fleet represented by the top – we can pop (or simply not push). Actually, we just compare with the **current slowest fleet ahead**; the top of the stack holds the time of the fleet that is immediately ahead. If the new car’s time is ≤ that, it merges and does not need to be pushed; if >, it becomes a new fleet and we push its time.  

At the end, the size of the stack is the number of fleets.

- **Why not a simple variable?** The stack maintains a history of fleets that are ahead, each with increasing arrival times. A new car only needs to compare with the most recent fleet (top). So a variable would suffice for counting, but the stack is a natural representation and simplifies reasoning. The standard solution often uses a **monotonic stack** concept: processing from right to left, we push only when the current time is greater than the last pushed time, then the number of pushes is the fleet count.  

Therefore, **stack** is used either explicitly or implicitly (just a counter and a variable for the last fleet time). The explicit stack is a clean monotonic stack example.

---

### 🔨 Brute Force Approach (Simulating with O(n²))

**Method:**  
For each car, repeatedly check if it will catch any car ahead of it.  
We can simulate by sorting by position and processing from front to back multiple times, merging those that catch up.  
A straightforward O(n²) way:  
- Sort cars by position.  
- For each car `i` (from 0 to n-1), look at all cars `j > i` that start ahead. Determine if `i` catches `j` before target. If yes, merge them (the faster car's speed becomes the slower car's speed, or we can mark it as removed).  
- Keep merging until no more merges happen, then count distinct fleets.  

This is messy and O(n²) due to repeated passes and collision checks.  

A slightly cleaner O(n²):  
- Sort cars by position.  
- Compute arrival times without interference.  
- For each car `i`, check all cars `j` ahead (`j > i`): if `time[i] <= time[j]`, then car `i` catches car `j`, so car `i` effectively has the same arrival time as car `j` (it merges). So we can update `time[i] = max(time[i], time[j])` for any `j > i` that it catches. At the end, count the number of distinct effective times. This still O(n²) due to nested loops.

```java
// Brute force (O(n^2)) - not efficient
public int carFleet(int target, int[] position, int[] speed) {
    int n = position.length;
    // combine and sort by position
    int[][] cars = new int[n][2];
    for (int i = 0; i < n; i++) {
        cars[i][0] = position[i];
        cars[i][1] = speed[i];
    }
    Arrays.sort(cars, (a, b) -> Integer.compare(a[0], b[0]));
    double[] times = new double[n];
    for (int i = 0; i < n; i++) {
        times[i] = (double)(target - cars[i][0]) / cars[i][1];
    }
    // propagate merges: from right to left maybe?
    // O(n^2) check
    for (int i = n-1; i >= 0; i--) {
        for (int j = i+1; j < n; j++) {
            if (times[i] <= times[j]) {
                times[i] = times[j]; // i merges with j's fleet, takes j's arrival time
                break; // once merged, no need to check further?
            }
        }
    }
    // count distinct times
    Set<Double> fleets = new HashSet<>();
    for (double t : times) fleets.add(t);
    return fleets.size();
}
```
Too slow for n=10⁵.

---

### ⚡ Optimized Approach – Sorting + Monotonic Stack (O(n log n) time, O(n) space)

**Method:**  
1. Pair each car’s `position` and `speed`, then sort these pairs in **descending order of position** (closest to target first).  
2. Use a stack (`Deque<Double>`) to store the arrival times of fleets.  
3. For each car (from closest to farthest):  
   - Compute its time to reach the target: `time = (double)(target - pos) / speed`.  
   - If the stack is empty, push `time`.  
   - Else, if `time > stack.peek()`: this car cannot catch the fleet ahead (it’s slower/arrives later), so it forms a **new fleet**, push `time`.  
   - Else (`time <= stack.peek()`): this car will catch the fleet ahead before the target; it merges and does **not** create a new fleet (we do nothing, effectively discarding this car).  
4. The number of fleets is `stack.size()`.

**Why descending order?**  
Processing from the car closest to the target ensures that the fleet’s arrival time (the slowest in that fleet) is already determined. A car from behind can only merge if it would catch up before the fleet reaches target, i.e., its unhindered time ≤ fleet’s time.

**Time:** O(n log n) due to sorting.  
**Space:** O(n) for the stack and the cars array.

```java
import java.util.*;

public int carFleet(int target, int[] position, int[] speed) {
    int n = position.length;
    if (n == 0) return 0;

    // combine position and speed into a 2D array
    int[][] cars = new int[n][2];
    for (int i = 0; i < n; i++) {
        cars[i][0] = position[i];
        cars[i][1] = speed[i];
    }

    // sort by position descending (closest to target first)
    Arrays.sort(cars, (a, b) -> Integer.compare(b[0], a[0]));

    Deque<Double> stack = new ArrayDeque<>();

    for (int[] car : cars) {
        double time = (double)(target - car[0]) / car[1];
        if (stack.isEmpty() || time > stack.peek()) {
            stack.push(time); // new fleet
        }
        // else: merges into the fleet represented by stack.peek(), do nothing
    }
    return stack.size();
}
```

**Note:** We could avoid the stack entirely and just keep a variable `lastTime` (the slowest fleet’s time so far). If the current car’s time > `lastTime`, increment fleet count and update `lastTime`. This gives O(1) extra space beyond the cars array.

```java
// O(1) extra space (excluding input copy)
double lastTime = -1;
int fleets = 0;
for (int[] car : cars) {
    double time = (double)(target - car[0]) / car[1];
    if (time > lastTime) {
        fleets++;
        lastTime = time;
    }
}
return fleets;
```

This is even simpler and still O(n log n) time. I'll present both as the optimized solution – the stack one illustrates monotonic stack, the variable one shows we don't truly need the stack.

---

### 📊 Solution Comparison & Trade‑offs

| Solution                | Time     | Space    | Notes |
|-------------------------|----------|----------|-------|
| Brute force (O(n²))     | O(n²)    | O(n)     | Too slow; conceptual only. |
| Sorting + Stack         | O(n log n) | O(n)   | Demonstrates monotonic stack elegantly. |
| Sorting + lastTime var  | O(n log n) | O(1) (excluding input copy) | Simplest, minimal space; uses same logic. |

**Trade‑off:**  
- The stack version explicitly models the fleet formation and is a nice example of a monotonic stack, but it uses O(n) space.  
- The variable version realises that we only need to compare with the most recent fleet’s time, so we can replace the stack with a single variable. Both are linear after sorting.  
- In an interview, I’d present the stack logic and then note the constant‑space optimization.

---

### 🎯 What to Present to the Interviewer

1. Clarify the no‑overtaking rule and fleet merging.  
2. Define the time to target for each car: `(target - pos) / speed`.  
3. Sort cars by position **descending** (closest to target first).  
4. Explain that a car merges with the fleet ahead if its time ≤ the fleet’s time.  
5. Use a **stack** (monotonic increasing in time) to store the times of fleets. Walk through an example.  
6. Write the Java code with a `Deque<Double>`.  
7. Point out that the stack can be replaced by a single variable (`lastTime`) and a counter, achieving O(1) extra space.  
8. State final complexity: O(n log n) time due to sorting, O(n) or O(1) space.

**One‑sentence summary:**  
*Sort cars by distance to target in descending order and compute arrival times; a car forms a new fleet only if its time is strictly greater than the time of the fleet ahead, which can be tracked with a monotonic stack (or a single variable) to count fleets in O(n log n) time.*