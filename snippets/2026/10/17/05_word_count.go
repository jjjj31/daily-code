package main

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
	text := "delta pixel orbit harbor relay engine jitter kernel relay jitter matrix"
	for word, count := range countWords(text) {
		fmt.Printf("%s=%d\n", word, count)
	}
}
