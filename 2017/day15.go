package main

import "fmt"

type nextFn func() int

func gen(value, factor, mod int) (int, int) {
	for {
		value = (value * factor) % 2147483647
		if value%mod == 0 {
			return value, value & 0xffff
		}
	}
}

func generator(value, factor, mod int) nextFn {
	return func() int {
		var ret int
		value, ret = gen(value, factor, mod)
		return ret
	}
}

func sum(a, b nextFn, N int) int {
	total := 0
	for i := 0; i < N; i++ {
		if a() == b() {
			total++
		}
	}
	return total
}

func run(A, B int) {
	FACTOR_A := 16807
	FACTOR_B := 48271
	FORTY_MILLION := 40000000
	FIVE_MILLION := 5000000
	MOD_4 := 4
	MOD_8 := 8

	fmt.Println(sum(generator(A, FACTOR_A, 1), generator(B, FACTOR_B, 1), FORTY_MILLION))
	fmt.Println(sum(generator(A, FACTOR_A, MOD_4), generator(B, FACTOR_B, MOD_8), FIVE_MILLION))
}

func main() {
	run(65, 8921)
	// 588
	// 309

	run(883, 879)
	// 609
	// 253
}
