"""每日练习片段的代码生成器。

每个生成器接收一个 random.Random 实例，返回 (文件名主干, 文件内容)。
生成的内容都是能独立运行或解析的小程序，只用标准库，不依赖外部包。
模板里的 __XXX__ 占位符在填充时替换，避免 f-string 与目标语言的大括号冲突。
"""

from __future__ import annotations

import random

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

WORD_POOL = [
    "alpha", "bravo", "cache", "delta", "engine", "fiber", "gamma", "harbor",
    "index", "jitter", "kernel", "lambda", "matrix", "nexus", "orbit", "pixel",
    "quartz", "relay", "signal", "token", "vector", "wallet", "yield", "zephyr",
]


def _ints(rnd: random.Random, n: int, lo: int = -50, hi: int = 200, ordered: bool = False) -> list[int]:
    values = [rnd.randint(lo, hi) for _ in range(n)]
    if ordered:
        values.sort()
    return values


def _words(rnd: random.Random, n: int) -> list[str]:
    return [rnd.choice(WORD_POOL) for _ in range(n)]


def _py_list(values) -> str:
    return "[" + ", ".join(repr(v) for v in values) + "]"


def _js_list(values) -> str:
    return "[" + ", ".join(str(v) for v in values) + "]"


def _c_list(values) -> str:
    return "{" + ", ".join(str(v) for v in values) + "}"


def _go_slice(values) -> str:
    return "[]int{" + ", ".join(str(v) for v in values) + "}"


def _sql_list(values) -> str:
    return ", ".join(str(v) for v in values)


# ---------------------------------------------------------------------------
# Python
# ---------------------------------------------------------------------------

PY_BINARY_SEARCH = '''"""二分查找练习。"""


def binary_search(items, target):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def main():
    data = __DATA__
    target = __TARGET__
    print("index:", binary_search(data, target))


if __name__ == "__main__":
    main()
'''

PY_QUICK_SORT = '''"""快速排序练习。"""


def quick_sort(items):
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    smaller = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    larger = [x for x in items if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)


def main():
    data = __DATA__
    print(quick_sort(data))


if __name__ == "__main__":
    main()
'''

PY_WORD_COUNT = '''"""词频统计练习。"""

from collections import Counter


def count_words(text):
    counter = Counter(word.lower() for word in text.split())
    return counter.most_common(__TOP__)


def main():
    text = "__TEXT__"
    for word, count in count_words(text):
        print(word, count)


if __name__ == "__main__":
    main()
'''

PY_GCD_LCM = '''"""最大公约数与最小公倍数练习。"""


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def main():
    pairs = __PAIRS__
    for a, b in pairs:
        print(a, b, "->", gcd(a, b), lcm(a, b))


if __name__ == "__main__":
    main()
'''

PY_RLE = '''"""游程编码练习。"""


def encode(text):
    if not text:
        return []
    result = []
    current = text[0]
    count = 1
    for char in text[1:]:
        if char == current:
            count += 1
        else:
            result.append((current, count))
            current = char
            count = 1
    result.append((current, count))
    return result


def decode(pairs):
    return "".join(char * count for char, count in pairs)


def main():
    text = "__TEXT__"
    encoded = encode(text)
    print(encoded)
    assert decode(encoded) == text


if __name__ == "__main__":
    main()
'''

PY_MATRIX = '''"""矩阵转置与对角线求和练习。"""


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def diagonal_sum(matrix):
    return sum(matrix[i][i] for i in range(min(len(matrix), len(matrix[0]))))


def main():
    matrix = __MATRIX__
    print(transpose(matrix))
    print(diagonal_sum(matrix))


if __name__ == "__main__":
    main()
'''


def py_binary_search(rnd: random.Random):
    data = _ints(rnd, rnd.randint(8, 16), 0, 99, ordered=True)
    target = rnd.choice(data)
    code = PY_BINARY_SEARCH.replace("__DATA__", _py_list(data)).replace("__TARGET__", str(target))
    return "binary_search", code


def py_quick_sort(rnd: random.Random):
    data = _ints(rnd, rnd.randint(6, 12))
    code = PY_QUICK_SORT.replace("__DATA__", _py_list(data))
    return "quick_sort", code


