### 📘 Chapter: Stack  
### 📌 Problem 7: Car Fleet (LeetCode 853)

---

**Input**  
- `target`: integer — the destination mile marker.  
- `position`: integer array — starting positions of `n` cars (miles from start).  
- `speed`: integer array — speeds (miles/hour) of each car.

**Output**  
- The number of **car fleets** that arrive at the destination.

**Definition**  
- Cars **cannot pass** each other. A faster car catching up to a slower car (or fleet) merges into it and travels at the slower speed.  
- A **car fleet** is a group of one or more cars traveling together.  
- If a car catches up to a fleet **exactly at the destination**, it's still part of that fleet.

**Constraints**  
- `n == position.length == speed.length`  
- `1 <= n <= 10⁵`  
- `0 < target <= 10⁶`  
- `0 <= position[i] < target` (all positions unique)  
- `0 < speed[i] <= 10⁶`

**Example**  
```
Input:  target = 12, position = [10, 8, 0, 5, 3], speed = [2, 4, 1, 1, 3]
Output: 3
Explanation:
  Car at pos=10, speed=2 → time = (12-10)/2 = 1 hr
  Car at pos=8,  speed=4 → time = (12-8)/4  = 1 hr → catches car at 10 → FLEET 1
  Car at pos=5,  speed=1 → time = (12-5)/1  = 7 hr → too slow to catch Fleet 1 → FLEET 2
  Car at pos=3,  speed=3 → time = (12-3)/3  = 3 hr → catches Fleet 2 (3 ≤ 7) → merges
  Car at pos=0,  speed=1 → time = (12-0)/1  = 12 hr → too slow → FLEET 3
  Total: 3 fleets.

Input:  target = 10, position = [3], speed = [3]
Output: 1

Input:  target = 100, position = [0,2,4], speed = [4,2,1]
Output: 1
Explanation: All cars eventually merge into one fleet.
```

**Follow-up**  
- None explicitly. The optimal solution is O(n log n) due to sorting.

---

### 🧠 Core Idea

Each car has an **unhindered arrival time**: `time = (target - position) / speed`.

A car can only merge with a car/fleet **ahead** of it (closer to target). If we process cars from **closest to target → farthest**:

- The first car (closest) defines a fleet with arrival time `t₁`.
- The next car has time `t₂`:
  - If `t₂ ≤ t₁`: this car is **faster** (or equal) — it catches the fleet ahead → **merges** (no new fleet).
  - If `t₂ > t₁`: this car is **slower** — it can never catch up → **new fleet**.

This naturally forms a **monotonic stack** of fleet arrival times (increasing from top to bottom).

**Why sorting by position descending?**  
The car closest to target is the "leader" — no one is ahead of it. Each subsequent car (farther back) can only interact with fleets already processed (ahead of it). This one-directional dependency makes a single pass sufficient.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Pairwise Merge Simulation (O(n²) Time)

