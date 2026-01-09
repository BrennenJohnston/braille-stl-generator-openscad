# Manual Fixture Generation Guide

**Purpose**: Generate reference STL files from the web generator UI since the server-side API has been deprecated.

**Date**: January 8, 2026  
**Status**: Active (Web API deprecated on 2026-01-05)

---

## Background

The web generator removed server-side STL generation in favor of client-side CSG generation. Reference fixtures must now be generated manually through the web UI.

## Prerequisites

- Web generator running: http://localhost:5001
- Browser (Chrome/Edge/Firefox recommended)
- Test case definitions: `tests/fixtures/cross_platform/test_cases.json`

---

## Quick Start

### 1. Open Web Generator

```powershell
# In a separate terminal (if not already running)
cd ..\braille-card-and-cylinder-stl-generator
python backend.py
```

Then open in browser: **http://localhost:5001**

### 2. Generate Reference Fixtures

For each of the 10 test cases, follow the process below.

---

## Test Case Checklist

Use this checklist to track progress:

- [ ] 1. **card_rounded_emboss_basic** - Default card, rounded dots
- [ ] 2. **card_rounded_counter_basic** - Counter plate for test 1
- [ ] 3. **card_cone_emboss_basic** - Card with cone-shaped dots
- [ ] 4. **card_cone_counter_basic** - Counter plate for test 3
- [ ] 5. **cylinder_rounded_emboss_basic** - Default cylinder
- [ ] 6. **cylinder_rounded_counter_basic** - Counter plate for test 5
- [ ] 7. **card_rounded_emboss_custom_spacing** - Custom spacing
- [ ] 8. **card_rounded_emboss_indicators_off** - No indicators
- [ ] 9. **card_rounded_emboss_max_grid** - All 4 lines filled
- [ ] 10. **cylinder_rounded_emboss_custom_cutout** - Hexagonal cutout

---

## Detailed Process for Each Test Case

### Step-by-Step Instructions

#### 1. **card_rounded_emboss_basic**

**Parameters** (from `tests/fixtures/cross_platform/card_rounded_emboss_basic/params.json`):

```
Text Input:
  Line 1: ⠓⠑⠇⠇⠕
  Line 2-4: (empty)

Shape and Plate:
  Output Shape: Card (Flat Plate)
  Plate Type: Embossing Plate
  
Expert Mode - Shape Selection:
  Braille Dot Shape: Rounded
  Indicator Shapes: On

Expert Mode - Surface Dimensions:
  Card Width: 90 mm
  Card Height: 52 mm
  Card Thickness: 2.0 mm

Expert Mode - Braille Spacing:
  Grid Columns: 11
  Grid Rows: 4
  Cell Spacing: 6.5 mm
  Line Spacing: 10.0 mm
  Dot Spacing: 2.5 mm
  X Adjust: 0.0 mm
  Y Adjust: 0.0 mm

Expert Mode - Braille Dot Adjustments (Rounded):
  Base Diameter: 2.0 mm
  Base Height: 0.2 mm
  Dome Diameter: 1.5 mm
  Dome Height: 0.6 mm

Expert Mode - Braille Dot Adjustments (Counter Bowl):
  Bowl Base Diameter: 1.8 mm
  Counter Dot Depth: 0.8 mm

Rendering Quality:
  Hemisphere Quality: Medium (32 segments)
  Cone Segments: 16
```

**Steps**:
1. Open web UI: http://localhost:5001
2. Enter parameters as listed above
3. Click "Generate STL" (or equivalent button)
4. Wait for generation (client-side, may take a moment)
5. Download STL file
6. Save as: `tests\fixtures\cross_platform\card_rounded_emboss_basic\reference.stl`

---

#### 2. **card_rounded_counter_basic**

**Parameters**: Same as test 1, except:
- **Plate Type**: Universal Counter Plate

**Save as**: `tests\fixtures\cross_platform\card_rounded_counter_basic\reference.stl`

---

#### 3. **card_cone_emboss_basic**

**Parameters**:

```
Text Input:
  Line 1: ⠺⠕⠗⠇⠙
  Line 2-4: (empty)

Shape and Plate:
  Output Shape: Card
  Plate Type: Embossing Plate
  
Expert Mode - Shape Selection:
  Braille Dot Shape: Cone
  Indicator Shapes: On

Expert Mode - Surface Dimensions:
  Card Width: 90 mm
  Card Height: 52 mm
  Card Thickness: 2.0 mm

Expert Mode - Braille Spacing:
  (All defaults: 11 columns, 4 rows, 6.5/10.0/2.5 spacing, 0/0 adjust)

Expert Mode - Braille Dot Adjustments (Cone):
  Emboss Dot Base Diameter: 1.8 mm
  Emboss Dot Height: 1.0 mm
  Emboss Dot Flat Hat: 0.4 mm

Expert Mode - Braille Dot Adjustments (Counter Cone):
  Cone Counter Base Diameter: 1.6 mm
  Cone Counter Height: 0.8 mm
  Cone Counter Flat Hat: 0.4 mm

Rendering Quality:
  Hemisphere Quality: Medium
  Cone Segments: 16
```

