package main

import "fmt"

func reverse(input string) string {
	runes := []rune(input)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func main() {
	for _, word := range []string{"nexus", "lambda", "pixel", "index"} {
		fmt.Println(word, "->", reverse(word))
	}
}
