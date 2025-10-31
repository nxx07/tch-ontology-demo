---
layout: ontology_detail
id: tch
title: tch-ontology-demo
jobs:
  - id: https://travis-ci.org/nxx07/tch
    type: travis-ci
build:
  checkout: git clone https://github.com/nxx07/tch.git
  system: git
  path: "."
contact:
  email: nxx07@example.com
  label: TCH Ontology Team
  github: nxx07
description: Traditional Chinese Medicine Cold-Heat Pattern Ontology (TCH) is a formal ontology for representing TCM cold-heat patterns, diseases, symptoms, signs, herbs, formulas, and therapeutic methods. Built on BFO/RO standards with bilingual support (Chinese/English).
domain: health
homepage: https://github.com/nxx07/tch
products:
  - id: tch.owl
    name: "tch-ontology-demo main release in OWL format"
  - id: tch.obo
    name: "tch-ontology-demo additional release in OBO format"
  - id: tch.json
    name: "tch-ontology-demo additional release in OBOJSon format"
  - id: tch/tch-base.owl
    name: "tch-ontology-demo main release in OWL format"
  - id: tch/tch-base.obo
    name: "tch-ontology-demo additional release in OBO format"
  - id: tch/tch-base.json
    name: "tch-ontology-demo additional release in OBOJSon format"
dependencies:
- id: ro
- id: bfo
- id: pato
- id: iao
tracker: https://github.com/nxx07/tch/issues
license:
  url: http://creativecommons.org/licenses/by/3.0/
  label: CC-BY
activity_status: active
---

Enter a detailed description of your ontology here. You can use arbitrary markdown and HTML.
You can also embed images too.

