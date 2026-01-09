# Critical Decisions for STL Validation Framework

**Date:** 2026-01-08  
**Status:** 🟡 Awaiting Decisions  
**Purpose:** Document decision options with pros/cons for implementation planning

---

## Decision 1: Repository Structure 🚨 **HIGHEST PRIORITY**

### Context
The validation framework needs to compare STLs from TWO sources:
- **Web Generator:** Python/FastAPI backend at `braille-card-and-cylinder-stl-generator`
- **OpenSCAD Generator:** This repo (`braille-stl-generator-openscad`)

### Options

#### **Option A: Validation Framework in OpenSCAD Repo** ⭐ **RECOMMENDED**

Place all validation code in `braille-stl-generator-openscad/tests/`

**Pros:**
- ✅ **Natural fit:** Validates OpenSCAD implementation against web standard
- ✅ **Single repo workflow:** Clone one repo to run OpenSCAD tests
- ✅ **CI simplicity:** GitHub Actions runs in same repo as OpenSCAD code
- ✅ **Version alignment:** Tests version-locked to OpenSCAD code they validate
- ✅ **Clear ownership:** OpenSCAD maintainers own validation of their implementation
- ✅ **No submodules needed:** Access web API over network (deployed or local)

**Cons:**
- ❌ **Network dependency:** Must access web API (deployed or run locally)
- ❌ **Cross-repo coordination:** Web API changes could break tests
- ❌ **Duplicate tooling:** May need to recreate some web test utilities
- ❌ **Language mismatch:** OpenSCAD is not Python (but tests ARE Python + trimesh)

**Implementation:**
```
braille-stl-generator-openscad/
├── tests/
│   ├── openscad_runner.py        # NEW: OpenSCAD CLI wrapper
│   ├── web_api_client.py         # NEW: Web API client
│   ├── mesh_comparison.py        # NEW: trimesh + CloudCompare
│   ├── cross_platform_validation.py  # NEW: pytest test suite
│   └── fixtures/cross_platform/  # NEW: test cases + reference STLs
└── .github/workflows/stl_validation.yml  # NEW: CI
```

**Web API Access:**
- Hit deployed API: `https://braille-card-and-cylinder-stl-gener.vercel.app`
- Fallback: Run web backend locally via Docker or uvicorn

---

#### **Option B: Validation Framework in Web Repo**

Extend `braille-card-and-cylinder-stl-generator/tests/` with OpenSCAD validation

**Pros:**
- ✅ **Existing test infrastructure:** Reuse `generate_golden_fixtures.py`
- ✅ **Direct web access:** No API calls, import web backend as Python module
- ✅ **Shared fixtures:** Use existing `tests/fixtures/` structure
- ✅ **Python-native:** All code in same language
- ✅ **Single CI pipeline:** Test both implementations together

**Cons:**
- ❌ **Backward dependency:** Web repo now depends on OpenSCAD (awkward)
- ❌ **Scope creep:** Web repo tests two separate implementations
- ❌ **OpenSCAD as dependency:** Must download/install OpenSCAD to run web tests
- ❌ **CI complexity:** Web CI now needs OpenSCAD CLI installed
- ❌ **Cross-project file access:** Tests need path to `.scad` file (git submodule or config)
- ❌ **Ownership confusion:** Web maintainers don't "own" OpenSCAD code

**Implementation:**
```
braille-card-and-cylinder-stl-generator/
├── tests/
│   ├── generate_golden_fixtures.py  # EXISTS: Extend with OpenSCAD support
│   ├── test_openscad_comparison.py  # NEW: OpenSCAD validation tests
│   ├── openscad_runner.py           # NEW: OpenSCAD CLI wrapper
│   └── fixtures/
│       ├── ...existing...
│       └── openscad_comparison/     # NEW: OpenSCAD validation fixtures
└── openscad/                        # NEW: Git submodule or downloaded file
    └── Braille_Card_And_Cylinder_STL_Generator.scad
```

---