**Save as**: `tests\fixtures\cross_platform\card_cone_emboss_basic\reference.stl`

---

#### 4. **card_cone_counter_basic**

**Parameters**: Same as test 3, except:
- **Plate Type**: Universal Counter Plate

**Save as**: `tests\fixtures\cross_platform\card_cone_counter_basic\reference.stl`

---

#### 5. **cylinder_rounded_emboss_basic**

**Parameters**:

```
Text Input:
  Line 1: ⠞⠑⠌
  Line 2-4: (empty)

Shape and Plate:
  Output Shape: Cylinder
  Plate Type: Embossing Plate
  
Expert Mode - Shape Selection:
  Braille Dot Shape: Rounded
  Indicator Shapes: On

Expert Mode - Surface Dimensions (Cylinder):
  Cylinder Diameter: 30.75 mm
  Cylinder Height: 52 mm
  Cutout Radius: 13.0 mm
  Cutout Points: 12
  Seam Offset: 355.0 degrees

Expert Mode - Braille Spacing:
  (All defaults: 11 columns, 4 rows, 6.5/10.0/2.5 spacing, 0/0 adjust)

Expert Mode - Braille Dot Adjustments (Rounded):
  Base Diameter: 2.0 mm
  Base Height: 0.2 mm
  Dome Diameter: 1.5 mm
  Dome Height: 0.6 mm

Expert Mode - Braille Dot Adjustments (Counter Bowl):
  Bowl Base Diameter: 1.8 mm
  Counter Dot Depth: 0.8 mm

Rendering Quality:
  Hemisphere Quality: Medium
  Cone Segments: 16
```

**Save as**: `tests\fixtures\cross_platform\cylinder_rounded_emboss_basic\reference.stl`

---

#### 6. **cylinder_rounded_counter_basic**

**Parameters**: Same as test 5, except:
- **Plate Type**: Universal Counter Plate

**Save as**: `tests\fixtures\cross_platform\cylinder_rounded_counter_basic\reference.stl`

---

#### 7. **card_rounded_emboss_custom_spacing**

**Parameters**:

```
Text Input:
  Line 1: ⠁⠃⠉
  Line 2: ⠙⠑⠋
  Line 3-4: (empty)

Shape and Plate:
  Output Shape: Card
  Plate Type: Embossing Plate
  
Expert Mode - Shape Selection:
  Braille Dot Shape: Rounded
  Indicator Shapes: On

Expert Mode - Surface Dimensions:
  Card Width: 90 mm
  Card Height: 52 mm
  Card Thickness: 2.0 mm

Expert Mode - Braille Spacing:
  Grid Columns: 11
  Grid Rows: 4
  Cell Spacing: 7.0 mm  ← CUSTOM
  Line Spacing: 12.0 mm  ← CUSTOM
  Dot Spacing: 2.5 mm
  X Adjust: 0.0 mm
  Y Adjust: 0.0 mm

Expert Mode - Braille Dot Adjustments:
  (All defaults from test 1)

Rendering Quality:
  Hemisphere Quality: Medium
  Cone Segments: 16
```

**Save as**: `tests\fixtures\cross_platform\card_rounded_emboss_custom_spacing\reference.stl`

---

#### 8. **card_rounded_emboss_indicators_off**

**Parameters**:

```
Text Input:
  Line 1: ⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅
  Line 2-4: (empty)

Shape and Plate:
  Output Shape: Card
  Plate Type: Embossing Plate
  
Expert Mode - Shape Selection:
  Braille Dot Shape: Rounded
  Indicator Shapes: Off  ← KEY CHANGE

Expert Mode - Surface Dimensions:
  Card Width: 90 mm
  Card Height: 52 mm
  Card Thickness: 2.0 mm

Expert Mode - Braille Spacing:
  (All defaults: 11 columns, 4 rows, 6.5/10.0/2.5 spacing, 0/0 adjust)

Expert Mode - Braille Dot Adjustments:
  (All defaults from test 1)

Rendering Quality:
  Hemisphere Quality: Medium
  Cone Segments: 16
```

**Save as**: `tests\fixtures\cross_platform\card_rounded_emboss_indicators_off\reference.stl`

---

#### 9. **card_rounded_emboss_max_grid**

**Parameters**:

```
Text Input:
  Line 1: ⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅
  Line 2: ⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧
  Line 3: ⠺⠭⠽⠵⠁⠃⠉⠙⠑⠋⠛
  Line 4: ⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗

Shape and Plate:
  Output Shape: Card
  Plate Type: Embossing Plate
  
Expert Mode - Shape Selection:
  Braille Dot Shape: Rounded
  Indicator Shapes: On

Expert Mode - Surface Dimensions:
  Card Width: 90 mm
  Card Height: 52 mm
  Card Thickness: 2.0 mm

Expert Mode - Braille Spacing:
  (All defaults: 11 columns, 4 rows, 6.5/10.0/2.5 spacing, 0/0 adjust)

Expert Mode - Braille Dot Adjustments:
  (All defaults from test 1)

Rendering Quality:
  Hemisphere Quality: Medium
  Cone Segments: 16
```

