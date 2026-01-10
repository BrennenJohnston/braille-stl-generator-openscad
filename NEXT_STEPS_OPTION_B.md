# Next Steps: Option B - Web Cross-Platform Validation

## Current Status

✅ **Phase 1-5 Complete** - Framework implemented and validated  
✅ **Option A Complete** - OpenSCAD self-test working (12/12 tests passing)  
⏳ **Option B Pending** - Web cross-platform validation (next phase)

---

## What is Option B?

**Option B** generates reference STL fixtures from the **web generator** (JavaScript implementation) instead of OpenSCAD, enabling true cross-platform validation to detect geometry discrepancies between the two implementations.

### Why It Matters

- **Option A (Current)**: OpenSCAD validates against itself (internal consistency)
- **Option B (Next)**: OpenSCAD validates against web generator (cross-platform parity)

Option B will likely reveal:
- Geometry discrepancies (rounded/cone dot shapes)
- Indicator recess bugs (counter plates)
- Tessellation differences
- Coordinate system variations

---

## Prerequisites for Option B

### 1. Web Generator Access

You need one of:

**Option 1: Deployed Web App (Easiest)**
- URL of deployed braille STL generator web app
- Web app must be accessible from your machine
- Example: `https://braille-generator.example.com`

**Option 2: Local Web Server**
- Clone and run web generator locally
- Start development server (e.g., `npm run dev`)
- Note the local URL (e.g., `http://localhost:3000`)

**Option 3: Web Source Code (Best)**
- Clone web generator repository
- Run it headlessly via Node.js (requires implementation)
- Most deterministic but needs development

### 2. Playwright Setup (Already Done ✅)

```bash
# Install Playwright (if not already installed)
pip install playwright

# Install Chromium browser
python -m playwright install chromium
```

### 3. Web Generator Information Needed

Before proceeding, gather:
- [ ] Web generator URL (deployed or local)
- [ ] Web generator repository URL (for commit tracking)
- [ ] Web generator version/commit hash (for fixture metadata)
- [ ] Verification that web UI shows cylinder option

---

## Implementation Steps

### Step 1: Inspect Web UI Structure (30-60 min)

```bash
# Open web generator in browser
# Inspect elements to identify selectors

# Key elements to find:
# - Line 1-4 text input fields (textarea or input)
# - Shape type dropdown (should show "Cylinder")
# - Plate type dropdown (Embossing/Counter)
# - Dot shape dropdown (Rounded/Cone)
# - Indicators dropdown (On/Off)
# - Download/Generate STL button
```

**Document selectors** for:
- Text input: `#line1`, `textarea[name="line1"]`, etc.
- Dropdowns: `select[name="shape_type"]`, etc.
- Button: `button:has-text("Download STL")`, etc.

### Step 2: Update Playwright Selectors (15-30 min)

Edit `scripts/generate_web_fixtures.py`:

```python
# Line ~90: Update text input selectors
selector = f"#line{i}, [name='line{i}'], textarea[placeholder*='Line {i}']"

# Line ~105: Update dropdown selectors
selector = f"select[name='{param_name}'], #{param_name}"

# Line ~140: Update download button selectors
download_button_selectors = [
    "button:has-text('Download STL')",
    "button:has-text('Generate')",
    "#download-stl",
]
```

### Step 3: Test Web Fixture Generation (30-60 min)

```bash
# Test with visible browser (debug mode)
python scripts/generate_web_fixtures.py \
  --web-url YOUR_WEB_URL_HERE \
  --test-case cylinder_rounded_emboss_indicators_on \
  --no-headless

# Watch the browser automation:
# - Does it navigate correctly?
# - Does it fill in parameters?
# - Does it click download button?
# - Does the STL download?

# Fix selectors until automation works smoothly
```

### Step 4: Generate All Web Fixtures (1-2 hours)

```bash
# Generate all 11 fixtures
python scripts/generate_web_fixtures.py \
  --web-url YOUR_WEB_URL_HERE \
  --verbose

# This will:
# - Generate 11 STL files from web generator
# - Extract mesh properties
# - Create fixture metadata
# - Record web generator version
```

### Step 5: Run Cross-Platform Validation (30-60 min)

```bash
# Run tests with web reference fixtures
python -m pytest tests/cross_platform_validation.py::TestCrossPlatformValidation -v

# EXPECT FAILURES - this is normal!
# Document all failures:
# - Volume/area mismatches (geometry discrepancies)
# - Surface deviation warnings
# - Watertightness issues
# - Bounding box differences
```

### Step 6: Analyze and Document Failures (1-2 hours)

