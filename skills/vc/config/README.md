# Firm Customization

Customize claude-vc for your firm by creating config files in this
directory. These override the defaults in `references/` without
replacing them entirely.

## How to Activate

1. Copy the `.example` file for the config you want to customize
2. Remove the `.example` extension
3. Edit the file with your firm's preferences

```bash
cp firm-criteria.md.example firm-criteria.md
cp firm-templates.md.example firm-templates.md
```

## Available Config Files

### `firm-criteria.md`

Override the default investment criteria scoring framework. Customize:

- Dimension weights (market, team, product, financials, timing)
- Scoring thresholds for each dimension
- Firm-specific red flags and green flags
- Minimum Deal Score for investment consideration

When present, skills that load `investment-criteria.md` will check for
this file first and merge your custom criteria with the defaults.

### `firm-templates.md`

Override the default output formatting. Customize:

- Investment memo section headers and ordering
- KPI report formatting preferences
- Portfolio report layout
- Required sections for your IC process

When present, skills that generate reports will use your templates
for section structure and formatting.

## Which Skills Check for Config

| Config File        | Skills That Use It                         |
| ------------------ | ------------------------------------------ |
| `firm-criteria.md` | vc-screen, vc-memo, vc-compare, vc-kpi     |
| `firm-templates.md`| vc-memo, vc-kpi, vc-portfolio, vc-returns  |
