using HypergeometricFunctions: _₂F₁
using SpecialFunctions: gamma,SpecialFunctions
# https://journals.aps.org/pra/abstract/10.1103/PhysRevA.94.033841

gf(G, U) = G/U
cf(Δ, γ, U) = (Δ + im*γ/2)/U
function ℱ(m, Δ, G, U, γ)
    c = cf(Δ, γ, U)
    g = gf(G, U)
    return ℱ(m, c, g)
end
function ℱ(m, c, g)
    if isodd(m)
        return 0.0
    else
        n = m÷2
        cste = (-g)^n
        hgf = gamma(0.5+n)/gamma(0.5+n-c)
        return cste*hgf
    end
end
ℱ′(m, c, g) = abs2((im*√(complex(g)))^m)*abs2(_₂F₁(-m, -c, -2c, 2))
# ℱ(m, Δ) = ℱ(m, Δ+im*0.015, 1)
# ℱ(10, 0, 1, 1, 0.03)
function normalize_cte_old(Δ, G, U, γ; max_m = 100)
    f = m -> 2^m*abs2(ℱ(m, Δ, G, U, γ))/factorial(big(m))
    cte = sum(f.(0:max_m))
end

# normalize_cte(args...; kwargs...) = normalize_cte(big.(args)...; kwargs...)
function normalize_cte(Δ, G, U, γ; max=200)
    c = cf(Δ, γ, U)
    g = gf(G, U)

    n=0
    term = 1.0
    s = term*abs2(ℱ(n, Δ, G, U, γ))
    ε = eps(term) # error threshold to stop sum
    while true && n < max
        n +=1
        term *= abs2(-g)*2/(n*(2n-1))
        ff = gamma(big(0.5+n))
        fd = gamma(0.5+n-c)
        s += (δs = term*abs2(ff/fd))
        abs(δs) ≤ ε && break
    end
    return s
end
# function normalize_cte_new(Δ, G, U, γ)
#     c = cf(Δ, γ, U)
#     g = gf(G, U)

#     n=0
#     term = 1.0
#     s = term*abs2(ℱ(n, c, g))
#     ε = eps(term) # error threshold to stop sum
#     while true
#         n +=1
#         # isodd(n) && continue
#         term *= 2/n
#         s += (δs = term*abs2(ℱ(n, c, g)))
#         # @show n δs
#         0 < abs(δs) ≤ ε && break
#     end
#     return s
# end
# number_op(args...; kwargs...) = number_op(big.(args)...; kwargs...)
function number_op(Δ, G, U, γ; max = 200)
    c = cf(Δ, γ, U)
    g = gf(G, U)

    function ff(mm)
        if isodd(mm)
            return 0.0
        else
        nn = mm÷2
        # cste = gg(mm)
        hgf = gamma(0.5+nn)/gamma(0.5+nn-c)
        return hgf
        end
    end

    gg(mm) = isodd(mm) ? 1.0 : (-g)^(mm÷2)

    n=0
    term = abs2(im*√(complex(g)))
    s = term*abs2(ff(1))
    ε = eps(term) # error threshold to stop sum
    while true && n < max
        n +=1
        # isodd(n+1) && continue
        term *= 2*abs2(im*√(complex(g)))/n
        s += (δs = term*abs2(ff(n+1)))
        # @show n δs
        0 < abs(δs) ≤ ε && break
    end
    𝒩 = normalize_cte(Δ, G, U, γ; max)
    return s/𝒩
end
# g2(args...; kwargs...) = g2(big.(args)...; kwargs...)
function g2(Δ, G, U, γ; max = 200)
    𝒩 = normalize_cte(Δ, G, U, γ; max)
    aa = number_op(Δ, G, U, γ; max)

    c = cf(Δ, γ, U)
    g = gf(G, U)

    function ff(mm)
        if isodd(mm)
            return 0.0
        else
        nn = mm÷2
        # cste = gg(mm)
        hgf = gamma(0.5+nn)/gamma(0.5+nn-c)
        return hgf
        end
    end

    gg(mm) = isodd(mm) ? 1.0 : (-g)^(mm÷2)

    n=0
    term = abs2((im*√(complex(g)))^(n+2))
    s = term*abs2(ff(n+2))
    ε = eps(term) # error threshold to stop sum
    while true && n < max
        n +=1
        # isodd(n+1) && continue
        term *= 2*abs2(im*√(complex(g)))/n
        s += (δs = term*abs2(ff(n+2)))
        # @show n δs
        0 < abs(δs) ≤ ε && break
    end

    return (s/𝒩)/aa^2
end
function number_op_old(Δ, G, U, γ; max_m = 60)
    f = m -> 2^m*abs2(ℱ(m+1, Δ, G, U, γ))/factorial(big(m))
    𝒩 = normalize_cte_old(Δ, G, U, γ; max_m)
    cte = sum(f, 0:max_m)/𝒩
end

function wigner(z, Δ, G, U, γ; max_m = 60)
    f = m -> (2*conj(z))^m*ℱ(m, Δ, G, U, γ)/factorial(big(m))
    𝒩 = normalize_cte(Δ, G, U, γ)
    cte = sum(f.(0:max_m))
    2*abs2(cte)*exp(-2*abs2(z))/(π*𝒩)
end

Gₑ(ωₚ, F, K, Δ, ω₀) = (256 * F^2) * K * ω₀^3 / (ωₚ * (Δ^4 - 16 * Δ^2 * ωₚ^2))
Δₑ(ωₚ, F, K, Δ, ω₀) = (ωₚ^2 - ω₀^2) / (2ωₚ)-(512 * F^2) * K * ω₀^3 * (Δ^2 + 16 * ωₚ^2) / (ωₚ * (Δ^3 - 16 * Δ * ωₚ^2)^2)
