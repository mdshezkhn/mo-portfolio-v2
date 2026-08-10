# Baseline Capture - Phase 10

## File Hashes
- build.py: f23c461f
- templates/cv/base.html: a0e361e6
- templates/cv/partials/summary.html: a0bb3e91
- templates/cv/partials/experience.html: 397267bf
- templates/cv/partials/education.html: 7351dd96
- templates/cv/partials/competencies.html: d4e3ed52
- templates/cv/profiles/master.json: 74eb882d
- templates/cv/profiles/eal.json: f3c1b1ef
- templates/cv/profiles/stem.json: e9a4f549
- templates/cv/profiles/coordinator.json: 4b8e5581
- templates/cv/profiles/td.json: 57414266

## CSS Selector Inventory
Found 10 unique classes in templates/cv/styles.css: ['.contact-info', '.entry', '.entry-date', '.entry-header', '.entry-subtitle', '.entry-title', '.manifest', '.no-print', '.page-break-before', '.subtitle']

## Profile -> Output Mapping
- master.json -> CV_Master.html
- eal.json -> CV_Primary_EAL.html (expected)
- stem.json -> CV_STEM_EAL.html (expected)
- 	d.json -> CV_Teacher_Development.html (expected)
- coordinator.json -> CV_EAL_Coordinator.html (expected)

## Existing Privacy Behavior
Privacy logic is currently absent from build.py. It assumes profile JSONs already contain the exact presentation strings.