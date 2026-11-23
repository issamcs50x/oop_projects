# شرح دوال فحص الفوز (Win Check)

تشرح هذه الوثيقة الدوال الأربع في كلاس `Refree` المسؤولة عن اكتشاف الفوز في لعبة إكس-أو.

## الفكرة العامة

- كل لاعب لديه قائمة حركات `player_moves`.
- كل حركة هي زوج `(row, col)` بفهرسة صفرية (تبدأ من 0).
- يفوز اللاعب حين يكمل **خطًا كاملًا** عدد خاناته يساوي `board_side`.
- كل دالة تبحث عن نمط مختلف، وكلها تقارن النتيجة بـ `board_side`، ولذلك تعمل مع أي حجم لوحة وليس 3×3 فقط.

---

## 1. `row_case`: نفس الصف

```python
@staticmethod
def row_case(board_side, player_moves):
    rows = [move[0] for move in player_moves]
    counter = Counter(rows)
    return board_side == max(counter.values())
```

- تستخرج رقم الصف من كل حركة.
- يحسب `Counter` عدد مرات تكرار كل صف.
- إذا تكرر أي صف `board_side` مرة، فقد ملأ اللاعب صفًا كاملًا.

**مثال (3×3):** الحركات `(1,0), (1,1), (1,2)` تعطي الصفوف `[1, 1, 1]`، فالتكرار الأقصى 3 يساوي الضلع، والنتيجة فوز.

---

## 2. `col_case`: نفس العمود

```python
@staticmethod
def col_case(board_side, player_moves):
    cols = [move[1] for move in player_moves]
    counter = Counter(cols)
    return board_side == max(counter.values())
```

- نفس فكرة الصف تمامًا، لكن باستخراج `move[1]` (رقم العمود) بدل `move[0]`.

**مثال (3×3):** الحركات `(0,2), (1,2), (2,2)` تعطي الأعمدة `[2, 2, 2]`، فيتكرر العمود 2 ثلاث مرات، والنتيجة فوز.

---

## 3. `main_diameter_case`: القطر الرئيسي

```python
@staticmethod
def main_diameter_case(board_side, player_moves):
    filtred = list(filter(lambda move: move[0] == move[1], player_moves))
    return len(filtred) == board_side
```

- خانات القطر الرئيسي (من أعلى اليسار إلى أسفل اليمين) **رقم صفها يساوي رقم عمودها**: `(0,0), (1,1), (2,2)`.
- تُبقي الدالة الحركات التي تحقق `row == col` فقط.
- إذا كان عددها يساوي `board_side`، فقد ملأ اللاعب القطر بالكامل.

---

## 4. `rev_diameter_case`: القطر العكسي

```python
@staticmethod
def rev_diameter_case(board_side, player_moves):
    filtred = list(filter(lambda move: move[0] + move[1] == board_side - 1,
                          player_moves))
    return len(filtred) == board_side
```

- خانات القطر العكسي (من أعلى اليمين إلى أسفل اليسار): `(0,2), (1,1), (2,0)`.
- **مجموع الصف والعمود ثابت** في كل خانة منها، وهو `board_side - 1`. في لوحة 3×3: `0+2 = 1+1 = 2+0 = 2`.
- سبب `- 1` هو الفهرسة الصفرية: أكبر فهرس هو `board_side - 1` وليس `board_side`.
- إذا كان عدد الحركات المطابقة يساوي `board_side`، فقد ملأ اللاعب هذا القطر.

---

## الملخص

| الدالة | الشرط على كل حركة | شرط الفوز |
|---|---|---|
| `row_case` | نفس قيمة `row` | تكرارها = `board_side` |
| `col_case` | نفس قيمة `col` | تكرارها = `board_side` |
| `main_diameter_case` | `row == col` | عدد الحركات = `board_side` |
| `rev_diameter_case` | `row + col == board_side - 1` | عدد الحركات = `board_side` |

## ملاحظة

`max(counter.values())` يفشل مع خطأ إذا كانت `player_moves` فارغة. لا يحدث هذا في اللعبة لأن `game_logic` تتحقق أولًا من أن `len(player_moves) >= board_side`.