def py_word_count(rnd: random.Random):
    words = _words(rnd, rnd.randint(12, 20))
    code = PY_WORD_COUNT.replace("__TEXT__", " ".join(words)).replace("__TOP__", str(rnd.randint(3, 6)))
    return "word_count", code


def py_gcd_lcm(rnd: random.Random):
    pairs = [(_ints(rnd, 2, 1, 99)) for _ in range(rnd.randint(3, 5))]
    rendered = "[" + ", ".join(f"({a}, {b})" for a, b in pairs) + "]"
    code = PY_GCD_LCM.replace("__PAIRS__", rendered)
    return "gcd_lcm", code


def py_rle(rnd: random.Random):
    text = "".join(rnd.choice("aabbccdde") for _ in range(rnd.randint(10, 18)))
    code = PY_RLE.replace("__TEXT__", text)
    return "run_length_encoding", code


def py_matrix(rnd: random.Random):
    rows, cols = rnd.randint(3, 4), rnd.randint(3, 4)
    matrix = [_ints(rnd, cols, 0, 20) for _ in range(rows)]
    rendered = "[\n        " + ",\n        ".join(_py_list(r) for r in matrix) + ",\n    ]"
    code = PY_MATRIX.replace("__MATRIX__", rendered)
    return "matrix_transpose", code


# ---------------------------------------------------------------------------
# JavaScript
# ---------------------------------------------------------------------------

JS_DEBOUNCE = '''// 简易 debounce 实现
function debounce(fn, wait) {
  let timer = null;
  return function debounced(...args) {
    if (timer !== null) {
      clearTimeout(timer);
    }
    timer = setTimeout(() => {
      timer = null;
      fn.apply(this, args);
    }, wait);
  };
}

const log = debounce((value) => console.log("called with", value), __WAIT__);
log("first");
log("second");
'''

JS_FLATTEN = '''// 递归展平嵌套数组
function flatten(items, depth = Infinity) {
  const result = [];
  for (const item of items) {
    if (Array.isArray(item) && depth > 0) {
      result.push(...flatten(item, depth - 1));
    } else {
      result.push(item);
    }
  }
  return result;
}

const nested = __DATA__;
console.log(flatten(nested, __DEPTH__));
'''

JS_GROUP_BY = '''// 按指定字段分组
function groupBy(items, keyFn) {
  const buckets = new Map();
  for (const item of items) {
    const key = keyFn(item);
    if (!buckets.has(key)) {
      buckets.set(key, []);
    }
    buckets.get(key).push(item);
  }
  return buckets;
}

const records = __DATA__;
for (const [key, values] of groupBy(records, (item) => item.group)) {
  console.log(key, values.length);
}
'''

JS_CHUNK = '''// 把数组切成固定长度的小块
function chunk(items, size) {
  if (size <= 0) {
    throw new RangeError("size must be positive");
  }
  const result = [];
  for (let i = 0; i < items.length; i += size) {
    result.push(items.slice(i, i + size));
  }
  return result;
}

console.log(chunk(__DATA__, __SIZE__));
'''

JS_DEEP_CLONE = '''// 深拷贝（结构化克隆优先，失败时回退到递归实现）
function deepClone(value) {
  if (typeof structuredClone === "function") {
    return structuredClone(value);
  }
  if (value === null || typeof value !== "object") {
    return value;
  }
  if (Array.isArray(value)) {
    return value.map(deepClone);
  }
  const copy = {};
  for (const key of Object.keys(value)) {
    copy[key] = deepClone(value[key]);
  }
  return copy;
}

const source = { id: __ID__, tags: ["a", "b"], meta: { ok: true } };
const clone = deepClone(source);
clone.meta.ok = false;
console.log(source.meta.ok, clone.meta.ok);
'''


def js_debounce(rnd: random.Random):
    return "debounce", JS_DEBOUNCE.replace("__WAIT__", str(rnd.choice([100, 150, 200, 300, 500])))


def js_flatten(rnd: random.Random):
    inner = _js_list(_ints(rnd, 3))
    data = f"[1, [{', '.join(str(v) for v in _ints(rnd, 3))}, [{', '.join(str(v) for v in _ints(rnd, 2))}]], {inner}]"
    code = JS_FLATTEN.replace("__DATA__", data).replace("__DEPTH__", str(rnd.choice([1, 2, "Infinity"])))
    return "flatten", code


