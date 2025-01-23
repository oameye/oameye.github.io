# Computing the energy of a bosonic gas in an harmonic trap using automatic differentiation
using ForwardDiff: derivative
using CairoMakie, ProgressMeter
using BenchmarkTools

function z(β, d)
    return (exp(-0.5*β)/(1-exp(-β)))^d
end;

function Z(N, β, d)
    if N == 0
        return 1.0
    else
        return (1 / N) * sum(z(k * β, d) * Z(N - k, β, d) for k in 1:N)
    end
end;

function energy(N::Int64, β::Float64, d::Int64; type::Symbol = :boson)
    if type == :boson
        return -derivative(x -> log(Z(N, x, d)), β)
    else type == :boltzmannon
        return -derivative(x -> log(z(x, d)^N), β)
    end
end;



range2d = Iterators.product([1, 5, 10, 20], 1:0.1:10)
mat = @showprogress map(range2d) do (N, β)
    energy(N, β, 1)
end

fig = Figure()
ax = Axis(fig[1, 1], xscale = log10, yscale = log10)
for row in eachrow(mat)
    lines!(ax, row)
end

fig
