# ---
# title: Quantum Fisher Information with automatic differentiation
# summary: Computation of Quantum Fisher Information for a driven-dissipative Kerr Parametric Oscillator using automatic differentiation.
# menu:
#   sidebar:
#     name: Quantum Fisher Information
#     identifier: quantum_fisher_information
#     # parent: reproduced_papers
#     weight: 10
# date: "2025-7-13T00:00:00Z"
# hero: preview.svg
# tags:
# - Julia
# - Tutorial
# - Automatic Differentiation
# ---

# This notebook demonstrates the computation of Quantum Fisher Information (QFI) for a driven-dissipative Kerr Parametric Oscillator (KPO) using automatic differentiation. The QFI quantifies the ultimate precision limit for parameter estimation in quantum systems.

# We import the necessary packages for quantum simulations and automatic differentiation:


using QuantumToolbox      # Quantum optics simulations
using DifferentiationInterface  # Unified automatic differentiation interface
using SciMLSensitivity   # Allows for ODE sensitivity analysis
using FiniteDiff         # Finite difference methods
using LinearAlgebra      # Linear algebra operations
using CairoMakie              # Plotting
CairoMakie.activate!(type = "svg")


# ## System Parameters and Hamiltonian

# The KPO system is governed by the Hamiltonian:
# $$H = -p_1 a^\dagger a + K (a^\dagger)^2 a^2 - G (a^\dagger a^\dagger + a a)$$

# where:

# - $p_1$ is the parameter we want to estimate (detuning)
# - $K$ is the Kerr nonlinearity
# - $G$ is the parametric drive strength
# - $\gamma$ is the decay rate

function final_state(p, t)
    G, K, γ = 0.002, 0.001, 0.01

    N = 20 # cutoff of the Hilbert space dimension
    a = destroy(N) # annihilation operator

    coef(p,t) = - p[1]
    H = QobjEvo(a' * a , coef) + K * a' * a' * a * a - G * (a' * a' + a * a)
    c_ops = [sqrt(γ)*a]
    ψ0 = fock(N, 0) # initial state

    tlist = range(0, 2000, 100)
    sol = mesolve(H, ψ0, tlist, c_ops; params = p, progress_bar = Val(false), saveat = [t])
    return sol.states[end].data
end


# ## Quantum Fisher Information Calculation

# The QFI is computed using the symmetric logarithmic derivative (SLD). For a density matrix $\rho(\theta)$ parametrized by $\theta$:

# $$F_Q = \text{Tr}[\partial_\theta \rho \cdot L]$$

# where $L$ is the SLD satisfying: $\partial_\theta \rho = \frac{1}{2}(\rho L + L \rho)$

function compute_fisher_information(ρ, dρ)
    reg = 1e-12 * I # Add small regularization to avoid numerical issues with zero eigenvalues
    ρ_reg = ρ + reg

    L = sylvester(ρ_reg, ρ_reg, -2*dρ) # This is a Sylvester equation: ρL + Lρ = 2*dρ
    F = real(tr(dρ * L)) # Fisher information F = Tr(dρ * L)
    return F
end

# ## Automatic Differentiation Setup

# We use finite differences through DifferentiationInterface.jl to compute the derivative of the quantum state with respect to the parameter. This is a key step that enables efficient QFI computation without manual derivative calculations.


final_state([0], 100) # Test the system

state(p) = final_state(p, 2000) # Define state function for automatic differentiation

ρ, dρ = DifferentiationInterface.value_and_jacobian(state, AutoFiniteDiff(), [0.0])

dρ = QuantumToolbox.vec2mat(vec(dρ)) # Reshape the derivative back to matrix form

qfi_final = compute_fisher_information(ρ, dρ) # Compute QFI at final time
println("QFI at final time: ", qfi_final)


# ## Time Evolution of Quantum Fisher Information

# Now we compute how the QFI evolves over time to understand the optimal measurement time for parameter estimation:

ts = range(0, 2000, 100)

QFI_t = map(ts) do t
    state(p) = final_state(p, t)
    ρ, dρ = DifferentiationInterface.value_and_jacobian(state, AutoFiniteDiff(), [0.0])
    dρ = QuantumToolbox.vec2mat(vec(dρ))
    compute_fisher_information(ρ, dρ)
end

println("QFI computed for ", length(ts), " time points")

# ## Visualization

# Plot the time evolution of the Quantum Fisher Information:

fig = Figure()
ax = Axis(
 fig[1,1],
 xlabel = "Time",
 ylabel = "Quantum Fisher Information"
)
lines!(ax, ts, QFI_t)
fig

# ## Version Information

using InteractiveUtils
InteractiveUtils.versioninfo()

#

using Pkg
Pkg.status()
