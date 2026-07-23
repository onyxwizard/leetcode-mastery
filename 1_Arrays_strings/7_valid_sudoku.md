### 📘 Chapter: Arrays & Strings  
### 📌 Problem 7: Valid Sudoku (LeetCode 36)

---

**Input**  
- `board`: a `char[][]` of size `9 × 9`, containing characters `'1'`–`'9'` or `'.'` (empty cell).

**Output**  
- `true` if the board is valid according to Sudoku rules (no duplicate digits in any row, column, or `3×3` sub‑box); `false` otherwise.

**Constraints**  
- `board.length == 9` and `board[i].length == 9`  
- Each cell is a digit `'1'`–`'9'` or `'.'`

**Example**  
```
Input:
board =
[["5","3",".",".","7",".",".",".","."],
 ["6",".",".","1","9","5",".",".","."],
 [".","9","8",".",".",".",".","6","."],
 ["8",".",".",".","6",".",".",".","3"],
 ["4",".",".","8",".","3",".",".","1"],
 ["7",".",".",".","2",".",".",".","6"],
 [".","6",".",".",".",".","2","8","."],
 [".",".",".","4","1","9",".",".","5"],
 [".",".",".",".","8",".",".","7","9"]]

Output: true

Input:
board =
[["8","3",".",".","7",".",".",".","."],
 ["6",".",".","1","9","5",".",".","."],
 [".","9","8",".",".",".",".","6","."],
 ["8",".",".",".","6",".",".",".","3"],   ← '8' conflicts with row 0's '8' in box 0
 ["4",".",".","8",".","3",".",".","1"],
 ["7",".",".",".","2",".",".",".","6"],
 [".","6",".",".",".",".","2","8","."],
 [".",".",".","4","1","9",".",".","5"],
 [".",".",".",".","8",".",".","7","9"]]

Output: false  (digit '8' appears twice in box 0)
```

**Follow-up**  
- Not provided (problem is self‑contained). Common extensions: What if the board is `N×N` with `√N × √N` boxes? What about validating an **entirely filled** board (Sudoku solver check)?

---

### 🧠 Core Idea

The task is to detect **duplicate digits** per row, per column, and per `3×3` sub‑box.

- **Brute force:** Three separate passes — one for rows, one for columns, one for boxes. Simple but scans the board 3 times.
- **One-pass boolean arrays:** Maintain `rowSeen[9][9]`, `colSeen[9][9]`, `boxSeen[9][9]`. Single scan of 81 cells. Fastest in practice.
- **One-pass HashSet with encoded strings:** Encode each constraint as a string key (`"r0_5"`, `"c3_7"`, `"b2_1"`). Most concise code.

**Box-index formula:** For cell `(row, col)`, its 3×3 box index = `(row / 3) * 3 + (col / 3)`.

```
Box layout:
┌───┬───┬───┐
│ 0 │ 1 │ 2 │   rows 0-2
├───┼───┼───┤
│ 3 │ 4 │ 5 │   rows 3-5
├───┼───┼───┤
│ 6 │ 7 │ 8 │   rows 6-8
└───┴───┴───┘
 cols 0-2  3-5  6-8
```

> 📌 Since the board is **fixed 9×9**, all approaches are technically O(1) time and space. The focus is on **clean, bug-free code** and demonstrating the right data structure intuition.

---

---

# 🔨 SECTION 1: BRUTE FORCE APPROACH

---

## 1A. Three Separate Passes (Rows → Columns → Boxes)

**Idea:**  
1. **Pass 1 – Rows:** For each row, use a `boolean[9]` to track seen digits. Duplicate → return `false`.  
2. **Pass 2 – Columns:** Same logic, iterating column-wise.  
3. **Pass 3 – Boxes:** For each of the 9 boxes, iterate its 3×3 cells with a fresh `boolean[9]`.

**Time:** O(3 × 81) = O(1) — three full scans of the fixed board.  
**Space:** O(9) per pass (one `boolean[9]` reused) = O(1).