def js_group_by(rnd: random.Random):
    groups = ["alpha", "beta", "gamma"]
    records = [f"{{ id: {i}, group: '{rnd.choice(groups)}' }}" for i in range(1, rnd.randint(5, 8))]
    code = JS_GROUP_BY.replace("__DATA__", "[\n  " + ",\n  ".join(records) + ",\n]")
    return "group_by", code


def js_chunk(rnd: random.Random):
    code = JS_CHUNK.replace("__DATA__", _js_list(_ints(rnd, rnd.randint(7, 12)))).replace(
        "__SIZE__", str(rnd.randint(2, 4))
    )
    return "chunk", code


def js_deep_clone(rnd: random.Random):
    return "deep_clone", JS_DEEP_CLONE.replace("__ID__", str(rnd.randint(1000, 9999)))


# ---------------------------------------------------------------------------
# TypeScript
# ---------------------------------------------------------------------------

TS_UNIQUE_BY = '''// 按 key 去重，保留首次出现的元素
export function uniqueBy<T, K>(items: readonly T[], keyFn: (item: T) => K): T[] {
  const seen = new Set<K>();
  const result: T[] = [];
  for (const item of items) {
    const key = keyFn(item);
    if (!seen.has(key)) {
      seen.add(key);
      result.push(item);
    }
  }
  return result;
}

const rows = [
__DATA__
];

console.log(uniqueBy(rows, (row) => row.id));
'''

TS_MEMOIZE = '''// 泛型 memoize，键由参数序列化得到
export function memoize<A extends unknown[], R>(fn: (...args: A) => R): (...args: A) => R {
  const cache = new Map<string, R>();
  return (...args: A): R => {
    const key = JSON.stringify(args);
    if (!cache.has(key)) {
      cache.set(key, fn(...args));
    }
    return cache.get(key) as R;
  };
}

const slowSquare = memoize((value: number): number => {
  return value * value;
});

console.log(slowSquare(__VALUE__), slowSquare(__VALUE__));
'''

TS_RESULT = '''// 用联合类型表达可能失败的结果
export type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export function parsePositiveInt(input: string): Result<number> {
  const parsed = Number.parseInt(input, 10);
  if (Number.isNaN(parsed)) {
    return { ok: false, error: new Error("not a number") };
  }
  if (parsed <= 0) {
    return { ok: false, error: new Error("must be positive") };
  }
  return { ok: true, value: parsed };
}

for (const input of __INPUTS__) {
  const result = parsePositiveInt(input);
  console.log(input, result.ok ? result.value : result.error.message);
}
'''

TS_RANGE = '''// 生成整数区间，步长可控
export function range(start: number, end: number, step = 1): number[] {
  if (step === 0) {
    throw new RangeError("step must not be zero");
  }
  const result: number[] = [];
  if (step > 0) {
    for (let i = start; i < end; i += step) {
      result.push(i);
    }
  } else {
    for (let i = start; i > end; i += step) {
      result.push(i);
    }
  }
  return result;
}

console.log(range(__START__, __END__, __STEP__));
'''


def ts_unique_by(rnd: random.Random):
    rows = [
        f"  {{ id: {i}, name: \"{rnd.choice(WORD_POOL)}\" }}" for i in _ints(rnd, rnd.randint(5, 8), 1, 6)
    ]
    code = TS_UNIQUE_BY.replace("__DATA__", ",\n".join(rows))
    return "unique_by", code


def ts_memoize(rnd: random.Random):
    return "memoize", TS_MEMOIZE.replace("__VALUE__", str(rnd.randint(2, 30)))


def ts_result(rnd: random.Random):
    inputs = ['"42"', '"0"', '"-7"', '"abc"', '"128"']
    picked = rnd.sample(inputs, rnd.randint(3, 5))
    return "result_type", TS_RESULT.replace("__INPUTS__", "[" + ", ".join(picked) + "]")


def ts_range(rnd: random.Random):
    start = rnd.randint(0, 10)
    step = rnd.choice([1, 2, 3, 5])
    code = (
        TS_RANGE.replace("__START__", str(start))
        .replace("__END__", str(start + step * rnd.randint(4, 9)))
        .replace("__STEP__", str(step))
    )
    return "range", code


