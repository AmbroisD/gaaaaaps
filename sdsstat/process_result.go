package main

import (
	"fmt"
	"path"
	"strings"

	"kleos.unice.fr/peix/gsds/oca/sds/scanner"
)

type consolidatedStatistics struct {
	TotalGap int     `json:"total_gap"`
	NbGap    int     `json:"nb_gap"`
	Percent  float64 `json:"percent"`
	Overlap  int     `json:"overlap"`
}

type ResultProcessor struct {
	yearDir        string
	lastProcess    map[string]float64
	globalSds      map[string]map[string]consolidatedStatistics
	fileStatistics map[string]map[string]*scanner.DayFileStatistics
}

func (rp *ResultProcessor) dumpToDisk() {
	lastProcessFilepath := path.Join(rp.yearDir, "global_json", "dict_m_date.json")
	err := dumpJSON(rp.lastProcess, lastProcessFilepath)
	if err != nil {
		fmt.Printf("Error during dumping of %s\n", lastProcessFilepath)
	}
	globalSdsFilepath := path.Join(rp.yearDir, "global_json", "sds_global.json")
	err = dumpJSON(rp.globalSds, globalSdsFilepath)
	if err != nil {
		fmt.Printf("Error during dumping of %s\n", globalSdsFilepath)
	}
	for key, value := range rp.fileStatistics {
		currentFilepath := path.Join(rp.yearDir, key+".json")
		err = dumpJSON(value, currentFilepath)
		if err != nil {
			fmt.Printf("Error during dumping of %s\n", currentFilepath)
		}
	}
}

// NewResultProcessor initialize a new resultProcessor
func NewResultProcessor(yearDir string, lastProcess map[string]float64,
	globalSds map[string]map[string]consolidatedStatistics) ResultProcessor {
	return ResultProcessor{yearDir: yearDir, lastProcess: lastProcess,
		globalSds:      globalSds,
		fileStatistics: make(map[string]map[string]*scanner.DayFileStatistics)}
}

func (rp *ResultProcessor) saveFileStatistic(result scanner.ScanResult) {
	splitFilename := strings.Split(result.Filename, ".")
	entry := strings.Join(splitFilename[0:4], ".")
	if _, ok := rp.fileStatistics[entry]; !ok {
		filePath := path.Join(rp.yearDir, entry+".json")
		content := make(map[string]*scanner.DayFileStatistics)
		loadJSON(filePath, content)
		rp.fileStatistics[entry] = content
	}
	rp.fileStatistics[entry][strings.Join(splitFilename[6:7], ".")] = result.Statistics
}

func (rp *ResultProcessor) updateGlobalStatistic(result scanner.ScanResult) {
	splitFilename := strings.Split(result.Filename, ".")
	streamEntry := strings.Join(splitFilename[0:4], ".")
	dayEntry := strings.Join(splitFilename[5:6], ".")
	globalStat := consolidatedStatistics{TotalGap: int(result.Statistics.Gap.Duration() / 1e9),
		NbGap:   result.Statistics.Gap.Len(),
		Percent: float64(result.Statistics.Gap.Duration()) / 86400}
	if _, ok := rp.globalSds[streamEntry]; !ok {
		rp.globalSds[streamEntry] = make(map[string]consolidatedStatistics)
	}
	rp.globalSds[streamEntry][dayEntry] = globalStat
}

func (rp *ResultProcessor) processResult(result chan scanner.ScanResult) {
	for {
		select {
		case currentScanResult, ok := <-result:
			if !ok {
				// Save result
				rp.dumpToDisk()
				return
			}
			rp.lastProcess[currentScanResult.Filename] = float64(currentScanResult.Statistics.GeneratedTime.UnixNano()) / 1e9
			rp.saveFileStatistic(currentScanResult)
			rp.updateGlobalStatistic(currentScanResult)
		}
	}
}
