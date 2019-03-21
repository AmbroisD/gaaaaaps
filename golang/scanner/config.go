package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
)

//
// Config is main program configuration
//
type Config struct {
	SDSDir          string   `json:"sds_dir"`
	DataDir         string   `json:"data_dir"`
	AvailableYear   []string `json:"available_year"`
	StreamSelection []string `json:"stream_selection"`
}

//
// LoadConfig load scanner main configuration.
//
// configFile -- The configuration file
// verbose    -- verbose flag
//
func LoadConfig(configFile string, verbose bool) (config *Config, err error) {
	// Loading server directory
	if verbose {
		fmt.Printf("Loading main config file %s\n", configFile)
	}
	content, lerr := ioutil.ReadFile(configFile)
	if lerr != nil {
		err = lerr
		return
	}
	config = new(Config)
	err = json.Unmarshal(content, config)

	return
}
