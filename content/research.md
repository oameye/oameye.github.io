---
# Leave the homepage title empty to use the site title
title: ""
date: 2022-10-24
type: landing

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: markdown
    content:
      title: '📚 My Research'
      subtitle: ''
      text: |-
        My research focuses primarily on **driven-dissipative** few-body physics. Specifically, I apply **Floquet perturbative expansions** to interacting bosonic systems to extract non-equilibrium stationary states (NESS). The fluctuations of these NESS can then be analyzed using **linear response** theory. Additionally, I explore the optimal transition paths between two NESS in driven-dissipative systems under **Markovian noise**.
    design:
      spacing:
      # Customize the section spacing. Order is top, right, bottom, left.
        padding: ['6rem', '0', '0', '0']
  - block: collection
    id: papers
    content:
      title: Featured Publications
      filters:
        folders:
          - publication
        featured_only: true
    design:
      view: article-grid
      columns: 2
      spacing:
      # Customize the section spacing. Order is top, right, bottom, left.
        padding: ['6rem', '0', '0', '0']
  - block: collection
    content:
      title: Recent Publications
      text: ""
      filters:
        folders:
          - publication
        exclude_featured: false
    design:
      view: citation
      spacing:
      # Customize the section spacing. Order is top, right, bottom, left.
        padding: ['6rem', '0', '0', '0']
---
