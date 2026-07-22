### 📘 Chapter: Stack  
### 📌 Problem 8: Asteroid Collision (LeetCode 735)

---

**Input**  
- `asteroids`: an integer array representing asteroids in a row.  
  - Absolute value = size of the asteroid.  
  - Sign = direction: **positive** means moving right →, **negative** means moving left ←.  
  - All asteroids move at the same speed.

**Output**  
- The state of the asteroids after all collisions, as an array.  
  - When two asteroids collide, the **smaller** one explodes.  
  - If they are the **same size**, both explode.  
  - Asteroids moving in the **same direction** never meet.

**Constraints**  
- `2 <= asteroids.length <= 10⁴`  
- `-1000 <= asteroids[i] <= 1000`, `asteroids[i] != 0`

**Follow‑up**  
- Not explicitly given; the standard is to achieve **O(n) time** and **O(n) space** using a stack.

---

### 🧠 Why this Data Structure (Stack)?

Collisions can only happen between a **right‑moving** asteroid (positive) and a **left‑moving** asteroid (negative) that is **to the right** of it.  
- As we process asteroids from left to right:  
  - The stack maintains the stable asteroids that have survived so far.  
  - When we encounter a left‑moving asteroid (`< 0`), it may collide with the top of the stack (which is the nearest right‑moving asteroid on its left).  
  - While the stack top is positive and its size < current asteroid’s size, the right‑moving asteroid explodes (pop).  
  - If the stack top is positive and equal, both explode (pop and discard current).  
  - If the stack top is positive and larger, the current left‑moving asteroid explodes (do nothing).  
  - If the stack top is negative (or stack empty), the current asteroid simply pushes onto the stack (no collision, as both move left or it’s the first asteroid).  
- Right‑moving asteroids are always pushed onto the stack because they have no immediate collision; they might collide later with a future left‑moving asteroid.

This yields **O(n)** time (each asteroid pushed/popped at most once) and **O(n)** space for the stack, which is optimal.

---

### 🔨 Brute Force Approach (Repeated Pairwise Checks)

**Method:**  
Use a `List<Integer>` to simulate asteroids. Repeatedly scan from left to right, checking adjacent pairs where left moves right (`>0`) and right moves left (`<0`). Apply collision rules and update the list (remove destroyed asteroids). Repeat until no more collisions occur.

**Time:** O(n²) – each pass removes at least one asteroid, so up to n passes, each O(n).  
**Space:** O(n) – for the list.

```java
public int[] asteroidCollision(int[] asteroids) {
    List<Integer> list = new ArrayList<>();
    for (int a : asteroids) list.add(a);
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int i = 0; i < list.size() - 1; ) {
            int left = list.get(i), right = list.get(i + 1);
            if (left > 0 && right < 0) { // collision possible
                changed = true;
                if (Math.abs(left) > Math.abs(right)) {
                    list.remove(i + 1); // right explodes
                } else if (Math.abs(left) < Math.abs(right)) {
                    list.remove(i); // left explodes
                } else {
                    list.remove(i); // both explode, remove i first then i+1 becomes i
                    list.remove(i);
                }
                // do not increment i, recheck current position
            } else {
                i++;
            }
        }
    }
    return list.stream().mapToInt(i -> i).toArray();
}
```
Too slow for large inputs.

---

### ⚡ Optimized Approach – Stack (O(n) time, O(n) space)

**Method:**  
- Use a `Deque<Integer>` as a stack.  
- For each `asteroid` in the array:  
  - If `asteroid > 0` (moving right), simply push onto stack.  
  - Else (moving left):  
    - While stack is not empty and top of stack is positive (moving right) and its size < `abs(asteroid)`:
      - Pop the top (the right‑moving asteroid is destroyed).  
    - After the loop:  
      - If the stack is empty or top is negative (moving left), push `asteroid` (no collision or both moving left).  
      - If top is positive and its size == `abs(asteroid)`, pop the top (both explode) and do **not** push the current asteroid.  
      - If top is positive and its size > `abs(asteroid)`, do nothing (current asteroid explodes).  
- Convert the stack to an array in correct order (from bottom to top) and return.

**Time:** O(n) – each asteroid pushed/popped at most once.  
**Space:** O(n) – stack stores up to n elements.

```java
import java.util.*;

public int[] asteroidCollision(int[] asteroids) {
    Deque<Integer> stack = new ArrayDeque<>();
    for (int ast : asteroids) {
        if (ast > 0) {
            stack.push(ast);
        } else {
            // left-moving asteroid
            while (!stack.isEmpty() && stack.peek() > 0 && stack.peek() < -ast) {
                stack.pop(); // right-moving smaller asteroid destroyed
            }
            if (stack.isEmpty() || stack.peek() < 0) {
                stack.push(ast); // no collision or both moving left
            } else if (stack.peek() == -ast) {
                stack.pop(); // both explode
            }
            // else: stack.peek() > -ast, current asteroid explodes (do nothing)
        }
    }
    // Build result from bottom to top
    int[] result = new int[stack.size()];
    for (int i = result.length - 1; i >= 0; i--) {
        result[i] = stack.pop();
    }
    return result;
}
```

---

### 📊 Solution Comparison & Trade‑offs

| Solution              | Time  | Space | Notes |
|-----------------------|-------|-------|-------|
| Brute force (list scan)| O(n²) | O(n)  | Repeated passes; not efficient. |
| Stack (single pass)   | O(n)  | O(n)  | **Optimal**; processes each asteroid once. |

**Trade‑off:**  
- The brute force is easy to understand but far too slow for the given constraints.  
- The stack approach is the standard linear solution. No significant trade‑off; it’s the expected answer.

---

### 🎯 What to Present to the Interviewer

1. Clarify the collision rules: only right‑moving followed by left‑moving can collide.  
2. Explain why a **stack** is perfect: it simulates the order of asteroids; when a left‑moving asteroid appears, it interacts with the most recent right‑moving asteroids on its left (LIFO).  
3. Walk through the algorithm with an example (e.g., `[5,10,-5]`).  
4. Write the stack‑based Java code carefully, handling the three post‑loop conditions.  
5. State O(n) time, O(n) space.  
6. Optionally discuss that an in‑place array modification is possible but more complex; the stack version is clean and optimal.

**One‑sentence summary:**  
*Use a stack to simulate collisions: push right‑moving asteroids; when a left‑moving asteroid arrives, pop smaller right‑moving ones, explode on equal, or survive if the stack has no positive top, all in O(n) time.*