#### **Option C: Separate Validation Repository**

Create new repo: `braille-validation-suite`

**Pros:**
- ✅ **Clean separation:** Validation is independent concern
- ✅ **Multi-version testing:** Can test multiple versions of each generator
- ✅ **Shared by both projects:** Neutral ground for validation
- ✅ **Flexible:** Can add future implementations (FreeCAD, etc.)
- ✅ **Independent CI:** Doesn't pollute either project's CI

**Cons:**
- ❌ **Extra complexity:** Three repos to manage instead of two
- ❌ **Coordination overhead:** Changes require PRs to three places
- ❌ **Git submodules:** Likely needs both projects as submodules
- ❌ **CI setup:** Requires separate CI configuration
- ❌ **Discovery:** Users must know third repo exists
- ❌ **Maintenance burden:** Another repo to maintain
- ❌ **Overkill:** Not justified unless planning many implementations

**Implementation:**
```
braille-validation-suite/
├── README.md
├── tests/
│   ├── openscad_runner.py
│   ├── web_api_client.py
│   ├── mesh_comparison.py
│   └── fixtures/
├── generators/                      # Git submodules
│   ├── openscad/                    # Submodule: braille-stl-generator-openscad
│   └── web/                         # Submodule: braille-card-and-cylinder-stl-generator
└── .github/workflows/validation.yml
```

---

### **Recommendation: Option A** ⭐

**Rationale:**
1. **OpenSCAD is being validated** → tests belong with code under test
2. **Web is the reference standard** → treat as external dependency (API)
3. **Simplest setup** → no submodules, no cross-repo file dependencies
4. **Clear purpose** → "Validate OpenSCAD matches web implementation"

**Trade-off accepted:** Network dependency on web API (mitigated with fixture caching)

---

## Decision 2: Fixture Storage Strategy 🚨 **HIGH PRIORITY**

### Context
Reference STLs from web generator need storage. Each fixture ~100KB. Estimated 10-20 test cases × 4 variants = 40-80 files = 4-8MB total.

### Options

#### **Option A: Git LFS (Large File Storage)** ⭐ **RECOMMENDED**

Check STLs into git using Git LFS for efficient binary storage

**Pros:**
- ✅ **Always available:** No network dependency for tests
- ✅ **Versioned:** Fixtures tracked with code, can diff/rollback
- ✅ **Fast CI:** No download time, instant test execution
- ✅ **Reproducible:** Exact same fixtures every run
- ✅ **Offline-friendly:** Works without internet after initial clone
- ✅ **LFS handles binaries:** Doesn't bloat git history

**Cons:**
- ❌ **Git LFS setup:** Users must install Git LFS (`git lfs install`)
- ❌ **LFS bandwidth:** GitHub free tier = 1GB/month bandwidth (likely sufficient)
- ❌ **Storage cost:** GitHub free tier = 1GB LFS storage (sufficient for 4-8MB)
- ❌ **Initial clone slower:** LFS files downloaded separately
- ❌ **Update friction:** Regenerating fixtures requires commit + push

**Implementation:**
```bash
# Setup Git LFS
git lfs install
git lfs track "*.stl"
git add .gitattributes

# Add fixtures
git add tests/fixtures/**/*.stl
git commit -m "Add reference STL fixtures"
```

**File structure:**
```
tests/fixtures/cross_platform/
├── .gitattributes           # Git LFS tracking for *.stl
├── FIXTURES_VERSION.txt     # Web generator commit hash
├── test_cases.json          # Test case definitions
└── card_rounded_emboss_basic/
    ├── params.json          # Input parameters (text)
    ├── reference.stl        # <-- Git LFS
    └── reference_meta.json  # trimesh properties (text)
```

---

#### **Option B: Generate On-Demand from Web API**

No STL files checked in; generate during test execution

**Pros:**
- ✅ **No LFS needed:** No binary files in git
- ✅ **Always fresh:** Tests latest web API version
- ✅ **Zero storage cost:** No LFS bandwidth usage
- ✅ **Auto-update:** Web API improvements automatically included
- ✅ **Small repo:** Git repo stays lightweight

