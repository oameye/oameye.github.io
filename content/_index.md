---
title: ''
summary: ''
date: 2025-05-18
type: landing

sections:
  - block: resume-biography-3
    content:
      username: me
      text: ''
      button:
        text: Email me
        url: mailto:orjan.ameye@hotmail.com
      headings:
        about: ''
        education: ''
        interests: ''
    design:
      background:
        gradient_mesh:
          enable: true
      name:
        size: md
      avatar:
        size: medium
        shape: circle

  - block: markdown
    content:
      title: '📚 Research'
      subtitle: ''
      text: |-
        My research focuses on **driven-dissipative few-body physics**. I apply
        **Floquet perturbative expansions** to interacting bosonic systems to
        extract non-equilibrium stationary states (NESS), then analyse the
        fluctuations of these NESS via **linear-response theory**. I also study
        optimal transition paths between NESS in driven-dissipative systems
        under Markovian noise.

        Please reach out to collaborate.
    design:
      columns: '1'

  - block: collection
    id: publications
    content:
      title: Featured Publications
      filters:
        folders:
          - publications
        featured_only: true
    design:
      view: article-grid
      columns: 2

  - block: collection
    content:
      title: Recent Publications
      text: ''
      filters:
        folders:
          - publications
        exclude_featured: false
    design:
      view: citation

  - block: collection
    id: projects
    content:
      title: Projects
      filters:
        folders:
          - projects
    design:
      view: article-grid
      columns: 2

  - block: collection
    id: news
    content:
      title: Recent Posts
      page_type: blog
      count: 5
      filters:
        exclude_featured: false
        exclude_future: false
        exclude_past: false
      order: desc
    design:
      view: card
      spacing:
        padding: [0, 0, 0, 0]
---
