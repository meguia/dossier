# Manuel Eguía — Sound, space & perception

A permanent English/Spanish portfolio for sound artist, physicist and researcher Manuel Eguía.

**Website:** https://meguia.github.io/dossier/

## Edit and build

The editorial source is `content/portfolio.json`. It contains both languages, project credits, links and the selected CV. The site has no JavaScript runtime or external font dependencies.

```sh
python3 scripts/build.py
```

This generates fourteen static pages in `docs/`. GitHub Pages serves `docs/` from the `main` branch. Relative asset and navigation links support the `/dossier/` project path.

The PDF masters are generated separately:

```sh
python3 scripts/build_print.py
```

Open the resulting HTML files in `build/print/` and print to PDF with backgrounds enabled, no browser headers or footers, and the page sizes defined in the files. The portfolio has sixteen A4 landscape pages; the selected CV has two. Copy updated PDFs to `docs/downloads/` after reviewing them.

An optional `--proposal /path/to/residency-proposal.md` argument prepares a one-page A4 portrait application document. That source and the generated application document are kept outside `docs/`.

## Publication and credits

Only the curated text, selected images and finished portfolio/CV PDFs are included. Work credits appear alongside every project. Most photographs and stills come from the original dossiers. The Wind Chimes photographs are by Ximena Martinez, from Buenos Aires Sonora’s November 2011 archive. The IRIS teaser image is credited to Ezequiel Hilbert. These image credits appear on the relevant project pages. No licence for third-party artwork or photography is granted by this repository.

The fonts are Liberation Sans and Liberation Serif; their licence is included in `assets/fonts/LICENSE.txt`.

The project descriptions derive from the supplied Manuel Eguía, CERN, Transit and GRAPa dossiers. Career details use the supplied CVs and the author's stated 25 years working in an art-school environment. Dates and collaboration credits were cross-checked against records from UNQ, the Mercosul Biennial, La Biennale di Venezia, PAC Milano, Performing Arts Forum and the MCBA 2020 activity report. Research links point to the publishers' DOI records.

The Wind Chimes description and construction/performance credits use Buenos Aires Sonora’s 2011 project archive. IRIS uses UNQ project documentation, the supplied teaser and the 2022 Journal of New Music Research paper. The portfolio contains six selected projects.

The website opens with a short introduction and download links, followed by the six selected works. About / Sobre mí uses first-person prose; the PDF opens with a linked works index and places About after the project selection. The website and PDFs use Liberation Sans throughout.

About pairs a full-height portrait on the left with one merged text column on the right. The following sections run in this order: Interdisciplinary work and current research, selected international collaborations, PAF workshops, then the CV. The portfolio gives PAF workshops their own page immediately before the CV.