**Cons:**
- ❌ **Network required:** Tests fail if web API down or offline
- ❌ **Slower tests:** API roundtrip adds 2-5 seconds per fixture
- ❌ **Non-deterministic:** Web API changes break tests unpredictably
- ❌ **CI dependency:** CI requires network access to web API
- ❌ **Rate limiting risk:** API may rate-limit CI runs
- ❌ **Version drift:** Hard to test against specific web version

**Implementation:**
```python
# tests/web_api_client.py
def get_reference_stl(params):
    response = requests.post(
        "https://braille-card-and-cylinder-stl-gener.vercel.app/generate_braille_stl",
        json=params,
        timeout=30
    )
    return response.content  # STL bytes
```

---

#### **Option C: Hybrid (Cached + Fallback)**

Check STLs into Git LFS + regenerate script for updates

**Pros:**
- ✅ **Best of both:** Fast offline tests + easy regeneration
- ✅ **Reproducible:** Fixtures versioned in git
- ✅ **Updatable:** Script regenerates fixtures when needed
- ✅ **CI reliable:** Uses checked-in fixtures, no network dependency
- ✅ **Explicit versioning:** Update fixtures via explicit script + commit

**Cons:**
- ❌ **Complexity:** More moving parts (fixtures + regeneration script)
- ❌ **Two-phase workflow:** Generate fixtures, then commit
- ❌ **Potential drift:** Checked-in fixtures may age without updates
- ❌ **Git LFS still needed:** Same LFS limitations as Option A

**Implementation:**
```python
# scripts/regenerate_fixtures.py
"""
Regenerate all reference STLs from web API.
Run when web generator changes or adding new test cases.
"""
import requests
import json
from pathlib import Path

def regenerate_all_fixtures():
    test_cases = json.load(open("tests/fixtures/cross_platform/test_cases.json"))
    
    for test_case in test_cases:
        stl_bytes = call_web_api(test_case["params"])
        output_path = Path(f"tests/fixtures/cross_platform/{test_case['name']}/reference.stl")
        output_path.write_bytes(stl_bytes)
        print(f"✓ {test_case['name']}")
    
    # Record web generator version
    web_version = get_web_generator_version()
    Path("tests/fixtures/cross_platform/FIXTURES_VERSION.txt").write_text(web_version)

if __name__ == "__main__":
    regenerate_all_fixtures()
```

**Workflow:**
1. Normal development: Use checked-in fixtures (fast, reliable)
2. When web API changes: Run `python scripts/regenerate_fixtures.py`
3. Review diffs: `git diff tests/fixtures/`
4. Commit: `git commit -m "Update fixtures to web v1.2.3"`

---

#### **Option D: Download from GitHub Releases**

Store fixtures as release artifacts, download before tests

**Pros:**
- ✅ **No LFS cost:** Uses GitHub release storage (unlimited)
- ✅ **Versioned:** Each release has matching fixture set
- ✅ **No git bloat:** Binary files outside git history
- ✅ **CDN-backed:** Fast downloads from GitHub CDN

**Cons:**
- ❌ **Complex setup:** Requires release creation + artifact upload automation
- ❌ **Initial experience:** New contributors must download fixtures manually
- ❌ **CI complexity:** Must download before tests (adds script complexity)
- ❌ **Version coordination:** Must match fixture version to code version
- ❌ **Extra infrastructure:** Release management automation needed

---

### **Recommendation: Option C (Hybrid)** ⭐

**Rationale:**
1. **Reproducible tests:** Checked-in fixtures ensure deterministic CI
2. **Easy updates:** Regeneration script when web API improves
3. **Explicit versioning:** Fixtures updated via conscious decision (commit)
4. **Offline-friendly:** Tests work without network after initial clone
5. **Best practices:** Combines benefits of caching + automation

