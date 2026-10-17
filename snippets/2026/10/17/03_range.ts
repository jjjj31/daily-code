// 生成整数区间，步长可控
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

console.log(range(6, 15, 1));
