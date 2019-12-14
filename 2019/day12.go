package main

import (
	"fmt"
	"os"
)

const size = 4

func abs(value int) int {
	if value < 0 {
		return -value
	}
	return value
}

func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func lcm(a, b int) int {
	return (a * b) / gcd(a, b)
}

func lcm3(a, b, c int) int {
	return lcm(lcm(a, b), c)
}

type xyz struct {
	x, y, z int
}

type simulation struct {
	pos []xyz
	vel []xyz
}

func simulate(input []xyz) *simulation {
	length := len(input)
	pos := make([]xyz, length, length)
	copy(pos, input)
	return &simulation{
		pos: pos,
		vel: make([]xyz, length, length),
	}
}

func (s *simulation) applyGravity() {
	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			if i == j {
				continue
			}

			if s.pos[i].x < s.pos[j].x {
				s.vel[i].x++
				// s.vel[j].x--
			} else if s.pos[i].x > s.pos[j].x {
				s.vel[i].x--
				// s.vel[j].x++
			}

			if s.pos[i].y < s.pos[j].y {
				s.vel[i].y++
				// s.vel[j].y--
			} else if s.pos[i].y > s.pos[j].y {
				s.vel[i].y--
				// s.vel[j].y++
			}

			if s.pos[i].z < s.pos[j].z {
				s.vel[i].z++
				// s.vel[j].z--
			} else if s.pos[i].z > s.pos[j].z {
				s.vel[i].z--
				// s.vel[j].z++
			}
		}
	}
}

func (s *simulation) applyVelocity() {
	for i := 0; i < size; i++ {
		s.pos[i].x += s.vel[i].x
		s.pos[i].y += s.vel[i].y
		s.pos[i].z += s.vel[i].z
	}
}

func (s *simulation) step(steps int) {
	for i := 0; i < steps; i++ {
		s.applyGravity()
		s.applyVelocity()
	}
}

func (s *simulation) print() {
	for i := 0; i < size; i++ {
		fmt.Printf(
			"pos=<x=% 2d, y=% 2d, z=% 2d>, vel=<x=% 2d, y=% 2d, z=% 2d>\n",
			s.pos[i].x, s.pos[i].y, s.pos[i].z,
			s.vel[i].x, s.vel[i].y, s.vel[i].z,
		)
	}
}

func (s *simulation) totalEnergy() int {
	total := 0
	for i := 0; i < size; i++ {
		potential := abs(s.pos[i].x) + abs(s.pos[i].y) + abs(s.pos[i].z)
		kinetic := abs(s.vel[i].x) + abs(s.vel[i].y) + abs(s.vel[i].z)
		total += potential * kinetic
	}
	return total
}

func main() {
	input := []xyz{
		{x: -1, y: -4, z: 0},
		{x: 4, y: 7, z: -1},
		{x: -14, y: -10, z: 9},
		{x: 1, y: 2, z: 17},
	}

	fmt.Println("part1")
	part1(input)
	fmt.Println("---")

	fmt.Println("part2")
	part2(input)
	fmt.Println("---")
}

func fatalIf(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func part1(input []xyz) {
	s := simulate(input)
	s.step(1000)
	fmt.Println(s.totalEnergy())
}

func part2(input []xyz) {
	var (
		total int
		found int
		cycle xyz
	)

	s := simulate(input)

	for {
		s.applyGravity()
		s.applyVelocity()

		v0 := s.vel[0]
		v1 := s.vel[1]
		v2 := s.vel[2]
		v3 := s.vel[3]

		total++
		if found&0b001 == 0 && v0.x == 0 && v1.x == 0 && v2.x == 0 && v3.x == 0 {
			cycle.x = total
			found += 0b001
		}
		if found&0b010 == 0 && v0.y == 0 && v1.y == 0 && v2.y == 0 && v3.y == 0 {
			cycle.y = total
			found += 0b010
		}
		if found&0b100 == 0 && v0.z == 0 && v1.z == 0 && v2.z == 0 && v3.z == 0 {
			cycle.z = total
			found += 0b100
		}

		if found == 0b111 {
			break
		}
	}

	// like sin/cos functions, first period found is half-period
	cycle.x *= 2
	cycle.y *= 2
	cycle.z *= 2

	fmt.Println(lcm3(cycle.x, cycle.y, cycle.z))
}