**Setup priority:**
1. Initial fixtures: Generate + commit with Git LFS
2. Add regeneration script for future updates
3. Document in README when/how to regenerate

---

## Decision 3: Tool Version Pinning 🚨 **HIGH PRIORITY**

### Context
Tests need specific tool versions for reproducibility. Different versions may produce slightly different STL output (mesh triangulation).

### Options

#### **Option A: Pin Exact Versions** ⭐ **RECOMMENDED for CI**

Document and enforce specific versions

**Pros:**
- ✅ **Reproducible:** Same results across machines
- ✅ **CI stability:** Tests won't break from tool updates
- ✅ **Debugging:** Can isolate tool version issues
- ✅ **Explicit control:** Know exactly what's being tested

**Cons:**
- ❌ **Maintenance:** Must update versions periodically
- ❌ **Inflexibility:** Users can't test with newer versions
- ❌ **Installation friction:** Users must install specific versions

**Specification:**
```yaml
# tests/tool_versions.yml
required_tools:
  openscad:
    version: "2023.12.11"  # Latest stable as of Dec 2024
    download:
      windows: "https://files.openscad.org/OpenSCAD-2023.12.11-x86_64.zip"
      linux: "apt-get install openscad=2023.12.11"
      macos: "brew install openscad@2023.12.11"
    
  python:
    version: ">=3.9,<4.0"
    packages:
      - "trimesh==4.0.5"
      - "numpy==1.24.3"
      - "scipy==1.11.4"
      - "requests==2.31.0"
  
  cloudcompare:
    version: "2.13.1"  # Latest stable
    optional: true      # Tests skip numeric checks if missing
    download:
      windows: "https://www.cloudcompare.org/release/CloudCompare_v2.13.1_setup_x64.exe"
      linux: "snap install cloudcompare"
      macos: "brew install cloudcompare"
    paths:
      windows: "C:\\Program Files\\CloudCompare\\CloudCompare.exe"
      linux: "/usr/bin/CloudCompare"
      macos: "/Applications/CloudCompare.app/Contents/MacOS/CloudCompare"
```

---

#### **Option B: Version Ranges (Flexible)**

Allow range of compatible versions

**Pros:**
- ✅ **User-friendly:** Works with user's installed versions
- ✅ **Less maintenance:** No need to update constantly
- ✅ **Forward-compatible:** Tests work with newer tools
- ✅ **Easier onboarding:** Users don't need specific versions

**Cons:**
- ❌ **Non-reproducible:** Different versions = different results
- ❌ **Test instability:** Tool updates may break tests
- ❌ **Hard to debug:** Can't isolate version-specific issues
- ❌ **Tolerance tuning:** Must accommodate variation across versions

**Specification:**
```yaml
required_tools:
  openscad:
    min_version: "2021.01"    # Minimum supported
    max_version: "2024.12.31" # Maximum tested
    
  cloudcompare:
    min_version: "2.12.0"
    optional: true
```

---

#### **Option C: Hybrid (Pin CI, Flexible Local)** ⭐ **RECOMMENDED**

CI uses exact versions; local dev allows ranges

**Pros:**
- ✅ **CI reproducible:** Exact versions in CI for stability
- ✅ **Local flexibility:** Developers use installed versions
- ✅ **Best of both:** Rigorous testing + easy development
- ✅ **Clear expectations:** CI is ground truth, local is best-effort

**Cons:**
- ❌ **Dual maintenance:** Document both exact + range versions
- ❌ **Potential divergence:** Local tests may pass while CI fails
- ❌ **Documentation complexity:** Must explain two modes

**Implementation:**
```python
# tests/conftest.py (pytest config)
import os
import subprocess

def check_openscad_version():
    result = subprocess.run(["openscad", "--version"], capture_output=True, text=True)
    version = parse_version(result.stdout)
    
    if os.environ.get("CI"):
        # CI: Enforce exact version
        required = "2023.12.11"
        if version != required:
            pytest.fail(f"CI requires OpenSCAD {required}, found {version}")
    else:
        # Local: Allow range
        min_version = "2021.01"
        if version < min_version:
            pytest.skip(f"OpenSCAD {min_version}+ required, found {version}")
        elif version > "2024.12.31":
            pytest.warn(f"OpenSCAD {version} not tested, may have issues")
```

