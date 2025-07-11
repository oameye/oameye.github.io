# ---
# title: Automatic differentiation of a recursive partition function
# summary: Computing the energy of a bosonic gas in an harmonic trap using automatic differentiation.
# menu:
#   sidebar:
#     name: Automatic differentiation
#     identifier: automatic_differentiation
#     # parent: reproduced_papers
#     weight: 10
# date: "2022-04-02T00:00:00Z"
# hero: preview.png
# tags:
# - Julia
# - Tutorial
# - Automatic Differentiation
# ---

#
# This tutorial demonstrates how to compute the energy of a bosonic gas
# in a harmonic trap using automatic differentiation.
#
using ForwardDiff: derivative
using CairoMakie, ProgressMeter
using BenchmarkTools

using Pkg; Pkg.status()

#
using InteractiveUtils
InteractiveUtils.versioninfo()

# In statistical mechanics, the partition function is a central quantity
# that encodes all thermodynamic information of a system. For a bosonic gas
# in a harmonic trap, we need to compute the energy by differentiating the
# logarithm of the partition function with respect to the inverse temperature $β$.
#
#
# The energy of a quantum system is given by:
# $$
# E = -\frac{\partial}{\partial \beta} \ln Z(\beta)
# $$
# where $Z(β)$ is the partition function and $β = 1/(k_B T)$ is the inverse temperature.
#

# ### Single-Particle Partition Function
# The single-particle partition function for a d-dimensional harmonic oscillator:
# $$
# z(\beta, d) = \left(\frac{e^{-\beta/2}}{1-e^{-\beta}}\right)^d
# $$
# This accounts for the zero-point energy $(1/2)ℏω$ and the geometric series
# from the discrete energy levels $n·ℏω$.

function z(β, d)
    return (exp(-0.5*β)/(1-exp(-β)))^d
end;

# ### Many-Body Partition Function
#
# For N indistinguishable bosons, the partition function is computed recursively.
# This accounts for the bosonic statistics where multiple particles can occupy
# the same quantum state. The recursive formula is:
# $$
# Z(N, \beta, d) = \frac{1}{N} \sum_{k=1}^{N} z(k\beta, d) \cdot Z(N-k, \beta, d)
# $$
# with the boundary condition $Z(0, β, d) = 1$.
#
# This recursion arises from the cluster expansion of the grand canonical
# partition function, accounting for all possible ways to distribute N particles
# among the available energy levels.

function Z(N, β, d)
    if N == 0
        return 1.0
    else
        return (1 / N) * sum(z(k * β, d) * Z(N - k, β, d) for k in 1:N)
    end
end;

# ### Energy Calculation via Automatic Differentiation
#
# The energy is computed as the negative logarithmic derivative of the partition function:
# $$
# E = -\frac{\partial}{\partial \beta} \ln Z(\beta)
# $$
#
# We implement two different approaches:
# 1. **Bosonic**: Uses the full many-body partition function Z(N, β, d)
# 2. **Boltzmann**: Uses the classical approximation z(β, d)^N (non-interacting)
#
# The automatic differentiation (via ForwardDiff) computes the derivative
# analytically without numerical approximation, making it both accurate and efficient.

function energy(N::Int64, β::Float64, d::Int64; type::Symbol = :boson)
    if type == :boson
        return -derivative(x -> log(Z(N, x, d)), β)
    else type == :boltzmannon
        return -derivative(x -> log(z(x, d)^N), β)
    end
end;

# ## Numerical Experiment
#
# We now compute the energy for different numbers of particles N and
# different inverse temperatures β. This allows us to study:
# - How the energy depends on temperature $(β = 1/T)$
# - How quantum statistics affect the energy for different particle numbers
# - The transition from quantum to classical behavior
#
# ### Parameter Space
# - N: Number of particles $[1, 5, 10, 20]$
# - β: Inverse temperature range $[1, 10]$ (corresponds to $T ∈ [0.1, 1]$)
# - d: Dimensionality = 1 (1D harmonic oscillator)

range2d = Iterators.product([1, 5, 10, 20], 1:0.1:10)
mat = @showprogress map(range2d) do (N, β)
    energy(N, β, 1)
end


#
# We plot the energy as a function of inverse temperature β for different
# particle numbers N. The log-log scale reveals the power-law behavior
# in different temperature regimes:
# - High temperature (small β): Classical behavior E ∝ T
# - Low temperature (large β): Quantum behavior dominated by zero-point energy
#
# Each curve represents a different particle number, showing how bosonic
# statistics modify the energy compared to the classical case.

fig = Figure(size = (400, 250), fontsize = 7)
ax = Axis(fig[1, 1],
          xscale = log10,
          yscale = log10,
          xlabel = "Inverse Temperature β",
          ylabel = "Energy E",
          title = "Energy of Bosonic Gas in Harmonic Trap")

for (i, N) in enumerate([1, 5, 10, 20])
    row = mat[i, :]
    lines!(ax, 1:0.1:10, row, label = "N = $N")
end
Legend(fig[1,2], ax)
fig

#
# The results show several important features:
# 1. **Zero-point energy**: Even at $T → 0 (β → ∞)$, the energy remains finite
#    due to quantum fluctuations
# 2. **Bosonic enhancement**: Higher particle numbers show deviations from
#    classical behavior due to quantum statistics
# 3. **Temperature scaling**: The energy follows different power laws in
#    different temperature regimes
#
# ## Advantages of Automatic Differentiation
#
# Using automatic differentiation provides several benefits:
# - **Exact derivatives**: No numerical approximation errors
# - **Efficiency**: Computes derivatives in single forward pass
# - **Simplicity**: No need to derive analytical expressions manually
# - **Robustness**: Works with complex recursive functions
#
