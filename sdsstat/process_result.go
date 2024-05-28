package main

import (
	"fmt"
	"os"
	"os/signal"
	"path"
	"strconv"
	"strings"
	"syscall"
	"time"

	"kleos.unice.fr/peix/gsds/oca/sds/scanner"
)

type consolidatedStatistics struct {
	TotalGap int     `json:"total_gap"`
	NbGap    int     `json:"nb_gap"`
	Percent  float64 `json:"percent"`
	Overlap  int     `json:"overlap"`
}

func yesterday(julian_day string) string {
	splitDay := strings.Split(julian_day, ".")
	year, _ := strconv.Atoi(splitDay[0])
	day, _ := strconv.Atoi(splitDay[1])
	yesterdayTime := time.Date(year, 1, 1, 0, 0, 0, 0, time.UTC).Add(time.Duration(day-2) * time.Hour * 24)
	return fmt.Sprintf("%d.%d", yesterdayTime.Year(), yesterdayTime.YearDay())
}

func tomorrow(julian_day string) string {
	splitDay := strings.Split(julian_day, ".")
	year, _ := strconv.Atoi(splitDay[0])
	day, _ := strconv.Atoi(splitDay[1])
	yesterdayTime := time.Date(year, 1, 1, 0, 0, 0, 0, time.UTC).Add(time.Duration(day) * time.Hour * 24)
	return fmt.Sprintf("%d.%d", yesterdayTime.Year(), yesterdayTime.YearDay())
}

// ResultProcessor is used to save and consolidate result given by SDSScanner
type ResultProcessor struct {
	// The mapping between filename and last processing time
	lastProcess map[string]float64
	// The consolidated processing informations
	// streamID -> "<year>.<jday>" -> <consolidated statistics>
	globalSds map[string]map[string]consolidatedStatistics
	// The full processing informations
	// streamID -> "<year>.<jday>" -> statistics
	fileStatistics map[string]map[string]*scanner.DayFileStatistics
	// The data year directory
	yearDir string
}

// dumpToDisk dump all processed result to disk
func (rp *ResultProcessor) dumpToDisk() {
	lastProcessFilepath := path.Join(rp.yearDir, "global_json", "dict_m_date.json")
	err := dumpJSON(rp.lastProcess, lastProcessFilepath)
	if err != nil {
		fmt.Printf("Error during dumping of %s\n", lastProcessFilepath)
	}
	rp.fixStatistics()
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
//
// yearDir     -- The year data directoty
// lastProcess -- The last processing time informations
// globalSds   -- The consolidated informations mapping
func NewResultProcessor(yearDir string, lastProcess map[string]float64,
	globalSds map[string]map[string]consolidatedStatistics) ResultProcessor {
	return ResultProcessor{yearDir: yearDir, lastProcess: lastProcess,
		globalSds:      globalSds,
		fileStatistics: make(map[string]map[string]*scanner.DayFileStatistics)}
}

// saveFullStatistics save full statistics for a given ScanResult
//
// result -- The result to save
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

// fixStatistics Update Gaps according to data present in previous and next day.
// This method also recomopute consolidated statistics
func (rp *ResultProcessor) fixStatistics() {
	for streamID, statMap := range rp.fileStatistics {
		for day, dayStat := range statMap {
			// Update gap with yesterday data
			yesterday := yesterday(day)
			if yesterdayStat, ok := statMap[yesterday]; ok {
				for _, current := range yesterdayStat.Tomorrow.PeriodList {
					dayStat.Gap, _ = dayStat.Gap.Sub(current)
				}
				// Update gap with tomorrow data
				tomorrow := tomorrow(day)
				if tomorrowStat, ok := statMap[tomorrow]; ok {
					for _, current := range tomorrowStat.Yesterday.PeriodList {
						dayStat.Gap, _ = dayStat.Gap.Sub(current)
					}
				}
			}
			rp.setConsolidatedStatistics(streamID, day, dayStat)
		}
	}
}

// setConsolidatedStatistics set consolidated statistics of a given stream day statistics
func (rp *ResultProcessor) setConsolidatedStatistics(streamID, day string, dayStat *scanner.DayFileStatistics) {
	globalStat := consolidatedStatistics{TotalGap: int(dayStat.Gap.Duration() / 1e9),
		NbGap:   dayStat.Gap.Len(),
		Percent: 100 * (86400 - float64(dayStat.Gap.Duration()/1e9)) / 86400}
	if _, ok := rp.globalSds[streamID]; !ok {
		rp.globalSds[streamID] = make(map[string]consolidatedStatistics)
	}
	rp.globalSds[streamID][day] = globalStat

}

// processResult update full day statistics read from given channel
func (rp *ResultProcessor) processResult(result chan scanner.ScanResult) (mustStop bool) {
	signalChannel := make(chan os.Signal, 2)
	defer close(signalChannel)
	signal.Notify(signalChannel, syscall.SIGINT)
Loop:
	for {
		select {
		case currentScanResult, ok := <-result:
			if !ok {
				break Loop
			}
			rp.lastProcess[currentScanResult.Filename] = float64(currentScanResult.Statistics.GeneratedTime.UnixNano()) / 1e9
			rp.saveFullStatistics(currentScanResult)
		case <-signalChannel:
			mustStop = true
			break Loop
		}
	}
	rp.dumpToDisk()
	return
}