---

### **Recommendation: Option C (Hybrid)** ⭐

**Rationale:**
1. **CI stability:** Exact versions prevent flaky tests
2. **Dev velocity:** Don't force developers to install specific versions
3. **Realistic:** CI = production standard, local = development aid
4. **Pragmatic:** Balance rigor with usability

**Versions to Pin (CI):**
- **OpenSCAD:** 2023.12.11 (latest stable)
- **Python:** 3.11.x (modern, stable)
- **trimesh:** 4.0.5
- **CloudCompare:** 2.13.1 (optional, skip if missing)

---

## Decision 4: Web API Access Method 🚨 **HIGH PRIORITY**

### Context
Reference STLs come from web generator. Need reliable access for fixture generation and updates.

### Options

#### **Option A: Deployed Web API** ⭐ **RECOMMENDED for Fixture Generation**

Hit production API at `braille-card-and-cylinder-stl-gener.vercel.app`

**Pros:**
- ✅ **No local setup:** No need to run web backend locally
- ✅ **Latest version:** Always uses production web generator
- ✅ **Fast:** Vercel CDN-backed
- ✅ **Maintained:** Production API is maintained/updated
- ✅ **Simple:** Just HTTP requests

**Cons:**
- ❌ **Network dependency:** Requires internet connection
- ❌ **External dependency:** If API down, can't regenerate fixtures
- ❌ **Rate limiting:** May hit rate limits (unlikely for small fixture set)
- ❌ **Version coupling:** Can't test against specific old versions
- ❌ **API changes:** Breaking changes could fail fixture generation

**Implementation:**
```python
# tests/web_api_client.py
import requests
from typing import Dict, Any

WEB_API_BASE = "https://braille-card-and-cylinder-stl-gener.vercel.app"

def generate_reference_stl(params: Dict[str, Any]) -> bytes:
    """Generate STL from web API."""
    response = requests.post(
        f"{WEB_API_BASE}/generate_braille_stl",
        json=params,
        timeout=60
    )
    response.raise_for_status()
    return response.content  # STL bytes

def get_api_version() -> str:
    """Get web API version/commit hash."""
    response = requests.get(f"{WEB_API_BASE}/health")
    return response.json().get("version", "unknown")
```

---

#### **Option B: Local Web Backend**

Run web backend locally via Docker or uvicorn

**Pros:**
- ✅ **Offline:** No internet required
- ✅ **Version control:** Can test specific web versions (git checkout)
- ✅ **Fast:** No network latency
- ✅ **Deterministic:** Exact version control
- ✅ **No rate limits:** Local execution

**Cons:**
- ❌ **Setup complexity:** Must clone web repo + install dependencies
- ❌ **Dependency management:** Python env, liblouis, etc.
- ❌ **Cross-platform issues:** Web backend may have platform quirks
- ❌ **Maintenance:** Must keep local web backend updated
- ❌ **CI complexity:** CI must set up entire web backend

**Implementation:**
```bash
# Setup script
git clone https://github.com/BrennenJohnston/braille-card-and-cylinder-stl-generator.git
cd braille-card-and-cylinder-stl-generator
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Then hit http://localhost:8000/generate_braille_stl
```

---

#### **Option C: Python Import (Direct Integration)**

Import web backend as Python library

**Pros:**
- ✅ **No API calls:** Direct Python function calls
- ✅ **Fastest:** No network/API overhead
- ✅ **Testable:** Can mock/patch web backend components
- ✅ **Offline:** No internet required
- ✅ **Version pinnable:** Install specific web backend version

