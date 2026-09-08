#!/usr/bin/env julia

using LitPro

function usage(io::IO=stdout)
    println(io, "Usage: julia --project=julia julia/LitPro.jl <run|export|html> <file> [-o output]")
end

function main(args=ARGS)
    if length(args) < 2
        usage(stderr)
        return 2
    end

    command = args[1]
    file = args[2]
    output = nothing

    i = 3
    while i <= length(args)
        if args[i] == "-o" || args[i] == "--output"
            i == length(args) && error("missing value after $(args[i])")
            output = args[i + 1]
            i += 2
        else
            error("unknown argument: $(args[i])")
        end
    end

    if command == "run"
        run_litpro(file)
    elseif command == "export"
        export_litpro(file, output === nothing ? replace(file, r"\.lit$" => ".jl") : output)
    elseif command == "html"
        html_litpro(file, output === nothing ? replace(file, r"\.lit$" => ".html") : output)
    else
        usage(stderr)
        error("unknown command: $command")
    end

    return 0
end

if abspath(PROGRAM_FILE) == @__FILE__
    exit(main())
end