**Idea:** Sort cars by position. For each car, check all cars ahead to see if it catches them (its time ≤ their time). If it catches any, it merges (takes on the fleet's arrival time). Count distinct effective arrival times at the end.

**Time:** O(n²) — nested loop for merge propagation.  
**Space:** O(n).

```java
import java.util.*;

public int carFleet(int target, int[] position, int[] speed) {
    int n = position.length;
    int[][] cars = new int[n][2];
    for (int i = 0; i < n; i++) {
        cars[i][0] = position[i];
        cars[i][1] = speed[i];
    }
    Arrays.sort(cars, (a, b) -> Integer.compare(a[0], b[0])); // ascending position

    double[] times = new double[n];
    for (int i = 0; i < n; i++) {
        times[i] = (double)(target - cars[i][0]) / cars[i][1];
    }

    // Propagate merges: process from right (closest to target) to left
    for (int i = n - 2; i >= 0; i--) {
        for (int j = i + 1; j < n; j++) {
            if (times[i] <= times[j]) {
                times[i] = times[j]; // car i merges with fleet j
                break;
            }
        }
    }

    // Count distinct arrival times
    Set<Double> fleets = new HashSet<>();
    for (double t : times) fleets.add(t);
    return fleets.size();
}
```

### 🔍 Sample Iteration

**Input:** `target = 12, position = [10, 8, 0, 5, 3], speed = [2, 4, 1, 1, 3]`

**After sorting by position (ascending):**

| Index | Position | Speed | Unhindered time |
|-------|----------|-------|-----------------|
| 0 | 0 | 1 | (12-0)/1 = 12.0 |
| 1 | 3 | 3 | (12-3)/3 = 3.0 |
| 2 | 5 | 1 | (12-5)/1 = 7.0 |
| 3 | 8 | 4 | (12-8)/4 = 1.0 |
| 4 | 10 | 2 | (12-10)/2 = 1.0 |

**Merge propagation (right to left):**

| i | times[i] (before) | Check j ahead | Merge? | times[i] (after) |
|---|-------------------|---------------|--------|-------------------|
| 3 | 1.0 | j=4: times[4]=1.0. 1.0 ≤ 1.0 ✅ | Merges with car 4 | **1.0** |
| 2 | 7.0 | j=3: times[3]=1.0. 7.0 ≤ 1.0? ❌. j=4: 7.0 ≤ 1.0? ❌ | No merge | **7.0** |
| 1 | 3.0 | j=2: times[2]=7.0. 3.0 ≤ 7.0 ✅ | Merges with car 2's fleet | **7.0** |
| 0 | 12.0 | j=1: times[1]=7.0. 12.0 ≤ 7.0? ❌. j=2: 12.0 ≤ 7.0? ❌. j=3: 12.0 ≤ 1.0? ❌. j=4: ❌ | No merge | **12.0** |

**Final times:** `[12.0, 7.0, 7.0, 1.0, 1.0]`  
**Distinct times:** `{12.0, 7.0, 1.0}` → **3 fleets** ✅

> ⚠️ For n = 10⁵: the inner loop can scan up to n elements for each car → O(n²) = 10¹⁰ operations. **Too slow.**

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACHES

---

## 2A. Sorting + Monotonic Stack (O(n log n) Time, O(n) Space) ✅

**Idea:**  
1. Pair `(position, speed)` for each car. Sort by position **descending** (closest to target first).  
2. Use a stack to store arrival times of fleets.  
3. For each car (closest → farthest):  
   - Compute `time = (target - pos) / speed`.  
   - If stack is empty OR `time > stack.peek()`: this car is **slower** than the fleet ahead → **new fleet** → push `time`.  
   - Else (`time ≤ stack.peek()`): this car **catches** the fleet ahead → **merges** → do nothing (don't push).  
4. Answer = `stack.size()`.

**Why it works:**  
The stack maintains fleet arrival times in **increasing order** (top = most recent fleet = the one immediately ahead of the current car). A new car only needs to compare with the **nearest fleet ahead** (top of stack). If it can't catch that fleet, it certainly can't catch any fleet further ahead (which has an even smaller arrival time).

**Time:** O(n log n) — sorting dominates.  
**Space:** O(n) — stack + cars array.

```java
import java.util.*;

public int carFleet(int target, int[] position, int[] speed) {
    int n = position.length;
    if (n == 0) return 0;

    // Pair position and speed
    int[][] cars = new int[n][2];
    for (int i = 0; i < n; i++) {
        cars[i][0] = position[i];
        cars[i][1] = speed[i];
    }

    // Sort by position DESCENDING (closest to target first)
    Arrays.sort(cars, (a, b) -> Integer.compare(b[0], a[0]));

    Deque<Double> stack = new ArrayDeque<>();

    for (int[] car : cars) {
        double time = (double)(target - car[0]) / car[1];

        if (stack.isEmpty() || time > stack.peek()) {
            stack.push(time);  // new fleet (slower than fleet ahead)
        }
        // else: time <= stack.peek() → merges into fleet ahead (do nothing)
    }

    return stack.size();
}
```

### 🔍 Sample Iteration

**Input:** `target = 12, position = [10, 8, 0, 5, 3], speed = [2, 4, 1, 1, 3]`

**After sorting by position descending:**

| Order | Position | Speed | time = (12 - pos) / speed |
|-------|----------|-------|---------------------------|
| 1st | 10 | 2 | (12-10)/2 = **1.0** |
| 2nd | 8 | 4 | (12-8)/4 = **1.0** |
| 3rd | 5 | 1 | (12-5)/1 = **7.0** |
| 4th | 3 | 3 | (12-3)/3 = **3.0** |
| 5th | 0 | 1 | (12-0)/1 = **12.0** |

**Stack processing:**

| Step | Car (pos, speed) | time | Stack BEFORE (top→bottom) | time > peek? | Action | Stack AFTER | Fleets |
|------|-----------------|------|---------------------------|--------------|--------|-------------|--------|
| 1 | (10, 2) | 1.0 | `[]` (empty) | — | **Push** (first car) | `[1.0]` | 1 |
| 2 | (8, 4) | 1.0 | `[1.0]` | 1.0 > 1.0? **No** (≤) | **Merge** (catches fleet at time 1.0) | `[1.0]` | 1 |
| 3 | (5, 1) | 7.0 | `[1.0]` | 7.0 > 1.0? **Yes** | **Push** (new fleet, too slow to catch) | `[7.0, 1.0]` | 2 |
| 4 | (3, 3) | 3.0 | `[7.0, 1.0]` | 3.0 > 7.0? **No** (≤) | **Merge** (catches fleet at time 7.0) | `[7.0, 1.0]` | 2 |
| 5 | (0, 1) | 12.0 | `[7.0, 1.0]` | 12.0 > 7.0? **Yes** | **Push** (new fleet, too slow) | `[12.0, 7.0, 1.0]` | 3 |

**Result:** stack.size() = **3** ✅

---

### 🔍 Visual Stack Trace

```
Cars sorted by position (descending): pos=10, 8, 5, 3, 0
                                       time=1, 1, 7, 3, 12

Step 1: pos=10, time=1.0
  Stack: [1.0]  ← Fleet 1 (arrives at t=1)

Step 2: pos=8, time=1.0
  1.0 ≤ 1.0 → MERGES into Fleet 1
  Stack: [1.0]  ← Still 1 fleet

Step 3: pos=5, time=7.0
  7.0 > 1.0 → NEW FLEET (can't catch Fleet 1)
  Stack: [7.0, 1.0]  ← Fleet 2 (arrives at t=7), Fleet 1 (arrives at t=1)

Step 4: pos=3, time=3.0
  3.0 ≤ 7.0 → MERGES into Fleet 2 (catches it before target)
  Stack: [7.0, 1.0]  ← Still 2 fleets

Step 5: pos=0, time=12.0
  12.0 > 7.0 → NEW FLEET (can't catch Fleet 2)
  Stack: [12.0, 7.0, 1.0]  ← Fleet 3, Fleet 2, Fleet 1

Answer: 3 fleets ✅
```

---

### 🔍 Physical Interpretation (Timeline)

```
Position:  0     3     5     8    10    12 (target)
           |     |     |     |     |     |
Car:       E     D     C     B     A     🏁
Speed:     1     3     1     4     2

Time=0:    E(0)  D(3)  C(5)  B(8)  A(10)
Time=1:    E(1)  D(6)  C(6)  B(12) A(12) ← A and B arrive! Fleet 1 = {A, B}
                                         (B caught A at target, both at t=1)
Time=3:    E(3)  D(12) C(8)              ← D arrives at t=1? Wait...

Let me recalculate:
  A: pos=10, speed=2 → arrives at t=(12-10)/2=1
  B: pos=8,  speed=4 → arrives at t=(12-8)/4=1 → catches A exactly at target → Fleet 1
  C: pos=5,  speed=1 → arrives at t=(12-5)/1=7 → Fleet 2 (alone, no one ahead to catch)
  D: pos=3,  speed=3 → arrives at t=(12-3)/3=3 → would arrive at t=3, but C is ahead
     C arrives at t=7. D's time (3) ≤ C's time (7) → D catches C → merges into Fleet 2
     Fleet 2 = {C, D}, arrives at t=7 (speed of C, the slower one)
  E: pos=0,  speed=1 → arrives at t=(12-0)/1=12 → Fleet 3 (alone)

Fleets arriving:
  t=1:  Fleet 1 = {A, B}
  t=7:  Fleet 2 = {C, D}
  t=12: Fleet 3 = {E}

Total: 3 fleets ✅
```

---

### 🔍 Second Example: `target = 10, position = [0, 2, 4], speed = [4, 2, 1]`

**Sorted descending by position:** pos=4(speed=1), pos=2(speed=2), pos=0(speed=4)

| Step | Car | time | Stack | time > peek? | Action |
|------|-----|------|-------|--------------|--------|
| 1 | (4,1) | (10-4)/1=6.0 | `[]` | — | Push | `[6.0]` |
| 2 | (2,2) | (10-2)/2=4.0 | `[6.0]` | 4.0 > 6.0? **No** | Merge | `[6.0]` |
| 3 | (0,4) | (10-0)/4=2.5 | `[6.0]` | 2.5 > 6.0? **No** | Merge | `[6.0]` |

**Result:** 1 fleet ✅ (all cars merge into one — the fastest cars from behind all catch the slowest car ahead)

---

### 🔍 Third Example: All Different Fleets

**Input:** `target = 10, position = [0, 1, 2, 3, 4], speed = [1, 1, 1, 1, 1]`

**Sorted descending:** pos=4,3,2,1,0 (all speed=1)

| Step | Car | time | Stack | time > peek? | Action |
|------|-----|------|-------|--------------|--------|
| 1 | (4,1) | 6.0 | `[]` | — | Push | `[6.0]` |
| 2 | (3,1) | 7.0 | `[6.0]` | 7.0 > 6.0 ✅ | Push | `[7.0, 6.0]` |
| 3 | (2,1) | 8.0 | `[7.0, 6.0]` | 8.0 > 7.0 ✅ | Push | `[8.0, 7.0, 6.0]` |
| 4 | (1,1) | 9.0 | `[8.0, 7.0, 6.0]` | 9.0 > 8.0 ✅ | Push | `[9.0, 8.0, 7.0, 6.0]` |
| 5 | (0,1) | 10.0 | `[9.0, 8.0, 7.0, 6.0]` | 10.0 > 9.0 ✅ | Push | `[10.0, 9.0, 8.0, 7.0, 6.0]` |

**Result:** 5 fleets ✅ (all same speed, no one catches anyone — each car is its own fleet)

---

### 🔍 Why the Stack is Monotonically Increasing (Bottom to Top)

```
After processing all cars, the stack looks like:

Bottom → [t₁, t₂, t₃, ..., tₖ] ← Top
          1.0  7.0  12.0

Where t₁ < t₂ < t₃ < ... < tₖ

Why? We only push when time > peek. So each new push is STRICTLY GREATER than the previous top.
The stack is monotonically increasing from bottom to top.

Each entry represents a fleet that arrives LATER than the one below it.
The fleet at the bottom (smallest time) is closest to the target and arrives first.
The fleet at the top (largest time) is farthest from the target and arrives last.
```

---

## 2B. Sorting + Single Variable (O(n log n) Time, O(1) Extra Space)

**Idea:**  
We only ever compare with the **top** of the stack (the most recent fleet). We never pop. So the stack can be replaced by a single variable `lastTime` tracking the arrival time of the most recently formed fleet.

**Time:** O(n log n) — sorting.  
**Space:** O(1) extra (beyond the cars array for sorting).

```java
import java.util.*;

public int carFleet(int target, int[] position, int[] speed) {
    int n = position.length;
    if (n == 0) return 0;

    int[][] cars = new int[n][2];
    for (int i = 0; i < n; i++) {
        cars[i][0] = position[i];
        cars[i][1] = speed[i];
    }

    Arrays.sort(cars, (a, b) -> Integer.compare(b[0], a[0])); // descending position

    int fleets = 0;
    double lastTime = -1.0;  // arrival time of the most recent fleet

    for (int[] car : cars) {
        double time = (double)(target - car[0]) / car[1];
        if (time > lastTime) {
            fleets++;        // new fleet
            lastTime = time; // update the "barrier" time
        }
        // else: merges into existing fleet (time <= lastTime)
    }

    return fleets;
}
```

### 🔍 Sample Iteration (Same Example)

**Input:** `target = 12`, sorted cars: (10,2), (8,4), (5,1), (3,3), (0,1)

| Step | Car | time | lastTime | time > lastTime? | Action | fleets |
|------|-----|------|----------|------------------|--------|--------|
| 1 | (10,2) | 1.0 | -1.0 | 1.0 > -1.0 ✅ | New fleet. lastTime=1.0 | **1** |
| 2 | (8,4) | 1.0 | 1.0 | 1.0 > 1.0? **No** | Merge | 1 |
| 3 | (5,1) | 7.0 | 1.0 | 7.0 > 1.0 ✅ | New fleet. lastTime=7.0 | **2** |
| 4 | (3,3) | 3.0 | 7.0 | 3.0 > 7.0? **No** | Merge | 2 |
| 5 | (0,1) | 12.0 | 7.0 | 12.0 > 7.0 ✅ | New fleet. lastTime=12.0 | **3** |

**Result:** `3` ✅

> 📌 Same logic, same answer, but no stack allocation. Just one `double` variable and one counter.

---

### 🔍 Why We Never Need to Pop (Stack → Variable)

```
In the stack approach:
  - We push when time > peek (new fleet).
  - We do NOTHING when time <= peek (merge).
  - We NEVER pop.

Since we never pop, the stack only grows. And we only ever look at the TOP.
∴ The stack is equivalent to a single variable tracking the last pushed value.

The "stack" is monotonically increasing, and we only append to it.
The size of the stack = number of times we pushed = fleet count.
```

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force vs Stack vs Single Variable

| Metric | Brute Force (O(n²)) | Sorting + Stack | Sorting + Variable |
|--------|---------------------|-----------------|--------------------|
| Time | O(n²) | O(n log n) | **O(n log n)** |
| For n=10⁵ | ~10¹⁰ → **TLE** | ~1.7×10⁶ → fast | ~1.7×10⁶ → **fast** |
| Space | O(n) | O(n) | **O(1)** extra |
| Code complexity | Moderate (merge logic) | Clean | **Simplest** |
| Demonstrates monotonic stack? | ❌ | **✅** | Implicitly |
| Interview value | Baseline | Shows stack thinking | Shows optimization |

---

## Stack vs Single Variable (Head-to-Head)

| Metric | Explicit Stack | Single Variable |
|--------|---------------|-----------------|
| Time | O(n log n) | O(n log n) |
| Space | O(n) — Deque allocation | **O(1)** — one double |
| Code clarity | Shows the "stack" pattern explicitly | Slightly more abstract |
| When to present | First (illustrates the concept) | Second (optimization) |
| Correctness argument | Stack holds all fleet times | Only the last fleet time matters |
| GC pressure | Creates Double objects | **Zero** |

**Verdict:** Both are correct and O(n log n). The stack version is pedagogically clearer (shows the monotonic stack pattern). The variable version is the production-optimal solution. Present both in an interview.

---

## Why Sorting is Unavoidable

| Approach | Can we avoid sorting? |
|----------|----------------------|
| Without sorting | We'd need to know which cars are ahead of which → requires ordering by position |
| With a TreeMap/BST | O(n log n) anyway (insertion into sorted structure) |
| Counting sort (positions < target ≤ 10⁶) | O(n + target) — possible but target can be 10⁶ |
| **Comparison sort** | **O(n log n) — standard, clean, expected** |

> 📌 Sorting by position is the fundamental enabler. Without it, we can't process cars in the "closest to target first" order that makes the single-pass greedy work.

---

## 🏁 Final Master Comparison Table

| Approach | Time | Space | Correct? | Practical (n=10⁵)? | Key Insight |
|----------|------|-------|----------|--------------------|----|
| Pairwise Merge (Brute) | O(n²) | O(n) | ✅ | ❌ TLE | Check all pairs for catching |
| **Sort + Monotonic Stack** | **O(n log n)** | **O(n)** | **✅** | **✅** | **Push only if time > peek (new fleet)** |
| **Sort + Single Variable** | **O(n log n)** | **O(1)** | **✅** | **✅** | **Only last fleet time matters** |

---

### 🎯 What to Present to the Interviewer

1. **Define arrival time:** `time = (target - position) / speed`. This is the car's unhindered time to reach the destination.
2. **Explain the merging rule:** "A car merges with the fleet ahead if its arrival time ≤ the fleet's arrival time. It catches up before (or at) the target."
3. **Propose sorting by position descending:** "Process cars from closest-to-target to farthest. This ensures the fleet ahead is already determined when we process each car."
4. **Introduce the monotonic stack:**
   - "Push a car's time if it's greater than the stack top (new fleet — too slow to catch)."
   - "Skip if time ≤ stack top (merges into existing fleet)."
   - "The stack size at the end = number of fleets."
5. **Walk through** the example:
   - pos=10, time=1.0 → push. Stack: [1.0].
   - pos=8, time=1.0 → 1.0 ≤ 1.0, merge. Stack: [1.0].
   - pos=5, time=7.0 → 7.0 > 1.0, push. Stack: [7.0, 1.0].
   - pos=3, time=3.0 → 3.0 ≤ 7.0, merge. Stack: [7.0, 1.0].
   - pos=0, time=12.0 → 12.0 > 7.0, push. Stack: [12.0, 7.0, 1.0].
   - Answer: 3.
6. **Optimize to O(1) space:** "Since we never pop and only check the top, replace the stack with a single `lastTime` variable and a counter."
7. **State complexity:** O(n log n) time (sorting), O(1) extra space (variable version) or O(n) (stack version).
8. **If asked about the monotonic property:** "The stack is monotonically increasing (bottom to top). Each new fleet arrives strictly later than the previous one."

**One‑sentence summary:**  
*Sort cars by position descending, compute each car's arrival time, and count a new fleet only when a car's time exceeds the fleet ahead's time (tracked via a monotonic stack or single variable) — achieving O(n log n) time with the key insight that a slower car from behind can never catch a faster fleet ahead.*