**Cons:**
- ❌ **Tight coupling:** Web backend must be importable library
- ❌ **Dependency hell:** All web dependencies become test dependencies
- ❌ **Platform issues:** Native dependencies (trimesh, etc.) may conflict
- ❌ **Not realistic:** Doesn't test actual API contract
- ❌ **Web changes required:** Web backend may not be structured for import

**Implementation:**
```python
# Requires web backend as installable package
# pip install git+https://github.com/BrennenJohnston/braille-card-and-cylinder-stl-generator.git

from app.services.stl_generator import generate_stl
from app.models import CardSettings

# Direct function call
stl_bytes = generate_stl(CardSettings(...))
```

---

#### **Option D: Hybrid (API + Fixtures)** ⭐ **RECOMMENDED for Tests**

Use API for fixture generation; tests use cached fixtures

**Pros:**
- ✅ **Best of both:** Reliable tests (fixtures) + easy updates (API)
- ✅ **CI stability:** Tests use fixtures (no network dependency)
- ✅ **Update flexibility:** Regenerate fixtures via API when needed
- ✅ **Clear separation:** Fixture generation ≠ test execution

**Cons:**
- ❌ **Two modes:** Different workflows for fixture generation vs. tests
- ❌ **Documentation:** Must explain both workflows

**Implementation:**
```python
# Fixture generation (manual, occasional):
python scripts/regenerate_fixtures.py  # Hits web API

# Test execution (automatic, frequent):
pytest tests/  # Uses cached fixtures from git
```

---

### **Recommendation: Option D (Hybrid)** ⭐

**Rationale:**
1. **Tests don't need network:** Use cached fixtures for stability
2. **Updates are explicit:** Regenerate fixtures via script when web changes
3. **Simple for users:** Just run pytest, no web backend setup
4. **Flexible:** Can regenerate fixtures from deployed API anytime

**Workflow:**
- **Daily development:** Run tests using checked-in fixtures (fast, reliable)
- **Web updates:** Run `regenerate_fixtures.py` to fetch new STLs from API
- **CI:** Uses fixtures, no network dependency

---

## Decision 5: Test Case Selection 🚨 **MEDIUM PRIORITY**

### Context
Need to define specific test cases covering parameter space without over-testing.

### Minimum Viable Test Suite (10 Test Cases)

#### **Core Functionality (6 test cases)**

1. **`card_rounded_emboss_basic`**
   - Shape: Card, Plate: Emboss, Dots: Rounded
   - Braille: "⠓⠑⠇⠇⠕" (hello)
   - All defaults, indicators ON

2. **`card_rounded_counter_basic`**
   - Shape: Card, Plate: Counter, Dots: Rounded
   - Matching counter plate for test #1
   - Validates emboss/counter symmetry

3. **`card_cone_emboss_basic`**
   - Shape: Card, Plate: Emboss, Dots: Cone
   - Braille: "⠺⠕⠗⠇⠙" (world)
   - Tests cone shape variant

4. **`card_cone_counter_basic`**
   - Shape: Card, Plate: Counter, Dots: Cone
   - Matching counter for test #3

5. **`cylinder_rounded_emboss_basic`**
   - Shape: Cylinder, Plate: Emboss, Dots: Rounded
   - Braille: "⠞⠑⠌" (test)
   - Default cylinder params

6. **`cylinder_rounded_counter_basic`**
   - Shape: Cylinder, Plate: Counter, Dots: Rounded
   - Matching counter for test #5

#### **Parameter Variations (4 test cases)**

7. **`card_rounded_emboss_custom_spacing`**
   - Non-default braille spacing
   - cell_spacing: 7.0mm (vs default 6.5mm)
   - line_spacing: 12.0mm (vs default 10.0mm)
   - Tests spacing parameters

8. **`card_rounded_emboss_indicators_off`**
   - indicator_shapes: OFF
   - Tests grid without indicators
   - Validates grid_columns calculation

9. **`card_rounded_emboss_max_grid`**
   - All 4 lines filled
   - 11 characters each line (max for grid_columns=11)
   - Tests maximum text capacity

