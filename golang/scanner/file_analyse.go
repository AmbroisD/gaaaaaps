package main

import (
	"encoding/hex"
	"fmt"
	"io"
	"oca/mseed"
	"oca/timeperiod"
	"os"
	"slinkgo"
	"time"
)

//
// DayFileStatistics store all data metrics for one stream file
//
type DayFileStatistics struct {
	Tomorrow      *timeperiod.DiscontinuousTimePeriod
	Yesterday     *timeperiod.DiscontinuousTimePeriod
	DataMetrics   *slinkgo.DataMetric
	Gap           *timeperiod.DiscontinuousTimePeriod
	Overlap       *timeperiod.DiscontinuousTimePeriod
	GeneratedTime time.Time
}

//
// FileAnalyser is used to produce statistics on mseed file.
//
type FileAnalyser struct {
	minimalGap float64
}

func (fa *FileAnalyser) updateGap(mseedPacket *mseed.Packet) {

	if streamGap == nil {
		var minDuration time.Duration

		// Compute minimal gap size (1.5 * <sample duration>)
		if mseedPacket.SampleRate() >= 1 {
			minDuration = time.Duration(time.Second / time.Duration(mseedPacket.SampleRate()))
		} else {
			minDuration = time.Duration(1.0/mseedPacket.SampleRate()) * time.Second
		}
		minDuration = minDuration * time.Duration(fa.minimalGap)

		// Init gap and overlap
		midnight := time.Date(*processedYear, 1, 1, 0, 0, 0, 0, time.UTC).Add(time.Hour*time.Duration(24)*time.Duration(*processedDay-1) - 1)
		if midnight.Year() != *processedYear {
			fmt.Printf("processingDay value is 366 and %d is not a leap year\n", *processedYear)
			os.Exit(1)
		}
		streamGap = timeperiod.New(minDuration)
		streamOverlap = timeperiod.New(minDuration)
		initialGap := timeperiod.TimePeriod{StartTime: midnight.Add(-time.Minute).UTC(),
			EndTime: midnight.Add(time.Hour*24 + time.Minute).UTC()}

		streamGap = streamGap.Add(&initialGap)
	}

	// Add day gap if need
	endGapTime, _ := streamGap.End()
	if mseedPacket.CorrectedEndTime().After(endGapTime) {
		fmt.Printf("Warning packet end time don't belong to same day\n")
	}

	//
	// Update gaps and overlaps
	//
	packetPeriod := timeperiod.TimePeriod{StartTime: mseedPacket.CorrectedStartTime(),
		EndTime: mseedPacket.CorrectedEndTime()}
	if packetPeriod.EndTime.Before(packetPeriod.StartTime) {
		fmt.Printf("Bug: Computed end packed time before start packet time (%v-%v)\n",
			packetPeriod.StartTime, packetPeriod.EndTime)
		fmt.Printf("Packet header: %s\n", hex.EncodeToString(mseedPacket.Header()))
		return
	}
	newGapList, residual := streamGap.Sub(&packetPeriod)
	streamGap = newGapList
	streamOverlap = streamOverlap.Merge(residual)
}

func updateData(packet *mseed.Packet) (err error) {

	// Create dataProcessor if need
	if dataProcessor == nil {
		nbSample := packet.SampleRate() * 86520
		dataProcessor = slinkgo.NewDataMetricProcessor(int(nbSample * 2))
	}

	// Add new sample and update statistics if need
	if _, uerr := dataProcessor.Update(packet); uerr != nil {
		err = fmt.Errorf("Error dataProcessor buffer is too short (%v)\n", packet.SampleRate()*86400*2)
		return
	}
	return nil
}

func processPacket(packet *mseed.Packet) error {
	updateGap(packet)
	err := updateData(packet)
	return err
}

func createResult() (result DayFileStatistics) {
	dataProcessor.ForceComputation()
	metric = dataProcessor.Last()
	return DayFileStatistics{
		DataMetrics:   metric,
		Gap:           streamGap,
		Overlap:       streamOverlap,
		GeneratedTime: time.Now().UTC()}
}

var dataProcessor *slinkgo.DataMetricProcessor
var streamGap *timeperiod.DiscontinuousTimePeriod
var streamOverlap *timeperiod.DiscontinuousTimePeriod

func processOneFile(filepath string) (result DayFileStatistics, err error) {
	dataProcessor = nil
	streamGap = nil
	streamOverlap = nil

	// Open mseed file
	mseedReader, nerr := mseed.NewReader(filepath)
	if nerr != nil {
		err = fmt.Errorf("Error opening %s: %s\n", filepath, nerr.Error())
		return
	}

	// Read all mseed packet present in file
	for {
		nextPacket, rerr := mseedReader.Next()
		if nextPacket == nil {
			if rerr == io.EOF {
				result = createResult()
				return
			}
			err = fmt.Errorf("Error during read: %s\n", rerr.Error())
			return
		}
		if perr := processPacket(nextPacket); perr != nil {
			err = fmt.Errorf("Error during packet processing: %s\n", perr.Error())
			return
		}
	}
}
