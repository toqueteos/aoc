package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
)

func read(input string) []int {
	var program []int
	for _, n := range strings.Split(input, ",") {
		i, _ := strconv.Atoi(n)
		program = append(program, i)
	}

	return program
}

func decode(input int) (int, []int) {
	if input == 99 {
		return input, nil
	}

	op := input % 100
	var modes [2]int

	switch op {
	case 1, 2, 5, 6, 7, 8:
		input = input / 100
		modes[0] = input % 10
		input = input / 10
		modes[1] = input % 10
	}

	return op, modes[:]
}

func intcode(program []int, input chan int, output chan int) {
	ip := 0

	valueFor := func(params []int, offset int) int {
		// fmt.Println(params)
		switch params[offset-1] {
		case 0: // position
			return program[program[ip+offset]]
		case 1: // immediate
			return program[ip+offset]
		}

		panic("unreachable")
	}

	for {
		opcode, modes := decode(program[ip])
		// fmt.Println()
		// fmt.Println(program[ip:][:5])

		switch opcode {
		case 1: // add
			val1 := valueFor(modes, 1)
			val2 := valueFor(modes, 2)
			val3 := program[ip+3]
			// fmt.Printf("add %d %d %d => add %d %d %d\n",
			// 	program[ip+1], program[ip+2], program[ip+3],
			// 	val1, val2, val3)
			program[val3] = val1 + val2
			// fmt.Printf("debug %d => %d\n", val3, program[val3])
			ip += 4
		case 2: // mult
			val1 := valueFor(modes, 1)
			val2 := valueFor(modes, 2)
			val3 := program[ip+3]
			// fmt.Printf("mult %d %d %d => add %d %d %d\n",
			// 	program[ip+1], program[ip+2], program[ip+3],
			// 	val1, val2, val3)
			program[val3] = val1 * val2
			// fmt.Printf("debug %d => %d\n", val3, program[val3])
			ip += 4
		case 3: // input
			// fmt.Printf("store %d (%d)\n", program[ip+1], input)
			program[program[ip+1]] = <-input
			// fmt.Printf("debug %d => %d\n", program[ip+1], program[program[ip+1]])
			ip += 2
		case 4: // output
			output <- program[program[ip+1]]
			// fmt.Printf("load %d (%d)\n", program[ip+1], output)
			// fmt.Println("out", output)
			ip += 2
		case 5: // jump-if-true
			// fmt.Println("jump-if-true")
			val1 := valueFor(modes, 1)
			val2 := valueFor(modes, 2)
			// fmt.Printf("jump-if-true %d %d => jump-if-true %d %d\n",
			// 	program[ip+1], program[ip+2],
			// 	val1, val2)
			if val1 != 0 {
				ip = val2
			} else {
				ip += 3
			}
		case 6: // jump-if-false
			// fmt.Println("jump-if-false")
			val1 := valueFor(modes, 1)
			val2 := valueFor(modes, 2)
			if val1 == 0 {
				ip = val2
			} else {
				ip += 3
			}
		case 7: // less-than
			// fmt.Println("less-than")
			val1 := valueFor(modes, 1)
			val2 := valueFor(modes, 2)
			ip3 := program[ip+3]
			if val1 < val2 {
				program[ip3] = 1
			} else {
				program[ip3] = 0
			}
			ip += 4
		case 8: // equals
			// fmt.Println("equals")
			val1 := valueFor(modes, 1)
			val2 := valueFor(modes, 2)
			ip3 := program[ip+3]
			if val1 == val2 {
				program[ip3] = 1
			} else {
				program[ip3] = 0
			}
			ip += 4
		case 99:
			// fmt.Println("halt")
			return
		default:
			fmt.Println("error", ip)
			return
		}
	}

	return
}