10. **`cylinder_rounded_emboss_custom_cutout`**
    - Non-default cylinder dimensions
    - polygon_cutout_radius_mm: 10.0mm (vs 13.0mm)
    - polygon_cutout_points: 6 (vs 12) - hexagonal
    - seam_offset_degrees: 30.0 (vs 355.0)
    - Tests cylinder parameter variations

---

### Extended Test Suite (Future - 20+ test cases)

**Additional coverage:**
- Edge cases: Empty lines, single character, mixed empty/full lines
- Positioning: braille_x_adjust, braille_y_adjust variations
- Extreme dimensions: Large/small cards, large/small cylinders
- Dot dimensions: Custom emboss/counter sizes
- Unicode validation: Invalid characters, mixed ASCII/braille
- Rendering quality: Low/medium/high hemisphere quality

---

### Test Case Definition Format

```json
// tests/fixtures/cross_platform/test_cases.json
{
  "version": "1.0.0",
  "test_cases": [
    {
      "name": "card_rounded_emboss_basic",
      "description": "Default card with rounded dots, indicators on",
      "parameters": {
        "Line_1": "⠓⠑⠇⠇⠕",
        "Line_2": "",
        "Line_3": "",
        "Line_4": "",
        "shape_type": "card",
        "plate_type": "positive",
        "combined_shape": "rounded",
        "indicator_shapes": "on",
        "card_width": 90.0,
        "card_height": 52.0,
        "card_thickness": 2.0,
        "grid_columns": 11,
        "grid_rows": 4,
        "cell_spacing": 6.5,
        "line_spacing": 10.0,
        "dot_spacing": 2.5,
        "braille_x_adjust": 0.0,
        "braille_y_adjust": 0.0,
        "rounded_dot_base_diameter": 2.0,
        "rounded_dot_base_height": 0.2,
        "rounded_dot_dome_diameter": 1.5,
        "rounded_dot_dome_height": 0.6,
        "bowl_counter_dot_base_diameter": 1.8,
        "counter_dot_depth": 0.8,
        "hemisphere_quality": "medium",
        "cone_segments": 16
      },
      "expected_properties": {
        "is_watertight": true,
        "volume_mm3_approx": 9360.0,
        "surface_area_mm2_approx": 10100.0
      },
      "tolerances": {
        "volume_percent": 1.0,
        "surface_area_percent": 1.0,
        "bbox_mm": 0.1,
        "max_surface_deviation_mm": 0.05
      }
    }
  ]
}
```

---

### **Recommendation: Start with 10 Core Cases** ⭐

**Rationale:**
1. **Coverage:** Hits all major features (card/cylinder, rounded/cone, emboss/counter)
2. **Manageable:** Small enough to debug, large enough to catch issues
3. **Extensible:** Easy to add more cases later
4. **Fast CI:** 10 cases × 30 seconds each = 5 minutes total

**Implementation priority:**
1. Implement 6 core functionality tests first
2. Add 4 parameter variation tests next
3. Add extended suite (20+) as needed based on bug reports

---

## Summary of Recommendations

| Decision | Recommended Option | Priority |
|----------|-------------------|----------|
| Repository Structure | **Option A:** Validation in OpenSCAD repo | 🚨 Highest |
| Fixture Storage | **Option C:** Hybrid (Git LFS + regeneration script) | 🚨 High |
| Tool Versions | **Option C:** Hybrid (exact in CI, flexible local) | 🚨 High |
| Web API Access | **Option D:** Hybrid (API for fixtures, cached for tests) | 🚨 High |
| Test Cases | **10 core test cases** (detailed above) | 🚨 Medium |

---

## Next Steps

1. **Review and approve** these decisions (or request modifications)
2. **Document decisions** in plan update
3. **Create Phase 0 implementation** (repo structure, tooling setup)
4. **Proceed with Phase 1-6** from original plan

---

**Decision Document Status:** 🟡 Awaiting Approval  
**Created:** 2026-01-08  
**Review Required By:** Project maintainer
