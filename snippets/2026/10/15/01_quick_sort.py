"""快速排序练习。"""


def quick_sort(items):
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    smaller = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    larger = [x for x in items if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)


def main():
    data = [113, 78, 185, 174, 133, 185, 153, 65, -18, 132, 33, -39]
    print(quick_sort(data))


if __name__ == "__main__":
    main()
