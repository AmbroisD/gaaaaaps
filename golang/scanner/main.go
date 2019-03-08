package main

import (
	"flag"
	"fmt"
	"io"
	"oca/mseed"
	"os"
	"slinkgo"
	"strings"
	"time"
)

type lastComputationTime map[string]time.Time

type dayConsolidation struct {
	TotalGap float64 `json:"total_gap"`
	NbGap    int64   `json:"nb_gap"`
	Percent  float64 `json:"percent"`
	Overlap  int64   `json:"overlap"`
}

//
// ConsolidationFile define structure of sds_global.json
//
type ConsolidationFile map[string]map[string]dayConsolidation

func main() {

	// Command line management
	configFilepath := flag.String("c", "config.json", "MSeed input file")
	//debugFlag := flag.Bool("d", false, "Set debug flag")
	verboseFlag := flag.Bool("v", false, "Set verbose flag")
	flag.Parse()

	config = LoadConfig(configFilepath, *verboseFlag)
}
