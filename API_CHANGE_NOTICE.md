# Web Generator API Change Notice

**Date**: January 8, 2026  
**Severity**: Medium (Workaround available)  
**Status**: Documented

---

## What Changed

The web generator **removed server-side STL generation** on **2026-01-05** in favor of client-side CSG generation.

### Previous Behavior (Before 2026-01-05)
- Server-side API endpoint: `POST /generate_braille_stl`
- Backend generated STL files and returned binary data
- Automated fixture generation via API: ✅ Supported

### Current Behavior (After 2026-01-05)
- Server-side API endpoint: `POST /generate_braille_stl` returns HTTP 410 (Gone)
- Client-side generation only (Web Workers + CSG in browser)
- Automated fixture generation via API: ❌ Not supported

---

## API Response

```http
POST /generate_braille_stl
HTTP/1.1 410 Gone
Content-Type: application/json

{
  "error": "Server-side STL generation has been removed.",
  "reason": "This endpoint required Redis and Blob storage that caused deployment failures. The application now uses client-side CSG generation exclusively.",
  "solution": "Use the web interface at the root URL (/). STL generation happens automatically in your browser using Web Workers and client-side CSG.",
  "status": "deprecated",
  "deprecated_date": "2026-01-05",
  "documentation": "docs/development/CODEBASE_AUDIT_AND_RENOVATION_PLAN.md"
}
```

---

## Impact on Validation Framework

### ❌ What No Longer Works

1. **Automated Fixture Generation**
   - `scripts/regenerate_fixtures.py` with API calls
   - Batch generation of all test cases
   - CI/CD fixture regeneration

### ✅ What Still Works

1. **OpenSCAD Automation**
   - `tests/openscad_runner.py` - Generate STL from .scad file
   - All OpenSCAD CLI features
   - Automated STL generation from OpenSCAD

2. **Mesh Comparison**
   - `tests/mesh_comparison.py` - Compare any two STL files
   - Property analysis (volume, area, watertightness)
   - Optional CloudCompare integration

3. **Parameter Validation**
   - `tests/validate_parameter_schema.py` - Verify schema consistency
   - All 37 parameters validated

4. **Test Framework**
   - `tests/cross_platform_validation.py` - Full pytest suite
   - Works with manually generated fixtures
   - All comparison logic functional

---

## Workaround: Manual Fixture Generation

### Process

1. **Open web generator**: http://localhost:5001
2. **Enter parameters** from `params.json` files
3. **Generate STL** in browser (client-side)
4. **Download** and save as `reference.stl`
5. **Repeat** for each test case

### Documentation

- **Step-by-step guide**: `tests/MANUAL_FIXTURE_GENERATION.md`
- **Progress tracking**: `python scripts/check_fixtures.py`
- **Quick reference**: `NEXT_STEPS.md`

### Time Required

- Per fixture: 3-5 minutes
- All fixtures (10 total): 30-50 minutes
- One-time effort (fixtures are reusable)

---

## Alternative Solutions

### Option A: Browser Automation (Complex)

Use Selenium/Playwright to automate web UI interactions:

**Pros**:
- Automated fixture generation
- Reusable for future regeneration

**Cons**:
- Requires additional dependencies (Selenium/Playwright)
- More complex implementation
- Browser-dependent
- Maintenance overhead

**Status**: Not currently implemented

### Option B: Use Web Generator's Client-Side Libraries (Complex)

Import and use the web generator's CSG libraries directly in Python:

**Pros**:
- Fully automated
- No browser required
- Fast generation

**Cons**:
- Requires understanding web generator internals
- JavaScript/WASM dependencies in Python
- Significant development effort
- Coupling to web generator implementation

**Status**: Not currently implemented

### Option C: Manual Generation (Recommended)

Generate fixtures manually through web UI:

**Pros**:
- Simple, works today
- No additional code needed
- Fixtures are one-time effort
- Framework remains functional

**Cons**:
- Manual process (30-50 minutes)
- Need to regenerate if web generator improves

**Status**: ✅ **Implemented - Recommended approach**

---

## Future Considerations

### If API is Restored

If the web generator adds back a server-side API or provides alternative automation:

1. Update `scripts/regenerate_fixtures.py` with new endpoint
2. Test automated generation
3. Regenerate all fixtures
4. Update documentation

### If Client-Side Automation Desired

If browser automation becomes necessary:

1. Add Selenium/Playwright to `tests/requirements.txt`
2. Create `scripts/regenerate_fixtures_browser.py`
3. Implement web UI automation
4. Test on multiple browsers
5. Update documentation

---

## Documentation Updates

The following files document the workaround:

- ✅ `tests/MANUAL_FIXTURE_GENERATION.md` - Detailed generation guide
- ✅ `scripts/check_fixtures.py` - Progress tracking script
- ✅ `NEXT_STEPS.md` - Quick start guide
- ✅ `API_CHANGE_NOTICE.md` - This document

---

## Validation Framework Status

Despite the API change, the framework remains **fully functional**:

| Component | Status | Notes |
|-----------|--------|-------|
| OpenSCAD Runner | ✅ Working | Generates STL from .scad |
| Mesh Comparison | ✅ Working | Analyzes STL properties |
| Parameter Schema | ✅ Working | Validates consistency |
| Test Framework | ✅ Working | Full pytest suite |
| Documentation | ✅ Complete | 2,000+ lines |
| Fixture Generation | ⚠️ Manual | Requires web UI interaction |

---

## Recommendations

### For Immediate Use

1. ✅ **Use manual fixture generation** (Option C)
   - Follow `tests/MANUAL_FIXTURE_GENERATION.md`
   - Track progress with `python scripts/check_fixtures.py`
   - One-time effort: 30-50 minutes

2. ✅ **Validate OpenSCAD output independently**
   - Generate test STLs: `python tests/openscad_runner.py`
   - Analyze properties: `python tests/mesh_comparison.py`
   - No web generator fixtures needed

### For Long-Term

1. **Monitor web generator** for API changes
2. **Consider browser automation** if frequent regeneration needed
3. **Document any new endpoints** for future updates

---

## Impact Assessment

| Area | Impact | Severity |
|------|--------|----------|
| Framework Functionality | Low | Most features work |
| Fixture Generation | Medium | Manual process required |
| Test Execution | None | Works with any fixtures |
| Development Workflow | Low | One-time manual effort |
| CI/CD Integration | Medium | Fixtures must be committed |

**Overall**: ⚠️ **Medium Impact with Simple Workaround**

---

## Timeline

- **2026-01-05**: Web generator API deprecated
- **2026-01-08**: Change discovered during implementation
- **2026-01-08**: Manual generation workaround documented
- **Future**: Monitor for API restoration or improvements

---

## Questions?

See:
- `tests/MANUAL_FIXTURE_GENERATION.md` - How to generate fixtures
- `NEXT_STEPS.md` - What to do next
- `tests/VALIDATION_FRAMEWORK_GUIDE.md` - Full framework docs
- `VALIDATION_FRAMEWORK_COMPLETE.md` - Implementation summary