# ---------------------------------------------------------------------------
# Go
# ---------------------------------------------------------------------------

GO_REVERSE = '''package main

import "fmt"

func reverse(input string) string {
	runes := []rune(input)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func main() {
	for _, word := range []string{__WORDS__} {
		fmt.Println(word, "->", reverse(word))
	}
}
'''

GO_FIB = '''package main

import "fmt"

func fib(n int) []int {
	series := make([]int, 0, n)
	a, b := 0, 1
	for i := 0; i < n; i++ {
		series = append(series, a)
		a, b = b, a+b
	}
	return series
}

func main() {
	fmt.Println(fib(__COUNT__))
}
'''

GO_WORD_COUNT = '''package main

import (
	"fmt"
	"strings"
)

func countWords(text string) map[string]int {
	counts := make(map[string]int)
	for _, word := range strings.Fields(strings.ToLower(text)) {
		counts[word]++
	}
	return counts
}

func main() {
	text := "__TEXT__"
	for word, count := range countWords(text) {
		fmt.Printf("%s=%d\\n", word, count)
	}
}
'''

GO_BUBBLE_SORT = '''package main

import "fmt"

func bubbleSort(items []int) []int {
	sorted := make([]int, len(items))
	copy(sorted, items)
	for i := 0; i < len(sorted); i++ {
		swapped := false
		for j := 0; j < len(sorted)-i-1; j++ {
			if sorted[j] > sorted[j+1] {
				sorted[j], sorted[j+1] = sorted[j+1], sorted[j]
				swapped = true
			}
		}
		if !swapped {
			break
		}
	}
	return sorted
}

func main() {
	data := __DATA__
	fmt.Println(bubbleSort(data))
}
'''


def go_reverse(rnd: random.Random):
    words = _words(rnd, rnd.randint(3, 5))
    rendered = ", ".join(f'"{w}"' for w in words)
    return "reverse_string", GO_REVERSE.replace("__WORDS__", rendered)


def go_fib(rnd: random.Random):
    return "fibonacci", GO_FIB.replace("__COUNT__", str(rnd.randint(8, 15)))


def go_word_count(rnd: random.Random):
    return "word_count", GO_WORD_COUNT.replace("__TEXT__", " ".join(_words(rnd, rnd.randint(10, 16))))


def go_bubble_sort(rnd: random.Random):
    return "bubble_sort", GO_BUBBLE_SORT.replace("__DATA__", _go_slice(_ints(rnd, rnd.randint(6, 10))))


# ---------------------------------------------------------------------------
# Java
# ---------------------------------------------------------------------------

JAVA_BINARY_SEARCH = '''public class BinarySearch {

    static int search(int[] items, int target) {
        int low = 0;
        int high = items.length - 1;
        while (low <= high) {
            int mid = (low + high) >>> 1;
            if (items[mid] == target) {
                return mid;
            }
            if (items[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] data = __DATA__;
        System.out.println(search(data, __TARGET__));
    }
}
'''

JAVA_PALINDROME = '''public class Palindrome {

    static boolean isPalindrome(String input) {
        String normalized = input.replaceAll("[^A-Za-z0-9]", "").toLowerCase();
        int left = 0;
        int right = normalized.length() - 1;
        while (left < right) {
            if (normalized.charAt(left) != normalized.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }

    public static void main(String[] args) {
        String[] samples = {__SAMPLES__};
        for (String sample : samples) {
            System.out.println(sample + " -> " + isPalindrome(sample));
        }
    }
}
'''

JAVA_ANAGRAM = '''import java.util.Arrays;

public class Anagram {

    static boolean isAnagram(String left, String right) {
        char[] a = left.replaceAll("\\\\s", "").toLowerCase().toCharArray();
        char[] b = right.replaceAll("\\\\s", "").toLowerCase().toCharArray();
        Arrays.sort(a);
        Arrays.sort(b);
        return Arrays.equals(a, b);
    }

    public static void main(String[] args) {
        System.out.println(isAnagram("__LEFT__", "__RIGHT__"));
    }
}
'''

