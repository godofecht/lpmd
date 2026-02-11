#!/usr/bin/env julia

using ArgParse

function parse_commandline()
    s = ArgParseSettings(prog="litpro", description="LitPro - Literate Programming Framework for Julia")

    @add_arg_table s begin
        "command"
            help = "Command to execute (run, export, html)"
            arg_type = String
            required = true
        "file"
            help = "Path to the literate programming file (.lit)"
            arg_type = String
            required = true
        "--output", "-o"
            help = "Output file path (for export/html commands)"
            arg_type = String
    end

    return parse_args(s)
end

# Include the LitPro module
include("LitPro.jl")
using .LitPro

function main()
    parsed_args = parse_commandline()
    
    command = parsed_args["command"]
    file = parsed_args["file"]
    output = parsed_args["output"]
    
    if command == "run"
        run_litpro(file)
    elseif command == "export"
        output_file = output !== nothing ? output : replace(file, ".lit" => ".jl")
        export_litpro(file, output_file)
    elseif command == "html"
        output_file = output !== nothing ? output : replace(file, ".lit" => ".html")
        html_litpro(file, output_file)
    else
        println("Unknown command: \$command")
        println("Available commands: run, export, html")
    end
end

main()