```java
public boolean isValidSudoku(char[][] board) {
    // ─── Pass 1: Check all rows ───
    for (int i = 0; i < 9; i++) {
        boolean[] seen = new boolean[9];
        for (int j = 0; j < 9; j++) {
            if (board[i][j] != '.') {
                int num = board[i][j] - '1';  // '1'→0, '9'→8
                if (seen[num]) return false;
                seen[num] = true;
            }
        }
    }

    // ─── Pass 2: Check all columns ───
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

    // ─── Pass 3: Check all 3×3 boxes ───
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

### 🔍 Sample Iteration (Invalid Board — duplicate '8' in Box 0)

**Input (top-left 3×3 region highlighted):**
```
Row 0: [8, 3, . | . 7 . | . . .]
Row 1: [6, ., . | 1 9 5 | . . .]
Row 2: [. 9 8 | . . . | . 6 .]
Row 3: [8, ., . | . 6 . | . . 3]   ← '8' at (3,0) is in Box 3, not Box 0
       ─────────────────────────
Actually, let's use a clearer invalid case:
Row 0: [8, 3, . | ...]
Row 1: [6, ., . | ...]
Row 2: [. 9 8 | ...]   ← '8' at (2,2) is in Box 0
Row 3: [8, ., . | ...]   ← '8' at (3,0) is in Box 3 (different box, OK for box check)
```

Let's use a **clearer** invalid board where the conflict is in the **same row**:
```
Row 0: [5, 3, ., ., 7, ., ., ., .]
Row 1: [6, ., ., 1, 9, 5, ., ., .]
Row 2: [. 9, 8, ., ., ., ., 6, .]
Row 3: [8, ., ., ., 6, ., ., ., 3]
Row 4: [4, ., ., 8, ., 3, ., ., 1]
Row 5: [7, ., ., ., 2, ., ., ., 6]
Row 6: [. 6, ., ., ., ., 2, 8, .]
Row 7: [. ., ., 4, 1, 9, ., ., 5]
Row 8: [. ., ., ., 8, ., ., 7, 9]
```
Change `board[0][0]` from `'5'` to `'8'` → now row 0 has no conflict, but **Box 0** has `'8'` at (0,0) AND (2,2).

**Pass 1 – Rows (no conflict found):**

| Row | Digits seen | Duplicate? |
|-----|-------------|------------|
| 0 | 8, 3, 7 | No |
| 1 | 6, 1, 9, 5 | No |
| 2 | 9, 8, 6 | No |
| ... | ... | No |

→ Pass 1 returns no conflict.

**Pass 2 – Columns (no conflict found):**

| Col | Digits seen | Duplicate? |
|-----|-------------|------------|
| 0 | 8, 6, 8, 4, 7 | ← Wait! '8' at row 0 AND row 3! |

Actually let me pick a cleaner example. Let me use the **classic LeetCode invalid example**:

```
board[0][0] = '8' (changed from '5')
```

Now Box 0 contains: `(0,0)='8'`, `(1,0)='6'`, `(2,1)='9'`, `(2,2)='8'` → **duplicate '8'**.

**Pass 1 – Rows:**

| Row i | Cells scanned | seen[] state | Result |
|-------|---------------|--------------|--------|
| 0 | 8,3,.,.,7,.,.,.,. | {8,3,7} | ✅ No dup |
| 1 | 6,.,.,1,9,5,.,.,. | {6,1,9,5} | ✅ No dup |
| 2 | .,9,8,.,.,.,.,6,. | {9,8,6} | ✅ No dup |
| 3–8 | ... | ... | ✅ No dup |

→ Pass 1: **No conflict.**

**Pass 2 – Columns:**

| Col j | Cells scanned | seen[] state | Result |
|-------|---------------|--------------|--------|
| 0 | 8,6,.,8,4,7,.,.,. | {8,6,8,...} ← Wait! | ❌? |

Hmm, `(0,0)='8'` and `(3,0)='8'` — that's a **column** conflict too! Let me adjust the example to isolate the box conflict only.

**Cleaner invalid example (box conflict only):**
```
board[0][0] = '5' (original)
board[2][2] = '5' (changed from '8')  → Box 0 now has '5' at (0,0) and (2,2)
```

Row 0: `5,3,.,.,7,.,.,.,.` → has '5'  
Row 2: `.,9,5,.,.,.,.,6,.` → has '5'  
Col 0: `5,6,.,8,4,7,.,.,.` → only one '5'  
Col 2: `.,.,5,.,.,.,.,.,.` → only one '5'  
Box 0: `5,3,.,6,.,.,.,9,5` → **TWO '5's!** ← conflict here only.

**Pass 1 – Rows:** No row has duplicate '5'. ✅  
**Pass 2 – Columns:** No column has duplicate '5'. ✅  
**Pass 3 – Boxes:**

| Box | startRow, startCol | Cells scanned | seen[] state | Result |
|-----|--------------------|---------------|--------------|--------|
| 0 | (0, 0) | (0,0)=5→seen[4]=T, (0,1)=3→seen[2]=T, (0,2)='.'→skip, (1,0)=6→seen[5]=T, (1,1)='.'→skip, (1,2)='.'→skip, (2,0)='.'→skip, (2,1)=9→seen[8]=T, **(2,2)=5→seen[4] already TRUE!** | {5,3,6,9} | ❌ **RETURN FALSE** |

> ⚠️ The conflict is caught only in **Pass 3** (box check). Passes 1 and 2 did 162 cell visits for nothing. This redundancy is why the one-pass approach is preferred.

---

---

# ⚡ SECTION 2: OPTIMIZED APPROACHES

---

## 2A. One-Pass with 2D Boolean Arrays

**Idea:**  
Single scan of all 81 cells. Maintain three 2D boolean arrays:
- `rowSeen[9][9]` — `rowSeen[i][d]` = true if digit `d+1` already seen in row `i`.
- `colSeen[9][9]` — `colSeen[j][d]` = true if digit `d+1` already seen in column `j`.
- `boxSeen[9][9]` — `boxSeen[b][d]` = true if digit `d+1` already seen in box `b`.

For each non-empty cell `(i, j)`:
1. Compute `digit = board[i][j] - '1'` (maps '1'→0, ..., '9'→8).
2. Compute `boxIdx = (i / 3) * 3 + (j / 3)`.
3. If **any** of `rowSeen[i][digit]`, `colSeen[j][digit]`, `boxSeen[boxIdx][digit]` is already true → **return false**.
4. Otherwise, mark all three as true.

**Time:** O(81) = O(1) — single pass, constant work per cell.  
**Space:** O(3 × 9 × 9) = O(243 booleans) = O(1) — fixed regardless of input.

```java
public boolean isValidSudoku(char[][] board) {
    boolean[][] rowSeen = new boolean[9][9];
    boolean[][] colSeen = new boolean[9][9];
    boolean[][] boxSeen = new boolean[9][9];

    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            if (board[i][j] == '.') continue;

            int digit = board[i][j] - '1';          // '1'→0, '9'→8
            int boxIdx = (i / 3) * 3 + (j / 3);    // 0..8

            if (rowSeen[i][digit] || colSeen[j][digit] || boxSeen[boxIdx][digit]) {
                return false;  // duplicate found!
            }

            rowSeen[i][digit] = true;
            colSeen[j][digit] = true;
            boxSeen[boxIdx][digit] = true;
        }
    }

    return true;
}
```

### 🔍 Sample Iteration (Invalid Board — '5' duplicated in Box 0)

**Board (relevant cells):**
```
(0,0)='5'  (0,1)='3'  (0,2)='.'
(1,0)='6'  (1,1)='.'  (1,2)='.'
(2,0)='.'  (2,1)='9'  (2,2)='5'  ← CONFLICT with (0,0) in Box 0
```

| Step | Cell (i,j) | char | digit | boxIdx | rowSeen check | colSeen check | boxSeen check | Action |
|------|-----------|------|-------|--------|---------------|---------------|---------------|--------|
| 1 | (0,0) | '5' | 4 | (0/3)*3+(0/3)=**0** | rowSeen[0][4]=F ✅ | colSeen[0][4]=F ✅ | boxSeen[0][4]=F ✅ | Mark all true |
| 2 | (0,1) | '3' | 2 | (0/3)*3+(1/3)=**0** | rowSeen[0][2]=F ✅ | colSeen[1][2]=F ✅ | boxSeen[0][2]=F ✅ | Mark all true |
| 3 | (0,2) | '.' | — | — | — | — | — | **Skip** |
| 4 | (0,3) | '.' | — | — | — | — | — | **Skip** |
| 5 | (0,4) | '7' | 6 | (0/3)*3+(4/3)=**1** | rowSeen[0][6]=F ✅ | colSeen[4][6]=F ✅ | boxSeen[1][6]=F ✅ | Mark all true |
| ... | (0,5)–(0,8) | '.' | — | — | — | — | — | Skip |
| 6 | (1,0) | '6' | 5 | (1/3)*3+(0/3)=**0** | rowSeen[1][5]=F ✅ | colSeen[0][5]=F ✅ | boxSeen[0][5]=F ✅ | Mark all true |
| ... | (1,1)–(1,2) | '.' | — | — | — | — | — | Skip |
| 7 | (1,3) | '1' | 0 | (1/3)*3+(3/3)=**1** | rowSeen[1][0]=F ✅ | colSeen[3][0]=F ✅ | boxSeen[1][0]=F ✅ | Mark all true |
| 8 | (1,4) | '9' | 8 | **1** | rowSeen[1][8]=F ✅ | colSeen[4][8]=F ✅ | boxSeen[1][8]=F ✅ | Mark all true |
| 9 | (1,5) | '5' | 4 | **1** | rowSeen[1][4]=F ✅ | colSeen[5][4]=F ✅ | boxSeen[1][4]=F ✅ | Mark all true |
| ... | (2,0) | '.' | — | — | — | — | — | Skip |
| 10 | (2,1) | '9' | 8 | (2/3)*3+(1/3)=**0** | rowSeen[2][8]=F ✅ | colSeen[1][8]=F ✅ | boxSeen[0][8]=F ✅ | Mark all true |
| **11** | **(2,2)** | **'5'** | **4** | **(2/3)*3+(2/3)=0** | rowSeen[2][4]=F ✅ | colSeen[2][4]=F ✅ | **boxSeen[0][4]=TRUE ❌** | **RETURN FALSE** |

> 📌 At step 11, `boxSeen[0][4]` was already set to `true` at step 1 (when we processed `(0,0)='5'`). The duplicate is caught **immediately** — no need for separate passes.

**State of `boxSeen[0]` at the moment of failure:**
```
boxSeen[0] = [F, F, T, F, T, T, F, F, T]
                       ↑digit=2  ↑digit=4  ↑digit=5     ↑digit=8
                       ('3')    ('5')     ('6')        ('9')
                                ↑ CONFLICT: '5' seen again!