JAVA_MATRIX = '''public class MatrixDiagonal {

    static int diagonalSum(int[][] matrix) {
        int total = 0;
        for (int i = 0; i < matrix.length && i < matrix[i].length; i++) {
            total += matrix[i][i];
        }
        return total;
    }

    public static void main(String[] args) {
        int[][] matrix = __MATRIX__;
        System.out.println(diagonalSum(matrix));
    }
}
'''


def java_binary_search(rnd: random.Random):
    data = _ints(rnd, rnd.randint(6, 10), 0, 60, ordered=True)
    code = JAVA_BINARY_SEARCH.replace("__DATA__", _c_list(data)).replace(
        "__TARGET__", str(rnd.choice(data))
    )
    return "BinarySearch", code


def java_palindrome(rnd: random.Random):
    pool = ["level", "radar", "hello", "A man a plan a canal Panama", "world", "noon"]
    samples = rnd.sample(pool, rnd.randint(3, 5))
    code = JAVA_PALINDROME.replace("__SAMPLES__", ", ".join(f'"{s}"' for s in samples))
    return "Palindrome", code


def java_anagram(rnd: random.Random):
    pairs = [("listen", "silent"), ("triangle", "integral"), ("apple", "pabble"), ("dusty", "study")]
    left, right = rnd.choice(pairs)
    return "Anagram", JAVA_ANAGRAM.replace("__LEFT__", left).replace("__RIGHT__", right)


def java_matrix(rnd: random.Random):
    size = rnd.randint(3, 4)
    rows = ", ".join(_c_list(_ints(rnd, size, 0, 20)) for _ in range(size))
    return "MatrixDiagonal", JAVA_MATRIX.replace("__MATRIX__", "{" + rows + "}")


# ---------------------------------------------------------------------------
# C
# ---------------------------------------------------------------------------

C_PRIMES = '''#include <stdio.h>

static int is_prime(int value) {
    if (value < 2) {
        return 0;
    }
    for (int divisor = 2; divisor * divisor <= value; divisor++) {
        if (value % divisor == 0) {
            return 0;
        }
    }
    return 1;
}

int main(void) {
    int found = 0;
    for (int value = 2; found < __LIMIT__; value++) {
        if (is_prime(value)) {
            printf("%d ", value);
            found++;
        }
    }
    printf("\\n");
    return 0;
}
'''

C_REVERSE = '''#include <stdio.h>
#include <string.h>

static void reverse(char *text) {
    size_t length = strlen(text);
    for (size_t i = 0; i < length / 2; i++) {
        char tmp = text[i];
        text[i] = text[length - 1 - i];
        text[length - 1 - i] = tmp;
    }
}

int main(void) {
    char buffer[] = "__TEXT__";
    reverse(buffer);
    printf("%s\\n", buffer);
    return 0;
}
'''

C_BUBBLE_SORT = '''#include <stdio.h>

static void bubble_sort(int *items, int length) {
    for (int i = 0; i < length - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < length - 1 - i; j++) {
            if (items[j] > items[j + 1]) {
                int tmp = items[j];
                items[j] = items[j + 1];
                items[j + 1] = tmp;
                swapped = 1;
            }
        }
        if (!swapped) {
            break;
        }
    }
}

int main(void) {
    int items[] = __DATA__;
    int length = (int)(sizeof(items) / sizeof(items[0]));
    bubble_sort(items, length);
    for (int i = 0; i < length; i++) {
        printf("%d ", items[i]);
    }
    printf("\\n");
    return 0;
}
'''

C_GCD = '''#include <stdio.h>

static int gcd(int a, int b) {
    while (b != 0) {
        int remainder = a % b;
        a = b;
        b = remainder;
    }
    return a;
}

int main(void) {
    printf("%d\\n", gcd(__A__, __B__));
    return 0;
}
'''


def c_primes(rnd: random.Random):
    return "primes", C_PRIMES.replace("__LIMIT__", str(rnd.randint(10, 25)))


def c_reverse(rnd: random.Random):
    return "reverse_string", C_REVERSE.replace("__TEXT__", " ".join(_words(rnd, rnd.randint(2, 3))))


