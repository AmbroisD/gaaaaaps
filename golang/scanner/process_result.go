package main

import (
	"fmt"
	"oca/sds/scanner"
	"path"
	"strings"
)

type consolidatedStatistics struct {
	TotalGap int     `json:"total_gap"`
	NbGap    int     `json:"nb_gap"`
	Percent  float64 `json:"percent"`
	Overlap  int     `json:"overlap"`
}

//
// ResultProcessor is used to save and consolidate result given by SDSScanner
//
type ResultProcessor struct {
	// The data year directory
	yearDir string
	// The mapping between filename and last processing time
	lastProcess map[string]float64
	// The consolidated processing informations
	// streamID -> "<year>.<jday>" -> <consolidated statistics>
	globalSds map[string]map[string]consolidatedStatistics
	// The full processing informations
	// streamID -> "<year>.<jday>" -> statistics
	fileStatistics map[string]map[string]*scanner.DayFileStatistics
}

//
// dumpToDisk dump all processed result to disk
//
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

//
// NewResultProcessor initialize a new resultProcessor
//
// yearDir     -- The year data directoty
// lastProcess -- The last processing time informations
// globalSds   -- The consolidated informations mapping
//
func NewResultProcessor(yearDir string, lastProcess map[string]float64,
	globalSds map[string]map[string]consolidatedStatistics) ResultProcessor {
	return ResultProcessor{yearDir: yearDir, lastProcess: lastProcess,
		globalSds:      globalSds,
		fileStatistics: make(map[string]map[string]*scanner.DayFileStatistics)}
}

//
// saveFullStatistics save full statistics for a given ScanResult
//
// result -- The result to save
//
func (rp *ResultProcessor) saveFullStatistics(result scanner.ScanResult) {
	splitFilename := strings.Split(result.Filename, ".")
	entry := strings.Join(splitFilename[0:4], ".")
	if _, ok := rp.fileStatistics[entry]; !ok {
		filePath := path.Join(rp.yearDir, entry+".json")
		var content map[string]*scanner.DayFileStatistics
		if loadJSON(filePath, content) != nil {
			rp.fileStatistics[entry] = make(map[string]*scanner.DayFileStatistics)
		} else {
			rp.fileStatistics[entry] = content
		}
	}
	rp.fileStatistics[entry][strings.Join(splitFilename[5:7], ".")] = result.Statistics
}

//
// updateConsolidatedStatistics update consolidated statistics according to given
// ScanResult
//
// result -- The result to consolidate
//
func (rp *ResultProcessor) updateConsolidatedStatistics(result scanner.ScanResult) {
	splitFilename := strings.Split(result.Filename, ".")
	streamEntry := strings.Join(splitFilename[0:4], ".")
	dayEntry := strings.Join(splitFilename[5:7], ".")
	globalStat := consolidatedStatistics{TotalGap: int(result.Statistics.Gap.Duration() / 1e9),
		NbGap:   result.Statistics.Gap.Len(),
		Percent: 100 * (86400 - float64(result.Statistics.Gap.Duration()/1e9)) / 86400}
	if _, ok := rp.globalSds[streamEntry]; !ok {
		rp.globalSds[streamEntry] = make(map[string]consolidatedStatistics)
	}
	rp.globalSds[streamEntry][dayEntry] = globalStat
}

//
// processResult process result read from given channel until
// this channel is closed
//
// When the channel is closed all processed result are stored on dick
// before returning
//
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
			rp.saveFullStatistics(currentScanResult)
			rp.updateConsolidatedStatistics(currentScanResult)
		}
	}
}
