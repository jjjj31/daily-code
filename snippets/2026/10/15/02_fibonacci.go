package main

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
	fmt.Println(fib(15))
}
