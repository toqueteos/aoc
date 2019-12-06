package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	f, err := os.Open("input06.txt")
	fatalIf(err)

	scan := bufio.NewScanner(f)
	fatalIf(scan.Err())

	parent := make(map[string]string)
	for scan.Scan() {
		line := strings.TrimSpace(scan.Text())
		fatalIf(scan.Err())

		parts := strings.Split(line, ")")
		va, vb := parts[0], parts[1]
		parent[vb] = va
	}

	fmt.Println(part1(parent))
	fmt.Println(part2(parent))
}

func part1(parent map[string]string) int {
	orbits := 0
	for _, n := range parent {
		orbits += len(pathToCOM(n, parent))
	}
	return orbits
}

func part2(parent map[string]string) int {
	you := pathToCOM("YOU", parent)
	san := pathToCOM("SAN", parent)

	for i, p1 := range you {
		for j, p2 := range san {
			if p1 == p2 {
				return i + j
			}
		}
	}

	panic("unreachable")
}

func pathToCOM(node string, parents map[string]string) []string {
	var path []string
	for {
		parent := parents[node]
		path = append(path, parent)
		// fmt.Printf("%s <- %s\n", parent, node)

		if node == "COM" {
			return path
		}

		node = parent
	}

	panic("unreachable")
}

func fatalIf(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, "err")
		os.Exit(1)
	}
}