var permutations = [][]int{
	{0, 1, 2, 3, 4}, {0, 1, 2, 4, 3}, {0, 1, 3, 2, 4}, {0, 1, 3, 4, 2}, {0, 1, 4, 2, 3}, {0, 1, 4, 3, 2}, {0, 2, 1, 3, 4}, {0, 2, 1, 4, 3}, {0, 2, 3, 1, 4}, {0, 2, 3, 4, 1}, {0, 2, 4, 1, 3}, {0, 2, 4, 3, 1}, {0, 3, 1, 2, 4}, {0, 3, 1, 4, 2}, {0, 3, 2, 1, 4}, {0, 3, 2, 4, 1}, {0, 3, 4, 1, 2}, {0, 3, 4, 2, 1}, {0, 4, 1, 2, 3}, {0, 4, 1, 3, 2}, {0, 4, 2, 1, 3}, {0, 4, 2, 3, 1}, {0, 4, 3, 1, 2}, {0, 4, 3, 2, 1},
	{1, 0, 2, 3, 4}, {1, 0, 2, 4, 3}, {1, 0, 3, 2, 4}, {1, 0, 3, 4, 2}, {1, 0, 4, 2, 3}, {1, 0, 4, 3, 2}, {1, 2, 0, 3, 4}, {1, 2, 0, 4, 3}, {1, 2, 3, 0, 4}, {1, 2, 3, 4, 0}, {1, 2, 4, 0, 3}, {1, 2, 4, 3, 0}, {1, 3, 0, 2, 4}, {1, 3, 0, 4, 2}, {1, 3, 2, 0, 4}, {1, 3, 2, 4, 0}, {1, 3, 4, 0, 2}, {1, 3, 4, 2, 0}, {1, 4, 0, 2, 3}, {1, 4, 0, 3, 2}, {1, 4, 2, 0, 3}, {1, 4, 2, 3, 0}, {1, 4, 3, 0, 2}, {1, 4, 3, 2, 0},
	{2, 0, 1, 3, 4}, {2, 0, 1, 4, 3}, {2, 0, 3, 1, 4}, {2, 0, 3, 4, 1}, {2, 0, 4, 1, 3}, {2, 0, 4, 3, 1}, {2, 1, 0, 3, 4}, {2, 1, 0, 4, 3}, {2, 1, 3, 0, 4}, {2, 1, 3, 4, 0}, {2, 1, 4, 0, 3}, {2, 1, 4, 3, 0}, {2, 3, 0, 1, 4}, {2, 3, 0, 4, 1}, {2, 3, 1, 0, 4}, {2, 3, 1, 4, 0}, {2, 3, 4, 0, 1}, {2, 3, 4, 1, 0}, {2, 4, 0, 1, 3}, {2, 4, 0, 3, 1}, {2, 4, 1, 0, 3}, {2, 4, 1, 3, 0}, {2, 4, 3, 0, 1}, {2, 4, 3, 1, 0},
	{3, 0, 1, 2, 4}, {3, 0, 1, 4, 2}, {3, 0, 2, 1, 4}, {3, 0, 2, 4, 1}, {3, 0, 4, 1, 2}, {3, 0, 4, 2, 1}, {3, 1, 0, 2, 4}, {3, 1, 0, 4, 2}, {3, 1, 2, 0, 4}, {3, 1, 2, 4, 0}, {3, 1, 4, 0, 2}, {3, 1, 4, 2, 0}, {3, 2, 0, 1, 4}, {3, 2, 0, 4, 1}, {3, 2, 1, 0, 4}, {3, 2, 1, 4, 0}, {3, 2, 4, 0, 1}, {3, 2, 4, 1, 0}, {3, 4, 0, 1, 2}, {3, 4, 0, 2, 1}, {3, 4, 1, 0, 2}, {3, 4, 1, 2, 0}, {3, 4, 2, 0, 1}, {3, 4, 2, 1, 0},
	{4, 0, 1, 2, 3}, {4, 0, 1, 3, 2}, {4, 0, 2, 1, 3}, {4, 0, 2, 3, 1}, {4, 0, 3, 1, 2}, {4, 0, 3, 2, 1}, {4, 1, 0, 2, 3}, {4, 1, 0, 3, 2}, {4, 1, 2, 0, 3}, {4, 1, 2, 3, 0}, {4, 1, 3, 0, 2}, {4, 1, 3, 2, 0}, {4, 2, 0, 1, 3}, {4, 2, 0, 3, 1}, {4, 2, 1, 0, 3}, {4, 2, 1, 3, 0}, {4, 2, 3, 0, 1}, {4, 2, 3, 1, 0}, {4, 3, 0, 1, 2}, {4, 3, 0, 2, 1}, {4, 3, 1, 0, 2}, {4, 3, 1, 2, 0}, {4, 3, 2, 0, 1}, {4, 3, 2, 1, 0},
}

func inout(inputs ...int) (in chan int, out chan int) {
	in = make(chan int, 2)
	out = make(chan int)
	for _, input := range inputs {
		in <- input
	}
	return
}

func intcodeRun(wg *sync.WaitGroup, line string, in, out chan int) {
	intcode(read(line), in, out)
	wg.Done()
}

func part1(line string) {
	type pair struct {
		phase  []int
		output int
	}

	var output []pair

	for _, p := range permutations {
		cha := make(chan int, 2)
		cha <- p[0]
		cha <- 0
		chab := make(chan int, 2)
		chab <- p[1]
		chbc := make(chan int, 2)
		chbc <- p[2]
		chcd := make(chan int, 2)
		chcd <- p[3]
		chde := make(chan int, 2)
		chde <- p[4]
		chea := make(chan int, 2)

		var wg sync.WaitGroup
		wg.Add(5)

		go intcodeRun(&wg, line, cha, chab)
		go intcodeRun(&wg, line, chab, chbc)
		go intcodeRun(&wg, line, chbc, chcd)
		go intcodeRun(&wg, line, chcd, chde)
		go intcodeRun(&wg, line, chde, chea)

		wg.Wait()

		out := <-chea

		// fmt.Printf("phase: %v out: %d\n", p, out)

		output = append(output, pair{phase: p, output: out})
	}

	sort.SliceStable(output, func(i, j int) bool { return output[i].output > output[j].output })
	fmt.Println(output[0])
}

func part2(line string) {
	type pair struct {
		phase  []int
		output int
	}

	var output []pair

	for _, p := range permutations {
		chea := make(chan int, 2)
		chea <- p[0] + 5
		chea <- 0
		chab := make(chan int, 2)
		chab <- p[1] + 5
		chbc := make(chan int, 2)
		chbc <- p[2] + 5
		chcd := make(chan int, 2)
		chcd <- p[3] + 5
		chde := make(chan int, 2)
		chde <- p[4] + 5

		var wg sync.WaitGroup
		wg.Add(5)

		go intcodeRun(&wg, line, chea, chab)
		go intcodeRun(&wg, line, chab, chbc)
		go intcodeRun(&wg, line, chbc, chcd)
		go intcodeRun(&wg, line, chcd, chde)
		go intcodeRun(&wg, line, chde, chea)

		wg.Wait()

		out := <-chea

		// fmt.Printf("phase: %v out: %d\n", p, out)

		output = append(output, pair{phase: p, output: out})
	}

	sort.SliceStable(output, func(i, j int) bool { return output[i].output > output[j].output })
	fmt.Println(output[0])
}

func main() {
	contents, err := ioutil.ReadFile("input07.txt")
	fatalIf(err)

	line := string(bytes.TrimSpace(contents))

	fmt.Println("part1")
	part1(line)
	fmt.Println("---")

	fmt.Println("part2")
	part2(line)
	fmt.Println("---")
}

func fatalIf(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