For each failing test:
1. **Identify failure type**: Volume? Area? Surface deviation?
2. **Isolate cause**: Rounded dots? Cone dots? Indicators? Counter plate?
3. **Use isolation tests**: Run `cylinder_indicator_recess_*` tests
4. **Document in issue tracker**: Geometry type, magnitude, affected tests

Common expected failures:
- **Indicator recess bug**: Counter plates with indicators on
- **Rounded dot geometry**: Frustum + spherical cap differences
- **Cone dot geometry**: Frustum taper differences
- **Bowl recess**: Spherical cap depth/diameter
- **Tessellation**: Face count differences (informational only)

### Step 7: Fix Geometry Issues (4-8 hours)

Priority order:
1. **Indicator recesses** (project-breaking - alignment markers must match)
2. **Rounded emboss dots** (most common geometry)
3. **Bowl recesses** (counter plate for rounded)
4. **Cone emboss dots** (alternative geometry)
5. **Cone recesses** (counter plate for cone)

For each fix:
- Locate code in OpenSCAD (e.g., `cylinder_counter_plate()`)
- Compare to web generator implementation (inspect source or ask maintainer)
- Adjust OpenSCAD geometry to match
- Re-run specific test to verify fix
- Document change in commit message

### Step 8: Run Strict Validation (30-60 min)

After baseline tests pass:

```bash
# Run with strict tolerances
python -m pytest tests/cross_platform_validation.py \
  --comparison-config=tests/compare_config_strict.json \
  -v

# Strict profile catches subtle differences:
# - Volume within 0.1% (vs 1.0% baseline)
# - Area within 0.1% (vs 0.5% baseline)
# - Bbox within 0.01mm (vs 0.1mm baseline)
# - Surface deviation within 0.02mm (vs 0.05mm baseline)
```

---

## Time Estimates

| Step | Description | Time | Cumulative |
|------|-------------|------|------------|
| 1 | Inspect web UI | 30-60 min | 1 hour |
| 2 | Update selectors | 15-30 min | 1.5 hours |
| 3 | Test generation | 30-60 min | 2.5 hours |
| 4 | Generate fixtures | 1-2 hours | 4 hours |
| 5 | Run validation | 30-60 min | 5 hours |
| 6 | Analyze failures | 1-2 hours | 7 hours |
| 7 | Fix geometry | 4-8 hours | 15 hours |
| 8 | Strict validation | 30-60 min | 16 hours |

**Total estimated time**: 12-20 hours (can be spread across multiple sessions)

---

## Questions to Answer Before Proceeding

### Required Information

1. **What is your web generator URL?**
   - Deployed production URL?
   - Local development server?
   - Need to deploy first?

2. **Do you have access to web generator source code?**
   - Repository URL?
   - Can you identify the commit/version?
   - Prefer to implement headless generation instead of Playwright?

3. **What's your timeline?**
   - Need validation quickly? (Use Playwright as-is)
   - Have time for proper implementation? (Implement headless source method)
   - Just exploring? (Test with single fixture first)

### Optional Information

4. **Do you have CloudCompare installed?**
   - Enables surface deviation analysis (helpful but not required)
   - Can skip with `--skip-cloudcompare` flag

5. **Are there known geometry differences?**
   - Any documented discrepancies between implementations?
   - Known bugs or limitations in either implementation?

---

## Decision Tree

```
Do you have web generator URL?
├─ Yes → Proceed to Step 1 (Inspect Web UI)
└─ No  → Options:
         ├─ Deploy web app first
         ├─ Run locally (npm install + npm run dev)
         └─ Ask web generator maintainer for deployed URL

Can you access web generator source code?
├─ Yes → Consider implementing headless generation (better long-term)
└─ No  → Use Playwright automation (works well, easier setup)

Do you want to proceed now?
├─ Yes → Provide web URL and we'll start Step 1
└─ No  → Keep Option A fixtures, revisit Option B later
```

---

## What I Need From You

To proceed with Option B, please provide:

1. **Web generator URL**: `https://_______________` or `http://localhost:____`
2. **Access confirmation**: Can you access this URL in your browser?
3. **Version information**: Do you know the web generator version/commit?

Once you provide this information, I can:
- Help you inspect the web UI
- Update Playwright selectors
- Generate the first test fixture
- Run cross-platform validation
- Identify geometry discrepancies

---

## Alternative: Stay with Option A

If you're not ready for Option B, that's fine! You can:

- ✅ Use current OpenSCAD fixtures for regression testing
- ✅ Validate OpenSCAD changes ensure internal consistency
- ✅ Detect if OpenSCAD code changes break existing geometry
- ⏳ Defer cross-platform validation until needed

The framework is production-ready for OpenSCAD development. Option B adds cross-platform validation but isn't required for basic testing.

---

**Ready to proceed? Please provide your web generator URL and we'll start Option B!**
