// 用联合类型表达可能失败的结果
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

for (const input of ["42", "-7", "abc", "0"]) {
  const result = parsePositiveInt(input);
  console.log(input, result.ok ? result.value : result.error.message);
}