def c_bubble_sort(rnd: random.Random):
    return "bubble_sort", C_BUBBLE_SORT.replace("__DATA__", _c_list(_ints(rnd, rnd.randint(6, 10))))


def c_gcd(rnd: random.Random):
    a, b = _ints(rnd, 2, 12, 240)
    return "gcd", C_GCD.replace("__A__", str(a)).replace("__B__", str(b))


# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

SQL_RANK = '''-- 按部门统计薪资前三名
WITH ranked AS (
    SELECT
        employee_id,
        department_id,
        salary,
        RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank
    FROM employees
    WHERE department_id IN (__DEPARTMENTS__)
)
SELECT employee_id, department_id, salary, salary_rank
FROM ranked
WHERE salary_rank <= __TOP__
ORDER BY department_id, salary_rank;
'''

SQL_CTE_AGG = '''-- 用 CTE 汇总每月订单金额
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS order_count,
        SUM(amount) AS total_amount
    FROM orders
    WHERE created_at >= DATE '__SINCE__'
    GROUP BY 1
)
SELECT
    month,
    order_count,
    total_amount,
    ROUND(total_amount / NULLIF(order_count, 0), 2) AS avg_amount
FROM monthly
ORDER BY month DESC
LIMIT __LIMIT__;
'''

SQL_SELF_JOIN = '''-- 找出同一部门内薪资高于直属上级的员工
SELECT
    e.employee_id,
    e.name AS employee_name,
    m.name AS manager_name,
    e.salary,
    m.salary AS manager_salary
FROM employees AS e
JOIN employees AS m ON m.employee_id = e.manager_id
WHERE e.department_id = __DEPARTMENT__
  AND e.salary > m.salary
ORDER BY e.salary DESC;
'''

SQL_RECURSIVE = '''-- 递归查询组织层级，最多展开 __DEPTH__ 层
WITH RECURSIVE org AS (
    SELECT employee_id, manager_id, name, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.employee_id, e.manager_id, e.name, org.level + 1
    FROM employees AS e
    JOIN org ON e.manager_id = org.employee_id
    WHERE org.level < __DEPTH__
)
SELECT level, COUNT(*) AS headcount
FROM org
GROUP BY level
ORDER BY level;
'''


def sql_rank(rnd: random.Random):
    departments = rnd.sample(range(1, 9), rnd.randint(2, 4))
    code = SQL_RANK.replace("__DEPARTMENTS__", _sql_list(sorted(departments))).replace(
        "__TOP__", str(rnd.randint(3, 5))
    )
    return "salary_rank", code


def sql_cte_agg(rnd: random.Random):
    since = f"{rnd.randint(2023, 2025)}-{rnd.randint(1, 12):02d}-01"
    code = SQL_CTE_AGG.replace("__SINCE__", since).replace("__LIMIT__", str(rnd.randint(6, 12)))
    return "monthly_orders", code


def sql_self_join(rnd: random.Random):
    return "salary_vs_manager", SQL_SELF_JOIN.replace("__DEPARTMENT__", str(rnd.randint(1, 9)))


def sql_recursive(rnd: random.Random):
    return "org_hierarchy", SQL_RECURSIVE.replace("__DEPTH__", str(rnd.randint(3, 6)))


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------

SH_BACKUP = '''#!/usr/bin/env bash
# 打包指定目录到备份目录，文件名带时间戳
set -euo pipefail

SOURCE_DIR="${1:-__SOURCE__}"
BACKUP_DIR="${2:-./backups}"
STAMP="$(date +%Y%m%d-%H%M%S)"

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "source directory not found: $SOURCE_DIR" >&2
    exit 1
fi

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup-$STAMP.tar.gz" -C "$SOURCE_DIR" .
echo "created $BACKUP_DIR/backup-$STAMP.tar.gz"
'''

SH_LOG_CLEAN = '''#!/usr/bin/env bash
# 删除超过指定天数的日志文件
set -euo pipefail

LOG_DIR="${1:-__LOGDIR__}"
KEEP_DAYS="__DAYS__"

find "$LOG_DIR" -type f -name "*.log" -mtime "+$KEEP_DAYS" -print -delete
echo "cleaned logs older than $KEEP_DAYS days in $LOG_DIR"
'''

