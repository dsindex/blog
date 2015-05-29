package main

import (
    "fmt"
    "math"
    "math/cmplx"
    "math/rand"
    "runtime"
    "time"
)

func add(x int, y int) int {
    return x + y
}

func swap(x, y string) (string, string) {
    return y, x
}

func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return
}

func variable_test() {
    fmt.Println("Welcome to the playground!")
    fmt.Println("The time is", time.Now())
    fmt.Println("My favorite number is", rand.Intn(10))
    fmt.Println("Now you have %g problems.", math.Nextafter(2, 4))
    fmt.Println(math.Pi)
    fmt.Println(add(42, 13))
    a, b := swap("hello", "world")
    fmt.Println(a, b)
    fmt.Println(split(17))

    //var c, python, java bool
    var i, j int = 1, 2
    var c, python, java = true, false, "no!"
    k := 3
    fmt.Println(i, j, k, c, python, java)

    var (
        ToBe   bool       = false
        MaxInt uint64     = 1<<64 - 1
        z      complex128 = cmplx.Sqrt(-5 + 12i)
    )
    const f = "%T(%v)\n"
    fmt.Printf(f, ToBe, ToBe)
    fmt.Printf(f, MaxInt, MaxInt)
    fmt.Printf(f, z, z)

    var m int
    var n float64
    var e bool
    var s string
    fmt.Printf("%v %v %v %q\n", m, n, e, s)
}

func needInt(x int) int {
    return x*10 + 1
}

func needFloat(x float64) float64 {
    return x * 0.1
}

func const_test() {
    var x, y int = 3, 4
    var f float64 = math.Sqrt(float64(x*x + y*y))
    var z int = int(f)
    fmt.Printf("%d %d %f %d\n", x, y, f, z)
    fmt.Printf("f is of type %T\n", f)

    const Pi = 3.14
    const World = "世界"
    fmt.Println("Hello", World)
    fmt.Println("Happy", Pi, "Day")
    const Truth = true
    fmt.Println("Go rules?", Truth)
    const (
        Big   = 1 << 100
        Small = Big >> 99
    )
    fmt.Println(needInt(Small))
    fmt.Println(needFloat(Small))
    fmt.Println(needFloat(Big))
}

func for_test() {
    sum := 0
    for i := 0; i < 10; i++ {
        sum += i
    }
    fmt.Println(sum)
}

func pow(x, n, lim float64) float64 {
    if v := math.Pow(x, n); v < lim {
        return v
    } else {
        fmt.Printf("%g >= %g\n", v, lim)
    }
    // can't use v here, though
    return lim
}

func if_test() {
    fmt.Println(
        pow(3, 2, 10),
        pow(3, 3, 20),
    )
}

func switch_test() {
    fmt.Print("Go runs on ")
    switch os := runtime.GOOS; os {
    case "darwin":
        fmt.Println("OS X.")
    case "linux":
        fmt.Println("Linux.")
    default:
        // freebsd, openbsd,
        // plan9, windows...
        fmt.Printf("%s.", os)
    }
    fmt.Println("When's Saturday?")
    today := time.Now().Weekday()
    fmt.Println("today is", today)
    fmt.Println("today + 2 is", today+2)
    if today == time.Saturday-2 {
        fmt.Println("Saturday - 2 is today")
    }
    switch time.Saturday {
    case today + 0:
        fmt.Println("Today.")
    case today + 1:
        fmt.Println("Tomorrow.")
    case today + 2:
        fmt.Println("In two days.")
    default:
        fmt.Println("Too far away.")
    }
    t := time.Now()
    switch {
    case t.Hour() < 12:
        fmt.Println("Good morning!")
    case t.Hour() < 17:
        fmt.Println("Good afternoon.")
    default:
        fmt.Println("Good evening.")
    }
}

func defer_test_1() {
    defer fmt.Println("world!") // 2
    fmt.Println("hello")        // 1
}

func defer_test_2() {
    defer_test_1()

    fmt.Println("counting")

    for i := 0; i < 10; i++ {
        defer fmt.Println(i) // reverse order
    }

    fmt.Println("done")
}

func pointer_test() {

    i, j := 42, 2701

    p := &i         // point to i
    fmt.Println(*p) // read i through the pointer
    *p = 21         // set i through the pointer
    fmt.Println(i)  // see the new value of i

    p = &j         // point to j
    *p = *p / 37   // divide j through the pointer
    fmt.Println(j) // see the new value of j
}

type Vertex struct {
    X int
    Y int
}

func struct_test() {
    //var v Vertex = Vertex{1, 2}
    v := Vertex{1, 2}
    p := &v
    fmt.Println(p)
    p.X = 1e9 // 1000000000
    fmt.Printf("%d %d\n", p.X, p.Y)
    fmt.Printf("%d %d\n", v.X, v.Y)

    var (
        v1 = Vertex{1, 2}  // has type Vertex
        v2 = Vertex{X: 1}  // Y:0 is implicit
        v3 = Vertex{}      // X:0 and Y:0
        q  = &Vertex{1, 2} // has type *Vertex
    )
    fmt.Println(v1, q, v2, v3)
}

func array_test() {
    var a [2]string // [n]T, static size of array
    a[0] = "Hello"
    a[1] = "World"
    fmt.Println(a[0], a[1])
    fmt.Println(a)

    var v = [3]int{1, 2, 3}
    fmt.Println(v)
}

func slice_test_1() {
    s := []int{2, 3, 5, 7, 11, 13} // initialize slice
    fmt.Println("s ==", s)

    for i := 0; i < len(s); i++ {
        fmt.Printf("s[%d] == %d\n", i, s[i])
    }

    w := []int{2, 3, 5, 7, 11, 13}
    fmt.Println("w ==", w)
    fmt.Println("w[1:4] ==", w[1:4]) // index 1 ~ index 4-1

    // missing low index implies 0
    fmt.Println("w[:3] ==", w[:3]) // index 0 ~ index 3-1

    // missing high index implies len(s)
    fmt.Println("w[4:] ==", w[4:]) // index 4 ~ end
}

func printSlice(s string, x []int) {
    fmt.Printf("%s len=%d cap=%d %v\n",
        s, len(x), cap(x), x)
}

func slice_test_2() {
    // slice is reference to an array
    // for example
    // var v = [3]int{1,2,3} is an array, its type is [3]int
    // var v = []int{1,2,3} is a slice
    a := make([]int, 5) // slice refers to int array, size 5, cap 5(==size), zero initialzed
    printSlice("a", a)
    b := make([]int, 0, 5) // slice refers to int array, size 0, cap 5
    printSlice("b", b)

    c := b[:2] // size = 2, cap 5 is copied <---- XXX why?
    printSlice("c", c)
    d := c[2:5] // size = 3, cap 3
    printSlice("d", d)

    var z []int
    fmt.Println(z, len(z), cap(z))
    if z == nil { // nill slice
        fmt.Println("nil!")
    }
}

