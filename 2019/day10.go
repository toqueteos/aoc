package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strings"
)

const (
	mapSide     = 28
	mapEmpty    = '.'
	mapAsteroid = '#'

	objEmpty    = 0
	objAsteroid = 1
)

func main() {
	f, err := os.Open("input10.txt")
	fatalIf(err)

	scan := bufio.NewScanner(f)
	fatalIf(scan.Err())

	var lines []string
	for scan.Scan() {
		line := strings.TrimSpace(scan.Text())
		fatalIf(scan.Err())

		lines = append(lines, line)
	}

	// fmt.Println("samples")
	// part1([]string{".#..#", ".....", "#####", "....#", "...##"})
	// part1([]string{"......#.#.", "#..#.#....", "..#######.", ".#.#.###..", ".#..#.....", "..#....#.#", "#..#....#.", ".##.#..###", "##...#..#.", ".#....####"})
	// part1([]string{"#.#...#.#.", ".###....#.", ".#....#...", "##.#.#.#.#", "....#.#.#.", ".##..###.#", "..#...##..", "..##....##", "......#...", ".####.###."})
	// part1([]string{".#..#..###", "####.###.#", "....###.#.", "..###.##.#", "##.##.#.#.", "....###..#", "..#.#..#.#", "#..#.#.###", ".##...##.#", ".....#.#.."})
	// part1([]string{".#..##.###...#######", "##.############..##.", ".#.######.########.#", ".###.#######.####.#.", "#####.##.#.##.###.##", "..#####..#.#########", "####################", "#.####....###.#.#.##", "##.#################", "#####.##.###..####..", "..######..##.#######", "####.##.####...##..#", ".#####..#.######.###", "##...#.##########...", "#.##########.#######", ".####.#.###.###.#.##", "....##.##.###..#####", ".#.#.###########.###", "#.#.#.#####.####.###", "###.##.####.##.#..##"})
	// fmt.Println("---")

	fmt.Println("part1")
	part1(lines)
	fmt.Println("---")

	fmt.Println("part2")
	part2(lines)
	fmt.Println("---")
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

type pair struct {
	x, y int
}

func (p *pair) simplify() {
	cd := abs(gcd(p.x, p.y))
	if cd > 1 {
		p.x /= cd
		p.y /= cd
	}
}

func parseMap(lines []string) []pair {
	var as []pair
	for y := 0; y < len(lines); y++ {
		for x, elem := range lines[y] {
			if elem == mapAsteroid {
				as = append(as, pair{x: x, y: y})
			}
		}
	}
	return as
}

func vector(a, b pair) pair {
	return pair{x: b.x - a.x, y: b.y - a.y}
}

func vectoreq(a, b pair) bool {
	a.simplify()
	b.simplify()
	return a.x == b.x && a.y == b.y
}

func dist(a, b pair) int {
	x := b.x - a.x
	y := b.y - a.y
	d := x*x + y*y
	return d
}

type station struct {
	pos  pair
	sees int
}

func part1(lines []string) {
	var result []station
	stations := parseMap(lines)

	for _, src := range stations {
		// why copy stations when you can the parse map again?
		asteroids := parseMap(lines)

		vectors := make(map[pair]bool)
		for _, dst := range asteroids {
			if dst == src {
				continue
			}

			v := vector(src, dst)
			v.simplify()

			vectors[v] = true
		}

		result = append(result, station{pos: src, sees: len(vectors)})
	}

	sort.Slice(result, func(i, j int) bool {
		return result[i].sees > result[j].sees
	})

	fmt.Println(result[0])
}

func angle(p pair) float64 {
	a := -math.Atan2(float64(p.x), float64(p.y))
	a += math.Pi
	return a
}

func part2(lines []string) {
	station := pair{x: 22, y: 19}
	asteroids := parseMap(lines)

	laser := make(map[float64][]pair)
	for _, dst := range asteroids {
		if dst == station {
			continue
		}
		v := vector(station, dst)
		a := angle(v)
		laser[a] = append(laser[a], dst)
	}

	type kv struct {
		angle     float64
		asteroids []pair
	}
	var candidates []kv
	for a, as := range laser {
		candidates = append(candidates, kv{angle: a, asteroids: as})
	}
	sort.Slice(candidates, func(i, j int) bool { return candidates[i].angle < candidates[j].angle })

	// for _, c := range candidates {
	// 	fmt.Println(c)
	// }

	fmt.Println(candidates[199])
	asteroid200 := candidates[199].asteroids[0]
	fmt.Println(asteroid200.x*100 + asteroid200.y)
}

func fatalIf(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, "err")
		os.Exit(1)
	}
}
