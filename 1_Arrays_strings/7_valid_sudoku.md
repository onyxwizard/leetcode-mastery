### 📘 Chapter: Arrays & Strings  
### 📌 Problem 7: Valid Sudoku (LeetCode 36)

---

**Input**  
- `board`: a `char[][]` of size `9 x 9`, containing characters `'1'`–`'9'` or `'.'` (empty cell).

**Output**  
- `true` if the board is valid according to Sudoku rules (rows, columns, and `3x3` sub‑boxes contain each digit only once); `false` otherwise.

**Constraints**  
- `board.length == 9` and `board[i].length == 9`  
- Each cell is a digit `'1'`–`'9'` or `'.'`

**Follow-up**  
- Not provided (problem is self‑contained).

---

### 🧠 Why this Data Structure?

The task is to detect duplicate digits **per row, per column, and per `3x3` sub‑box**.  
- We need a quick way to check, for each digit, “have I seen this digit before in this row / column / box?”  
- A **HashSet** (or an array of booleans) per row, column, and box gives **O(1)** insertion and lookup.  
- Because the Sudoku grid is fixed `9x9`, **boolean arrays** (`boolean[9]`) are even faster than a general `HashSet` (no hashing overhead) and use truly constant space.

To map a cell `(row, col)` to its sub‑box index: `boxIndex = (row / 3) * 3 + (col / 3)`.  
This formula divides the board into nine `3x3` zones, numbered 0 to 8.

---

### 🔨 Brute Force Approach (Three Separate Passes)

**Method:**  
1. Check all rows: for each row, use a `boolean[9]` to track seen digits; return `false` on duplicate.  
2. Check all columns similarly.  
3. Check all `3x3` boxes: nested loops for each of the 9 boxes.

**Time:** O(3 × 81) = O(1) (constant, because board size is fixed)  
**Space:** O(9) per pass (reused array), overall O(1)

This is simple but scans the board three times.

```java
public boolean isValidSudoku(char[][] board) {
    // Check rows
    for (int i = 0; i < 9; i++) {
        boolean[] seen = new boolean[9];
        for (int j = 0; j < 9; j++) {
            if (board[i][j] != '.') {
                int num = board[i][j] - '1';
                if (seen[num]) return false;
                seen[num] = true;
            }
        }
    }
    // Check columns
    for (int j = 0; j < 9; j++) {
        boolean[] seen = new boolean[9];
        for (int i = 0; i < 9; i++) {
            if (board[i][j] != '.') {
                int num = board[i][j] - '1';
                if (seen[num]) return false;
                seen[num] = true;
            }
        }
    }
    // Check boxes
    for (int box = 0; box < 9; box++) {
        boolean[] seen = new boolean[9];
        int startRow = (box / 3) * 3;
        int startCol = (box % 3) * 3;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                char c = board[startRow + i][startCol + j];
                if (c != '.') {
                    int num = c - '1';
                    if (seen[num]) return false;
                    seen[num] = true;
                }
            }
        }
    }
    return true;
}
```

---

### ⚡ Optimized Approach 1 – One‑Pass with 2D boolean Arrays

**Method:**  
Use a single pass over the 81 cells. Maintain three 2D boolean arrays:  
- `rowSeen[9][9]` – `rowSeen[i][digit]` true if digit seen in row `i`  
- `colSeen[9][9]` – same for columns  
- `boxSeen[9][9]` – same for boxes, using the box‑index formula  

If any cell’s digit is already marked, invalid.

**Time:** O(81) = O(1) – single pass  
**Space:** O(3×9×9) = O(1) (fixed small arrays)

```java
public boolean isValidSudoku(char[][] board) {
    boolean[][] rowSeen = new boolean[9][9];
    boolean[][] colSeen = new boolean[9][9];
    boolean[][] boxSeen = new boolean[9][9];

    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            if (board[i][j] == '.') continue;
            int digit = board[i][j] - '1';
            int boxIdx = (i / 3) * 3 + (j / 3);

            if (rowSeen[i][digit] || colSeen[j][digit] || boxSeen[boxIdx][digit]) {
                return false;
            }
            rowSeen[i][digit] = true;
            colSeen[j][digit] = true;
            boxSeen[boxIdx][digit] = true;
        }
    }
    return true;
}
```

---

### ⚡ Optimized Approach 2 – Single HashSet with Encoded Strings

**Method:**  
Use one `HashSet<String>`. For each cell with a digit, create three strings that encode the constraint:  
- `"row" + i + digit`  
- `"col" + j + digit`  
- `"box" + boxIndex + digit`  

Try to add each to the set. If any `add()` returns `false`, a duplicate exists → invalid.

**Time:** O(81) = O(1)  
**Space:** O(81×3) = O(1) (constant, but creates many small strings)

This solution is extremely concise and self‑documenting.

```java
public boolean isValidSudoku(char[][] board) {
    Set<String> seen = new HashSet<>();
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            char c = board[i][j];
            if (c == '.') continue;
            int boxIdx = (i / 3) * 3 + (j / 3);
            String rowKey = "r" + i + c;
            String colKey = "c" + j + c;
            String boxKey = "b" + boxIdx + c;
            if (!seen.add(rowKey) || !seen.add(colKey) || !seen.add(boxKey)) {
                return false;
            }
        }
    }
    return true;
}
```

---

### 📊 Solution Comparison & Trade-offs

| Solution                      | Time | Space | Notes |
|-------------------------------|------|-------|-------|
| Brute force (three passes)    | O(1) | O(1)  | Clear logic, but redundant scanning. |
| One-pass with boolean arrays  | O(1) | O(1)  | **Fastest in practice** – direct array indexing, no hashing or string ops. |
| Single HashSet with strings   | O(1) | O(1)  | **Most concise** – easy to read, but creates many temporary strings; overhead is negligible for 9×9. |

**Trade‑off:**  
- Boolean arrays avoid object creation and use constant memory with zero GC pressure; the code is slightly longer but still readable.  
- The HashSet+strings version is elegant and minimal – the interviewer will appreciate its clarity. Both are acceptable; I typically present the string‑encoding method first because of its simplicity, then mention the array version as an optimisation.

---

### 🎯 What to Present to the Interviewer

1. Immediately note that the board is a **fixed size (9×9)**, so O(1) time and space are trivial – focus on clean, bug‑free code.  
2. Propose the **single‑pass boolean arrays** approach: one array for rows, one for columns, one for boxes (indexed by `(row/3)*3 + col/3`).  
3. Walk through the code step by step, showing how `digit - '1'` converts char to a 0‑based index.  
4. As an elegant alternative, show the **HashSet with encoded strings** solution – it reduces the code size dramatically and is self‑explanatory.  
5. Conclude that both are constant‑time and space; the string version is shorter, while the array version avoids creating extra objects.

**One‑sentence summary:**  
*Track seen digits per row, column, and 3×3 box using either boolean arrays (fast) or a HashSet of encoded strings (concise) – return false if a duplicate is found.*