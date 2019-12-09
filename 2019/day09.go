package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

const (
	opAdd                = 1
	opMult               = 2
	opInput              = 3
	opOutput             = 4
	opJumpIfTrue         = 5
	opJumpIfFalse        = 6
	opLessThan           = 7
	opEquals             = 8
	opRelativeBaseOffset = 9
	opHalt               = 99

	modePosition  = 0
	modeImmediate = 1
	modeRelative  = 2
)

var (
	opNames = map[int64]string{
		opAdd:                "add",
		opMult:               "mult",
		opInput:              "input",
		opOutput:             "output",
		opJumpIfTrue:         "jump-if-true",
		opJumpIfFalse:        "jump-if-false",
		opLessThan:           "less-than",
		opEquals:             "equals",
		opRelativeBaseOffset: "relative-base-offset",
		opHalt:               "halt",
	}

	opSizes = map[int64]int64{
		opAdd:                3,
		opMult:               3,
		opInput:              1,
		opOutput:             1,
		opJumpIfTrue:         2,
		opJumpIfFalse:        2,
		opLessThan:           3,
		opEquals:             3,
		opRelativeBaseOffset: 1,
		opHalt:               0,
	}
)

func read(input string) map[int64]int64 {
	program := make(map[int64]int64)
	for i, n := range strings.Split(input, ",") {
		v, _ := strconv.ParseInt(n, 10, 64)
		program[int64(i)] = v
	}

	return program
}

func decode(input int64) (int64, []int) {
	if input == 99 {
		return input, nil
	}

	op := input % 100
	var modes [3]int

	// input /= 10
	// for i := 0; i <= 2; i++ {
	// 	if input > 0 {
	// 		input = input / 100
	// 		modes[i] = int(input % 10)
	// 	}
	// }

	input = input / 100
	modes[0] = int(input % 10)
	input = input / 10
	modes[1] = int(input % 10)
	input = input / 10
	modes[2] = int(input % 10)

	return op, modes[:]
}

func slice(program map[int64]int64, start, offset int64) []int64 {
	var frag []int64
	for i := int64(0); i < offset; i++ {
		frag = append(frag, program[start+i])
	}
	return frag
}

func intcode(program map[int64]int64, input chan int64, output chan int64) {
	ip := int64(0)
	rb := int64(0)

	readValue := func(modes []int, offset int64) int64 {
		switch modes[offset-1] {
		case modePosition:
			return program[program[ip+offset]]
		case modeImmediate:
			return program[ip+offset]
		case modeRelative:
			return program[rb+program[ip+offset]]
		}

		panic("unreachable")
	}

	writeValue := func(modes []int, offset int64, value int64) {
		switch modes[offset-1] {
		case modePosition:
			program[program[ip+offset]] = value
		case modeImmediate:
			program[ip+offset] = value
		case modeRelative:
			program[rb+program[ip+offset]] = value
		}
	}

	for {
		opcode, modes := decode(program[ip])
		// fmt.Printf("[%s] input=%v modes=%v\n", opNames[opcode], slice(program, ip, opSizes[opcode]), modes)

		switch opcode {
		case 1: // add
			val1 := readValue(modes, 1)
			val2 := readValue(modes, 2)
			writeValue(modes, 3, val1+val2)
			ip += 4
		case 2: // mult
			val1 := readValue(modes, 1)
			val2 := readValue(modes, 2)
			writeValue(modes, 3, val1*val2)
			ip += 4
		case 3: // input
			value := <-input
			writeValue(modes, 1, value)
			ip += 2
		case 4: // output
			output <- readValue(modes, 1)
			ip += 2
		case 5: // jump-if-true
			val1 := readValue(modes, 1)
			val2 := readValue(modes, 2)
			if val1 != 0 {
				ip = val2
			} else {
				ip += 3
			}
		case 6: // jump-if-false
			val1 := readValue(modes, 1)
			val2 := readValue(modes, 2)
			if val1 == 0 {
				ip = val2
			} else {
				ip += 3
			}
		case 7: // less-than
			val1 := readValue(modes, 1)
			val2 := readValue(modes, 2)
			if val1 < val2 {
				writeValue(modes, 3, 1)
			} else {
				writeValue(modes, 3, 0)
			}
			ip += 4
		case 8: // equals
			val1 := readValue(modes, 1)
			val2 := readValue(modes, 2)
			if val1 == val2 {
				writeValue(modes, 3, 1)
			} else {
				writeValue(modes, 3, 0)
			}
			ip += 4
		case 9: // relative-base-offset
			rb += readValue(modes, 1)
			ip += 2
		case 99:
			// fmt.Println("halt")
			close(output)
			return
		default:
			fmt.Println("error", ip)
			return
		}
	}

	return
}

func run(line string, input int64) {
	in := make(chan int64, 2)
	out := make(chan int64, 2)

	in <- input
	go intcode(read(line), in, out)

	for v := range out {
		fmt.Println(v)
	}
}

func part1(line string) {
	run(line, 1)
}

func part2(line string) {
	run(line, 2)
}

func main() {
	contents, err := ioutil.ReadFile("input09.txt")
	fatalIf(err)

	line := string(bytes.TrimSpace(contents))

	// fmt.Println("tests")
	// part1("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
	// part1("1102,34915192,34915192,7,4,7,99,0")
	// part1("104,1125899906842624,99")
	// fmt.Println("---")

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