```

---

## 2B. Single HashSet with Encoded Strings

**Idea:**  
Use **one** `HashSet<String>`. For each non-empty cell `(i, j)` with digit `c`, generate three unique keys:
- `"r" + i + "_" + c` — encodes "digit c in row i"
- `"c" + j + "_" + c` — encodes "digit c in column j"
- `"b" + boxIdx + "_" + c` — encodes "digit c in box boxIdx"

Attempt to `add()` each key. If `add()` returns `false`, the key already exists → **duplicate detected** → return `false`.

**Time:** O(81) = O(1) — single pass, up to 3 hash operations per cell.  
**Space:** O(81 × 3) = O(243 strings) = O(1) — fixed maximum.

```java
import java.util.HashSet;
import java.util.Set;

public boolean isValidSudoku(char[][] board) {
    Set<String> seen = new HashSet<>();

    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            char c = board[i][j];
            if (c == '.') continue;

            int boxIdx = (i / 3) * 3 + (j / 3);

            String rowKey = "r" + i + "_" + c;
            String colKey = "c" + j + "_" + c;
            String boxKey = "b" + boxIdx + "_" + c;

            if (!seen.add(rowKey) || !seen.add(colKey) || !seen.add(boxKey)) {
                return false;  // duplicate found!
            }
        }
    }

    return true;
}
```

### 🔍 Sample Iteration (Same Invalid Board — '5' duplicated in Box 0)

| Step | Cell | char | Keys generated | HashSet state (relevant entries) | Result |
|------|------|------|----------------|----------------------------------|--------|
| 1 | (0,0) | '5' | `"r0_5"`, `"c0_5"`, `"b0_5"` | All new → added ✅ | Continue |
| 2 | (0,1) | '3' | `"r0_3"`, `"c1_3"`, `"b0_3"` | All new → added ✅ | Continue |
| 3 | (0,4) | '7' | `"r0_7"`, `"c4_7"`, `"b1_7"` | All new → added ✅ | Continue |
| 4 | (1,0) | '6' | `"r1_6"`, `"c0_6"`, `"b0_6"` | All new → added ✅ | Continue |
| 5 | (1,3) | '1' | `"r1_1"`, `"c3_1"`, `"b1_1"` | All new → added ✅ | Continue |
| 6 | (1,4) | '9' | `"r1_9"`, `"c4_9"`, `"b1_9"` | All new → added ✅ | Continue |
| 7 | (1,5) | '5' | `"r1_5"`, `"c5_5"`, `"b1_5"` | All new → added ✅ | Continue |
| 8 | (2,1) | '9' | `"r2_9"`, `"c1_9"`, `"b0_9"` | All new → added ✅ | Continue |
| **9** | **(2,2)** | **'5'** | `"r2_5"`, `"c2_5"`, **`"b0_5"`** | `"r2_5"` new ✅, `"c2_5"` new ✅, **`"b0_5"` ALREADY EXISTS** ❌ | **RETURN FALSE** |

**HashSet contents at failure (Box 0 entries only):**
```
{ "b0_5",   ← added at step 1 (cell 0,0)
  "b0_3",   ← added at step 2 (cell 0,1)
  "b0_6",   ← added at step 4 (cell 1,0)
  "b0_9",   ← added at step 8 (cell 2,1)
  "b0_5"   ← DUPLICATE at step 9 (cell 2,2) → add() returns false!
}
```

> 📌 The key `"b0_5"` was inserted at step 1 for cell `(0,0)='5'`. When cell `(2,2)='5'` tries to insert the same key at step 9, `HashSet.add()` returns `false` → immediate detection.

---

### 🔍 Valid Board — Full Trace (First Row + Key Cells)

**Input (valid board):**
```
Row 0: [5, 3, ., ., 7, ., ., ., .]
Row 1: [6, ., ., 1, 9, 5, ., ., .]
Row 2: [., 9, 8, ., ., ., ., 6, .]
...
```

| Step | Cell | char | digit | boxIdx | rowSeen | colSeen | boxSeen | OK? |
|------|------|------|-------|--------|---------|---------|---------|-----|
| 1 | (0,0) | '5' | 4 | 0 | [0][4]=F | [0][4]=F | [0][4]=F | ✅ Mark |
| 2 | (0,1) | '3' | 2 | 0 | [0][2]=F | [1][2]=F | [0][2]=F | ✅ Mark |
| 3 | (0,2) | '.' | — | — | — | — | — | Skip |
| 4 | (0,3) | '.' | — | — | — | — | — | Skip |
| 5 | (0,4) | '7' | 6 | 1 | [0][6]=F | [4][6]=F | [1][6]=F | ✅ Mark |
| 6–9 | (0,5)–(0,8) | '.' | — | — | — | — | — | Skip |
| 10 | (1,0) | '6' | 5 | 0 | [1][5]=F | [0][5]=F | [0][5]=F | ✅ Mark |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 81 | (8,8) | '9' | 8 | 8 | [8][8]=F | [8][8]=F | [8][8]=F | ✅ Mark |
| END | — | — | — | — | — | — | — | **RETURN TRUE** |

> 📌 All 81 cells processed. No duplicate detected. Every `rowSeen`, `colSeen`, `boxSeen` check returned `false` (not previously seen). Board is valid.

---

---

# 📊 SECTION 3: TRADE-OFFS & COMPARISONS

---

## Brute Force (Three Passes) vs One-Pass Approaches

| Metric | Three Separate Passes | One-Pass (Boolean Arrays or HashSet) |
|--------|----------------------|--------------------------------------|
| Board scans | 3 full passes (243 cell visits) | 1 pass (81 cell visits) |
| Early termination | Only within each pass | **Immediate** — catches conflict at the exact cell |
| Code length | Longer (3 loops) | Shorter (1 loop) |
| Redundant work | Passes 1 & 2 may pass, only Pass 3 catches box conflict | No redundancy |
| Interview clarity | Very explicit, easy to explain | Slightly more abstract (box formula) |

**Verdict:** One-pass is strictly better — fewer cell visits, earlier termination, cleaner code.

---

## Boolean Arrays vs HashSet with Strings

| Metric | 2D Boolean Arrays | HashSet + Encoded Strings |
|--------|-------------------|--------------------------|
| Time per cell | 3 array lookups (O(1), no hashing) | 3 `String` creations + 3 hash operations |
| Space | 3 × 81 booleans = 243 bytes | Up to 243 String objects (~several KB) |
| GC pressure | **Zero** (primitive arrays) | Creates up to 243 temporary String objects |
| Code conciseness | Moderate (12 lines) | **Very concise** (8 lines) |
| Readability | Requires understanding `digit - '1'` and box formula | Self-documenting keys (`"r0_5"`) |
| Scalability to N×N | Easy (change array size) | Easy (keys auto-adapt) |
| Interview impression | Shows performance awareness | Shows elegance and clarity |

**Verdict:**  
- **Boolean arrays** win on raw performance (no object creation, no hashing overhead).  
- **HashSet + strings** wins on code brevity and self-documentation.  
- For a fixed 9×9 board, the difference is negligible. Both are O(1).

---

## 🏁 Final Master Comparison Table

| Approach | Time | Extra Space | Passes | Early Termination? | Code Style |
|----------|------|-------------|--------|--------------------|------------|
| Brute Force (3 passes) | O(243) = O(1) | O(9) = O(1) | 3 | Per-pass only | Verbose, explicit |
| **One-Pass Boolean Arrays** | **O(81) = O(1)** | **O(243) = O(1)** | **1** | **Immediate** | Fast, no GC |
| **One-Pass HashSet + Strings** | **O(81) = O(1)** | **O(243) = O(1)** | **1** | **Immediate** | Concise, elegant |

> 📌 All three are O(1) because the board is fixed 9×9. The real differentiator is **code quality, clarity, and interview communication**.

---

### 🎯 What to Present to the Interviewer

1. **Immediately note** the board is fixed 9×9 → all solutions are O(1) time/space. The focus is on **correctness and clean code**.
2. **Explain the box-index formula:** `boxIdx = (row / 3) * 3 + (col / 3)`. Draw the 3×3 grid of boxes if helpful.
3. **Present the one-pass boolean arrays** approach:
   - Three 2D arrays: `rowSeen[9][9]`, `colSeen[9][9]`, `boxSeen[9][9]`.
   - Single nested loop over 81 cells.
   - `digit = board[i][j] - '1'` converts char to 0-based index.
   - Check all three arrays; if any is true → return false.
4. **Walk through** a small example showing how a box conflict is caught at the exact cell.
5. **As an elegant alternative**, show the **HashSet + encoded strings** solution — reduces code to ~8 lines and is self-explanatory.
6. **Mention the brute force** (three separate passes) as the conceptual baseline, but note it's redundant.
7. **Conclude:** Both one-pass solutions are constant-time; boolean arrays avoid object creation (performance), HashSet+strings is more concise (readability). Either is a strong interview answer.

**One‑sentence summary:**  
*Track seen digits per row, column, and 3×3 box in a single pass using either boolean arrays (fastest, zero GC) or a HashSet of encoded strings (most concise) — return false the instant a duplicate is detected.*