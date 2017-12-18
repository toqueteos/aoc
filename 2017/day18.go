package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type line struct {
	op   string
	args []string
}

func parseLine(input string) line {
	return line{
		op:   input[:3],
		args: strings.Fields(input[4:]),
	}
}

func parseInput(scan *bufio.Scanner) []line {
	var lines []line
	for scan.Scan() {
		line := scan.Text()
		lines = append(lines, parseLine(line))
	}
	return lines
}

var letters = "abcdefghijklmnopqrstuvwxyz"

func getValue(registers map[string]int64, index string) int64 {
	if strings.Contains(letters, index) {
		if r, ok := registers[index]; ok {
			return r
		}

		registers[index] = 0
		return 0
	}

	n, _ := strconv.ParseInt(index, 10, 64)
	return n
}

type step struct {
	line   line
	rx, ry string
	x, y   int64
	ip     int
}

func vmStep(lines []line, registers map[string]int64, ip int) step {
	li := lines[ip]

	rx := li.args[0]
	x := getValue(registers, rx)

	var ry string
	var y int64
	if len(li.args) > 1 {
		ry = li.args[1]
		y = getValue(registers, ry)
	}

	switch li.op {
	case "snd":
	case "rcv":
	case "set":
		registers[rx] = y
	case "add":
		registers[rx] = x + y
	case "mul":
		registers[rx] = x * y
	case "mod":
		registers[rx] = x % y
	case "jgz":
		if x > 0 {
			return step{rx: rx, ry: ry, x: x, y: y, line: li, ip: ip + int(y)}
		}
	default:
		panic(fmt.Sprintf("unknown op %q", li.op))
	}

	return step{rx: rx, ry: ry, x: x, y: y, line: li, ip: ip + 1}
}

func vm(lines []line) int64 {
	registers := map[string]int64{}

	var snd []int64
	ip := 0
	length := len(lines)

	for ip < length {
		step := vmStep(lines, registers, ip)
		ip = step.ip

		switch step.line.op {
		case "snd":
			snd = append(snd, step.x)
		case "rcv":
			if step.x > 0 {
				return snd[len(snd)-1]
			}
		}
	}

	panic("unreachable")
}

func vm2(lines []line, pid int64, snd, rcv chan int64, count chan bool) {
	registers := map[string]int64{
		"p": pid,
	}

	ip := 0
	length := len(lines)

	for ip < length {
		step := vmStep(lines, registers, ip)
		ip = step.ip

		switch step.line.op {
		case "snd":
			select {
			case snd <- step.x:
				if count != nil {
					count <- true
				}
			case <-time.After(1 * time.Second):
				if count != nil {
					close(count)
					break
				}
			}
		case "rcv":
			select {
			case y := <-rcv:
				registers[step.rx] = y
			case <-time.After(1 * time.Second):
				if count != nil {
					close(count)
					break
				}
			}
		}
	}

	panic("unreachable")
}

func firstRcv(lines []line) int64 {
	return vm(lines)
}

func countPid1Snd(lines []line) int {
	count := make(chan bool, 32)
	ch0 := make(chan int64, 1024)
	ch1 := make(chan int64, 1024)
	go vm2(lines, 1, ch0, ch1, count)
	go vm2(lines, 0, ch1, ch0, nil)

	total := 0
	for _ = range count {
		total++
	}

	return total
}

func main() {
	f, err := os.Open("input18.txt")
	if err != nil {
		panic(err)
	}

	lines := parseInput(bufio.NewScanner(f))

	fmt.Println(firstRcv(lines))
	fmt.Println(countPid1Snd(lines))
	// 8600
	// 7239
}