SH_PORT_CHECK = '''#!/usr/bin/env bash
# 批量探测端口是否可连接
set -uo pipefail

HOST="${1:-127.0.0.1}"
PORTS=(__PORTS__)

for port in "${PORTS[@]}"; do
    if (echo > "/dev/tcp/$HOST/$port") >/dev/null 2>&1; then
        echo "$port open"
    else
        echo "$port closed"
    fi
done
'''

SH_BATCH_RENAME = '''#!/usr/bin/env bash
# 给目录内文件批量加前缀，默认先做试运行
set -euo pipefail

TARGET_DIR="${1:-.}"
PREFIX="${2:-__PREFIX__}"
APPLY="${3:-no}"

count=0
for file in "$TARGET_DIR"/*; do
    [[ -f "$file" ]] || continue
    base="$(basename "$file")"
    [[ "$base" == "$PREFIX"* ]] && continue
    target="$TARGET_DIR/$PREFIX$base"
    if [[ "$APPLY" == "yes" ]]; then
        mv -- "$file" "$target"
    else
        echo "$file -> $target"
    fi
    count=$((count + 1))
done

echo "processed $count file(s)"
'''


def sh_backup(rnd: random.Random):
    return "backup", SH_BACKUP.replace("__SOURCE__", rnd.choice(["./data", "./src", "./config"]))


def sh_log_clean(rnd: random.Random):
    code = SH_LOG_CLEAN.replace("__LOGDIR__", rnd.choice(["./logs", "/var/log/app"])).replace(
        "__DAYS__", str(rnd.choice([7, 14, 30, 60]))
    )
    return "log_cleanup", code


def sh_port_check(rnd: random.Random):
    ports = " ".join(str(p) for p in sorted(rnd.sample([22, 80, 443, 3306, 5432, 6379, 8080, 9000], rnd.randint(3, 5))))
    return "port_check", SH_PORT_CHECK.replace("__PORTS__", ports)


def sh_batch_rename(rnd: random.Random):
    return "batch_rename", SH_BATCH_RENAME.replace("__PREFIX__", rnd.choice(["bak_", "old_", "2026_"]))


# ---------------------------------------------------------------------------
# 注册表
# ---------------------------------------------------------------------------

TEMPLATES = {
    "python": {
        "ext": "py",
        "builders": [
            py_binary_search,
            py_quick_sort,
            py_word_count,
            py_gcd_lcm,
            py_rle,
            py_matrix,
        ],
    },
    "javascript": {
        "ext": "js",
        "builders": [js_debounce, js_flatten, js_group_by, js_chunk, js_deep_clone],
    },
    "typescript": {
        "ext": "ts",
        "builders": [ts_unique_by, ts_memoize, ts_result, ts_range],
    },
    "go": {
        "ext": "go",
        "builders": [go_reverse, go_fib, go_word_count, go_bubble_sort],
    },
    "java": {
        "ext": "java",
        "builders": [java_binary_search, java_palindrome, java_anagram, java_matrix],
    },
    "c": {
        "ext": "c",
        "builders": [c_primes, c_reverse, c_bubble_sort, c_gcd],
    },
    "sql": {
        "ext": "sql",
        "builders": [sql_rank, sql_cte_agg, sql_self_join, sql_recursive],
    },
    "shell": {
        "ext": "sh",
        "builders": [sh_backup, sh_log_clean, sh_port_check, sh_batch_rename],
    },
}


def generate_one(rnd: random.Random, language: str):
    """生成一个片段，返回 (语言, 文件名主干, 扩展名, 内容)。"""
    spec = TEMPLATES[language]
    stem, code = rnd.choice(spec["builders"])(rnd)
    return language, stem, spec["ext"], code


def make_pool(rnd: random.Random, languages: list[str]) -> list[tuple[str, object]]:
    """把指定语言的所有模板打散成一个池子，供一天内不重复地取用。"""
    pool = [(language, builder) for language in languages for builder in TEMPLATES[language]["builders"]]
    rnd.shuffle(pool)
    return pool


def render(rnd: random.Random, language: str, builder):
    """用指定模板渲染一个片段，返回 (语言, 文件名主干, 扩展名, 内容)。"""
    stem, code = builder(rnd)
    return language, stem, TEMPLATES[language]["ext"], code
