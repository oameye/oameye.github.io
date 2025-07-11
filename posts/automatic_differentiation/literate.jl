using DrWatson
@quickactivate "BosonicGas"
projectdir()

using Literate

extra_literate_config = Dict()
function preprocess(content)
    sub = SubstitutionString("""
                             """)
    content = replace(content, r"^# # [^\n]*"m => sub; count=1)

    # remove VSCode `##` block delimiter lines
    content = replace(content, r"^##$."ms => "")
    return content
end
input = joinpath(projectdir(), "index.jl")
Literate.markdown(
    input,
    projectdir();
    flavor=Literate.CommonMarkFlavor(),
    config=extra_literate_config,
    execute=true
    # preprocess=preprocess,
)
