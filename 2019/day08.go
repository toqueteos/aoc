package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"
)

const (
	width     = 25
	height    = 6
	layerSize = width * height

	black       = 0
	white       = 1
	transparent = 2
)

func main() {
	contents, err := ioutil.ReadFile("input08.txt")
	fatalIf(err)

	image := strings.TrimSpace(string(contents))

	fmt.Println(part1(image))
	fmt.Println(part2(image))
}

func part1(image string) int {
	type layer struct {
		zeros int
		crc   int
	}

	var layers []layer

	for i := 0; i < (len(image) / layerSize); i++ {
		hist := make(map[rune]int, layerSize)

		for _, pixel := range image[i*layerSize:][:layerSize] {
			hist[pixel]++
		}

		// fmt.Println(hist)

		layers = append(layers, layer{zeros: hist['0'], crc: hist['1'] * hist['2']})
	}

	sort.Slice(layers, func(i, j int) bool { return layers[i].zeros < layers[j].zeros })
	// fmt.Println(layers)

	return layers[0].crc
}

func part2(image string) string {
	var message [layerSize]int

	for i, pixel := range image[:layerSize] {
		message[i] = int(pixel) - 48
	}

	for j := 1; j < (len(image) / layerSize); j++ {
		offset := j * layerSize
		for i, pixel := range image[offset:][:layerSize] {
			value := int(pixel) - 48

			if message[i] == transparent && value != transparent {
				message[i] = int(pixel) - 48
			}
		}
	}

	var sb strings.Builder
	r := strings.NewReplacer("[", "", "]", "", "0", " ", "1", "@")
	for i := 0; i < height; i++ {
		line := fmt.Sprint(message[i*width:][:width])
		// fmt.Println(line)
		sb.WriteString(r.Replace(line))
		sb.WriteString("\n")
	}

	return sb.String()
}

func fatalIf(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, "err")
		os.Exit(1)
	}
}
