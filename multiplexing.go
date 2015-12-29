package main

import (
    "bufio"
    "fmt"
    "os"
    "runtime"
    "sync"
    "time"
)

func worker(jobs chan string, outs chan string, jobs_wg *sync.WaitGroup, jobs_shutdown chan bool) {
    // jobs -> outs
    defer jobs_wg.Done()
    for {
        select {
        case line, _ := <-jobs:
            out := "do something here"
            outs <- out
        case _ = <-jobs_shutdown:
            fmt.Fprintf(os.Stderr, "shutdown worker\n")
            return
        }
    }
}

func outputer(outs chan string, outs_wg *sync.WaitGroup, outs_shutdown chan bool) {
    // outs -> stdout
    // synchronize standard out
    defer outs_wg.Done()
    for {
        select {
        case _ = <-outs_shutdown:
            fmt.Fprintf(os.Stderr, "shutdown outputer\n")
            return
        case out := <-outs:
            fmt.Printf("out = %s\n", out)
        }
    }
}

func prepare_workers(n_worker int, jobs chan string, outs chan string, jobs_wg_list *[]*sync.WaitGroup, jobs_shutdown_list *[]chan bool) {
    for i := 0; i < n_worker; i++ {
        jobs_wg := &sync.WaitGroup{}
        jobs_wg.Add(1)
        *jobs_wg_list = append(*jobs_wg_list, jobs_wg)
        jobs_shutdown := make(chan bool)
        *jobs_shutdown_list = append(*jobs_shutdown_list, jobs_shutdown)
        go worker(jobs, outs, jobs_wg, jobs_shutdown)
    }
}

func prepare_outputer(outs chan string, outs_wg *sync.WaitGroup, outs_shutdown chan bool) {
    go outputer(outs, outs_wg, outs_shutdown)
}

func main() {
    const n_worker = 10
    const n_core = 10
    const size_buff = 100

    runtime.GOMAXPROCS(n_core)

    var jobs = make(chan string, size_buff)
    var outs = make(chan string, size_buff)
    var jobs_wg_list []*sync.WaitGroup
    var jobs_shutdown_list []chan bool
    outs_wg := &sync.WaitGroup{}
    outs_wg.Add(1)
    outs_shutdown := make(chan bool)

    // prepare workers, outputer
    prepare_workers(n_worker, jobs, outs, &jobs_wg_list, &jobs_shutdown_list)
    prepare_outputer(outs, outs_wg, outs_shutdown)

    start := time.Now() // get current time
    scanner := bufio.NewScanner(os.Stdin)
    for scanner.Scan() {
        line := scanner.Text()
        jobs <- line
    }
    
    // shutdown all workers
    fmt.Fprintf(os.Stderr, "jobs_shutdown_list size : %v\n", len(jobs_shutdown_list))
    fmt.Fprintf(os.Stderr, "jobs_wg_list size : %v\n", len(jobs_wg_list))
    for i, jobs_shutdown := range jobs_shutdown_list {
        fmt.Fprintf(os.Stderr, "close jobs_shutdown : %v\n", i)
        close(jobs_shutdown)
        // wait until finish job
        fmt.Fprintf(os.Stderr, "wait jobs_wg : %v\n", i)
        jobs_wg := jobs_wg_list[i]
        jobs_wg.Wait()
        fmt.Fprintf(os.Stderr, "done jobs_wg\n")
    }

    // shutdown outputer
    fmt.Fprintf(os.Stderr, "close outs_shutdown\n")
    close(outs_shutdown)
    // wait until outputer ends
    fmt.Fprintf(os.Stderr, "wait outs_wg\n")
    outs_wg.Wait()
    fmt.Fprintf(os.Stderr, "done outs_wg\n")

    elapsed := time.Since(start)
    fmt.Fprintf(os.Stderr, "elapsed time = %s\n", elapsed)
}
