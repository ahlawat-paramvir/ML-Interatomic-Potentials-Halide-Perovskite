## Adapted from ACE-Julia ## 

using Pkg
Pkg.activate(".")
Pkg.Registry.add("General")  
Pkg.Registry.add(RegistrySpec(url="https://github.com/ACEsuit/ACEregistry"))
Pkg.add("ACEpotentials")

import Pkg; Pkg.add("Plots"); Pkg.add("LaTeXStrings"); Pkg.add("MultivariateStats")

using ACEpotentials, MultivariateStats, Plots, LaTeXStrings

dataset = read_extxyz("mol_cspbi3_melted.extxyz")

basis = ACE1x.ace_basis(elements = [:Cs, :I, :Pb],
                        rcut = 7.0,
                        order = 3,       
                        totaldegree = 8);

descriptors = []
config_types = []
for atoms in dataset
    struct_descriptor = sum(site_descriptors(basis, atoms)) / length(atoms)
    push!(descriptors, struct_descriptor)
end


descriptors = hcat(descriptors...)
M = fit(PCA, descriptors; maxoutdim=2, pratio=1)
descriptors_trans = transform(M, descriptors)
p = scatter(
    descriptors_trans[1,:], descriptors_trans[2,:],
    marker=:circle, linewidth=0, legend=:right)
plot!(p, xlabel="PC1", ylabel="PC2", camera=(20,10))

### radial distribution function and angular distribution function from ACE 
rdf = ACEpotentials.get_rdf(dataset, r_cut; rescale = true)

r_cut_adf = 1.25 * rnn(:Cs)
adf = ACEpotentials.get_adf(dataset, 1.25 * rnn(:Cs));

plt_rdf = histogram(rdf[(:Cs, :Cs)], bins=150, label = "rdf",
                     xlabel = L"r [\AA]", ylabel = "RDF", yticks = [])

plt_adf = histogram(adf, bins=25, label = "adf", yticks = [], c = 3,
                  xlabel = L"\theta", ylabel = "ADF", xlims = (0, π))

plot(plt_rdf, plt_adf, layout = (2,1), size = (800, 400))