**Save as**: `tests\fixtures\cross_platform\card_rounded_emboss_max_grid\reference.stl`

---

#### 10. **cylinder_rounded_emboss_custom_cutout**

**Parameters**:

```
Text Input:
  Line 1: ⠓⠑⠭
  Line 2-4: (empty)

Shape and Plate:
  Output Shape: Cylinder
  Plate Type: Embossing Plate
  
Expert Mode - Shape Selection:
  Braille Dot Shape: Rounded
  Indicator Shapes: On

Expert Mode - Surface Dimensions (Cylinder):
  Cylinder Diameter: 30.75 mm
  Cylinder Height: 52 mm
  Cutout Radius: 10.0 mm  ← CUSTOM
  Cutout Points: 6  ← CUSTOM (hexagonal)
  Seam Offset: 30.0 degrees  ← CUSTOM

Expert Mode - Braille Spacing:
  (All defaults: 11 columns, 4 rows, 6.5/10.0/2.5 spacing, 0/0 adjust)

Expert Mode - Braille Dot Adjustments:
  (All defaults from test 1)

Rendering Quality:
  Hemisphere Quality: Medium
  Cone Segments: 16
```

**Save as**: `tests\fixtures\cross_platform\cylinder_rounded_emboss_custom_cutout\reference.stl`

---

## After Generating All Fixtures

### Verify Fixtures Are In Place

```powershell
# Run the validation check
python scripts/validate_setup.py
```

You should now see:
```
✓ Found 10 test case fixture(s)
  10 with reference.stl
```

### Update Fixture Version File

Edit `tests\fixtures\cross_platform\FIXTURES_VERSION.txt` and add:

```
# Generated manually from web UI (client-side generation)
# Date: 2026-01-08
# Web Generator Version: [Check web UI or git commit]
# Browser: [Your browser name/version]
```

---

## Running Validation Tests

Once all fixtures are generated:

### Run All Tests

```powershell
pytest tests/cross_platform_validation.py -v
```

### Run Specific Test

```powershell
pytest tests/cross_platform_validation.py -k "card_rounded_emboss_basic" -v
```

### Run Test Groups

```powershell
# Basic tests only
pytest tests/cross_platform_validation.py::TestBasicCases -v

# Card tests
pytest tests/cross_platform_validation.py::TestCardShapes -v

# Cylinder tests
pytest tests/cross_platform_validation.py::TestCylinderShapes -v
```

---

## Tips & Troubleshooting

### Copying Braille Characters

The test case parameter files contain Unicode braille characters. To copy them:

1. Open `tests\fixtures\cross_platform\<test_name>\params.json`
2. Find the `Line_1`, `Line_2`, etc. values
3. Copy the braille characters directly
4. Paste into web UI

**Example**: For `card_rounded_emboss_basic`, copy `⠓⠑⠇⠇⠕` from params.json

### Verifying Parameters Match

Before generating each fixture, double-check that ALL parameters in the web UI match the params.json file for that test case.

### File Naming

Always save reference STL files as exactly:
```
reference.stl
```
(Not `reference (1).stl` or `card_rounded_emboss_basic.stl`)

### Browser Download Location

Most browsers save to `Downloads` folder. You'll need to move files to the correct fixture directory:

```powershell
# Example
Move-Item "$env:USERPROFILE\Downloads\reference.stl" "tests\fixtures\cross_platform\card_rounded_emboss_basic\"
```

---

## Automation Alternative

If you prefer a semi-automated approach, you could:

1. Use browser automation tools (Selenium/Playwright)
2. Script the web UI interactions
3. Automatically download STL files

This would require additional development but could save time for frequent regeneration.

---

## Next Steps After Fixture Generation

1. **Verify setup**: `python scripts/validate_setup.py`
2. **Run one test**: `pytest tests/cross_platform_validation.py -k "card_rounded_emboss_basic" -v`
3. **Run all tests**: `pytest tests/cross_platform_validation.py -v`
4. **Review results**: Check `*_results.json` files for detailed metrics
5. **Compare STL files**: Visually inspect in STL viewer if needed

---

## Maintenance

When to regenerate fixtures:
- ✅ Web generator geometry improvements
- ✅ Bug fixes in web generator
- ✅ Adding new test cases
- ❌ UI-only changes (doesn't affect STL output)
- ❌ Routine testing (use existing fixtures)

---

## Questions?

See:
- `tests/VALIDATION_FRAMEWORK_GUIDE.md` - Full framework documentation
- `tests/README.md` - Test suite overview
- `tests/fixtures/cross_platform/test_cases.json` - Test case definitions
- `tests/parameter_mapping.json` - Parameter reference
