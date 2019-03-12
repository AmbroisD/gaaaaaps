package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"oca/sds"
	"oca/sds/scanner"
	"os"
	"path"
	"runtime/pprof"
	"strconv"
)

// Associate each filename with last process time
//lastProcess map[string]float64
// streamId -> <Y.JD> -> statistics
//streamStats map[string]map[string]DayFileStatistics

func isDirectory(path string) (e error) {
	var s os.FileInfo
	if s, e = os.Stat(path); os.IsNotExist(e) {
		return
	}
	if s.IsDir() {
		return
	}
	e = fmt.Errorf("%s is not a directory", path)
	return
}

func initData(dataDir string, year int) (lastProcess map[string]float64,
	globalSds map[string]map[string]consolidatedStatistics, err error) {
	var e error

	// Create year directory if need
	yearDir := path.Join(dataDir, fmt.Sprintf("%d", year))
	if _, e = os.Stat(yearDir); os.IsNotExist(e) {
		err = os.Mkdir(yearDir, 0755)
		if err != nil {
			return
		}
	}

	// Create year global result directory if need
	globalDir := path.Join(yearDir, "global_json")
	if _, e = os.Stat(globalDir); os.IsNotExist(e) {
		err = os.Mkdir(globalDir, 0755)
		if err != nil {
			return
		}
	}

	// Create last processing time file if need
	lastProcessFilepath := path.Join(globalDir, "dict_m_date.json")
	if _, e = os.Stat(lastProcessFilepath); os.IsNotExist(e) {
		lastProcess = make(map[string]float64)
		err = dumpJSON(lastProcess, lastProcessFilepath)
		if err != nil {
			return
		}
	} else {
		loadJSON(lastProcessFilepath, &lastProcess)
	}

	// Create consolidation file if need
	globalSdsFilepath := path.Join(globalDir, "sds_global.json")
	if _, e = os.Stat(globalSdsFilepath); os.IsNotExist(e) {
		globalSds = make(map[string]map[string]consolidatedStatistics)
		err = dumpJSON(globalSds, globalSdsFilepath)
		if err != nil {
			return
		}
	} else {
		loadJSON(globalSdsFilepath, &globalSds)
	}

	return
}

func loadJSON(filepath string, result interface{}) error {
	content, err := os.Open(filepath)
	if err != nil {
		return err
	}
	jsonParser := json.NewDecoder(content)
	err = jsonParser.Decode(result)
	if err != nil {
		return err
	}
	return nil
}

func dumpJSON(data interface{}, filepath string) error {
	// Writing channelDataInfo map in a state file
	dataJSON, _ := json.Marshal(data)
	err := ioutil.WriteFile(filepath, dataJSON, 0644)
	if err != nil {
		return fmt.Errorf("Error writing %s: %s", filepath, err.Error())
	}
	return nil
}

func main() {
	var err error
	var config *Config
	// Command line management
	configFilepath := flag.String("c", "config.json", "MSeed input file")
	nbWorkers := flag.Int("w", 1, "Set number of workers used to scan SDS")
	//debugFlag := flag.Bool("d", false, "Set debug flag")
	minimalGap := flag.Float64("g", 3/2, "Set the minimal gap size if term of inter sample duration")
	cpuprofile := flag.String("cpuprofile", "", "write cpu profile to `file`")
	verboseFlag := flag.Bool("v", false, "Set verbose flag")
	flag.Parse()

	if *cpuprofile != "" {
		f, perr := os.Create(*cpuprofile)
		if perr != nil {
			fmt.Printf("could not create CPU profile: %s\n", err.Error())
		}
		defer f.Close()
		if perr = pprof.StartCPUProfile(f); perr != nil {
			fmt.Printf("could not start CPU profile: %s\n", err.Error())
		}
		defer pprof.StopCPUProfile()
	}

	config, err = LoadConfig(*configFilepath, *verboseFlag)
	if err != nil {
		fmt.Printf("Can't load configuration: %s", err.Error())
		os.Exit(1)
	}
	if err = isDirectory(config.SDSDir); err != nil {
		fmt.Printf("Error: %s", err.Error())
		os.Exit(1)
	}

	if err = isDirectory(config.DataDir); err != nil {
		fmt.Printf("Error: %s", err.Error())
		os.Exit(1)
	}

	sdsManager, err := sds.NewManager(config.SDSDir)
	if err != nil {
		fmt.Printf("Can't initialize SDS manager: %s", err.Error())
		os.Exit(1)
	}
	if *verboseFlag {
		fmt.Printf("Creating SDS scanner\n")
	}
	sdsScanner := scanner.NewSDSScanner(*sdsManager, *nbWorkers, *minimalGap,
		*verboseFlag)
	var processedYear []int
	for _, current := range config.AvailableYear {
		intYear, err := strconv.Atoi(current)
		if err != nil {
			fmt.Printf("Can't convert %s to int: %s", current, err.Error())
			os.Exit(1)
		}
		processedYear = append(processedYear, intYear)
	}
	for _, currentYear := range processedYear {
		if *verboseFlag {
			fmt.Printf("Initialize directory structure for %d\n", currentYear)
		}
		lastComputationTime, globalSds, erri := initData(config.DataDir, currentYear)
		if erri != nil {
			fmt.Printf("Error initializing directory structure for yesr %d: %s\n", currentYear, erri.Error())
			continue
		}
		// Copy lastComputationTime for scanner
		lastComputationTimeCopy := make(map[string]float64)
		for k, v := range lastComputationTime {
			lastComputationTimeCopy[k] = v
		}
		result, err := sdsScanner.ScanOneYear(currentYear, config.StreamSelection, lastComputationTimeCopy)
		if err != nil {
			fmt.Printf("Error during scan of year %d: %s\n", currentYear, err.Error())
		}
		yearDir := path.Join(config.DataDir, fmt.Sprintf("%d", currentYear))
		resultProcessor := NewResultProcessor(yearDir, lastComputationTime, globalSds)
		resultProcessor.processResult(result)
	}
}
